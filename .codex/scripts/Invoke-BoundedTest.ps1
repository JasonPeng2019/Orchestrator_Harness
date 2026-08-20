[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Command,

    [Parameter(Mandatory = $true)]
    [string]$WorkingDirectory,

    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 2147483647)]
    [int]$MaximumLifetimeSeconds,

    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 2147483647)]
    [int]$ExpectedUpperBoundSeconds,

    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 120)]
    [int]$CleanupAllowanceSeconds,

    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 60)]
    [int]$HeartbeatIntervalSeconds,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$TimeoutBasis,

    [Parameter(Mandatory = $true)]
    [string]$ResultPath
)

$ErrorActionPreference = 'Stop'

function Write-Heartbeat {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    [Console]::Out.WriteLine($Message)
    [Console]::Out.Flush()
}

function Get-ObservedProcessIds {
    param(
        [Parameter(Mandatory = $true)]
        [int]$RootProcessId
    )

    $observed = [System.Collections.Generic.HashSet[int]]::new()
    [void]$observed.Add($RootProcessId)
    $frontier = [System.Collections.Generic.Queue[int]]::new()
    $frontier.Enqueue($RootProcessId)
    while ($frontier.Count -gt 0) {
        $parent = $frontier.Dequeue()
        foreach ($child in @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$parent" -ErrorAction SilentlyContinue)) {
            $childId = [int]$child.ProcessId
            if ($observed.Add($childId)) {
                $frontier.Enqueue($childId)
            }
        }
    }
    return @($observed)
}

if (-not (Test-Path -LiteralPath $WorkingDirectory -PathType Container)) {
    throw "Working directory does not exist: $WorkingDirectory"
}

$expectedMaximumLifetime = $ExpectedUpperBoundSeconds + $CleanupAllowanceSeconds
if ($MaximumLifetimeSeconds -ne $expectedMaximumLifetime) {
    throw (
        "MaximumLifetimeSeconds must equal ExpectedUpperBoundSeconds plus " +
        "CleanupAllowanceSeconds ($ExpectedUpperBoundSeconds + $CleanupAllowanceSeconds = " +
        "$expectedMaximumLifetime), not $MaximumLifetimeSeconds."
    )
}
$maximumReasonableCleanup = [Math]::Max(
    5,
    [Math]::Min(120, [Math]::Ceiling($ExpectedUpperBoundSeconds * 0.25))
)
if ($CleanupAllowanceSeconds -gt $maximumReasonableCleanup) {
    throw (
        "CleanupAllowanceSeconds=$CleanupAllowanceSeconds is excessive for " +
        "ExpectedUpperBoundSeconds=$ExpectedUpperBoundSeconds; maximum reasonable cleanup " +
        "allowance is $maximumReasonableCleanup seconds."
    )
}

$resolvedWorkingDirectory = (Resolve-Path -LiteralPath $WorkingDirectory).Path
$resolvedResultPath = [IO.Path]::GetFullPath($ResultPath)
$resultDirectory = Split-Path -Parent $resolvedResultPath
if ([string]::IsNullOrWhiteSpace($resultDirectory)) {
    throw 'ResultPath must include a parent directory.'
}
[IO.Directory]::CreateDirectory($resultDirectory) | Out-Null
$resultStem = [IO.Path]::GetFileNameWithoutExtension($resolvedResultPath)
$stdoutPath = Join-Path $resultDirectory "$resultStem.stdout.log"
$stderrPath = Join-Path $resultDirectory "$resultStem.stderr.log"
$exitCodePath = Join-Path $resultDirectory "$resultStem.exit-code.txt"

$shellPath = (Get-Process -Id $PID).Path
$innerCommand = @"
& {
$Command
}
if (`$null -ne `$LASTEXITCODE) { exit `$LASTEXITCODE }
if (-not `$?) { exit 1 }
exit 0
"@
$innerEncodedCommand = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($innerCommand))
$escapedShellPath = $shellPath.Replace("'", "''")
$escapedExitCodePath = $exitCodePath.Replace("'", "''")
$wrappedCommand = @"
& '$escapedShellPath' -NoLogo -NoProfile -NonInteractive -EncodedCommand '$innerEncodedCommand'
`$childExitCode = if (`$null -eq `$LASTEXITCODE) { 1 } else { [int]`$LASTEXITCODE }
[IO.File]::WriteAllText('$escapedExitCodePath', [string]`$childExitCode, [Text.Encoding]::ASCII)
exit `$childExitCode
"@
$encodedCommand = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($wrappedCommand))
$startedAt = [DateTimeOffset]::UtcNow
$process = Start-Process -FilePath $shellPath `
    -ArgumentList @('-NoLogo', '-NoProfile', '-NonInteractive', '-EncodedCommand', $encodedCommand) `
    -WorkingDirectory $resolvedWorkingDirectory `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath `
    -WindowStyle Hidden `
    -PassThru

$observedIds = [System.Collections.Generic.HashSet[int]]::new()
[void]$observedIds.Add([int]$process.Id)
$deadline = $startedAt.AddSeconds($MaximumLifetimeSeconds)
$status = 'FAILED'
$exitCode = 1
$cleanupVerified = $true

Write-Heartbeat "RUNNING pid=$($process.Id) elapsed_seconds=0 remaining_seconds=$MaximumLifetimeSeconds"
while (-not $process.HasExited) {
    $now = [DateTimeOffset]::UtcNow
    if ($now -ge $deadline) {
        foreach ($observedId in @(Get-ObservedProcessIds -RootProcessId $process.Id)) {
            [void]$observedIds.Add([int]$observedId)
        }
        # taskkill may report an already-gone descendant during the enumeration/termination
        # race; its stderr must not abort the supervisor before the terminal record is written.
        $previousErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        & "$env:SystemRoot\System32\taskkill.exe" /PID $process.Id /T /F *> $null
        $ErrorActionPreference = $previousErrorActionPreference
        $process.WaitForExit()
        foreach ($observedId in $observedIds) {
            if (Get-Process -Id $observedId -ErrorAction SilentlyContinue) {
                $cleanupVerified = $false
            }
        }
        $status = 'TIMED_OUT'
        $exitCode = 124
        break
    }

    $remaining = [Math]::Max(0, [Math]::Ceiling(($deadline - $now).TotalSeconds))
    $waitSeconds = [Math]::Min($HeartbeatIntervalSeconds, $remaining)
    if ($waitSeconds -gt 0) {
        [void]$process.WaitForExit($waitSeconds * 1000)
    }
    foreach ($observedId in @(Get-ObservedProcessIds -RootProcessId $process.Id)) {
        [void]$observedIds.Add([int]$observedId)
    }
    if (-not $process.HasExited) {
        $elapsed = [Math]::Floor(([DateTimeOffset]::UtcNow - $startedAt).TotalSeconds)
        $remaining = [Math]::Max(0, [Math]::Ceiling(($deadline - [DateTimeOffset]::UtcNow).TotalSeconds))
        $stdoutBytes = if (Test-Path -LiteralPath $stdoutPath) { (Get-Item -LiteralPath $stdoutPath).Length } else { 0 }
        $stderrBytes = if (Test-Path -LiteralPath $stderrPath) { (Get-Item -LiteralPath $stderrPath).Length } else { 0 }
        Write-Heartbeat "RUNNING pid=$($process.Id) elapsed_seconds=$elapsed remaining_seconds=$remaining stdout_bytes=$stdoutBytes stderr_bytes=$stderrBytes observed_processes=$($observedIds.Count)"
    }
}

if ($status -ne 'TIMED_OUT') {
    $process.WaitForExit()
    if (-not (Test-Path -LiteralPath $exitCodePath -PathType Leaf)) {
        $exitCode = 1
    }
    else {
        $exitCode = [int](Get-Content -LiteralPath $exitCodePath -Raw)
        Remove-Item -LiteralPath $exitCodePath -Force
    }
    $status = if ($exitCode -eq 0) { 'PASSED' } else { 'FAILED' }
}

$finishedAt = [DateTimeOffset]::UtcNow
$result = [ordered]@{
    schema = 'bounded-test-result-v1'
    status = $status
    command = $Command
    working_directory = $resolvedWorkingDirectory
    maximum_lifetime_seconds = $MaximumLifetimeSeconds
    expected_upper_bound_seconds = $ExpectedUpperBoundSeconds
    cleanup_allowance_seconds = $CleanupAllowanceSeconds
    heartbeat_interval_seconds = $HeartbeatIntervalSeconds
    timeout_basis = $TimeoutBasis
    started_at = $startedAt.ToString('o')
    finished_at = $finishedAt.ToString('o')
    elapsed_seconds = [Math]::Round(($finishedAt - $startedAt).TotalSeconds, 3)
    root_process_id = $process.Id
    observed_process_ids = @($observedIds | Sort-Object)
    cleanup_verified = $cleanupVerified
    exit_code = $exitCode
    stdout_path = $stdoutPath
    stderr_path = $stderrPath
}
$json = $result | ConvertTo-Json -Depth 4
[IO.File]::WriteAllText($resolvedResultPath, $json, [Text.UTF8Encoding]::new($false))
Write-Heartbeat "$status exit_code=$exitCode elapsed_seconds=$($result.elapsed_seconds) result=$resolvedResultPath cleanup_verified=$cleanupVerified"
exit $exitCode

param(
    [string]$SuiteRoot = "C:\Users\Jason\Documents\Jason\FirmCLI_Tester\Firmware-Test-Manual\MCP-Trial-3",
    [string]$Config = "orchestrator_harness/canary-20260731-s1-clean-l.json",
    [string]$Epoch = "20260731-s1-clean-l",
    [int]$IntervalSeconds = 75
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $SuiteRoot
$logRoot = Join-Path $SuiteRoot ".agent-workspace/ORCHESTRATOR_HARNESS"
if ($Epoch -match '-clean-') {
    $suffix = ($Epoch -replace '^.*-clean-', '').ToLowerInvariant()
} else {
    $suffix = (($Epoch -split '-')[-1]).ToLowerInvariant()
}
$tag = "S1$($suffix.ToUpperInvariant())"
$stopFile = Join-Path $SuiteRoot ".agent-workspace/CANARY_${tag}_SUPERVISION.stop"
$identityFile = Join-Path $logRoot "clean_${suffix}_primary_identity.json"
$stdoutFile = Join-Path $logRoot "clean_${suffix}_primary_watch.stdout.jsonl"
$stderrFile = Join-Path $logRoot "clean_${suffix}_primary_watch.stderr.log"
$supervisionFile = Join-Path $SuiteRoot ".agent-workspace/CANARY_${tag}_SUPERVISION.jsonl"
$runtimeName = ((Get-Content -Raw (Join-Path $SuiteRoot $Config) | ConvertFrom-Json).output_dir)
$runtimeFile = Join-Path $SuiteRoot ("orchestrator_harness/{0}/managed-watch-runtime.json" -f $runtimeName)

function Write-IdentityAtomic([string]$Path, $Value) {
    $temporary = "$Path.$PID.tmp"
    [IO.File]::WriteAllText($temporary, ($Value | ConvertTo-Json -Depth 6) + "`n", [Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $temporary -Destination $Path -Force
}

Remove-Item -LiteralPath $stopFile -Force -ErrorAction SilentlyContinue
$watch = Start-Process -FilePath "python" -ArgumentList @(
    "-m", "orchestrator_harness", "--config", $Config, "watch", "--managed"
) -WorkingDirectory $SuiteRoot -WindowStyle Hidden -PassThru `
  -RedirectStandardOutput $stdoutFile -RedirectStandardError $stderrFile

$owner = Get-Process -Id $PID
$watch.Refresh()
$identity = [ordered]@{
    schema = "canary-primary-owner/v1"
    epoch = $Epoch
    owner = @{ pid = $PID; created_utc = $owner.StartTime.ToUniversalTime().ToString("o") }
    watcher = @{ pid = $watch.Id; created_utc = $watch.StartTime.ToUniversalTime().ToString("o") }
    config = $Config
    started_utc = [DateTime]::UtcNow.ToString("o")
}
Write-IdentityAtomic $identityFile $identity

$exitReason = "stop-file"
try {
    $readyDeadline = [DateTime]::UtcNow.AddSeconds(45)
    while ($true) {
        $watch.Refresh()
        if ($watch.HasExited) { throw "managed watcher exited before publishing its runtime" }
        if ([DateTime]::UtcNow -ge $readyDeadline) { throw "managed watcher runtime startup timed out" }
        if (Test-Path -LiteralPath $runtimeFile) {
            try {
                $published = Get-Content -Raw -LiteralPath $runtimeFile | ConvertFrom-Json
                # The launched Python process is the managed watch owner; the harness
                # publishes its own exact child watcher identity separately.
                $live = (& python -c "import json,sys; from orchestrator_harness.models import iso_utc; from orchestrator_harness.processes import process_snapshot; snapshot=process_snapshot(); print(json.dumps({'complete':snapshot.complete,'identities':{str(item.pid):iso_utc(item.created_utc) for item in snapshot.processes}}))" | ConvertFrom-Json)
                $ownerCreation = $live.identities.PSObject.Properties[[string]$watch.Id].Value
                $watcherCreation = $live.identities.PSObject.Properties[[string]$published.watcher_pid].Value
                if ($live.complete -eq $true -and
                    $published.owner_pid -eq $watch.Id -and
                    $published.owner_created_utc -eq $ownerCreation -and
                    $published.watcher_pid -and
                    $published.watcher_created_utc -eq $watcherCreation) {
                    $identity.managed_owner = @{ pid = $published.owner_pid; created_utc = $published.owner_created_utc }
                    $identity.managed_watcher = @{ pid = $published.watcher_pid; created_utc = $published.watcher_created_utc }
                    Write-IdentityAtomic $identityFile $identity
                    break
                }
            } catch {
                # The managed watcher publishes atomically; retry a transient or prior-runtime read.
            }
        }
        Start-Sleep -Milliseconds 250
    }
    while (-not (Test-Path -LiteralPath $stopFile)) {
        $watch.Refresh()
        if ($watch.HasExited) { $exitReason = "watcher-exited"; break }
        $started = [DateTime]::UtcNow
        $line = (& python .agent-workspace/tools/canary_supervision_pass.py `
            --config $Config --epoch $Epoch --scan-dir .agent-workspace 2>&1 | Out-String)
        if ($LASTEXITCODE -ne 0) {
            $line = (@{ schema = "manager-supervision-error/v1"; observed_utc = [DateTime]::UtcNow.ToString("o"); epoch = $Epoch; exit_code = $LASTEXITCODE; output = $line.Trim() } | ConvertTo-Json -Compress)
        }
        [IO.File]::AppendAllText($supervisionFile, $line.TrimEnd() + "`n", [Text.UTF8Encoding]::new($false))
        $elapsed = ([DateTime]::UtcNow - $started).TotalSeconds
        $sleep = [Math]::Max(1, [Math]::Ceiling($IntervalSeconds - $elapsed))
        Start-Sleep -Seconds $sleep
    }
} catch {
    $exitReason = "owner-script-error"
    [IO.File]::AppendAllText($supervisionFile, (@{ schema = "manager-supervision-owner-error/v1"; observed_utc = [DateTime]::UtcNow.ToString("o"); epoch = $Epoch; error = $_.Exception.Message } | ConvertTo-Json -Compress) + "`n", [Text.UTF8Encoding]::new($false))
}
finally {
    $watch.Refresh()
    if (-not $watch.HasExited) {
        & python -m orchestrator_harness --config $Config watch stop | Out-Null
        $watch.WaitForExit(20000) | Out-Null
    }
    $identity["exit_reason"] = $exitReason
    $identity["ended_utc"] = [DateTime]::UtcNow.ToString("o")
    $watch.Refresh()
    $identity["watcher_exit_code"] = if ($watch.HasExited) { $watch.ExitCode } else { $null }
    Write-IdentityAtomic $identityFile $identity
}

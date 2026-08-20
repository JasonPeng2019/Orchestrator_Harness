$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..")).Path
$evidence = $PSScriptRoot
$runtime = Join-Path $evidence "runtime"
$config = Join-Path $runtime "watcher-config.json"
$source = Join-Path $runtime "source.jsonl"
$stopFile = Join-Path $runtime "stop.token"
$identityFile = Join-Path $runtime "owner-identity.json"
$sentinel = Join-Path $runtime "evaluator-sentinel.invoked"
$service = Join-Path $runtime "watcher\service.json"
$watcherEvents = Join-Path $runtime "watcher\events.jsonl"
$orchestratorEvents = Join-Path $runtime "orchestrator\events.jsonl"
$commandLog = Join-Path $runtime "commands-results.jsonl"
$ownerScript = Join-Path $repo "scripts\orchestration\optional_watcher_owner.ps1"
$ownerProcess = $null
$ownerPidLaunched = $null
$launchExact = $null
$watcherExpected = $null
$practicalPass = $false
$testPass = $false
$failure = $null

function Write-Evidence {
    param([string]$Label, [object]$Value)
    $record = [ordered]@{
        timestamp_utc = [DateTime]::UtcNow.ToString("o")
        label = $Label
        value = $Value
    }
    [IO.File]::AppendAllText($commandLog, (($record | ConvertTo-Json -Compress -Depth 20) + "`n"), [Text.UTF8Encoding]::new($false))
}

function Require-Check {
    param([bool]$Condition, [string]$Message)
    Write-Evidence "check:$Message" @{ pass = $Condition }
    if (-not $Condition) { throw "FAIL_CLOSED: $Message" }
}

function Read-JsonFile {
    param([string]$Path)
    return (Get-Content -Raw -LiteralPath $Path | ConvertFrom-Json)
}

function Get-ExactIdentity {
    param([int]$ProcessId)
    $raw = (& python -c "import json,sys; from harness_common.process_identity import exact_process_identity; print(json.dumps(exact_process_identity(int(sys.argv[1]))))" $ProcessId 2>&1 | Out-String).Trim()
    $code = $LASTEXITCODE
    if ($code -ne 0) { throw "identity helper failed for pid ${ProcessId}: $raw" }
    $parsed = $raw | ConvertFrom-Json
    return [ordered]@{ pid = $ProcessId; raw = $raw; identity = $parsed }
}

function Same-Identity {
    param([object]$A, [object]$B)
    return ($null -ne $A -and $null -ne $B -and [int]$A.pid -eq [int]$B.pid -and [string]$A.created_utc -eq [string]$B.created_utc)
}

function Invoke-RecordedPython {
    param([string]$Label, [string[]]$Arguments)
    Write-Evidence "command:$Label" @{ executable = "python"; arguments = $Arguments }
    $raw = (& python @Arguments 2>&1 | Out-String).Trim()
    $code = $LASTEXITCODE
    Write-Evidence "result:$Label" @{ exit_code = $code; output = $raw }
    return [ordered]@{ exit_code = $code; output = $raw }
}

function Get-EventRecords {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    $records = @()
    foreach ($line in (Get-Content -LiteralPath $Path)) {
        if ($line.Trim()) { $records += ($line | ConvertFrom-Json) }
    }
    return $records
}

function Copy-RawIfPresent {
    param([string]$SourcePath, [string]$TargetPath)
    if (Test-Path -LiteralPath $SourcePath) { Copy-Item -LiteralPath $SourcePath -Destination $TargetPath -Force }
}

try {
    if (-not (Test-Path -LiteralPath $ownerScript)) { throw "FAIL_CLOSED: owner script does not exist" }
    if (Test-Path -LiteralPath $runtime) { throw "FAIL_CLOSED: runtime was not fresh before initialization" }
    New-Item -ItemType Directory -Path $runtime -Force | Out-Null
    [IO.File]::WriteAllText($commandLog, "", [Text.UTF8Encoding]::new($false))
    Write-Evidence "command:initialization" @{ repository = $repo; evidence = $evidence; runtime = $runtime; constraints = @("no hardware", "no providers", "no MCP servers", "no firmware", "no experiment leases", "no broad process termination") }
    Require-Check (Test-Path -LiteralPath $ownerScript) "owner script exists"
    Require-Check (-not (Test-Path -LiteralPath (Join-Path $runtime "preexisting.marker"))) "runtime contains no preexisting marker"

    [IO.File]::WriteAllText($source, "", [Text.UTF8Encoding]::new($false))
    $relativeRuntime = "multi-agent-logs/verification/m5-watcher-repair-luna/runtime"
    $sentinelCommand = "Set-Content -LiteralPath '$sentinel' -Value invoked -Encoding utf8"
    $rawConfig = [ordered]@{
        poll_interval_seconds = 1
        observed_sources = @([ordered]@{ path = $source; role = "orchestrator"; source_id = "luna-smoke-source" })
        runtime_root = $relativeRuntime
        no_progress_seconds = 3600
        max_tail_bytes = 131072
        evaluator_command = @("powershell.exe", "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden", "-Command", $sentinelCommand)
        attention_logging_enabled = $false
        evaluator_enabled = $false
        attention_producers = @()
        attention_lock_timeout_seconds = 5.0
    }
    [IO.File]::WriteAllText($config, ($rawConfig | ConvertTo-Json -Depth 10), [Text.UTF8Encoding]::new($false))
    Write-Evidence "raw-config-created" @{ config_path = $config; evaluator_enabled = $false; evaluator_command = $rawConfig.evaluator_command; source = $source; runtime_root = $relativeRuntime }
    Require-Check (-not (Test-Path -LiteralPath $sentinel)) "evaluator sentinel is absent before launch"

    $ownerArgs = @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", $ownerScript, "-SuiteRoot", $repo, "-Config", $config, "-StopFile", $stopFile, "-IdentityFile", $identityFile)
    Write-Evidence "command:launch-hidden-owner" @{ executable = "powershell.exe"; window_style = "Hidden"; arguments = $ownerArgs }
    $ownerProcess = Start-Process -FilePath "powershell.exe" -ArgumentList $ownerArgs -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runtime "owner.stdout.log") -RedirectStandardError (Join-Path $runtime "owner.stderr.log")
    $ownerPidLaunched = $ownerProcess.Id
    $launchExact = (Get-ExactIdentity $ownerPidLaunched).identity
    Write-Evidence "owner-launched" @{ process_id = $ownerProcess.Id; exact_identity = $launchExact; process_name = $ownerProcess.ProcessName }
    Require-Check ($null -ne $launchExact) "owner exact launch identity is available"

    $readyState = $null
    for ($i = 0; $i -lt 120; $i++) {
        if (Test-Path -LiteralPath $service) {
            try {
                $candidate = Read-JsonFile $service
                if ($candidate.startup_status -eq "READY" -and $candidate.owner -and $candidate.watcher -and $candidate.watcher.pid) { $readyState = $candidate; break }
            } catch { }
        }
        Start-Sleep -Milliseconds 250
    }
    Require-Check ($null -ne $readyState) "watcher published READY service state"
    Copy-RawIfPresent $service (Join-Path $runtime "service-ready.json")
    $ownerServiceIdentity = $readyState.owner
    $watcherExpected = $readyState.watcher
    $ownerCurrent = (Get-ExactIdentity ([int]$ownerServiceIdentity.pid)).identity
    $watcherCurrent = (Get-ExactIdentity ([int]$watcherExpected.pid)).identity
    Require-Check (Same-Identity $launchExact $ownerServiceIdentity) "service owner identity equals launch identity"
    Require-Check (Same-Identity $ownerServiceIdentity $ownerCurrent) "owner is alive at READY with exact identity"
    Require-Check (Same-Identity $watcherExpected $watcherCurrent) "watcher is alive at READY with exact identity"
    for ($i = 0; $i -lt 40 -and -not (Test-Path -LiteralPath $runtime\watcher\cursor.json); $i++) { Start-Sleep -Milliseconds 250 }
    Require-Check (Test-Path -LiteralPath $runtime\watcher\cursor.json) "baseline cursor exists before source append"
    if (Test-Path -LiteralPath $identityFile) { Copy-Item -LiteralPath $identityFile -Destination (Join-Path $runtime "owner-identity-ready.json") -Force }
    Write-Evidence "ready-identities" @{ service_owner = $ownerServiceIdentity; watcher = $watcherExpected; owner_current = $ownerCurrent; watcher_current = $watcherCurrent; service = $readyState }
    $statusReady = Invoke-RecordedPython "status-ready" @("-m", "harness_watcher_implementation", "--config", $config, "status")
    Require-Check ($statusReady.exit_code -eq 0 -and $statusReady.output -match '"running"\s*:\s*true') "status reports running at READY"

    $scalarLine = "1"
    $hugeObject = [ordered]@{ payload = ("x" * 70000); kind = "oversized-wrapper-probe" }
    $hugeLine = $hugeObject | ConvertTo-Json -Compress -Depth 5
    $validLine = '{"record":"valid-after-oversized","sequence":1}'
    $initialText = $scalarLine + "`n" + $hugeLine + "`n" + $validLine + "`n"
    $hugeBytes = [Text.Encoding]::UTF8.GetByteCount($hugeLine + "`n")
    $preview = [ordered]@{ schema = "harness-watcher-log/v1"; timestamp_utc = [DateTime]::UtcNow.ToString("o"); source_category = "orchestrator"; source_id = "luna-smoke-source"; event_type = "ACTIVITY_INGESTED"; data = [ordered]@{ source_path = $source; offset = 0; records = @([pscustomobject]$hugeObject) } }
    $wrapperBytes = [Text.Encoding]::UTF8.GetByteCount(($preview | ConvertTo-Json -Compress -Depth 10) + "`n")
    Write-Evidence "source-append-initial" @{ scalar = $scalarLine; oversized_object_marker = $hugeObject.kind; oversized_raw_line_utf8_bytes = $hugeBytes; routed_wrapper_preview_utf8_bytes = $wrapperBytes; route_limit = 65536; valid = $validLine }
    Require-Check ($wrapperBytes -gt 65536) "oversized object routed wrapper preview exceeds 65536 bytes"
    [IO.File]::AppendAllText($source, $initialText, [Text.UTF8Encoding]::new($false))

    $initialSatisfied = $false
    for ($i = 0; $i -lt 120; $i++) {
        $watchEvents = @(Get-EventRecords $watcherEvents)
        $orchEvents = @(Get-EventRecords $orchestratorEvents)
        $scalarRejected = @($watchEvents | Where-Object { $_.event_type -eq "ROUTE_REJECTED" -and $_.data.reason -eq "json record is not an object" }).Count
        $hugeRejected = @($watchEvents | Where-Object { $_.event_type -eq "ROUTE_REJECTED" -and $_.data.reason -eq "record exceeds route limit" }).Count
        $validRouted = @($orchEvents | Where-Object { $_.event_type -eq "ACTIVITY_INGESTED" -and $_.data.records -and ($_.data.records | ConvertTo-Json -Compress) -match "valid-after-oversized" }).Count
        $polls = @($watchEvents | Where-Object { $_.event_type -eq "POLL" }).Count
        if ($scalarRejected -eq 1 -and $hugeRejected -eq 1 -and $validRouted -ge 1 -and $polls -ge 2) { $initialSatisfied = $true; break }
        Start-Sleep -Milliseconds 250
    }
    Require-Check $initialSatisfied "scalar and oversized records are bounded-rejected while following valid record routes"
    $watchEvents = @(Get-EventRecords $watcherEvents)
    $orchEvents = @(Get-EventRecords $orchestratorEvents)
    $routeSummary = [ordered]@{
        scalar_rejected = @($watchEvents | Where-Object { $_.event_type -eq "ROUTE_REJECTED" -and $_.data.reason -eq "json record is not an object" }).Count
        oversized_rejected = @($watchEvents | Where-Object { $_.event_type -eq "ROUTE_REJECTED" -and $_.data.reason -eq "record exceeds route limit" }).Count
        oversized_encoded_size = @($watchEvents | Where-Object { $_.event_type -eq "ROUTE_REJECTED" -and $_.data.reason -eq "record exceeds route limit" } | Select-Object -First 1).data.encoded_size
        valid_routed = @($orchEvents | Where-Object { $_.event_type -eq "ACTIVITY_INGESTED" -and $_.data.records -and ($_.data.records | ConvertTo-Json -Compress) -match "valid-after-oversized" }).Count
        poll_count = @($watchEvents | Where-Object { $_.event_type -eq "POLL" }).Count
    }
    Write-Evidence "route-summary-after-initial" $routeSummary
    Require-Check ([int]$routeSummary.oversized_encoded_size -eq $hugeBytes) "oversized rejection retains exact raw line byte size"
    Require-Check (-not (Test-Path -LiteralPath $sentinel)) "evaluator sentinel remains absent after initial data"
    Require-Check (@($watchEvents | Where-Object { $_.event_type -eq "EVALUATOR_SKIPPED" }).Count -ge 1) "EVALUATOR_SKIPPED is recorded"

    $stateInitial = Read-JsonFile $service
    $ownerInitial = (Get-ExactIdentity ([int]$ownerServiceIdentity.pid)).identity
    $watcherInitial = (Get-ExactIdentity ([int]$watcherExpected.pid)).identity
    Require-Check ($stateInitial.exit_reason -eq $null -and -not $stateInitial.stop_requested) "service remains non-terminal after initial routing"
    Require-Check (Same-Identity $ownerServiceIdentity $ownerInitial) "owner remains alive across initial poll cycles"
    Require-Check (Same-Identity $watcherExpected $watcherInitial) "watcher remains alive across initial poll cycles"
    Write-Evidence "continuity-after-initial" @{ service = $stateInitial; owner_current = $ownerInitial; watcher_current = $watcherInitial; poll_count = $routeSummary.poll_count }
    Copy-RawIfPresent $service (Join-Path $runtime "service-after-initial.json")
    $statusInitial = Invoke-RecordedPython "status-after-initial" @("-m", "harness_watcher_implementation", "--config", $config, "status")
    Require-Check ($statusInitial.exit_code -eq 0 -and $statusInitial.output -match '"running"\s*:\s*true') "status reports running after initial routing"

    Start-Sleep -Seconds 2
    $stateBeforeLater = Read-JsonFile $service
    $ownerBeforeLater = (Get-ExactIdentity ([int]$ownerServiceIdentity.pid)).identity
    $watcherBeforeLater = (Get-ExactIdentity ([int]$watcherExpected.pid)).identity
    $watchEventsBeforeLater = @(Get-EventRecords $watcherEvents)
    Require-Check (@($watchEventsBeforeLater | Where-Object { $_.event_type -eq "POLL" }).Count -gt [int]$routeSummary.poll_count) "at least one later poll occurs before later append"
    Require-Check (Same-Identity $ownerServiceIdentity $ownerBeforeLater) "owner remains alive before later append"
    Require-Check (Same-Identity $watcherExpected $watcherBeforeLater) "watcher remains alive before later append"
    Write-Evidence "continuity-before-later-append" @{ service = $stateBeforeLater; owner_current = $ownerBeforeLater; watcher_current = $watcherBeforeLater; poll_count = @($watchEventsBeforeLater | Where-Object { $_.event_type -eq "POLL" }).Count }

    $laterLine = '{"record":"later-append","sequence":2}'
    Write-Evidence "source-append-later" @{ line = $laterLine; reason = "append after a completed poll cycle" }
    [IO.File]::AppendAllText($source, $laterLine + "`n", [Text.UTF8Encoding]::new($false))
    $laterSatisfied = $false
    for ($i = 0; $i -lt 80; $i++) {
        $orchEvents = @(Get-EventRecords $orchestratorEvents)
        $laterRouted = @($orchEvents | Where-Object { $_.event_type -eq "ACTIVITY_INGESTED" -and $_.data.records -and ($_.data.records | ConvertTo-Json -Compress) -match "later-append" }).Count
        if ($laterRouted -ge 1) { $laterSatisfied = $true; break }
        Start-Sleep -Milliseconds 250
    }
    Require-Check $laterSatisfied "later append routes after prior rejected record"
    $watchEvents = @(Get-EventRecords $watcherEvents)
    $orchEvents = @(Get-EventRecords $orchestratorEvents)
    $finalRouteSummary = [ordered]@{
        scalar_rejected = @($watchEvents | Where-Object { $_.event_type -eq "ROUTE_REJECTED" -and $_.data.reason -eq "json record is not an object" }).Count
        oversized_rejected = @($watchEvents | Where-Object { $_.event_type -eq "ROUTE_REJECTED" -and $_.data.reason -eq "record exceeds route limit" }).Count
        valid_routed = @($orchEvents | Where-Object { $_.event_type -eq "ACTIVITY_INGESTED" -and $_.data.records -and ($_.data.records | ConvertTo-Json -Compress) -match "valid-after-oversized" }).Count
        later_routed = @($orchEvents | Where-Object { $_.event_type -eq "ACTIVITY_INGESTED" -and $_.data.records -and ($_.data.records | ConvertTo-Json -Compress) -match "later-append" }).Count
        evaluator_skipped = @($watchEvents | Where-Object { $_.event_type -eq "EVALUATOR_SKIPPED" }).Count
        polls = @($watchEvents | Where-Object { $_.event_type -eq "POLL" }).Count
    }
    Write-Evidence "final-route-summary" $finalRouteSummary
    Require-Check ([int]$finalRouteSummary.scalar_rejected -eq 1 -and [int]$finalRouteSummary.oversized_rejected -eq 1) "ROUTE_REJECTED evidence is bounded to one scalar and one oversized record"
    Require-Check ([int]$finalRouteSummary.valid_routed -ge 1 -and [int]$finalRouteSummary.later_routed -ge 1) "valid records route after oversized rejection and later append"
    Require-Check (-not (Test-Path -LiteralPath $sentinel)) "evaluator sentinel is absent after later append"
    Require-Check ([int]$finalRouteSummary.evaluator_skipped -ge 2) "diagnostic-only evaluator skips are recorded across cycles"
    $stateLater = Read-JsonFile $service
    $ownerLater = (Get-ExactIdentity ([int]$ownerServiceIdentity.pid)).identity
    $watcherLater = (Get-ExactIdentity ([int]$watcherExpected.pid)).identity
    Require-Check ($stateLater.exit_reason -eq $null -and -not $stateLater.stop_requested) "service remains live after later append"
    Require-Check (Same-Identity $ownerServiceIdentity $ownerLater) "owner remains alive after later append"
    Require-Check (Same-Identity $watcherExpected $watcherLater) "watcher remains alive after later append"
    Write-Evidence "continuity-after-later" @{ service = $stateLater; owner_current = $ownerLater; watcher_current = $watcherLater; poll_count = $finalRouteSummary.polls }
    Copy-RawIfPresent $service (Join-Path $runtime "service-before-stop.json")
    $statusLater = Invoke-RecordedPython "status-after-later" @("-m", "harness_watcher_implementation", "--config", $config, "status")
    Require-Check ($statusLater.exit_code -eq 0 -and $statusLater.output -match '"running"\s*:\s*true') "status reports running after later append"

    Write-Evidence "command:create-stop-token" @{ path = $stopFile; method = "cooperative owner stop token" }
    [IO.File]::WriteAllText($stopFile, "stop`n", [Text.UTF8Encoding]::new($false))
    $shutdownDone = $false
    for ($i = 0; $i -lt 160; $i++) {
        $ownerNow = (Get-ExactIdentity ([int]$ownerServiceIdentity.pid)).identity
        $watcherNow = (Get-ExactIdentity ([int]$watcherExpected.pid)).identity
        $serviceNow = if (Test-Path -LiteralPath $service) { Read-JsonFile $service } else { $null }
        $ownerIdentity = if (Test-Path -LiteralPath $identityFile) { Read-JsonFile $identityFile } else { $null }
        if ($null -eq $ownerNow -and $null -eq $watcherNow -and $serviceNow -and $serviceNow.exit_reason -and $ownerIdentity -and $ownerIdentity.exit_reason -eq "stop-file") { $shutdownDone = $true; break }
        Start-Sleep -Milliseconds 250
    }
    Require-Check $shutdownDone "owner and watcher complete cooperative shutdown"
    $finalOwnerCheck = Get-ExactIdentity ([int]$ownerServiceIdentity.pid)
    $finalWatcherCheck = Get-ExactIdentity ([int]$watcherExpected.pid)
    $finalService = Read-JsonFile $service
    $finalOwnerIdentity = Read-JsonFile $identityFile
    Write-Evidence "final-process-absence" @{ owner_expected = $ownerServiceIdentity; owner_check = $finalOwnerCheck; watcher_expected = $watcherExpected; watcher_check = $finalWatcherCheck; service = $finalService; owner_identity = $finalOwnerIdentity; stop_token = $stopFile; broad_kill_used = $false }
    Require-Check ($null -eq $finalOwnerCheck.identity) "exact owner PID and creation identity are absent after stop"
    Require-Check ($null -eq $finalWatcherCheck.identity) "exact watcher PID and creation identity are absent after stop"
    Require-Check ($finalService.exit_reason -ne $null) "service records terminal cooperative exit"
    Require-Check ($finalOwnerIdentity.exit_reason -eq "stop-file") "owner records stop-file exit reason"
    Copy-RawIfPresent $service (Join-Path $runtime "service-final.json")
    Copy-RawIfPresent $identityFile (Join-Path $runtime "owner-identity-final.json")
    $statusFinal = Invoke-RecordedPython "status-final" @("-m", "harness_watcher_implementation", "--config", $config, "status")
    Require-Check ($statusFinal.exit_code -eq 0 -and $statusFinal.output -match '"running"\s*:\s*false') "status reports stopped after cooperative shutdown"
    $practicalPass = $true
}
catch {
    $failure = $_.Exception.Message
    try { Write-Evidence "failure" @{ message = $failure; line = $_.InvocationInfo.ScriptLineNumber } } catch { }
    if ($null -ne $ownerPidLaunched) {
        try {
            if (-not (Test-Path -LiteralPath $stopFile)) { [IO.File]::WriteAllText($stopFile, "stop`n", [Text.UTF8Encoding]::new($false)) }
            for ($i = 0; $i -lt 120; $i++) {
                $ownerNow = (Get-ExactIdentity ([int]$ownerPidLaunched)).identity
                $watcherNow = $null
                if (Test-Path -LiteralPath $service) {
                    try {
                        $cleanupState = Read-JsonFile $service
                        if ($cleanupState.watcher.pid) { $watcherNow = (Get-ExactIdentity ([int]$cleanupState.watcher.pid)).identity }
                    } catch { }
                }
                if ($null -eq $ownerNow -and $null -eq $watcherNow) { break }
                Start-Sleep -Milliseconds 250
            }
            Write-Evidence "failure-cooperative-cleanup" @{ owner_exact_after_wait = (Get-ExactIdentity ([int]$ownerPidLaunched)); broad_kill_used = $false }
        } catch { }
    }
}
finally {
    if (Test-Path -LiteralPath $runtime) {
        Copy-RawIfPresent $config (Join-Path $runtime "config-raw.json")
        Copy-RawIfPresent $source (Join-Path $runtime "source-raw.jsonl")
        Copy-RawIfPresent $watcherEvents (Join-Path $runtime "watcher-events-raw.jsonl")
        Copy-RawIfPresent $orchestratorEvents (Join-Path $runtime "orchestrator-events-raw.jsonl")
    }
}

try {
    Write-Evidence "command:focused-repaired-watcher-tests" @{ executable = "python"; arguments = @("-m", "unittest", "harness_watcher_implementation.tests.test_watcher_smoke"); cwd = $repo }
    $testOut = Join-Path $runtime "focused-tests.stdout.txt"
    $testErr = Join-Path $runtime "focused-tests.stderr.txt"
    $pythonExe = (Get-Command python.exe -ErrorAction Stop).Source
    $testPsi = [Diagnostics.ProcessStartInfo]::new()
    $testPsi.FileName = $pythonExe
    $testPsi.Arguments = "-m unittest harness_watcher_implementation.tests.test_watcher_smoke"
    $testPsi.WorkingDirectory = $repo
    $testPsi.UseShellExecute = $false
    $testPsi.CreateNoWindow = $true
    $testPsi.RedirectStandardOutput = $true
    $testPsi.RedirectStandardError = $true
    $testProc = [Diagnostics.Process]::new()
    $testProc.StartInfo = $testPsi
    [void]$testProc.Start()
    $testStdout = $testProc.StandardOutput.ReadToEnd()
    $testStderr = $testProc.StandardError.ReadToEnd()
    $testProc.WaitForExit()
    $testCode = $testProc.ExitCode
    [IO.File]::WriteAllText($testOut, $testStdout, [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText($testErr, $testStderr, [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText((Join-Path $runtime "focused-tests.result.json"), (([ordered]@{ exit_code = $testCode; stdout = $testStdout; stderr = $testStderr; test = "harness_watcher_implementation.tests.test_watcher_smoke" } | ConvertTo-Json -Depth 10) + "`n"), [Text.UTF8Encoding]::new($false))
    Write-Evidence "result:focused-repaired-watcher-tests" @{ exit_code = $testCode; stdout = $testStdout; stderr = $testStderr }
    $testPass = ($testCode -eq 0)
} catch {
    $testPass = $false
    $failure = if ($failure) { $failure } else { $_.Exception.Message }
    try { Write-Evidence "failure:focused-repaired-watcher-tests" @{ message = $_.Exception.Message } } catch { }
}

$overall = ($practicalPass -and $testPass)
$report = @"
# Luna practical watcher repair report

Result: **$(if ($overall) { 'PASS' } else { 'FAIL' })**

- Practical isolated runtime: runtime/
- Practical topology: one JSONL source, evaluator disabled, sentinel command configured and absent.
- Owner: hidden external `scripts/orchestration/optional_watcher_owner.ps1`; exact PID plus creation identity retained.
- Routing: scalar rejected, routed wrapper over 65,536 bytes rejected once, following valid record routed, and later append routed.
- Continuity: owner and watcher exact identities remained live across multiple poll cycles.
- Shutdown: stop token used; exact owner and watcher identities absent afterward; no broad process kill used.
- Focused tests: `harness_watcher_implementation.tests.test_watcher_smoke` => $(if ($testPass) { 'PASS' } else { 'FAIL' }).

Evidence: raw config/source/service/events/identity/process checks and command results are under runtime/.
$(if ($failure) { "`nFailure detail: $failure`n" } else { "" })
"@
[IO.File]::WriteAllText((Join-Path $evidence "REPORT.md"), $report, [Text.UTF8Encoding]::new($false))
Write-Output $report
if (-not $overall) { exit 1 }

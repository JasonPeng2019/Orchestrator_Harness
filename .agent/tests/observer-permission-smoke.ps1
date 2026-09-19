param([switch]$Child)
$ErrorActionPreference = 'Stop'
$work = $PSScriptRoot
$ready = Join-Path $work 'observer-ready.json'
$stop = Join-Path $work 'observer-stop'
if ($Child) {
    [ordered]@{ pid = $PID; ready = $true } | ConvertTo-Json | Set-Content -LiteralPath $ready -Encoding UTF8
    while (-not (Test-Path -LiteralPath $stop)) { Start-Sleep -Milliseconds 100 }
    exit 0
}
if ((Test-Path -LiteralPath $ready) -or (Test-Path -LiteralPath $stop)) { throw 'Use a fresh smoke workspace.' }
$childProcess = Start-Process powershell.exe -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $PSCommandPath + '"'), '-Child') -WindowStyle Hidden -PassThru
try {
    $until = [DateTime]::UtcNow.AddSeconds(15)
    while (-not (Test-Path -LiteralPath $ready)) {
        if ($childProcess.HasExited) { throw 'Observer exited before readiness.' }
        if ([DateTime]::UtcNow -gt $until) { throw 'Disposable observer did not become ready.' }
        Start-Sleep -Milliseconds 100
    }
    $observed = Get-Content -Raw -LiteralPath $ready | ConvertFrom-Json
    $identity = Get-CimInstance Win32_Process -Filter "ProcessId = $($childProcess.Id)"
    if ($null -eq $identity -or $observed.pid -ne $childProcess.Id) { throw 'Observer identity mismatch.' }
    $creation = $identity.CreationDate.ToUniversalTime().ToString('o')
} finally {
    Set-Content -LiteralPath $stop -Value 'stop' -Encoding UTF8
    if (-not $childProcess.WaitForExit(15000)) {
        # This handle belongs to the child created above; never kill by a broad process match.
        $childProcess.Kill()
        $childProcess.WaitForExit()
        throw 'Observer required forced cleanup.'
    }
}
$proof = [ordered]@{ outcome = 'PASS'; pid = $childProcess.Id; creation_utc = $creation; ready = $true; cleanup_proven = $childProcess.HasExited }
$proof | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $work 'OBSERVER_SMOKE.json') -Encoding UTF8
@{ outcome = 'PASS'; summary = 'Disposable observer became ready and stopped cooperatively.'; checks = @(@{ name = 'observer readiness and exact cleanup'; outcome = 'PASS' }) } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $work 'facts.json') -Encoding UTF8
$settings = Get-Content -Raw -LiteralPath (Join-Path $work 'smoke-paths.json') | ConvertFrom-Json
& python $settings.emitter --context (Join-Path $work 'result-context.json') --facts (Join-Path $work 'facts.json')
if ($LASTEXITCODE -ne 0) { throw 'Result publication failed.' }

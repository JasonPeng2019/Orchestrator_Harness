param(
    [Parameter(Mandatory = $true)][string]$HarnessRoot,
    [Parameter(Mandatory = $true)][string]$DevRoot,
    [Parameter(Mandatory = $true)][string]$FixtureRoot
)

$ErrorActionPreference = 'Stop'

New-Item -ItemType Directory -Force -Path $FixtureRoot | Out-Null
$primary = Join-Path $FixtureRoot 'primary'
$lane = Join-Path $FixtureRoot 'prepared-lane'
New-Item -ItemType Directory -Force -Path $primary | Out-Null
& git -C $primary init --initial-branch main | Out-Null
& git -C $primary config user.email 'super-cache@example.invalid'
& git -C $primary config user.name 'Super Cache Test'
Set-Content -LiteralPath (Join-Path $primary 'super_cache_probe.py') -Value 'VALUE = 0' -NoNewline
& git -C $primary add super_cache_probe.py
& git -C $primary commit -m 'baseline probe' | Out-Null

# The lane intentionally has no .venv.  These two wrappers make the primary
# worktree's environment discoverable by the checked-in verifier.
$scripts = Join-Path $primary '.venv\Scripts'
New-Item -ItemType Directory -Force -Path $scripts | Out-Null
Set-Content -LiteralPath (Join-Path $scripts 'ruff.cmd') -Value "@echo off`nuv run --project `"$DevRoot`" --locked ruff %*" -NoNewline
Set-Content -LiteralPath (Join-Path $scripts 'pyright.cmd') -Value "@echo off`nuv run --project `"$DevRoot`" --locked basedpyright %*" -NoNewline
& git -C $primary worktree add -b prepared-lane $lane HEAD | Out-Null
if (Test-Path -LiteralPath (Join-Path $lane '.venv')) { throw 'prepared lane unexpectedly has a virtual environment' }

& python -m orchestrator_harness workspace super-cache ingest --source (Join-Path $HarnessRoot 'super-cache') --harness-worktree $primary | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'super-cache ingest failed' }
& python -m orchestrator_harness workspace prepare --super-cache (Join-Path $primary 'super-cache') --worktree $lane --role subagent --receipt (Join-Path $FixtureRoot 'receipt.json') | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'super-cache prepare failed' }

$env:AGENT_STOP_GATE_ENABLED = '1'
Push-Location $lane
try {
    $env:AGENT_STOP_GATE_BOUNDARY = 'baseline'
    $baseline = & powershell -NoProfile -NonInteractive -File (Join-Path $lane '.agent\stop-verify.ps1')
    $baselineJson = $baseline | Select-Object -Last 1 | ConvertFrom-Json
    if ($baselineJson.continue -ne $true) { throw "baseline rejected: $($baselineJson.reason)" }

    Set-Content -LiteralPath (Join-Path $lane 'super_cache_probe.py') -Value 'VALUE = 1' -NoNewline
    $env:AGENT_STOP_GATE_BOUNDARY = 'final'
    $final = & powershell -NoProfile -NonInteractive -File (Join-Path $lane '.agent\stop-verify.ps1')
    $finalJson = $final | Select-Object -Last 1 | ConvertFrom-Json
    if ($finalJson.continue -ne $true) { throw "final rejected: $($finalJson.reason)" }
    if (@($finalJson.checks).Count -ne 2) { throw "expected Ruff and Pyright checks, got $($finalJson.checks | ConvertTo-Json -Compress)" }
    if (@($finalJson.checks | Where-Object { $_.exit_code -ne 0 }).Count) { throw 'the checked-in verifier reported a failed check' }
} finally {
    Pop-Location
}

[PSCustomObject]@{
    baseline = $baselineJson
    final = $finalJson
    lane_has_venv = Test-Path -LiteralPath (Join-Path $lane '.venv')
    receipt = Join-Path $FixtureRoot 'receipt.json'
} | ConvertTo-Json -Depth 6 -Compress

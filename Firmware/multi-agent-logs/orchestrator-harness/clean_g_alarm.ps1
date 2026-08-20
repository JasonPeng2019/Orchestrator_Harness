param([string]$Root,[string]$StopFile,[string]$LogFile,[string]$ErrorFile)
Set-Location -LiteralPath $Root
while(-not (Test-Path -LiteralPath $StopFile)) {
  Start-Sleep -Seconds 75
  if(Test-Path -LiteralPath $StopFile){break}
  & python .agent-workspace/tools/canary_supervision_pass.py --config orchestrator_harness/canary-20260731-s1-clean-g.json --epoch 20260731-s1-clean-g 1>> $LogFile 2>> $ErrorFile
  if($LASTEXITCODE -ne 0){"$(Get-Date -AsUTC -Format o) alarm_exit=$LASTEXITCODE" | Add-Content -LiteralPath $ErrorFile}
}

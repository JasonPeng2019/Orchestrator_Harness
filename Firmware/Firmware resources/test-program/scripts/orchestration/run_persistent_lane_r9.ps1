param(
 [Parameter(Mandatory=$true)][string]$RunRoot,
 [Parameter(Mandatory=$true)][string]$ThreadId,
 [Parameter(Mandatory=$true)][string]$PromptPath,
 [Parameter(Mandatory=$true)][string]$Label,
 [Parameter(Mandatory=$true)][string]$Doer,
 [Parameter(Mandatory=$true)][string]$Task,
 [Parameter(Mandatory=$true)][string]$Phase,
 [Parameter(Mandatory=$true)][string]$LaneId,
 [Parameter(Mandatory=$true)][string]$StatusPath,
 [Parameter(Mandatory=$true)][string]$JsonlPath,
 [Parameter(Mandatory=$true)][string]$StderrPath,
 [Parameter(Mandatory=$true)][string]$LastMessagePath,
 [Parameter(Mandatory=$true)][string]$LaneEventLog,
 [string[]]$Leases=@(),
 [string[]]$BoardTokens=@()
)
$ErrorActionPreference='Stop'
function Write-AtomicJson([string]$Path,$Value){$tmp="$Path.$PID.tmp";[IO.File]::WriteAllText($tmp,($Value|ConvertTo-Json -Depth 10)+"`n",[Text.UTF8Encoding]::new($false));Move-Item -LiteralPath $tmp -Destination $Path -Force}
function Append-JsonLine([string]$Path,$Value){[IO.File]::AppendAllText($Path,($Value|ConvertTo-Json -Compress -Depth 8)+"`n",[Text.UTF8Encoding]::new($false))}
$root=(Resolve-Path -LiteralPath $RunRoot).Path; $prompt=(Resolve-Path -LiteralPath $PromptPath).Path
$controller=Get-Process -Id $PID; $controllerUtc=$controller.StartTime.ToUniversalTime().ToString('o'); $started=[DateTime]::UtcNow.ToString('o')
$arguments=@('exec','resume',$ThreadId,'--dangerously-bypass-approvals-and-sandbox','--ignore-user-config','--skip-git-repo-check','-c','approval_policy="never"','-c','approvals_reviewer="user"','-m','gpt-5.6-luna','-c','model_reasoning_effort="high"','-c','service_tier="default"','--json','--output-last-message',$LastMessagePath)
$codex=Start-Process -FilePath 'codex.exe' -ArgumentList $arguments -WorkingDirectory $root -RedirectStandardInput $prompt -RedirectStandardOutput $JsonlPath -RedirectStandardError $StderrPath -WindowStyle Hidden -PassThru
$codex.Refresh();$codexUtc=$codex.StartTime.ToUniversalTime().ToString('o')
$status=[ordered]@{schema='orchestrator-lane-controller/v1';state='RUNNING_CODEX';controller_pid=$PID;controller_started_utc=$controllerUtc;controller_created_utc=$controllerUtc;codex_pid=$codex.Id;codex_started_utc=$codexUtc;codex_created_utc=$codexUtc;declared_lane_id=$LaneId;doer=$Doer;task=$Task;phase=$Phase;thread_id=$ThreadId;started_utc=$started;prompt_path=$prompt;status_path=$StatusPath;jsonl_path=$JsonlPath;stderr_path=$StderrPath;last_message_path=$LastMessagePath;leases=$Leases;board_tokens=$BoardTokens;mcp_servers=@();launcher_settings=[ordered]@{model='gpt-5.6-luna';model_reasoning_effort='high';service_tier='default';approval_policy='never';sandbox='danger-full-access';ephemeral=$false;jsonl=$true;argv=@('codex')+$arguments}}
Write-AtomicJson $StatusPath $status; Append-JsonLine $LaneEventLog ([ordered]@{event='CODEX_STARTED';utc=[DateTime]::UtcNow.ToString('o');label=$Label;declared_lane_id=$LaneId;controller_pid=$PID;codex_pid=$codex.Id})
$codex.WaitForExit();$codex.Refresh();$status.state='CODEX_EXITED';$status.exit_code=$codex.ExitCode;$status.ended_utc=[DateTime]::UtcNow.ToString('o');Write-AtomicJson $StatusPath $status;Append-JsonLine $LaneEventLog ([ordered]@{event='CODEX_EXITED';utc=[DateTime]::UtcNow.ToString('o');label=$Label;declared_lane_id=$LaneId;thread_id=$ThreadId;exit_code=$codex.ExitCode})
exit $codex.ExitCode

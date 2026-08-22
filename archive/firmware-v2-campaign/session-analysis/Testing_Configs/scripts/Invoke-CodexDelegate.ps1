[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0)]
    [ValidateSet('luna', 'deepseek')]
    [string]$Agent,

    [Parameter(Mandatory, Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$Task,

    [switch]$ReadOnly,

    [switch]$New
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$profilePath = Join-Path $repoRoot ".codex\delegates\$Agent.toml"
$sessionDirectory = Join-Path $repoRoot '.codex\delegates\sessions'
$sessionPath = Join-Path $sessionDirectory "$Agent.json"

function Get-DelegateProfile {
    param([string]$Path)

    $settings = @{}
    foreach ($rawLine in Get-Content -LiteralPath $Path) {
        $line = $rawLine.Trim()
        if (-not $line -or $line.StartsWith('#')) { continue }

        if ($line -notmatch '^(?<key>[A-Za-z0-9_]+)\s*=\s*(?<value>.+?)\s*$') {
            throw "Unsupported profile line in $Path`: $rawLine"
        }

        $key = $Matches.key
        $value = $Matches.value.Trim()
        if ($value -match '^"(?<text>(?:[^"\\]|\\.)*)"$') {
            $value = $Matches.text -replace '\\"', '"' -replace '\\\\', '\\'
        }
        elseif ($value -match '^(true|false)$') {
            $value = [bool]::Parse($value)
        }
        elseif ($value -match '^\d+$') {
            $value = [long]$value
        }
        else {
            throw "Unsupported TOML value for '$key' in $Path"
        }
        $settings[$key] = $value
    }
    return $settings
}

if (-not (Test-Path -LiteralPath $profilePath)) {
    throw "Delegate profile not found: $profilePath"
}
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw 'The Codex CLI was not found on PATH.'
}

$profile = Get-DelegateProfile -Path $profilePath
$taskText = $Task -join ' '

function ConvertTo-TomlLiteral {
    param($Value)
    if ($Value -is [bool]) { return $Value.ToString().ToLowerInvariant() }
    if ($Value -is [int] -or $Value -is [long]) { return $Value.ToString() }
    return ($Value | ConvertTo-Json -Compress)
}

$commonConfigArgs = @(
    '--model', $profile.model,
    '--config', "model_reasoning_effort=$(ConvertTo-TomlLiteral $profile.model_reasoning_effort)",
    '--config', "model_context_window=$(ConvertTo-TomlLiteral $profile.model_context_window)",
    '--config', "model_auto_compact_token_limit=$(ConvertTo-TomlLiteral $profile.model_auto_compact_token_limit)",
    '--config', "model_auto_compact_token_limit_scope=$(ConvertTo-TomlLiteral $profile.model_auto_compact_token_limit_scope)"
)

if (-not $ReadOnly -and $profile.ContainsKey('windows_sandbox')) {
    $commonConfigArgs += '--config', "windows.sandbox=$(ConvertTo-TomlLiteral $profile.windows_sandbox)"
}
if ($profile.ContainsKey('model_catalog_json')) {
    $catalogPath = Join-Path (Split-Path -Parent $profilePath) $profile.model_catalog_json
    if (-not (Test-Path -LiteralPath $catalogPath)) {
        throw "Model catalog not found: $catalogPath"
    }
    $commonConfigArgs += '--config', "model_catalog_json=$(ConvertTo-TomlLiteral $catalogPath)"
}
if ($profile.ContainsKey('local_provider')) {
    $providerConfig = "model_provider=$(ConvertTo-TomlLiteral $profile.local_provider)"
}

function Save-DelegateSession {
    param([string]$ThreadId)

    New-Item -ItemType Directory -Force -Path $sessionDirectory | Out-Null
    [ordered]@{
        agent = $Agent
        thread_id = $ThreadId
        model = $profile.model
        created_or_updated = (Get-Date).ToString('o')
    } | ConvertTo-Json | Set-Content -LiteralPath $sessionPath -Encoding utf8
}

$session = $null
if ((Test-Path -LiteralPath $sessionPath) -and -not $New) {
    try { $session = Get-Content -Raw -LiteralPath $sessionPath | ConvertFrom-Json }
    catch { throw "Invalid delegate session record: $sessionPath" }
    if (-not $session.thread_id) { throw "Delegate session record has no thread_id: $sessionPath" }
}

if ($session) {
    $mode = 'resuming'
    $prompt = $taskText
    $codexArgs = @('exec', 'resume', '--strict-config', '--ignore-user-config', '--skip-git-repo-check', '--json')
    $codexArgs += $commonConfigArgs
    if ($providerConfig) { $codexArgs += '--config', $providerConfig }
    $codexArgs += $session.thread_id
}
else {
    $mode = 'starting'
    $prompt = "$($profile.developer_instructions)`n`nDelegated task:`n$taskText"
    $codexArgs = @(
        'exec', '--strict-config', '--ignore-user-config', '--skip-git-repo-check', '--json',
        '--cd', $repoRoot,
        '--sandbox', $(if ($ReadOnly) { 'read-only' } else { 'workspace-write' })
    )
    $codexArgs += $commonConfigArgs
    $codexArgs += '--config', "developer_instructions=$(ConvertTo-TomlLiteral $profile.developer_instructions)"
    if ($profile.ContainsKey('use_oss') -and $profile.use_oss) {
        $codexArgs += '--oss', '--local-provider', $profile.local_provider
    }
}

Write-Host "$($mode.Substring(0, 1).ToUpper() + $mode.Substring(1)) $Agent with a $($profile.model_auto_compact_token_limit)-token auto-compaction threshold."
& codex @codexArgs $prompt | ForEach-Object {
    $eventText = $_
    try { $event = $eventText | ConvertFrom-Json -ErrorAction Stop }
    catch { Write-Host $eventText; return }

    if ($event.type -eq 'thread.started') {
        Save-DelegateSession -ThreadId $event.thread_id
        Write-Host "Delegate session: $($event.thread_id)"
    }
    elseif ($event.type -eq 'item.completed' -and $event.item.type -eq 'agent_message') {
        Write-Output $event.item.text
    }
    elseif ($event.type -eq 'item.completed' -and $event.item.type -eq 'error') {
        Write-Warning $event.item.message
    }
}
exit $LASTEXITCODE

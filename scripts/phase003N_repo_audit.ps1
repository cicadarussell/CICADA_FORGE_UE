Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003N REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "tools\cicada_health\cicada_health_report.py",
    "tools\cicada_launcher\cicada_command_center.py",
    "scripts\diagnostics\cicada_health_report.ps1",
    "scripts\launcher\cicada_generate_command_center.ps1",
    "scripts\open_cicada_command_center.ps1",
    "scripts\cicada_control_room.ps1",
    "scripts\headless\cicada_headless_phase003N_full_check.ps1",
    "scripts\cicada_forge.ps1",
    "docs\PHASE_CLUSTER_003N_COMMAND_CENTER_AND_PASSIVE_HEALTH.md",
    "docs\checklists\PHASE_003N_SMOKE_TEST.md",
    "docs\debug\PASSIVE_HEALTH_CONTRACT.md",
    "docs\debug\COMMAND_CENTER_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003N.md"
)

$missing = @()
foreach ($file in $required) {
    if (Test-Path $file) { Write-Host "[OK]      $file" }
    else { Write-Host "[MISSING] $file"; $missing += $file }
}

Write-Host ""
git status --short
Write-Host ""

if ($missing.Count -gt 0) {
    Write-Host "AUDIT FAIL: missing required files."
    exit 1
}

$config = Get-Content "Config\CICADAForgeState.ini" -Raw
$wrapper = Get-Content "scripts\cicada_forge.ps1" -Raw
$health = Get-Content "tools\cicada_health\cicada_health_report.py" -Raw
$center = Get-Content "tools\cicada_launcher\cicada_command_center.py" -Raw

if ($config -notmatch "Phase 003N: command center and passive health report are alive") {
    Write-Host "AUDIT FAIL: 003N config marker missing."
    exit 1
}

foreach ($marker in @("health-report", "command-center", "control-room", "phase003N-full-check")) {
    if ($wrapper -notmatch $marker) {
        Write-Host "AUDIT FAIL: wrapper marker missing: $marker"
        exit 1
    }
}

if ($health -notmatch "NOT_RUN") {
    Write-Host "AUDIT FAIL: passive health NOT_RUN marker missing."
    exit 1
}

if ($center -notmatch "CICADA COMMAND CENTER") {
    Write-Host "AUDIT FAIL: command center title marker missing."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003N files present."

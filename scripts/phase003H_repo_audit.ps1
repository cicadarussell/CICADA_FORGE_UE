Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003H REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "tools\cicada_dashboard\cicada_artifact_dashboard.py",
    "tools\cicada_headless\cicada_forge_headless.py",
    "scripts\cicada_forge.ps1",
    "scripts\open_cicada_dashboard.ps1",
    "scripts\headless\cicada_headless_dashboard.ps1",
    "scripts\diagnostics\cicada_dashboard_quick_check.ps1",
    "docs\PHASE_CLUSTER_003H_LOCAL_DASHBOARD_CONTROL_ROOM.md",
    "docs\checklists\PHASE_003H_SMOKE_TEST.md",
    "docs\debug\LOCAL_DASHBOARD_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003H.md"
)

$missing = @()

foreach ($file in $required) {
    if (Test-Path $file) {
        Write-Host "[OK]      $file"
    } else {
        Write-Host "[MISSING] $file"
        $missing += $file
    }
}

Write-Host ""
git status --short
Write-Host ""

if ($missing.Count -gt 0) {
    Write-Host "AUDIT FAIL: missing required files."
    exit 1
}

$config = Get-Content "Config\CICADAForgeState.ini" -Raw
$dashboard = Get-Content "tools\cicada_dashboard\cicada_artifact_dashboard.py" -Raw
$headless = Get-Content "tools\cicada_headless\cicada_forge_headless.py" -Raw
$wrapper = Get-Content "scripts\cicada_forge.ps1" -Raw

if ($config -notmatch "Phase 003H: local artifact dashboard and control room are alive") {
    Write-Host "AUDIT FAIL: Phase 003H marker not found in config."
    exit 1
}

if ($dashboard -notmatch "CICADA FORGE CONTROL ROOM") {
    Write-Host "AUDIT FAIL: dashboard title marker not found."
    exit 1
}

if ($dashboard -notmatch "direct_printer_send") {
    Write-Host "AUDIT FAIL: dashboard direct printer safety marker not found."
    exit 1
}

if ($headless -notmatch "dashboard") {
    Write-Host "AUDIT FAIL: headless dashboard command marker not found."
    exit 1
}

if ($wrapper -notmatch "dashboard") {
    Write-Host "AUDIT FAIL: wrapper dashboard command marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003H files present."

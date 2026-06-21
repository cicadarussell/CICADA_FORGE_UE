Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003G REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "tools\cicada_headless\cicada_forge_headless.py",
    "scripts\cicada_forge.ps1",
    "scripts\headless\cicada_headless_full_check.ps1",
    "scripts\headless\cicada_headless_demo_box.ps1",
    "scripts\headless\cicada_headless_custom_box.ps1",
    "scripts\headless\cicada_headless_doctor.ps1",
    "scripts\headless\cicada_headless_inventory.ps1",
    "scripts\headless\cicada_headless_run_report.ps1",
    "docs\PHASE_CLUSTER_003G_HEADLESS_CONTROL_TOWER.md",
    "docs\checklists\PHASE_003G_SMOKE_TEST.md",
    "docs\debug\HEADLESS_CONTROL_TOWER_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003G.md"
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
$headless = Get-Content "tools\cicada_headless\cicada_forge_headless.py" -Raw
$wrapper = Get-Content "scripts\cicada_forge.ps1" -Raw

if ($config -notmatch "Phase 003G: headless forge control tower is alive") {
    Write-Host "AUDIT FAIL: Phase 003G marker not found in config."
    exit 1
}

if ($headless -notmatch "full-check") {
    Write-Host "AUDIT FAIL: headless full-check marker not found."
    exit 1
}

if ($headless -notmatch "manifest-check") {
    Write-Host "AUDIT FAIL: manifest safety check marker not found."
    exit 1
}

if ($headless -notmatch "Direct printer send: LOCKED") {
    Write-Host "AUDIT FAIL: printer lock marker not found."
    exit 1
}

if ($wrapper -notmatch "custom-box") {
    Write-Host "AUDIT FAIL: wrapper custom-box marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003G files present."

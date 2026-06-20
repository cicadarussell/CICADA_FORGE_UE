Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002F REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_002F_VISIBLE_SELECTED_ACTION_STATE.md",
    "docs\checklists\PHASE_002F_SMOKE_TEST.md"
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
$module = Get-Content "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp" -Raw
$state = Get-Content "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp" -Raw

if ($config -notmatch "Phase 002F: selected action state updates on screen") {
    Write-Host "AUDIT FAIL: Phase 002F marker not found in config."
    exit 1
}

if ($module -notmatch "Selected action: none") {
    Write-Host "AUDIT FAIL: selected-action initial text not found."
    exit 1
}

if ($module -notmatch "Selected action: \{0\} - safe stub only") {
    Write-Host "AUDIT FAIL: selected-action format not found."
    exit 1
}

if ($state -notmatch "NormalizeConfigIniPath") {
    Write-Host "AUDIT FAIL: config path normalization not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002F files present."

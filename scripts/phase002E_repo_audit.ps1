Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002E REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_002E_SAFE_ACTION_BUTTON_STUBS.md",
    "docs\checklists\PHASE_002E_SMOKE_TEST.md"
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

if ($config -notmatch "Phase 002E: action button stubs are alive") {
    Write-Host "AUDIT FAIL: Phase 002E marker not found in config."
    exit 1
}

if ($module -notmatch "SButton") {
    Write-Host "AUDIT FAIL: SButton not found in editor module."
    exit 1
}

if ($module -notmatch "safe action stub clicked") {
    Write-Host "AUDIT FAIL: safe action log marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002E files present."

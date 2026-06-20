Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002D REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Public\CICADAForgeProjectState.h",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "docs\PHASE_CLUSTER_002D_PERSISTENT_PROJECT_STATE.md",
    "docs\checklists\PHASE_002D_SMOKE_TEST.md"
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
$model = Get-Content "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp" -Raw
$state = Get-Content "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp" -Raw

if ($config -notmatch "Phase 002D: persistent project state feeds the shell") {
    Write-Host "AUDIT FAIL: Phase 002D marker not found in config."
    exit 1
}

if ($model -notmatch "MakePhase002DDefault") {
    Write-Host "AUDIT FAIL: status model does not expose MakePhase002DDefault."
    exit 1
}

if ($state -notmatch "LoadFromConfig") {
    Write-Host "AUDIT FAIL: project state config loader not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002D files present."

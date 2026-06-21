Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003A REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_003A_FEATURE_GRAPH_V0.md",
    "docs\checklists\PHASE_003A_SMOKE_TEST.md",
    "docs\debug\FEATURE_GRAPH_V0_CONTRACT.md",
    "scripts\diagnostics\cicada_saved_artifact_inventory.ps1"
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

if ($config -notmatch "Phase 003A: feature graph V0 and backend inspector are alive") {
    Write-Host "AUDIT FAIL: Phase 003A marker not found in config."
    exit 1
}

if ($module -notmatch "Feature Graph V0 Controls") {
    Write-Host "AUDIT FAIL: Feature Graph V0 Controls marker not found."
    exit 1
}

if ($module -notmatch "Add Box primitive") {
    Write-Host "AUDIT FAIL: Add Box primitive marker not found."
    exit 1
}

if ($module -notmatch "Run feature validation dry-run") {
    Write-Host "AUDIT FAIL: feature validation marker not found."
    exit 1
}

if ($module -notmatch "CICADAForge/FeatureGraphs") {
    Write-Host "AUDIT FAIL: feature graph save path marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003A files present."

Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002I REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_002I_SESSION_METADATA_PANEL.md",
    "docs\checklists\PHASE_002I_SMOKE_TEST.md"
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

if ($config -notmatch "Phase 002I: session metadata panel tracks the local Forge run") {
    Write-Host "AUDIT FAIL: Phase 002I marker not found in config."
    exit 1
}

if ($module -notmatch "Session Metadata") {
    Write-Host "AUDIT FAIL: Session Metadata UI marker not found."
    exit 1
}

if ($module -notmatch "BuildSessionMetadataText") {
    Write-Host "AUDIT FAIL: session metadata builder not found."
    exit 1
}

if ($module -notmatch "Persistence: memory only") {
    Write-Host "AUDIT FAIL: memory-only persistence marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002I files present."

Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002H REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_002H_IN_MEMORY_EVENT_LOG.md",
    "docs\checklists\PHASE_002H_SMOKE_TEST.md"
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

if ($config -notmatch "Phase 002H: in-memory event log records safe UI clicks") {
    Write-Host "AUDIT FAIL: Phase 002H marker not found in config."
    exit 1
}

if ($module -notmatch "Event Log") {
    Write-Host "AUDIT FAIL: Event Log UI marker not found."
    exit 1
}

if ($module -notmatch "BuildEventLogText") {
    Write-Host "AUDIT FAIL: Event Log builder not found."
    exit 1
}

if ($module -notmatch "safe stub logged only") {
    Write-Host "AUDIT FAIL: safe event log marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002H files present."

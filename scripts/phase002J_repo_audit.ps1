Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002J REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_002J_EVIDENCE_RECEIPT_COCKPIT.md",
    "docs\checklists\PHASE_002J_SMOKE_TEST.md"
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

if ($config -notmatch "Phase 002J: evidence receipt cockpit is alive") {
    Write-Host "AUDIT FAIL: Phase 002J marker not found in config."
    exit 1
}

if ($module -notmatch "Evidence Receipt Controls") {
    Write-Host "AUDIT FAIL: Evidence Receipt Controls UI marker not found."
    exit 1
}

if ($module -notmatch "Evidence Receipt Preview") {
    Write-Host "AUDIT FAIL: Evidence Receipt Preview UI marker not found."
    exit 1
}

if ($module -notmatch "Screenshot observed") {
    Write-Host "AUDIT FAIL: Screenshot observed evidence marker not found."
    exit 1
}

if ($module -notmatch "Clear visible event log") {
    Write-Host "AUDIT FAIL: Clear visible event log marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002J files present."

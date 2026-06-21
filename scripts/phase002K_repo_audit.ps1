Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002K REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_002K_DEBUG_COCKPIT_AND_RECEIPT_DRY_RUN.md",
    "docs\checklists\PHASE_002K_SMOKE_TEST.md",
    "docs\debug\UNREAL_OUTPUT_LOG_TRIAGE.md",
    "scripts\diagnostics\cicada_unreal_log_quickscan.ps1"
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
$quickscan = Get-Content "scripts\diagnostics\cicada_unreal_log_quickscan.ps1" -Raw

if ($config -notmatch "Phase 002K: debug cockpit and receipt dry-run are alive") {
    Write-Host "AUDIT FAIL: Phase 002K marker not found in config."
    exit 1
}

if ($module -notmatch "Evidence \\+ Debug Controls") {
    Write-Host "AUDIT FAIL: Evidence + Debug Controls UI marker not found."
    exit 1
}

if ($module -notmatch "Diagnostics") {
    Write-Host "AUDIT FAIL: Diagnostics UI marker not found."
    exit 1
}

if ($module -notmatch "Save local dry-run receipt") {
    Write-Host "AUDIT FAIL: receipt dry-run button marker not found."
    exit 1
}

if ($module -notmatch "Saved/CICADAForge/Receipts") {
    Write-Host "AUDIT FAIL: scoped receipt path marker not found."
    exit 1
}

if ($quickscan -notmatch "CICADA UNREAL LOG QUICKSCAN") {
    Write-Host "AUDIT FAIL: log quickscan script marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002K files present."

Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002L REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_002L_SCROLLABLE_BACKEND_DEBUG_COCKPIT.md",
    "docs\checklists\PHASE_002L_SMOKE_TEST.md",
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
$triage = Get-Content "docs\debug\UNREAL_OUTPUT_LOG_TRIAGE.md" -Raw

if ($config -notmatch "Phase 002L: scrollable backend debug cockpit is alive") {
    Write-Host "AUDIT FAIL: Phase 002L marker not found in config."
    exit 1
}

if ($module -notmatch "SScrollBox") {
    Write-Host "AUDIT FAIL: SScrollBox marker not found."
    exit 1
}

if ($module -notmatch "Backend Inspector") {
    Write-Host "AUDIT FAIL: Backend Inspector marker not found."
    exit 1
}

if ($module -notmatch "Backend Health") {
    Write-Host "AUDIT FAIL: Backend Health marker not found."
    exit 1
}

if ($module -notmatch "Show backend map") {
    Write-Host "AUDIT FAIL: Show backend map marker not found."
    exit 1
}

if ($triage -notmatch "EOSSDK") {
    Write-Host "AUDIT FAIL: EOSSDK triage marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002L files present."

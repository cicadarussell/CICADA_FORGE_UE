Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002C REPO AUDIT ==="

$required = @(
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Public\CICADAForgeStatusModel.h",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "docs\process\UNREAL_STALE_BINARY_FIX.md",
    "docs\process\CICADA_APP_BUILD_LOOP_STANDING_RULE.md",
    "docs\PHASE_CLUSTER_002C_STATUS_MODEL.md",
    "docs\checklists\PHASE_002C_SMOKE_TEST.md"
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

$model = Get-Content "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp" -Raw
$module = Get-Content "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp" -Raw

if ($model -notmatch "Phase 002C: status model feeds the shell") {
    Write-Host "AUDIT FAIL: Phase 002C marker not found in status model."
    exit 1
}

if ($module -notmatch "MakePhase002CDefault") {
    Write-Host "AUDIT FAIL: editor module is not reading from the Phase 002C status model."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002C files present."

Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003C REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_003C_PRINT_READY_STL_HANDOFF.md",
    "docs\checklists\PHASE_003C_SMOKE_TEST.md",
    "docs\debug\PRINT_HANDOFF_CONTRACT.md",
    "tools\cicada_stl_sidecar\cicada_parametric_box_stl.py",
    "scripts\open_latest_stl_in_default_app.ps1",
    "scripts\diagnostics\cicada_find_slicers.ps1",
    "scripts\diagnostics\cicada_validate_latest_stl.ps1"
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
$contract = Get-Content "docs\debug\PRINT_HANDOFF_CONTRACT.md" -Raw

if ($config -notmatch "Phase 003C: print-ready STL handoff workflow is alive") {
    Write-Host "AUDIT FAIL: Phase 003C marker not found in config."
    exit 1
}

if ($module -notmatch "Print-Ready Sketch Box Workflow") {
    Write-Host "AUDIT FAIL: Print-Ready workflow marker not found."
    exit 1
}

if ($module -notmatch "Open latest STL in default app") {
    Write-Host "AUDIT FAIL: default app/slicer button marker not found."
    exit 1
}

if ($module -notmatch "direct_printer_send") {
    Write-Host "AUDIT FAIL: printer lock manifest marker not found."
    exit 1
}

if ($contract -notmatch "send directly to printer") {
    Write-Host "AUDIT FAIL: print handoff safety contract marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003C files present."

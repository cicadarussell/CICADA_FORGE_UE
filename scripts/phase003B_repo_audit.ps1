Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003B REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_003B_SKETCH_BOX_TO_STL.md",
    "docs\checklists\PHASE_003B_SMOKE_TEST.md",
    "docs\debug\SKETCH_TO_STL_CONTRACT.md",
    "tools\cicada_stl_sidecar\cicada_box_stl_sidecar.py",
    "scripts\generate_example_box_stl.ps1",
    "scripts\diagnostics\cicada_validate_latest_stl.ps1",
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
$sidecar = Get-Content "tools\cicada_stl_sidecar\cicada_box_stl_sidecar.py" -Raw

if ($config -notmatch "Phase 003B: sketch box to STL export pipeline is alive") {
    Write-Host "AUDIT FAIL: Phase 003B marker not found in config."
    exit 1
}

if ($module -notmatch "Generate box STL") {
    Write-Host "AUDIT FAIL: Generate box STL marker not found."
    exit 1
}

if ($module -notmatch "Prepare locked print handoff manifest") {
    Write-Host "AUDIT FAIL: locked print handoff marker not found."
    exit 1
}

if ($module -notmatch "CICADAForge/STL") {
    Write-Host "AUDIT FAIL: STL output scope marker not found."
    exit 1
}

if ($sidecar -notmatch "Direct printer send: LOCKED") {
    Write-Host "AUDIT FAIL: sidecar printer lock marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003B files present."

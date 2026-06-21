Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003I REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "tools\cicada_cad_sidecar\cicada_cad_sidecar.py",
    "tools\cicada_cad_sidecar\schemas\cicada_part_schema_v0_1.json",
    "examples\cad_parts\simple_box.part.json",
    "examples\cad_parts\mounting_plate_2holes.part.json",
    "examples\cad_parts\electronics_enclosure_blank.part.json",
    "scripts\cad\cicada_cad_doctor.ps1",
    "scripts\cad\cicada_cad_validate_examples.ps1",
    "scripts\cad\cicada_cad_generate_part.ps1",
    "scripts\cad\cicada_cad_demo.ps1",
    "scripts\diagnostics\cicada_cad_sidecar_quick_check.ps1",
    "docs\PHASE_CLUSTER_003I_CAD_SIDECAR_CONTRACT.md",
    "docs\checklists\PHASE_003I_SMOKE_TEST.md",
    "docs\debug\CAD_SIDECAR_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003I.md",
    "docs\cad\README_CAD_SIDECAR_V0.md"
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
$sidecar = Get-Content "tools\cicada_cad_sidecar\cicada_cad_sidecar.py" -Raw
$contract = Get-Content "docs\debug\CAD_SIDECAR_CONTRACT.md" -Raw
$dashboard = Get-Content "tools\cicada_dashboard\cicada_artifact_dashboard.py" -Raw

if ($config -notmatch "Phase 003I: CAD sidecar contract and exact-geometry boundary are alive") {
    Write-Host "AUDIT FAIL: Phase 003I marker not found in config."
    exit 1
}

if ($sidecar -notmatch "No fake STEP") {
    Write-Host "AUDIT WARNING: literal No fake STEP marker not found. Checking alternate marker..."
}

if ($sidecar -notmatch "Exact STEP export blocked") {
    Write-Host "AUDIT FAIL: blocked STEP marker not found in sidecar."
    exit 1
}

if ($contract -notmatch "No-fake-STEP rule") {
    Write-Host "AUDIT FAIL: no-fake-STEP contract marker not found."
    exit 1
}

if ($dashboard -notmatch "CADReports") {
    Write-Host "AUDIT FAIL: dashboard CADReports marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003I files present."

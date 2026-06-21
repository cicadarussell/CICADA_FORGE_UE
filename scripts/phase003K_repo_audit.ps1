Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003K REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "tools\cicada_cad_sidecar\cicada_cad_sidecar.py",
    "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py",
    "tools\cicada_cad_sidecar\cicada_part_compare.py",
    "tools\cicada_cad_sidecar\schemas\cicada_part_schema_v0_2.json",
    "examples\cad_parts\robot_sensor_plate_v02.part.json",
    "examples\cad_parts\slotted_motor_mount_v02.part.json",
    "scripts\cad\cicada_cad_make_sensor_plate.ps1",
    "scripts\cad\cicada_cad_make_slotted_motor_mount.ps1",
    "scripts\cad\cicada_cad_sample_pack.ps1",
    "scripts\cad\cicada_cad_compare_parts.ps1",
    "scripts\cicada_forge.ps1",
    "docs\PHASE_CLUSTER_003K_RICHER_CAD_FEATURE_INTENT.md",
    "docs\checklists\PHASE_003K_SMOKE_TEST.md",
    "docs\debug\CAD_FEATURE_INTENT_V0_2_CONTRACT.md",
    "docs\debug\CAD_SAMPLE_PACK_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003K.md",
    "docs\cad\CAD_FEATURES_V0_2.md"
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
$builder = Get-Content "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py" -Raw
$wrapper = Get-Content "scripts\cicada_forge.ps1" -Raw
$dashboard = Get-Content "tools\cicada_dashboard\cicada_artifact_dashboard.py" -Raw

if ($config -notmatch "Phase 003K: richer CAD feature intent and sample pack are alive") {
    Write-Host "AUDIT FAIL: Phase 003K marker not found in config."
    exit 1
}

foreach ($marker in @("slot", "standoff", "cicada_part_v0_2", "No fake STEP")) {
    if ($sidecar -notmatch $marker) {
        Write-Host "AUDIT FAIL: sidecar marker missing: $marker"
        exit 1
    }
}

if ($builder -notmatch "slotted-motor-mount") {
    Write-Host "AUDIT FAIL: slotted motor mount builder marker missing."
    exit 1
}

if ($wrapper -notmatch "cad-sample-pack") {
    Write-Host "AUDIT FAIL: cad-sample-pack wrapper marker missing."
    exit 1
}

if ($dashboard -notmatch "Command Cards") {
    Write-Host "AUDIT FAIL: dashboard command cards marker missing."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003K files present."

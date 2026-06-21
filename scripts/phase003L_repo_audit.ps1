Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003L REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "tools\cicada_env\cicada_environment_manager.py",
    "tools\cicada_slicer\cicada_slicer_readiness.py",
    "scripts\env\cicada_env_doctor.ps1",
    "scripts\env\cicada_env_plan.ps1",
    "scripts\env\cicada_env_create_cadquery_venv.ps1",
    "scripts\env\cicada_env_install_cadquery.ps1",
    "scripts\slicer\cicada_slicer_readiness.ps1",
    "scripts\headless\cicada_headless_env_slicer_full_check.ps1",
    "scripts\cicada_forge.ps1",
    "docs\PHASE_CLUSTER_003L_ENV_AND_SLICER_READINESS.md",
    "docs\checklists\PHASE_003L_SMOKE_TEST.md",
    "docs\debug\CAD_ENVIRONMENT_CONTRACT.md",
    "docs\debug\SLICER_READINESS_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003L.md"
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
$wrapper = Get-Content "scripts\cicada_forge.ps1" -Raw
$slicer = Get-Content "tools\cicada_slicer\cicada_slicer_readiness.py" -Raw
$env = Get-Content "tools\cicada_env\cicada_environment_manager.py" -Raw
$dashboard = Get-Content "tools\cicada_dashboard\cicada_artifact_dashboard.py" -Raw

if ($config -notmatch "Phase 003L: CAD engine bootstrap and slicer readiness are alive") {
    Write-Host "AUDIT FAIL: 003L config marker missing."
    exit 1
}

foreach ($marker in @("env-doctor", "slicer-readiness", "env-slicer-full-check")) {
    if ($wrapper -notmatch $marker) {
        Write-Host "AUDIT FAIL: wrapper marker missing: $marker"
        exit 1
    }
}

if ($slicer -notmatch "gcode_generated") {
    Write-Host "AUDIT FAIL: slicer no-gcode marker missing."
    exit 1
}

if ($env -notmatch "automatic_install") {
    Write-Host "AUDIT FAIL: env automatic install safety marker missing."
    exit 1
}

if ($dashboard -notmatch "SlicerReports") {
    Write-Host "AUDIT FAIL: dashboard SlicerReports marker missing."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003L files present."

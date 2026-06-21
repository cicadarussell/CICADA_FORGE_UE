Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003M REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "tools\cicada_env\cicada_cad_engine_launcher.py",
    "tools\cicada_slicer\cicada_slicer_dryrun_planner.py",
    "scripts\env\cicada_cad_engine_launcher_doctor.ps1",
    "scripts\cad\cicada_cad_generate_part_engine.ps1",
    "scripts\slicer\cicada_slicer_dryrun_plan.ps1",
    "scripts\headless\cicada_headless_phase003M_full_check.ps1",
    "scripts\cicada_forge.ps1",
    "docs\PHASE_CLUSTER_003M_CAD_ENGINE_LAUNCHER_AND_SLICER_DRYRUN.md",
    "docs\checklists\PHASE_003M_SMOKE_TEST.md",
    "docs\debug\CAD_ENGINE_LAUNCHER_CONTRACT.md",
    "docs\debug\SLICER_DRYRUN_PLAN_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003M.md"
)

$missing = @()
foreach ($file in $required) {
    if (Test-Path $file) { Write-Host "[OK]      $file" }
    else { Write-Host "[MISSING] $file"; $missing += $file }
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
$launcher = Get-Content "tools\cicada_env\cicada_cad_engine_launcher.py" -Raw
$slicer = Get-Content "tools\cicada_slicer\cicada_slicer_dryrun_planner.py" -Raw

if ($config -notmatch "Phase 003M: CAD engine launcher and slicer dry-run planner are alive") {
    Write-Host "AUDIT FAIL: 003M config marker missing."
    exit 1
}

foreach ($marker in @("cad-engine-doctor", "cad-generate-engine", "slicer-dryrun-plan", "phase003M-full-check")) {
    if ($wrapper -notmatch $marker) {
        Write-Host "AUDIT FAIL: wrapper marker missing: $marker"
        exit 1
    }
}

if ($launcher -notmatch ".cicada_envs") {
    Write-Host "AUDIT FAIL: launcher venv marker missing."
    exit 1
}

if ($slicer -notmatch "gcode_generated") {
    Write-Host "AUDIT FAIL: slicer no-gcode marker missing."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003M files present."

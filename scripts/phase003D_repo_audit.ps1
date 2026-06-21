Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003D REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "tools\cicada_stl_sidecar\cicada_box_job_runner.py",
    "examples\box_jobs\test_block_20x20x10.json",
    "scripts\run_box_job.ps1",
    "scripts\run_all_box_jobs.ps1",
    "scripts\diagnostics\cicada_project_on_track_check.ps1",
    "scripts\diagnostics\cicada_validate_box_job_files.ps1",
    "docs\PHASE_CLUSTER_003D_PROJECT_TRACK_AND_BOX_JOB_RUNNER.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003D.md",
    "docs\checklists\PHASE_003D_SMOKE_TEST.md"
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
$runner = Get-Content "tools\cicada_stl_sidecar\cicada_box_job_runner.py" -Raw

if ($config -notmatch "Phase 003D: project tracker and box job runner are alive") {
    Write-Host "AUDIT FAIL: Phase 003D marker not found in config."
    exit 1
}

if ($runner -notmatch "Direct printer send: LOCKED") {
    Write-Host "AUDIT FAIL: box job runner printer lock marker not found."
    exit 1
}

if ($runner -notmatch "220 x 220 x 250") {
    Write-Host "AUDIT FAIL: generic build volume validation marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003D files present."

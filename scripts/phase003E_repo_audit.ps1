Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003E REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "tools\cicada_stl_sidecar\cicada_box_job_runner.py",
    "tools\cicada_job_editor\local_box_job_editor.html",
    "scripts\open_box_job_editor.ps1",
    "scripts\new_box_job.ps1",
    "scripts\new_and_run_box_job.ps1",
    "scripts\diagnostics\cicada_box_job_summary.ps1",
    "docs\PHASE_CLUSTER_003E_EDITABLE_BOX_JOB_PIPELINE.md",
    "docs\checklists\PHASE_003E_SMOKE_TEST.md",
    "docs\debug\EDITABLE_BOX_JOB_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003E.md"
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
$editor = Get-Content "tools\cicada_job_editor\local_box_job_editor.html" -Raw

if ($config -notmatch "Phase 003E: editable box job pipeline is alive") {
    Write-Host "AUDIT FAIL: Phase 003E marker not found in config."
    exit 1
}

if ($runner -notmatch "subparsers") {
    Write-Host "AUDIT FAIL: runner subcommand interface not found."
    exit 1
}

if ($runner -notmatch "Direct printer send: LOCKED") {
    Write-Host "AUDIT FAIL: printer lock marker not found in runner."
    exit 1
}

if ($editor -notmatch "CICADA BOX JOB EDITOR") {
    Write-Host "AUDIT FAIL: local editor marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003E files present."

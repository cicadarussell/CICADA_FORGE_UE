Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003F REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "tools\cicada_stl_sidecar\cicada_stl_analyzer.py",
    "scripts\diagnostics\cicada_analyze_latest_stl.ps1",
    "scripts\diagnostics\cicada_generate_latest_stl_report.ps1",
    "scripts\diagnostics\cicada_stl_quality_gate.ps1",
    "scripts\open_latest_stl_report.ps1",
    "scripts\new_run_analyze_box_job.ps1",
    "docs\PHASE_CLUSTER_003F_STL_PREVIEW_AND_QUALITY_GATE.md",
    "docs\checklists\PHASE_003F_SMOKE_TEST.md",
    "docs\debug\STL_PROOF_GATE_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003F.md"
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
$analyzer = Get-Content "tools\cicada_stl_sidecar\cicada_stl_analyzer.py" -Raw

if ($config -notmatch "Phase 003F: STL preview and quality gate are alive") {
    Write-Host "AUDIT FAIL: Phase 003F marker not found in config."
    exit 1
}

if ($analyzer -notmatch "non_manifold_edge_count") {
    Write-Host "AUDIT FAIL: analyzer non-manifold check marker not found."
    exit 1
}

if ($analyzer -notmatch "Direct printer send: LOCKED") {
    Write-Host "AUDIT FAIL: analyzer printer lock marker not found."
    exit 1
}

if ($analyzer -notmatch "make_html_report") {
    Write-Host "AUDIT FAIL: HTML report function marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003F files present."

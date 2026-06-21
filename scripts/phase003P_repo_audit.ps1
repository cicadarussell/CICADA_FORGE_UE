Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003P REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "scripts\cicada_forge.ps1",
    "scripts\headless\cicada_headless_phase003P_full_check.ps1",
    "scripts\diagnostics\cicada_full_project_audit.ps1",
    "tools\cicada_integration\cicada_full_project_audit.py",
    "tools\cicada_cad_sidecar\cicada_cad_sidecar.py",
    "tools\cicada_slicer\cicada_slicer_readiness.py",
    "tools\cicada_slicer\cicada_slicer_dryrun_planner.py",
    "tools\cicada_dashboard\cicada_artifact_dashboard.py",
    "tools\cicada_health\cicada_health_report.py",
    "tools\cicada_launcher\cicada_command_center.py",
    "tools\cicada_ledger\cicada_run_ledger.py",
    "docs\PHASE_CLUSTER_003P_FULL_INTEGRATION_AUDIT_BUGFIX.md",
    "docs\checklists\PHASE_003P_FULL_INTEGRATION_TEST.md",
    "docs\debug\FULL_PROJECT_AUDIT_CONTRACT.md"
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
if ($config -notmatch "Phase 003P") {
    Write-Host "AUDIT FAIL: Phase 003P config marker missing."
    exit 1
}

$bad = Get-ChildItem -Recurse -Path "scripts" -Filter "*.ps1" |
    Where-Object { $_.Name -notmatch "^phase" -and $_.FullName -notmatch "diagnostics\\cicada_full_project_audit" } |
    Select-String -SimpleMatch "-OpenReport:`$OpenReport", "-OpenDashboard:`$OpenDashboard", "-OpenStl:`$OpenStl", "-OpenReport:`$Open", "-OpenDashboard:`$Open" |
    Where-Object { $_.Line -notmatch "PassOpenReport|PassOpenDashboard|PassOpenStl|WithOpenReport|WithOpenDashboard|WithOpenStl" }

if ($bad) {
    Write-Host "AUDIT FAIL: old external switch forwarding remains:"
    $bad | ForEach-Object { Write-Host "$($_.Path):$($_.LineNumber): $($_.Line)" }
    exit 1
}

Write-Host "AUDIT PASS: Phase 003P full integration bugfix files present."
exit 0

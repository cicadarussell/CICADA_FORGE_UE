Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003O1 CLEANUP AUDIT ==="

$required = @(
    ".gitignore",
    "Config\CICADAForgeState.ini",
    "scripts\headless\cicada_headless_phase003O_full_check.ps1",
    "scripts\phase003O1_cleanup_audit.ps1",
    "scripts\cicada_forge.ps1",
    "tools\cicada_ledger\cicada_run_ledger.py",
    "tools\cicada_health\cicada_health_report.py",
    "tools\cicada_launcher\cicada_command_center.py",
    "docs\PHASE_CLUSTER_003O1_CLEANUP_SWITCHFIX_TEST_HARNESS.md",
    "docs\checklists\PHASE_003O1_CLEAN_TEST.md"
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
$fullCheck = Get-Content "scripts\headless\cicada_headless_phase003O_full_check.ps1" -Raw
$gitignore = Get-Content ".gitignore" -Raw

if ($config -notmatch "Phase 003O1|Phase 003P") {
    Write-Host "AUDIT FAIL: cleanup/current config marker missing."
    exit 1
}

if ($fullCheck -notmatch "Invoke-CicadaStep") {
    Write-Host "AUDIT FAIL: safe Invoke-CicadaStep helper missing."
    exit 1
}

if ($fullCheck.Contains('-OpenReport:$OpenReport')) {
    Write-Host "AUDIT FAIL: old external nested switch forwarding remains in 003O full check."
    exit 1
}

if ($gitignore -notmatch "\.cicada_envs/") {
    Write-Host "AUDIT FAIL: .cicada_envs ignore missing."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003O1 cleanup files present."
exit 0

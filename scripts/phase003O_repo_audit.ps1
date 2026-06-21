Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
Write-Host "=== CICADA FORGE PHASE 003O REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "tools\cicada_ledger\cicada_run_ledger.py",
    "scripts\ledger\cicada_ledger_record.ps1",
    "scripts\ledger\cicada_ledger_latest.ps1",
    "scripts\ledger\cicada_release_gate.ps1",
    "scripts\headless\cicada_headless_phase003O_full_check.ps1",
    "scripts\cicada_forge.ps1",
    "docs\PHASE_CLUSTER_003O_RUN_LEDGER_RELEASE_GATE.md",
    "docs\checklists\PHASE_003O_SMOKE_TEST.md",
    "docs\debug\RUN_LEDGER_CONTRACT.md",
    "docs\debug\RELEASE_GATE_CONTRACT.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003O.md"
)

$missing = @()
foreach ($file in $required) {
    if (Test-Path $file) { Write-Host "[OK]      $file" }
    else { Write-Host "[MISSING] $file"; $missing += $file }
}
Write-Host ""
git status --short
Write-Host ""

if ($missing.Count -gt 0) { Write-Host "AUDIT FAIL: missing required files."; exit 1 }

$config = Get-Content "Config\CICADAForgeState.ini" -Raw
$wrapper = Get-Content "scripts\cicada_forge.ps1" -Raw
$ledger = Get-Content "tools\cicada_ledger\cicada_run_ledger.py" -Raw

if ($config -notmatch "Phase 003O: run ledger and release candidate gate are alive") { Write-Host "AUDIT FAIL: 003O config marker missing."; exit 1 }
foreach ($marker in @("ledger-record", "ledger-latest", "release-gate", "phase003O-full-check")) {
    if ($wrapper -notmatch $marker) { Write-Host "AUDIT FAIL: wrapper marker missing: $marker"; exit 1 }
}
foreach ($marker in @("RC_READY", "RC_PARTIAL", "BLOCKED")) {
    if ($ledger -notmatch $marker) { Write-Host "AUDIT FAIL: ledger marker missing: $marker"; exit 1 }
}
Write-Host "AUDIT PASS: Phase 003O files present."

param([switch]$OpenReport)
$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\headless\cicada_headless_phase003N_full_check.ps1" -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\ledger\cicada_ledger_record.ps1" -Phase "003O" -Verdict "PASS_OR_PARTIAL" -Note "Phase 003O full check executed; review health/release reports for exact status." -Source "phase003O-full-check"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\ledger\cicada_release_gate.ps1" -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard:$OpenReport
exit $LASTEXITCODE

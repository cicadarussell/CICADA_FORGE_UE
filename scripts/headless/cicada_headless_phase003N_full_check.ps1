param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\diagnostics\cicada_health_report.ps1" -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\launcher\cicada_generate_command_center.ps1" -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\headless\cicada_headless_phase003M_full_check.ps1" -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\diagnostics\cicada_health_report.ps1" -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard:$OpenReport
exit $LASTEXITCODE

param(
    [switch]$OpenReport,
    [switch]$OpenDashboard
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_doctor.ps1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_validate_examples.ps1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_sample_pack.ps1" -OpenReport:$OpenReport -OpenDashboard:$OpenDashboard
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\diagnostics\cicada_cad_sidecar_quick_check.ps1"
exit $LASTEXITCODE

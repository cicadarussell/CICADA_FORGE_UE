param(
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\env\cicada_env_doctor.ps1" -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\slicer\cicada_slicer_readiness.ps1" -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard:$OpenReport
exit $LASTEXITCODE

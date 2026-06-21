param(
    [switch]$OpenReport,
    [switch]$OpenDashboard
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Args = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cad\cicada_cad_full_check.ps1")
if ($OpenReport) { $Args += "-OpenReport" }
if ($OpenDashboard) { $Args += "-OpenDashboard" }
& powershell @Args
exit $LASTEXITCODE

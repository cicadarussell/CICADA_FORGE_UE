param([switch]$Open)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Args = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "dashboard")
if ($Open) { $Args += "-OpenDashboard" }
& powershell @Args
exit $LASTEXITCODE

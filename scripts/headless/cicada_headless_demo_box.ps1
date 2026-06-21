param(
    [switch]$OpenReport,
    [switch]$OpenStl
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Args = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "demo")
if ($OpenReport) { $Args += "-OpenReport" }
if ($OpenStl) { $Args += "-OpenStl" }
& powershell @Args
exit $LASTEXITCODE

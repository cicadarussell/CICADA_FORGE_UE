param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Args = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cad\cicada_cad_demo.ps1")
if ($OpenReport) { $Args += "-OpenReport" }
& powershell @Args
exit $LASTEXITCODE

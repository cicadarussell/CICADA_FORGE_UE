param([switch]$Open)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Args = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "run-report")
if ($Open) { $Args += "-OpenReport" }
& powershell @Args
exit $LASTEXITCODE

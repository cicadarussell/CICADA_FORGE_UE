param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_env\cicada_cad_engine_launcher.py"

py -3 $Tool --repo $Repo doctor

if ($OpenReport) {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command env-doctor -OpenReport
}

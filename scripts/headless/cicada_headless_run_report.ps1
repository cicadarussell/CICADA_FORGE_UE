param([switch]$Open)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command run-report -OpenReport:$Open

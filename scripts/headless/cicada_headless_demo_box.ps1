param(
    [switch]$OpenReport,
    [switch]$OpenStl
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command demo -OpenReport:$OpenReport -OpenStl:$OpenStl

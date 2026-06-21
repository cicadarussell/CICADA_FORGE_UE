param(
    [switch]$OpenReport,
    [switch]$OpenDashboard
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_full_check.ps1" -OpenReport:$OpenReport -OpenDashboard:$OpenDashboard

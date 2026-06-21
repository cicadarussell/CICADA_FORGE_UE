param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_demo.ps1" -OpenReport:$OpenReport

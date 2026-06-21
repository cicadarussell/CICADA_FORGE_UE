param(
    [string]$Name = "custom_box",
    [double]$Width = 80,
    [double]$Depth = 40,
    [double]$Height = 12,
    [string]$Material = "PLA",
    [double]$LayerHeight = 0.20,
    [int]$Walls = 3,
    [int]$Infill = 15,
    [string]$Supports = "off",
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\new_and_run_box_job.ps1" `
    -Name $Name `
    -Width $Width `
    -Depth $Depth `
    -Height $Height `
    -Material $Material `
    -LayerHeight $LayerHeight `
    -Walls $Walls `
    -Infill $Infill `
    -Supports $Supports

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\diagnostics\cicada_stl_quality_gate.ps1"

if ($OpenReport) {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\diagnostics\cicada_generate_latest_stl_report.ps1" -Open
} else {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\diagnostics\cicada_generate_latest_stl_report.ps1"
}

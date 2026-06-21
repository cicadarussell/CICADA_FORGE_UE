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
    [string]$Note = "Generated from scripts/new_box_job.ps1"
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_stl_sidecar\cicada_box_job_runner.py"

if (-not (Test-Path $Tool)) {
    throw "Missing box job runner: $Tool"
}

py -3 $Tool init --name $Name --width $Width --depth $Depth --height $Height --material $Material --layer-height $LayerHeight --walls $Walls --infill $Infill --supports $Supports --note $Note

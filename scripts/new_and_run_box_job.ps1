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
    [switch]$Open
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_stl_sidecar\cicada_box_job_runner.py"
$JobDir = Join-Path $Repo "Saved\CICADAForge\BoxJobs"
New-Item -ItemType Directory -Path $JobDir -Force | Out-Null

$SafeName = ($Name -replace '[^a-zA-Z0-9_-]', '_').Trim('_')
if ([string]::IsNullOrWhiteSpace($SafeName)) { $SafeName = "custom_box" }

$JobPath = Join-Path $JobDir "$SafeName.json"

py -3 $Tool init --name $Name --width $Width --depth $Depth --height $Height --material $Material --layer-height $LayerHeight --walls $Walls --infill $Infill --supports $Supports --out $JobPath

$args = @($Tool, "run", $JobPath)
if ($Open) { $args += "--open" }

py -3 @args

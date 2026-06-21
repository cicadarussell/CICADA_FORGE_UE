param(
    [string]$Part = "examples\cad_parts\robot_sensor_plate_v02.part.json",
    [ValidateSet("auto", "cadquery", "freecad", "none")]
    [string]$Engine = "auto",
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_env\cicada_cad_engine_launcher.py"
$PartPath = Join-Path $Repo $Part

if (-not (Test-Path $PartPath)) {
    throw "Missing CAD part: $PartPath"
}

$args = @($Tool, "--repo", $Repo, "generate", $PartPath, "--engine", $Engine)
if ($OpenReport) { $args += "--open-report" }

py -3 @args

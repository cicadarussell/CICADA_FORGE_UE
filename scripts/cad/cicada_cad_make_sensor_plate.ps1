param(
    [string]$Name = "robot_sensor_plate",
    [double]$Width = 120,
    [double]$Depth = 70,
    [double]$Height = 6,
    [string]$Material = "PETG",
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Builder = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py"
$Sidecar = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_cad_sidecar.py"
$Out = Join-Path $Repo ("Saved\CICADAForge\CADIntent\" + $Name + ".part.json")

py -3 $Builder sensor-plate --name $Name --width $Width --depth $Depth --height $Height --material $Material --out $Out
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$args = @($Sidecar, "generate", $Out)
if ($OpenReport) { $args += "--open-report" }

py -3 @args

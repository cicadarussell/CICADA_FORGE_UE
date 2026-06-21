param(
    [string]$Name = "robot_mount_plate",
    [double]$Width = 120,
    [double]$Depth = 70,
    [double]$Height = 8,
    [string]$Material = "PETG",
    [double]$RailSpacing = 60,
    [double]$HoleDiameter = 4.2,
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Builder = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py"
$Sidecar = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_cad_sidecar.py"
$Out = Join-Path $Repo ("Saved\CICADAForge\CADIntent\" + $Name + ".part.json")

py -3 $Builder robot-plate --name $Name --width $Width --depth $Depth --height $Height --material $Material --rail-spacing $RailSpacing --hole-diameter $HoleDiameter --out $Out

$args = @($Sidecar, "generate", $Out)
if ($OpenReport) { $args += "--open-report" }

py -3 @args

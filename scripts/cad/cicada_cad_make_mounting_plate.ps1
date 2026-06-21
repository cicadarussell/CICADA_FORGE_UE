param(
    [string]$Name = "mounting_plate",
    [double]$Width = 100,
    [double]$Depth = 40,
    [double]$Height = 6,
    [string]$Material = "PETG",
    [double]$HoleDiameter = 5,
    [double]$Inset = 12,
    [ValidateSet(2, 4)]
    [int]$Holes = 2,
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Builder = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py"
$Sidecar = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_cad_sidecar.py"
$Out = Join-Path $Repo ("Saved\CICADAForge\CADIntent\" + $Name + ".part.json")

py -3 $Builder mounting-plate --name $Name --width $Width --depth $Depth --height $Height --material $Material --hole-diameter $HoleDiameter --inset $Inset --holes $Holes --out $Out

$args = @($Sidecar, "generate", $Out)
if ($OpenReport) { $args += "--open-report" }

py -3 @args

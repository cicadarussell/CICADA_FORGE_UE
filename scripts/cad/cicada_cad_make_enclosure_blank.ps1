param(
    [string]$Name = "electronics_enclosure_blank",
    [double]$Width = 120,
    [double]$Depth = 70,
    [double]$Height = 28,
    [string]$Material = "PETG",
    [double]$HoleDiameter = 3.4,
    [double]$Inset = 12,
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Builder = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py"
$Sidecar = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_cad_sidecar.py"
$Out = Join-Path $Repo ("Saved\CICADAForge\CADIntent\" + $Name + ".part.json")

py -3 $Builder enclosure-blank --name $Name --width $Width --depth $Depth --height $Height --material $Material --hole-diameter $HoleDiameter --inset $Inset --out $Out

$args = @($Sidecar, "generate", $Out)
if ($OpenReport) { $args += "--open-report" }

py -3 @args

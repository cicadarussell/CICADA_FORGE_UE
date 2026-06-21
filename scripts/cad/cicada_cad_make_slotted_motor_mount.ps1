param(
    [string]$Name = "slotted_motor_mount",
    [double]$Width = 100,
    [double]$Depth = 60,
    [double]$Height = 8,
    [string]$Material = "PETG",
    [double]$SlotLength = 28,
    [double]$SlotWidth = 5.2,
    [double]$HoleDiameter = 4.2,
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Builder = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py"
$Sidecar = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_cad_sidecar.py"
$Out = Join-Path $Repo ("Saved\CICADAForge\CADIntent\" + $Name + ".part.json")

py -3 $Builder slotted-motor-mount --name $Name --width $Width --depth $Depth --height $Height --material $Material --slot-length $SlotLength --slot-width $SlotWidth --hole-diameter $HoleDiameter --out $Out
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$args = @($Sidecar, "generate", $Out)
if ($OpenReport) { $args += "--open-report" }

py -3 @args

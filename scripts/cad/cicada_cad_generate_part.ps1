param(
    [string]$Part = "examples\cad_parts\mounting_plate_2holes.part.json",
    [ValidateSet("auto", "cadquery", "freecad", "none")]
    [string]$Engine = "auto",
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_cad_sidecar.py"
$PartPath = Join-Path $Repo $Part

if (-not (Test-Path $Tool)) {
    throw "Missing CAD sidecar: $Tool"
}

if (-not (Test-Path $PartPath)) {
    throw "Missing CAD part file: $PartPath"
}

$args = @($Tool, "generate", $PartPath, "--engine", $Engine)

if ($OpenReport) {
    $args += "--open-report"
}

py -3 @args

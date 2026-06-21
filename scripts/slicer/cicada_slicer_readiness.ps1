param(
    [switch]$OpenReport,
    [switch]$ProbeVersions
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_slicer\cicada_slicer_readiness.py"

$args = @($Tool)
if ($OpenReport) { $args += "--open-report" }
if ($ProbeVersions) { $args += "--probe-versions" }

py -3 @args

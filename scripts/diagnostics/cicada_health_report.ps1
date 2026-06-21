param(
    [switch]$OpenReport,
    [switch]$Strict
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_health\cicada_health_report.py"

$args = @($Tool, "--repo", $Repo)
if ($OpenReport) { $args += "--open-report" }
if ($Strict) { $args += "--strict" }

py -3 @args

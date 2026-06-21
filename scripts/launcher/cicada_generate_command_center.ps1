param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_launcher\cicada_command_center.py"

$args = @($Tool, "--repo", $Repo)
if ($OpenReport) { $args += "--open-report" }

py -3 @args

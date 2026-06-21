param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_env\cicada_environment_manager.py"

$args = @($Tool, "doctor")
if ($OpenReport) { $args += "--open-report" }

py -3 @args

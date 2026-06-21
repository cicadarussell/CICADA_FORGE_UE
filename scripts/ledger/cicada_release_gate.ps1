param([switch]$OpenReport, [switch]$Strict)
$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_ledger\cicada_run_ledger.py"
$args = @($Tool, "--repo", $Repo, "release-gate")
if ($OpenReport) { $args += "--open-report" }
if ($Strict) { $args += "--strict" }
py -3 @args

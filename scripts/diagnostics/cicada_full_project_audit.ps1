param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Args = @("-3", "$Repo\tools\cicada_integration\cicada_full_project_audit.py", "--repo", $Repo)
if ($OpenReport) { $Args += "--open-report" }
& py @Args
exit $LASTEXITCODE

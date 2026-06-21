param(
    [switch]$OpenReport,
    [switch]$OpenDashboard
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

function Invoke-Step {
    param([string]$ScriptPath, [switch]$WithOpenReport, [switch]$WithOpenDashboard)
    $Args = @("-ExecutionPolicy", "Bypass", "-File", $ScriptPath)
    if ($WithOpenReport) { $Args += "-OpenReport" }
    if ($WithOpenDashboard) { $Args += "-OpenDashboard" }
    & powershell @Args
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

& powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_doctor.ps1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_validate_examples.ps1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Invoke-Step -ScriptPath "$Repo\scripts\cad\cicada_cad_sample_pack.ps1" -WithOpenReport:$OpenReport -WithOpenDashboard:$OpenDashboard

& powershell -ExecutionPolicy Bypass -File "$Repo\scripts\diagnostics\cicada_cad_sidecar_quick_check.ps1"
exit $LASTEXITCODE

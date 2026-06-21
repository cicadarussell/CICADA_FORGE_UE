param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

& powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_doctor.ps1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_validate_examples.ps1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$Args = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cad\cicada_cad_generate_part.ps1", "-Part", "examples\cad_parts\mounting_plate_2holes.part.json")
if ($OpenReport) { $Args += "-OpenReport" }
& powershell @Args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$DashArgs = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "dashboard")
if ($OpenReport) { $DashArgs += "-OpenDashboard" }
& powershell @DashArgs
exit $LASTEXITCODE

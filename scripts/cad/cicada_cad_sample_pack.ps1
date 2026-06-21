param(
    [switch]$OpenReport,
    [switch]$OpenDashboard
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

function Invoke-Cad {
    param([string]$ScriptPath, [string[]]$ExtraArgs = @(), [switch]$WithOpenReport)
    $Args = @("-ExecutionPolicy", "Bypass", "-File", $ScriptPath)
    $Args += $ExtraArgs
    if ($WithOpenReport) { $Args += "-OpenReport" }
    & powershell @Args
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Invoke-Cad -ScriptPath "$Repo\scripts\cad\cicada_cad_make_mounting_plate.ps1" -ExtraArgs @("-Name", "sample_mounting_plate", "-Width", "100", "-Depth", "40", "-Height", "6", "-Material", "PETG", "-HoleDiameter", "5", "-Inset", "12", "-Holes", "2") -WithOpenReport:$OpenReport
Invoke-Cad -ScriptPath "$Repo\scripts\cad\cicada_cad_make_robot_plate.ps1" -ExtraArgs @("-Name", "sample_robot_plate", "-Width", "120", "-Depth", "70", "-Height", "8", "-Material", "PETG", "-RailSpacing", "60", "-HoleDiameter", "4.2") -WithOpenReport:$OpenReport
Invoke-Cad -ScriptPath "$Repo\scripts\cad\cicada_cad_make_sensor_plate.ps1" -ExtraArgs @("-Name", "sample_sensor_plate", "-Width", "120", "-Depth", "70", "-Height", "6", "-Material", "PETG") -WithOpenReport:$OpenReport
Invoke-Cad -ScriptPath "$Repo\scripts\cad\cicada_cad_make_slotted_motor_mount.ps1" -ExtraArgs @("-Name", "sample_slotted_motor_mount", "-Width", "100", "-Depth", "60", "-Height", "8", "-Material", "PETG") -WithOpenReport:$OpenReport

$DashArgs = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "dashboard")
if ($OpenDashboard) { $DashArgs += "-OpenDashboard" }
& powershell @DashArgs
exit $LASTEXITCODE

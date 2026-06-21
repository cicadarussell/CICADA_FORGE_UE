param(
    [switch]$OpenReport,
    [switch]$OpenDashboard
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_make_mounting_plate.ps1" -Name "sample_mounting_plate" -Width 100 -Depth 40 -Height 6 -Material PETG -HoleDiameter 5 -Inset 12 -Holes 2 -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_make_robot_plate.ps1" -Name "sample_robot_plate" -Width 120 -Depth 70 -Height 8 -Material PETG -RailSpacing 60 -HoleDiameter 4.2 -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_make_sensor_plate.ps1" -Name "sample_sensor_plate" -Width 120 -Depth 70 -Height 6 -Material PETG -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_make_slotted_motor_mount.ps1" -Name "sample_slotted_motor_mount" -Width 100 -Depth 60 -Height 8 -Material PETG -OpenReport:$OpenReport
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard:$OpenDashboard

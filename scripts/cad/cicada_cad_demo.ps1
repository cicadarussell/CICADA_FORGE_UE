param(
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_doctor.ps1"
powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_validate_examples.ps1"
powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_generate_part.ps1" -Part "examples\cad_parts\mounting_plate_2holes.part.json" -OpenReport:$OpenReport
powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard:$OpenReport

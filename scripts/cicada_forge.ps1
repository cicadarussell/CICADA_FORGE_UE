param(
    [ValidateSet("doctor", "inventory", "demo", "custom-box", "analyze", "manifest-check", "dashboard", "run-report", "full-check", "open-editor", "cad-doctor", "cad-demo", "cad-validate", "cad-generate")]
    [string]$Command = "full-check",

    [string]$Name = "custom_box",
    [double]$Width = 80,
    [double]$Depth = 40,
    [double]$Height = 12,
    [string]$Material = "PLA",
    [double]$LayerHeight = 0.20,
    [int]$Walls = 3,
    [int]$Infill = 15,
    [string]$Supports = "off",

    [string]$Part = "examples\cad_parts\mounting_plate_2holes.part.json",
    [ValidateSet("auto", "cadquery", "freecad", "none")]
    [string]$Engine = "auto",

    [switch]$OpenReport,
    [switch]$OpenStl,
    [switch]$OpenDashboard
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_headless\cicada_forge_headless.py"
$Editor = Join-Path $Repo "tools\cicada_job_editor\local_box_job_editor.html"

if ($Command -eq "open-editor") {
    if (-not (Test-Path $Editor)) { throw "Missing job editor: $Editor" }
    Start-Process $Editor
    exit 0
}

if ($Command -eq "cad-doctor") {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_doctor.ps1"
    exit $LASTEXITCODE
}

if ($Command -eq "cad-validate") {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_validate_examples.ps1"
    exit $LASTEXITCODE
}

if ($Command -eq "cad-demo") {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_demo.ps1" -OpenReport:$OpenReport
    exit $LASTEXITCODE
}

if ($Command -eq "cad-generate") {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_generate_part.ps1" -Part $Part -Engine $Engine -OpenReport:$OpenReport
    exit $LASTEXITCODE
}

if (-not (Test-Path $Tool)) {
    throw "Missing headless control tower: $Tool"
}

$args = @($Tool, $Command)

if ($Command -eq "custom-box") {
    $args += @(
        "--name", $Name,
        "--width", $Width,
        "--depth", $Depth,
        "--height", $Height,
        "--material", $Material,
        "--layer-height", $LayerHeight,
        "--walls", $Walls,
        "--infill", $Infill,
        "--supports", $Supports
    )
}

if ($Command -eq "dashboard" -and $OpenDashboard) { $args += "--open" }
if ($OpenReport) { $args += "--open-report" }
if ($OpenStl) { $args += "--open-stl" }

py -3 @args

param(
    [ValidateSet("doctor", "inventory", "demo", "custom-box", "analyze", "manifest-check", "dashboard", "run-report", "full-check", "open-editor", "cad-doctor", "cad-demo", "cad-validate", "cad-generate", "cad-full-check", "cad-sample-pack", "cad-build-mounting-plate", "cad-build-robot-plate", "cad-build-enclosure", "cad-build-sensor-plate", "cad-build-motor-mount", "cad-compare", "cadquery-check", "cadquery-install-user", "env-doctor", "env-plan", "env-create-cadquery", "env-install-cadquery", "slicer-readiness", "env-slicer-full-check", "cad-engine-doctor", "cad-generate-engine", "slicer-dryrun-plan", "phase003M-full-check", "health-report", "command-center", "control-room", "phase003N-full-check", "ledger-record", "ledger-latest", "release-gate", "phase003O-full-check", "full-project-audit", "phase003P-full-check")]
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
    [string]$PartA = "examples\cad_parts\mounting_plate_2holes.part.json",
    [string]$PartB = "examples\cad_parts\robot_sensor_plate_v02.part.json",
    [ValidateSet("auto", "cadquery", "freecad", "none")]
    [string]$Engine = "auto",

    [double]$HoleDiameter = 5.0,
    [double]$Inset = 12.0,
    [int]$Holes = 2,
    [double]$RailSpacing = 60.0,
    [double]$SlotLength = 28.0,
    [double]$SlotWidth = 5.2,

    [switch]$OpenReport,
    [switch]$OpenStl,
    [switch]$OpenDashboard,
    [switch]$Install
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_headless\cicada_forge_headless.py"
$Editor = Join-Path $Repo "tools\cicada_job_editor\local_box_job_editor.html"

function Invoke-CicadaPowerShellScript {
    param(
        [Parameter(Mandatory=$true)][string]$ScriptPath,
        [string[]]$Arguments = @(),
        [switch]$PassOpenReport,
        [switch]$PassOpenDashboard
    )

    if (-not (Test-Path $ScriptPath)) {
        throw "Missing script: $ScriptPath"
    }

    $CallArgs = @("-ExecutionPolicy", "Bypass", "-File", $ScriptPath)
    $CallArgs += $Arguments

    if ($PassOpenReport) { $CallArgs += "-OpenReport" }
    if ($PassOpenDashboard) { $CallArgs += "-OpenDashboard" }

    & powershell @CallArgs
    exit $LASTEXITCODE
}

if ($Command -eq "open-editor") {
    if (-not (Test-Path $Editor)) { throw "Missing job editor: $Editor" }
    Start-Process $Editor
    exit 0
}

if ($Command -eq "cad-doctor") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_doctor.ps1"
}

if ($Command -eq "cad-validate") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_validate_examples.ps1"
}

if ($Command -eq "cad-demo") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_demo.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-generate") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_generate_part.ps1" -Arguments @("-Part", $Part, "-Engine", $Engine) -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-full-check") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_full_check.ps1" -PassOpenReport:$OpenReport -PassOpenDashboard:$OpenDashboard
}

if ($Command -eq "cad-sample-pack") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_sample_pack.ps1" -PassOpenReport:$OpenReport -PassOpenDashboard:$OpenDashboard
}

if ($Command -eq "cad-build-mounting-plate") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_make_mounting_plate.ps1" -Arguments @("-Name", $Name, "-Width", "$Width", "-Depth", "$Depth", "-Height", "$Height", "-Material", $Material, "-HoleDiameter", "$HoleDiameter", "-Inset", "$Inset", "-Holes", "$Holes") -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-build-robot-plate") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_make_robot_plate.ps1" -Arguments @("-Name", $Name, "-Width", "$Width", "-Depth", "$Depth", "-Height", "$Height", "-Material", $Material, "-HoleDiameter", "$HoleDiameter", "-RailSpacing", "$RailSpacing") -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-build-enclosure") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_make_enclosure_blank.ps1" -Arguments @("-Name", $Name, "-Width", "$Width", "-Depth", "$Depth", "-Height", "$Height", "-Material", $Material, "-HoleDiameter", "$HoleDiameter", "-Inset", "$Inset") -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-build-sensor-plate") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_make_sensor_plate.ps1" -Arguments @("-Name", $Name, "-Width", "$Width", "-Depth", "$Depth", "-Height", "$Height", "-Material", $Material) -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-build-motor-mount") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_make_slotted_motor_mount.ps1" -Arguments @("-Name", $Name, "-Width", "$Width", "-Depth", "$Depth", "-Height", "$Height", "-Material", $Material, "-SlotLength", "$SlotLength", "-SlotWidth", "$SlotWidth", "-HoleDiameter", "$HoleDiameter") -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-compare") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_compare_parts.ps1" -Arguments @("-PartA", $PartA, "-PartB", $PartB)
}


if ($Command -eq "env-doctor") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\env\cicada_env_doctor.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "env-plan") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\env\cicada_env_plan.ps1"
}

if ($Command -eq "env-create-cadquery") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\env\cicada_env_create_cadquery_venv.ps1"
}

if ($Command -eq "env-install-cadquery") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\env\cicada_env_install_cadquery.ps1"
}

if ($Command -eq "slicer-readiness") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\slicer\cicada_slicer_readiness.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "env-slicer-full-check") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\headless\cicada_headless_env_slicer_full_check.ps1" -PassOpenReport:$OpenReport
}




if ($Command -eq "ledger-record") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\ledger\cicada_ledger_record.ps1" -Arguments @("-Phase", "003O", "-Verdict", "RECORDED", "-Note", "Manual ledger record from cicada_forge wrapper.", "-Source", "wrapper")
}

if ($Command -eq "ledger-latest") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\ledger\cicada_ledger_latest.ps1"
}

if ($Command -eq "release-gate") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\ledger\cicada_release_gate.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "phase003O-full-check", "full-project-audit", "phase003P-full-check") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\headless\cicada_headless_phase003O_full_check.ps1" -PassOpenReport:$OpenReport
}


if ($Command -eq "full-project-audit") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\diagnostics\cicada_full_project_audit.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "phase003P-full-check") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\headless\cicada_headless_phase003P_full_check.ps1" -PassOpenReport:$OpenReport -PassOpenDashboard:$OpenDashboard
}

if ($Command -eq "health-report") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\diagnostics\cicada_health_report.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "command-center") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\launcher\cicada_generate_command_center.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "control-room") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cicada_control_room.ps1"
}

if ($Command -eq "phase003N-full-check") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\headless\cicada_headless_phase003N_full_check.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-engine-doctor") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\env\cicada_cad_engine_launcher_doctor.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "cad-generate-engine") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cad_generate_part_engine.ps1" -Arguments @("-Part", $Part, "-Engine", $Engine) -PassOpenReport:$OpenReport
}

if ($Command -eq "slicer-dryrun-plan") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\slicer\cicada_slicer_dryrun_plan.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "phase003M-full-check") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\headless\cicada_headless_phase003M_full_check.ps1" -PassOpenReport:$OpenReport
}

if ($Command -eq "cadquery-check") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cadquery_setup_helper.ps1"
}

if ($Command -eq "cadquery-install-user") {
    Invoke-CicadaPowerShellScript -ScriptPath "$Repo\scripts\cad\cicada_cadquery_setup_helper.ps1" -Arguments @("-InstallUser")
}

if (-not (Test-Path $Tool)) {
    throw "Missing headless control tower: $Tool"
}

$args = @($Tool, $Command)

if ($Command -eq "custom-box") {
    $args += @("--name", $Name, "--width", $Width, "--depth", $Depth, "--height", $Height, "--material", $Material, "--layer-height", $LayerHeight, "--walls", $Walls, "--infill", $Infill, "--supports", $Supports)
}

if ($Command -eq "dashboard" -and $OpenDashboard) { $args += "--open" }
if ($OpenReport) { $args += "--open-report" }
if ($OpenStl) { $args += "--open-stl" }

py -3 @args

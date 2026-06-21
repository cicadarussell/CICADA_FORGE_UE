Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 003J REPO AUDIT ==="

$required = @(
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeProjectState.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "tools\cicada_cad_sidecar\cicada_cad_sidecar.py",
    "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py",
    "scripts\cicada_forge.ps1",
    "scripts\cad\cicada_cad_make_mounting_plate.ps1",
    "scripts\cad\cicada_cad_make_robot_plate.ps1",
    "scripts\cad\cicada_cad_make_enclosure_blank.ps1",
    "scripts\cad\cicada_cad_full_check.ps1",
    "scripts\cad\cicada_cadquery_setup_helper.ps1",
    "scripts\headless\cicada_headless_cad_full_check.ps1",
    "docs\PHASE_CLUSTER_003J_CAD_BUILDER_AND_SWITCH_FIX.md",
    "docs\checklists\PHASE_003J_SMOKE_TEST.md",
    "docs\debug\POWERSHELL_SWITCH_FORWARDING_FIX.md",
    "docs\debug\CAD_BUILDER_CONTRACT.md",
    "docs\cad\CADQUERY_SETUP_NOTES.md",
    "docs\roadmap\CICADA_FORGE_TRACKER_003J.md"
)

$missing = @()

foreach ($file in $required) {
    if (Test-Path $file) {
        Write-Host "[OK]      $file"
    } else {
        Write-Host "[MISSING] $file"
        $missing += $file
    }
}

Write-Host ""
git status --short
Write-Host ""

if ($missing.Count -gt 0) {
    Write-Host "AUDIT FAIL: missing required files."
    exit 1
}

$config = Get-Content "Config\CICADAForgeState.ini" -Raw
$wrapper = Get-Content "scripts\cicada_forge.ps1" -Raw
$sidecar = Get-Content "tools\cicada_cad_sidecar\cicada_cad_sidecar.py" -Raw
$builder = Get-Content "tools\cicada_cad_sidecar\cicada_mechanical_part_builder.py" -Raw

if ($config -notmatch "Phase 003J: CAD builder and PowerShell switch fix are alive") {
    Write-Host "AUDIT FAIL: Phase 003J marker not found in config."
    exit 1
}

if ($wrapper -notmatch "Invoke-CicadaPowerShellScript") {
    Write-Host "AUDIT FAIL: robust PowerShell invocation helper not found."
    exit 1
}

if ($wrapper -notmatch 'cad-full-check') {
    Write-Host "AUDIT FAIL: cad-full-check command not found."
    exit 1
}

if ($sidecar -notmatch "No fake STEP") {
    Write-Host "AUDIT FAIL: literal No fake STEP marker not found."
    exit 1
}

if ($sidecar -notmatch 'preferred == "none"') {
    Write-Host "AUDIT FAIL: explicit engine=none handling not found."
    exit 1
}

if ($builder -notmatch "robot-plate") {
    Write-Host "AUDIT FAIL: robot-plate builder marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 003J files present."

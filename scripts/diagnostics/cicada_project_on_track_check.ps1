$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PROJECT ON-TRACK CHECK ==="
Write-Host ""

$checks = [ordered]@{
    "UE project file" = "CICADA_FORGE_UE.uproject"
    "Plugin descriptor" = "Plugins\CICADAForge\CICADAForge.uplugin"
    "Editor module C++" = "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp"
    "State config" = "Config\CICADAForgeState.ini"
    "Box job runner" = "tools\cicada_stl_sidecar\cicada_box_job_runner.py"
    "STL analyzer" = "tools\cicada_stl_sidecar\cicada_stl_analyzer.py"
    "Headless control tower" = "tools\cicada_headless\cicada_forge_headless.py"
    "Local box job editor" = "tools\cicada_job_editor\local_box_job_editor.html"
    "Box job examples" = "examples\box_jobs"
    "STL validation script" = "scripts\diagnostics\cicada_validate_latest_stl.ps1"
    "STL quality gate" = "scripts\diagnostics\cicada_stl_quality_gate.ps1"
    "Printer safety contract" = "docs\debug\PRINT_HANDOFF_CONTRACT.md"
    "Headless contract" = "docs\debug\HEADLESS_CONTROL_TOWER_CONTRACT.md"
}

$Failed = $false

foreach ($name in $checks.Keys) {
    $path = Join-Path $Repo $checks[$name]
    if (Test-Path $path) {
        Write-Host "[OK]      $name"
    } else {
        Write-Host "[MISSING] $name -> $path"
        $Failed = $true
    }
}

Write-Host ""
Write-Host "Safety boundaries:"
Write-Host "  STL export: allowed"
Write-Host "  STL quality reports: allowed"
Write-Host "  Headless full-check: allowed"
Write-Host "  Manual slicer handoff: allowed"
Write-Host "  Direct printer send: locked"
Write-Host "  Serial/G-code streaming: locked"
Write-Host "  CAD/STEP sidecar: not built yet"

if ($Failed) {
    exit 1
}

Write-Host ""
Write-Host "ON TRACK: no-Unreal diagnostic path exists; direct printer bridge remains locked."

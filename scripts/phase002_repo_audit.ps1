Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002A REPO AUDIT ==="

$required = @(
    "Plugins\CICADAForge\CICADAForge.uplugin",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\CICADAForgeEditor.Build.cs",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Public\CICADAForgeEditorModule.h",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "docs\checklists\PHASE_002A_SMOKE_TEST.md",
    "docs\PHASE_CLUSTER_002A_FORGE_UI_SHELL.md",
    "docs\ui\FORGE_UI_SHELL_SPEC.md"
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

Write-Host "AUDIT PASS: Phase 002A files present."

Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 001 REPO AUDIT ==="

$required = @(
    "CICADA_FORGE_UE.uproject",
    "Config\DefaultGame.ini",
    "Config\DefaultEngine.ini",
    "Plugins\CICADAForge\CICADAForge.uplugin",
    "Plugins\CICADAForge\Source\CICADAForge\CICADAForge.Build.cs",
    "Plugins\CICADAForge\Source\CICADAForge\Public\CICADAForgeModule.h",
    "Plugins\CICADAForge\Source\CICADAForge\Private\CICADAForgeModule.cpp",
    "docs\checklists\PHASE_001_SMOKE_TEST.md",
    "docs\evidence\EVIDENCE_LOG.md"
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

Write-Host "AUDIT PASS: Phase 001A files present."

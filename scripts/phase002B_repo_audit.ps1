Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002B REPO AUDIT ==="

$required = @(
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "docs\PHASE_CLUSTER_002B_STRUCTURED_FORGE_COCKPIT.md",
    "docs\checklists\PHASE_002B_SMOKE_TEST.md",
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

$cpp = Get-Content "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp" -Raw

if ($cpp -notmatch "Phase 002B: structured cockpit shell is alive") {
    Write-Host "AUDIT FAIL: Phase 002B marker not found in editor module."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002B files present."

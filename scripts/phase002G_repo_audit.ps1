Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE PHASE 002G REPO AUDIT ==="

$required = @(
    "Config\DefaultGame.ini",
    "Config\CICADAForgeState.ini",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp",
    "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeStatusModel.cpp",
    "docs\PHASE_CLUSTER_002G_LAST_ACTION_STATUS_CARD.md",
    "docs\checklists\PHASE_002G_SMOKE_TEST.md"
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

$game = Get-Content "Config\DefaultGame.ini" -Raw
$config = Get-Content "Config\CICADAForgeState.ini" -Raw
$module = Get-Content "Plugins\CICADAForge\Source\CICADAForgeEditor\Private\CICADAForgeEditorModule.cpp" -Raw

if ($game -notmatch "ProjectID=\(A=") {
    Write-Host "AUDIT FAIL: ProjectID is not in struct-style format."
    exit 1
}

if ($config -notmatch "Phase 002G: last action status card mirrors button clicks") {
    Write-Host "AUDIT FAIL: Phase 002G marker not found in config."
    exit 1
}

if ($module -notmatch "Last Action") {
    Write-Host "AUDIT FAIL: Last Action UI marker not found."
    exit 1
}

if ($module -notmatch "Result: safe stub logged only") {
    Write-Host "AUDIT FAIL: Last Action result marker not found."
    exit 1
}

Write-Host "AUDIT PASS: Phase 002G files present."

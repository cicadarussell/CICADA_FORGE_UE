Write-Host "=== CICADA SLICER DISCOVERY ==="
Write-Host "This only searches common install paths. It does not launch or send print jobs."
Write-Host ""

$patterns = @(
    "$env:ProgramFiles\Prusa3D\PrusaSlicer\prusa-slicer.exe",
    "$env:ProgramFiles\PrusaSlicer\prusa-slicer.exe",
    "$env:ProgramFiles\UltiMaker Cura*\UltiMaker-Cura.exe",
    "$env:ProgramFiles\Ultimaker Cura*\Cura.exe",
    "$env:ProgramFiles\Bambu Studio\bambu-studio.exe",
    "$env:ProgramFiles\OrcaSlicer\orca-slicer.exe",
    "$env:LOCALAPPDATA\Programs\OrcaSlicer\orca-slicer.exe"
)

$found = @()

foreach ($pattern in $patterns) {
    Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        $found += $_.FullName
    }
}

if ($found.Count -eq 0) {
    Write-Host "No common slicer EXE found. Windows may still open STL through file association."
} else {
    Write-Host "Possible slicers found:"
    $found | Sort-Object -Unique | ForEach-Object { Write-Host "  $_" }
}

Write-Host ""
Write-Host "Direct printer send remains LOCKED."

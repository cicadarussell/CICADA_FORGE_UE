$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$StlDir = Join-Path $Repo "Saved\CICADAForge\STL"

if (-not (Test-Path $StlDir)) {
    throw "No STL directory found: $StlDir"
}

$Stl = Get-ChildItem $StlDir -Filter "*.stl" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Stl) {
    throw "No STL file found in $StlDir"
}

Write-Host "Opening latest STL with Windows default app:"
Write-Host $Stl.FullName
Start-Process $Stl.FullName

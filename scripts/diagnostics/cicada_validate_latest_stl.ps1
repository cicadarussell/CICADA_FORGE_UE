$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$StlDir = Join-Path $Repo "Saved\CICADAForge\STL"

Write-Host "=== CICADA LATEST STL VALIDATION ==="
Write-Host "STL dir: $StlDir"
Write-Host ""

if (-not (Test-Path $StlDir)) {
    Write-Host "No STL directory found yet."
    exit 1
}

$Stl = Get-ChildItem $StlDir -Filter "*.stl" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Stl) {
    Write-Host "No STL files found."
    exit 1
}

$Text = Get-Content $Stl.FullName -Raw
$FacetCount = ([regex]::Matches($Text, "facet normal")).Count
$VertexCount = ([regex]::Matches($Text, "vertex ")).Count

Write-Host "Latest STL: $($Stl.FullName)"
Write-Host "Size bytes: $($Stl.Length)"
Write-Host "Facets: $FacetCount"
Write-Host "Vertices: $VertexCount"

if ($Text -notmatch "^solid") {
    Write-Host "FAIL: STL does not start with solid."
    exit 1
}

if ($FacetCount -ne 12) {
    Write-Host "WARN: expected 12 facets for simple box, found $FacetCount."
} else {
    Write-Host "PASS: simple box STL has expected 12 facets."
}

if ($Text -notmatch "endsolid") {
    Write-Host "FAIL: STL missing endsolid."
    exit 1
}

Write-Host "PASS: STL text structure looks valid enough for V0."

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$ReportDir = Join-Path $Repo "Saved\CICADAForge\Reports"

if (-not (Test-Path $ReportDir)) {
    throw "No reports folder found: $ReportDir"
}

$Report = Get-ChildItem $ReportDir -Filter "*.html" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Report) {
    throw "No HTML STL report found in $ReportDir"
}

Write-Host "Opening latest STL report:"
Write-Host $Report.FullName
Start-Process $Report.FullName

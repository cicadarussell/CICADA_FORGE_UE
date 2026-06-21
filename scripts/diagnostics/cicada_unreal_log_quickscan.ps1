$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$LogDir = Join-Path $Repo "Saved\Logs"

Write-Host "=== CICADA UNREAL LOG QUICKSCAN ==="
Write-Host "Repo: $Repo"
Write-Host "LogDir: $LogDir"
Write-Host ""

if (-not (Test-Path $LogDir)) {
    Write-Host "No Saved\Logs folder found yet."
    exit 1
}

$Log = Get-ChildItem $LogDir -Filter "*.log" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Log) {
    Write-Host "No .log files found."
    exit 1
}

Write-Host "Scanning latest log:"
Write-Host $Log.FullName
Write-Host ""

$Text = Get-Content $Log.FullName -Raw

$patterns = [ordered]@{
    "BuildSucceeded" = "Rebuild All: 1 succeeded|Result: Succeeded"
    "BuildFailed" = "Rebuild All: 0 succeeded|Result: Failed|UnrealBuildTool failed|Module could not be loaded"
    "CICADAForgeLines" = "CICADA Forge"
    "Errors" = " error |error C|fatal error|LNK[0-9]+"
    "Warnings" = "Warning:| warning "
    "KnownNoise" = "aqProf|VtuneApi|WinPix|RenderDoc|XGE|DerivedDataCache|Zen|EOSSDK|Slate.*Roboto|Failed to SetupSDK|Audio Buffer Underrun|SourceControl: Revision control is disabled"
    "MachineRisk" = "GCode|CNC|printer|machine bridge|serial|COM[0-9]|M104|G1 "
    "ReceiptDryRun" = "receipt dry-run|Saved/CICADAForge/Receipts|CICADAForgeReceipt"
}

foreach ($name in $patterns.Keys) {
    $matches = [regex]::Matches($Text, $patterns[$name], "IgnoreCase")
    Write-Host ("{0,-18}: {1}" -f $name, $matches.Count)
}

Write-Host ""
Write-Host "Recent CICADA lines:"
$Text -split "`n" |
    Where-Object { $_ -match "CICADA Forge" } |
    Select-Object -Last 20 |
    ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "Quick verdict:"
if ($Text -match "Rebuild All: 1 succeeded|Result: Succeeded") {
    Write-Host "PASS SIGNAL: build success marker found."
} else {
    Write-Host "NO PASS SIGNAL: build success marker not found in latest log."
}

if ($Text -match "fatal error|UnrealBuildTool failed|Result: Failed|Module could not be loaded") {
    Write-Host "FAIL SIGNAL: real build failure marker found."
} else {
    Write-Host "NO OBVIOUS BUILD FAILURE MARKER."
}

if ($Text -match "GCode|CNC|M104|G1 ") {
    Write-Host "CHECK: possible machine/CNC/G-code text found. Review manually."
} else {
    Write-Host "SAFE: no obvious machine/G-code command markers found."
}

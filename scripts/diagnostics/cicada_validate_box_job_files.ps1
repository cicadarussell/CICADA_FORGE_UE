$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Jobs = Join-Path $Repo "examples\box_jobs"

Write-Host "=== CICADA BOX JOB FILE VALIDATION ==="
Write-Host "Jobs: $Jobs"
Write-Host ""

if (-not (Test-Path $Jobs)) {
    throw "Missing jobs folder: $Jobs"
}

$Failed = $false

Get-ChildItem $Jobs -Filter "*.json" | Sort-Object Name | ForEach-Object {
    try {
        $Data = Get-Content $_.FullName -Raw | ConvertFrom-Json
        $Box = $Data.box_mm
        $W = [double]$Box.width
        $D = [double]$Box.depth
        $H = [double]$Box.height

        $Fits = ($W -gt 0 -and $D -gt 0 -and $H -gt 0 -and $W -le 220 -and $D -le 220 -and $H -le 250)

        if ($Fits) {
            Write-Host "[PASS] $($_.Name)  ${W}x${D}x${H} mm"
        } else {
            Write-Host "[FAIL] $($_.Name)  ${W}x${D}x${H} mm"
            $Failed = $true
        }
    } catch {
        Write-Host "[FAIL] $($_.Name)  $($_.Exception.Message)"
        $Failed = $true
    }
}

if ($Failed) {
    exit 1
}

Write-Host ""
Write-Host "All box jobs valid for generic 220 x 220 x 250 mm build volume."

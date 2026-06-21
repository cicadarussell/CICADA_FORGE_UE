$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$ReportDir = Join-Path $Repo "Saved\CICADAForge\CADReports"

Write-Host "=== CICADA CAD SIDECAR QUICK CHECK ==="

powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_doctor.ps1"
powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cad\cicada_cad_validate_examples.ps1"

if (Test-Path $ReportDir) {
    $Latest = Get-ChildItem $ReportDir -Filter "*.cad_report.json" |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($Latest) {
        $Json = Get-Content $Latest.FullName -Raw | ConvertFrom-Json
        Write-Host "Latest CAD report: $($Latest.FullName)"
        Write-Host "Validation pass: $($Json.validation_pass)"
        Write-Host "Exact STEP exported: $($Json.exact_step_exported)"
        Write-Host "Machine bridge: $($Json.machine_bridge)"
        Write-Host "Direct printer send: $($Json.direct_printer_send)"
    } else {
        Write-Host "No CAD report yet. Run scripts\cad\cicada_cad_demo.ps1."
    }
} else {
    Write-Host "No CADReports folder yet. Run scripts\cad\cicada_cad_demo.ps1."
}

Write-Host "CAD sidecar quick check complete."

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

function Run-Cicada {
    param([string]$CommandLine)
    Write-Host ""
    Write-Host "RUNNING:"
    Write-Host $CommandLine
    Write-Host ""
    Invoke-Expression $CommandLine
    Write-Host ""
    Read-Host "Press Enter to return to CICADA Control Room"
}

while ($true) {
    Clear-Host
    Write-Host "=== CICADA FORGE CONTROL ROOM ==="
    Write-Host "1. Phase 003N full check"
    Write-Host "2. Passive health report"
    Write-Host "3. Open dashboard"
    Write-Host "4. Open command center"
    Write-Host "5. CAD full check"
    Write-Host "6. Build sensor plate"
    Write-Host "7. Build slotted motor mount"
    Write-Host "8. Environment doctor"
    Write-Host "9. Slicer dry-run plan"
    Write-Host "0. Exit"
    Write-Host ""
    $choice = Read-Host "Choose"

    switch ($choice) {
        "1" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command phase003N-full-check -OpenReport" }
        "2" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command health-report -OpenReport" }
        "3" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command dashboard -OpenDashboard" }
        "4" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command command-center -OpenReport" }
        "5" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command cad-full-check -OpenReport -OpenDashboard" }
        "6" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command cad-build-sensor-plate -Name robot_sensor_plate -OpenReport" }
        "7" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command cad-build-motor-mount -Name slotted_motor_mount -OpenReport" }
        "8" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command env-doctor -OpenReport" }
        "9" { Run-Cicada "powershell -ExecutionPolicy Bypass -File `"$Repo\scripts\cicada_forge.ps1`" -Command slicer-dryrun-plan -OpenReport" }
        "0" { exit 0 }
        default { Start-Sleep -Milliseconds 500 }
    }
}

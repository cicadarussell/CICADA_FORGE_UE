$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Editor = Join-Path $Repo "tools\cicada_job_editor\local_box_job_editor.html"

if (-not (Test-Path $Editor)) {
    throw "Missing box job editor: $Editor"
}

Start-Process $Editor

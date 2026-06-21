$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_env\cicada_environment_manager.py"
py -3 $Tool plan

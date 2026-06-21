param(
    [string]$Phase = "003O",
    [string]$Verdict = "RECORDED",
    [string]$Note = "Manual run recorded.",
    [string]$Source = "manual"
)
$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_ledger\cicada_run_ledger.py"
py -3 $Tool --repo $Repo record --phase $Phase --verdict $Verdict --note $Note --source $Source

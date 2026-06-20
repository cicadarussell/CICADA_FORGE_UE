# CICADA APP PHASE RESPONSE TEMPLATE

Use this template when generating future phase cluster responses.

```markdown
[Download Phase XXX patch ZIP](sandbox:/mnt/data/<zip-name>.zip)

## Completeness

| Scope | Percent |
|---|---:|
| Whole app mega-build | X% |
| V0 alpha | Y% |
| Phase XXX patch | 100% ready to extract |

## What this patch does

- item
- item
- item

## PowerShell installer

```powershell
$Repo = "C:\CICADA\CICADA_APPS\APP_NAME"
$Downloads = Join-Path $env:USERPROFILE "Downloads"

$Zip = Get-ChildItem $Downloads -Filter "ZIP_NAME*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "Could not find patch ZIP in Downloads."
}

$Temp = Join-Path $env:TEMP ("cicada_patch_" + [guid]::NewGuid().ToString())

New-Item -ItemType Directory -Path $Temp -Force | Out-Null
Expand-Archive -Path $Zip.FullName -DestinationPath $Temp -Force

robocopy $Temp $Repo /E /NFL /NDL /NJH /NJS /NP
$RoboCode = $LASTEXITCODE

if ($RoboCode -gt 7) {
    throw "Robocopy failed with code $RoboCode"
}

Remove-Item -LiteralPath $Temp -Recurse -Force
Write-Host "Patch installed."
```

## Commit message

`Phase XXX: Clear commit message`

## Push

GitHub Desktop:

1. Review changes.
2. Commit to main.
3. Push origin.

## Next verification

Ask:

`next phase cluster`
```

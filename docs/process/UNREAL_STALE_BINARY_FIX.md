# UNREAL STALE BINARY FIX

## Problem

Sometimes GitHub/local source is updated, but Unreal still shows the previous UI text.

Example from this project:

- Source contained Phase 002B.
- Unreal still displayed Phase 002A.
- GitHub Desktop showed no local changes.

## Cause

Unreal was running an old compiled plugin/module binary.

Because naturally the source was right and the compiled goblin was lying.

## Fix

Close Unreal fully, then run:

```powershell
$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Remove-Item "$Repo\Binaries" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$Repo\Intermediate" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$Repo\Saved" -Recurse -Force -ErrorAction SilentlyContinue

Remove-Item "$Repo\Plugins\CICADAForge\Binaries" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$Repo\Plugins\CICADAForge\Intermediate" -Recurse -Force -ErrorAction SilentlyContinue
```

Then reopen:

```text
C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\CICADA_FORGE_UE.uproject
```

Allow Unreal to rebuild once.

## Standing rule

When the code says new phase and Unreal shows old phase:

1. Check local source text.
2. Check GitHub source text.
3. Clean compiled folders.
4. Rebuild once.
5. Only then assume the patch is broken.

Do not edit random files while Unreal is lying from stale binaries. That is how software becomes haunted.

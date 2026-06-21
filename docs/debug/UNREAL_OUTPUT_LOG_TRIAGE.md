# UNREAL OUTPUT LOG TRIAGE

## Goal

Stop losing time to normal Unreal noise.

Unreal logs like a paranoid cathedral. Not every warning is a project failure.

## Known non-blocking noise seen so far

These are usually not blockers for the current Win64 editor-only CICADA Forge test:

- `aqProf.dll` missing
- `VtuneApi.dll` missing
- `VtuneApi32e.dll` missing
- PIX capture plugin not initialized
- RenderDoc not loaded unless launched with RenderDoc
- XGE license not activated, standalone mode used
- Android SDK missing
- IOS SDK missing
- Linux SDK missing
- Mac SDK missing
- TVOS SDK missing
- DerivedDataCache maintenance
- Zen cache startup/maintenance
- EOS SDK config update/no change
- one-off audio buffer underrun
- source control disabled

## Important pass signals

These matter:

```text
Rebuild All: 1 succeeded, 0 failed, 0 skipped
Result: Succeeded
CICADA Forge safe action stub clicked:
CICADA Forge evidence stub clicked:
CICADA Forge debug stub clicked:
CICADA Forge receipt dry-run save:
```

## Important fail signals

These need action:

```text
error C
fatal error
LNK
UnrealBuildTool failed
Module could not be loaded
Incompatible or missing module after rebuild failure
Result: Failed
Rebuild All: 0 succeeded
```

## Rule

Noise can be ignored only if:

1. build succeeds
2. the Forge tab opens
3. expected Phase text appears
4. CICADA Forge click logs appear
5. no crash occurs

Otherwise, treat it as a real failure and capture the relevant lines.

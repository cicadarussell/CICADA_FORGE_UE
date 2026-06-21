# UNREAL OUTPUT LOG TRIAGE

## Goal

Stop losing time to normal Unreal noise.

Unreal logs like a haunted switchboard. Not every warning is a project failure.

## Known non-blocking noise seen so far

Usually not blockers for the current Win64 editor-only CICADA Forge test:

- `DerivedDataCache: Maintenance finished... deleted 0 files`
- `EOSSDK: SDK Config Product Update Request Completed - No Change`
- `EOSSDK: ScheduleNextSDKConfigDataUpdate`
- Slate Roboto font lazy loading
- `aqProf.dll` missing
- `VtuneApi.dll` missing
- PIX capture plugin not initialized
- RenderDoc not loaded unless launched with RenderDoc
- XGE license not activated, standalone mode used
- Android/iOS/Linux/Mac SDK checks
- one-off audio buffer underrun
- source control disabled

## Important pass signals

These matter:

```text
Rebuild All: 1 succeeded, 0 failed, 0 skipped
Result: Succeeded
CICADA Forge safe action stub clicked:
CICADA Forge evidence stub clicked:
CICADA Forge debug/evidence stub clicked:
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
2. Forge tab opens
3. expected Phase text appears
4. CICADA Forge click logs appear
5. no crash occurs

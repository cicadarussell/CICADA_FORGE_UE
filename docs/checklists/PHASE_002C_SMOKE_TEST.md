# PHASE 002C SMOKE TEST

## Before opening Unreal

Expected files:

- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Public/CICADAForgeStatusModel.h`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeStatusModel.cpp`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/process/UNREAL_STALE_BINARY_FIX.md`
- [ ] `docs/checklists/PHASE_002C_SMOKE_TEST.md`

## GitHub Desktop

- [ ] Commit message used:
      `Phase 002C: Add Forge UI status model`
- [ ] Push succeeds.
- [ ] GitHub browser shows Phase 002C files.

## Unreal open after patch

- [ ] Close Unreal fully.
- [ ] If Unreal may be stale, run the stale-binary clean.
- [ ] Double-click `CICADA_FORGE_UE.uproject`.
- [ ] If Unreal asks to rebuild modules, click Yes once.
- [ ] If rebuild fails, screenshot the error and stop.

## Menu/tab test

- [ ] Open:
      `Window -> CICADA Forge`
- [ ] Confirm a tab opens.
- [ ] Confirm the tab includes:
      `CICADA FORGE`
- [ ] Confirm the tab includes:
      `Phase 002C: status model feeds the shell`
- [ ] Confirm bottom strip includes:
      `LOG: Phase 002C status model loaded.`
- [ ] Confirm `PROJECT`, `FORGE WORKSPACE`, and `STATUS` still appear.

## Verdict

- [ ] PASS - status model UI opens.
- [ ] PARTIAL - project opens but status model/layout fails.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`

Do not move to Phase 002D until this is answered. The shell now has a tiny brain. We check the brain before giving it hands.

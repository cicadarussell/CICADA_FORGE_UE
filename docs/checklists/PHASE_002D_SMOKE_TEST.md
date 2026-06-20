# PHASE 002D SMOKE TEST

## Before opening Unreal

Expected files:

- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Public/CICADAForgeProjectState.h`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeProjectState.cpp`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeStatusModel.cpp`
- [ ] `docs/checklists/PHASE_002D_SMOKE_TEST.md`

## GitHub Desktop

- [ ] Commit message used:
      `Phase 002D: Add persistent Forge project state`
- [ ] Push succeeds.
- [ ] GitHub browser shows Phase 002D files.

## Unreal clean/rebuild

- [ ] Close Unreal fully.
- [ ] Run stale-binary clean if C++ changed.
- [ ] Double-click `CICADA_FORGE_UE.uproject`.
- [ ] If Unreal asks to rebuild modules, click Yes once.
- [ ] If rebuild fails, screenshot the error and stop.

## Menu/tab test

- [ ] Open:
      `Window -> CICADA Forge`
- [ ] Confirm the tab includes:
      `CICADA FORGE`
- [ ] Confirm the tab includes:
      `Phase 002D: persistent project state feeds the shell`
- [ ] Confirm status rail includes:
      `Project State`
- [ ] Confirm bottom strip includes:
      `LOG: Phase 002D persistent project state loaded.`
- [ ] Confirm `PROJECT`, `FORGE WORKSPACE`, and `STATUS` still appear.

## Verdict

- [ ] PASS - persistent project state feeds UI.
- [ ] PARTIAL - project opens but config/state does not appear.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`

Do not move to Phase 002E until this is answered. The shell now remembers its own name. Revolutionary, apparently.

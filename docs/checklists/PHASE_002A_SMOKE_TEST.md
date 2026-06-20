# PHASE 002A SMOKE TEST

## Before opening Unreal

Expected files:

- [ ] `Plugins/CICADAForge/CICADAForge.uplugin`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/CICADAForgeEditor.Build.cs`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Public/CICADAForgeEditorModule.h`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`

## GitHub Desktop

- [ ] Commit message used:
      `Phase 002A: Add Forge editor UI shell`
- [ ] Push succeeds.
- [ ] GitHub browser shows Phase 002A files.

## Unreal first open after patch

- [ ] Double-click `CICADA_FORGE_UE.uproject`.
- [ ] If Unreal asks to rebuild modules, click Yes once.
- [ ] If rebuild fails, screenshot the error and stop.
- [ ] If project opens, open Output Log.
- [ ] Search for:
      `CICADA Forge Editor module started.`

## Menu/tab test

- [ ] In Unreal Editor, open top menu:
      `Window`
- [ ] Find:
      `CICADA Forge`
- [ ] Click it.
- [ ] Confirm a tab opens.
- [ ] Confirm the tab includes text:
      `CICADA FORGE`
      `Phase 002A: Forge UI shell is alive.`

## Verdict

- [ ] PASS - menu exists and tab opens.
- [ ] PARTIAL - project opens but menu/tab fails.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`

Do not move to Phase 002B until this is answered. We are not building a cathedral on a tab that might be imaginary.

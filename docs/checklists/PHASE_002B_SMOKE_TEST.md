# PHASE 002B SMOKE TEST

## Before opening Unreal

Expected files:

- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_002B_STRUCTURED_FORGE_COCKPIT.md`
- [ ] `docs/checklists/PHASE_002B_SMOKE_TEST.md`

## GitHub Desktop

- [ ] Commit message used:
      `Phase 002B: Add structured Forge cockpit shell`
- [ ] Push succeeds.
- [ ] GitHub browser shows Phase 002B files.

## Unreal open after patch

- [ ] Double-click `CICADA_FORGE_UE.uproject`.
- [ ] If Unreal asks to rebuild modules, click Yes once.
- [ ] If rebuild fails, screenshot the error and stop.
- [ ] If project opens, open Output Log.

## Menu/tab test

- [ ] Open:
      `Window -> CICADA Forge`
- [ ] Confirm a tab opens.
- [ ] Confirm the tab includes:
      `CICADA FORGE`
- [ ] Confirm the tab includes:
      `Phase 002B: structured cockpit shell is alive.`
- [ ] Confirm left section includes:
      `PROJECT`
- [ ] Confirm centre section includes:
      `FORGE WORKSPACE`
- [ ] Confirm right section includes:
      `STATUS`
- [ ] Confirm bottom strip includes:
      `LOG: Phase 002B shell loaded.`

## Verdict

- [ ] PASS - structured shell opens.
- [ ] PARTIAL - project opens but layout/menu fails.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`

Do not move to Phase 002C until this is answered. The tab is now the chassis. We check the chassis before bolting on the engine like absolute maniacs.

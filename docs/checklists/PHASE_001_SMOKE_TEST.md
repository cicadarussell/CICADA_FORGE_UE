# PHASE 001 SMOKE TEST

Use this checklist after extracting the Phase 001A patch.

## 0. Before opening Unreal

Repo root should contain:

- [ ] `CICADA_FORGE_UE.uproject`
- [ ] `Config/DefaultGame.ini`
- [ ] `Config/DefaultEngine.ini`
- [ ] `Plugins/CICADAForge/CICADAForge.uplugin`
- [ ] `Plugins/CICADAForge/Source/CICADAForge/CICADAForge.Build.cs`
- [ ] `Plugins/CICADAForge/Source/CICADAForge/Public/CICADAForgeModule.h`
- [ ] `Plugins/CICADAForge/Source/CICADAForge/Private/CICADAForgeModule.cpp`

## 1. GitHub Desktop

- [ ] GitHub Desktop points to `C:\CICADA\CICADA_APPS\CICADA_FORGE_UE`
- [ ] Commit message used:
      `Phase 001A: Add UE project and CICADAForge plugin skeleton`
- [ ] Push succeeds.
- [ ] GitHub browser shows the files.

## 2. Unreal first open

- [ ] Double-click `CICADA_FORGE_UE.uproject`.
- [ ] If Unreal asks to rebuild modules, click Yes once.
- [ ] If rebuild fails, screenshot the error and stop.
- [ ] If project opens, open Output Log.
- [ ] Search for:
      `CICADA Forge module started.`

## 3. Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`

## 4. Verdict

- [ ] PASS - project opens and plugin loads.
- [ ] PARTIAL - project opens but plugin compile/loading fails.
- [ ] FAIL - project does not open.

Do not move to Phase 002 until this is answered. We are not doing vibes-based engineering, regrettably for the entire startup industry.

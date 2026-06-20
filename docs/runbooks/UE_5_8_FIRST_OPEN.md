# UE5.8 FIRST OPEN RUNBOOK

## Goal

Open the CICADA FORGE UE project and verify the minimal CICADAForge plugin skeleton.

## Path

Repo root:

`C:\CICADA\CICADA_APPS\CICADA_FORGE_UE`

Project file:

`C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\CICADA_FORGE_UE.uproject`

## Steps

1. Close Unreal Engine.
2. Extract Phase 001A patch into repo root.
3. Commit and push the patch.
4. Double-click `CICADA_FORGE_UE.uproject`.
5. If Unreal asks to rebuild modules, click Yes once.
6. If it opens, go to:
   `Window > Developer Tools > Output Log`
7. Search for:
   `CICADA Forge module started.`

## If Unreal cannot build the module

Capture:

- screenshot of popup
- output log text
- Visual Studio/compiler error
- exact Unreal version
- whether Visual Studio Build Tools are installed

Then do not randomly delete folders. We patch from evidence because apparently civilisation requires restraint.

## Expected outcome

Phase 001A should either:

- open cleanly and prove the plugin loads, or
- fail with a specific C++/toolchain error that we can patch.

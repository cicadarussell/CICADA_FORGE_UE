# PHASE 002I SMOKE TEST

## Files expected

- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_002I_SESSION_METADATA_PANEL.md`
- [ ] `docs/checklists/PHASE_002I_SMOKE_TEST.md`

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 002I: session metadata panel tracks the local Forge run`
- [ ] Right rail shows:
      `Session Metadata`
- [ ] Session Metadata shows:
      `Session ID:`
      `Started:`
      `Safe UI events: 0`
      `Last action: none`
      `Persistence: memory only`
- [ ] Clicking `New design` increments Safe UI events and changes Last action.
- [ ] Clicking all four buttons increments Safe UI events.
- [ ] Event Log still records latest safe UI events.
- [ ] Output Log still logs:
      `CICADA Forge safe action stub clicked:`
- [ ] No file export occurs.
- [ ] No CAD sidecar call occurs.
- [ ] No machine bridge action occurs.

## Verdict

- [ ] PASS - Session Metadata updates safely.
- [ ] PARTIAL - UI opens but session metadata does not update.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`

# PHASE 002H SMOKE TEST

## Files expected

- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_002H_IN_MEMORY_EVENT_LOG.md`
- [ ] `docs/checklists/PHASE_002H_SMOKE_TEST.md`

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 002H: in-memory event log records safe UI clicks`
- [ ] Right rail shows:
      `Event Log`
- [ ] Event Log initially shows:
      `Waiting for safe UI events.`
- [ ] Clicking `New design` adds:
      `New design -> safe stub logged only`
- [ ] Clicking `Open feature graph` adds:
      `Open feature graph -> safe stub logged only`
- [ ] Clicking `Run validation` adds:
      `Run validation -> safe stub logged only`
- [ ] Clicking `Export proof receipt` adds:
      `Export proof receipt -> safe stub logged only`
- [ ] Output Log still logs:
      `CICADA Forge safe action stub clicked:`
- [ ] No file export occurs.
- [ ] No CAD sidecar call occurs.
- [ ] No machine bridge action occurs.

## Verdict

- [ ] PASS - Event Log accumulates safe UI events.
- [ ] PARTIAL - UI opens but event log does not update.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`

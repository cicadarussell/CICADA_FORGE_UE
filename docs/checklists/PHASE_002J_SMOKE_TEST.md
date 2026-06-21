# PHASE 002J SMOKE TEST

## Files expected

- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_002J_EVIDENCE_RECEIPT_COCKPIT.md`
- [ ] `docs/checklists/PHASE_002J_SMOKE_TEST.md`

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 002J: evidence receipt cockpit is alive`
- [ ] Centre workspace shows:
      `Evidence Receipt Controls`
- [ ] Right rail shows:
      `Evidence Receipt Preview`
- [ ] Receipt Preview initially shows:
      `Status: waiting for evidence`
      `Last evidence: none`
      `Save mode: disabled until Phase 003`
- [ ] Clicking `Screenshot observed` updates Receipt Preview.
- [ ] Clicking `Output log checked` updates Receipt Preview.
- [ ] Clicking `UI pass candidate` updates Receipt Preview.
- [ ] Clicking normal action buttons still updates selected action, Last Action, Event Log, and Session Metadata.
- [ ] Clicking `Clear visible event log` clears visible log and records a system event.
- [ ] Output Log still logs safe action/evidence/system stubs.
- [ ] No file export occurs.
- [ ] No CAD sidecar call occurs.
- [ ] No machine bridge action occurs.

## Verdict

- [ ] PASS - Evidence receipt cockpit updates safely.
- [ ] PARTIAL - UI opens but one state panel does not update.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`

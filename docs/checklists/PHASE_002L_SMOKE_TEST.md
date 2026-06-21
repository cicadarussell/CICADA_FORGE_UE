# PHASE 002L SMOKE TEST

## Files expected

- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_002L_SCROLLABLE_BACKEND_DEBUG_COCKPIT.md`
- [ ] `docs/checklists/PHASE_002L_SMOKE_TEST.md`
- [ ] `docs/debug/UNREAL_OUTPUT_LOG_TRIAGE.md`

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 002L: scrollable backend debug cockpit is alive`
- [ ] Right rail no longer cuts off critical status cards.
- [ ] Left rail scrolls if needed.
- [ ] Centre workspace scrolls if needed.
- [ ] Right rail scrolls if needed.
- [ ] Centre workspace shows:
      `Backend Inspector`
- [ ] Right rail shows:
      `Backend Health`
- [ ] Click:
      `[debug] Show backend map`
- [ ] Backend Inspector lists working/not-built/locked systems.
- [ ] Click:
      `[debug] Classify known log noise`
- [ ] It classifies DDC, EOSSDK, and Slate font lazy loading as known non-blocking noise.
- [ ] No CAD export occurs.
- [ ] No sidecar call occurs.
- [ ] No machine bridge action occurs.

## Verdict

- [ ] PASS - UI is scrollable and backend readiness is clear.
- [ ] PARTIAL - UI opens but one debug/status panel fails.
- [ ] FAIL - project fails to open or compile.

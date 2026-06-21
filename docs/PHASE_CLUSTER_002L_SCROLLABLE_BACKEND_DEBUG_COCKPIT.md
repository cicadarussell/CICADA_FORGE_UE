# PHASE CLUSTER 002L - SCROLLABLE BACKEND DEBUG COCKPIT

## Build type

Mainline cumulative patch.

## Why this phase exists

User identified two real problems:

1. The right side of the UI is overflowing off-screen.
2. The UI needs to make it obvious what backend pieces are working, not built, stubbed, or locked.

This phase fixes the first layout problem and makes backend readiness visible.

## Scope

This phase adds:

- scroll boxes to left, centre, and right rails
- right rail proportion adjustment
- centre `Backend Inspector`
- right-rail `Backend Health`
- `Show backend map` debug button
- backend map listing:
  - working pieces
  - explicit dry-run pieces
  - not-built pieces
  - locked machine bridge
- log triage docs updated for DDC/EOS/Slate font lazy-load noise

## Strict boundaries

Allowed:

- UI updates
- Output Log lines
- local JSON receipt under project `Saved`
- PowerShell log scan script

Not allowed:

- CAD export
- sidecar calls
- machine commands
- automated screenshot capture
- arbitrary file writing outside project `Saved/CICADAForge/Receipts`
- destructive actions

## Pass condition

Phase 002L passes when:

1. Unreal opens after rebuild.
2. UI shows:
   `Phase 002L: scrollable backend debug cockpit is alive`
3. Right rail can scroll instead of overflowing/cutting off.
4. Centre workspace shows:
   `Backend Inspector`
5. Right rail shows:
   `Backend Health`
6. Clicking `Show backend map` lists working/not-built/locked systems.
7. DDC/EOS/Slate font messages are treated as known noise, not blockers.
8. No CAD export, sidecar call, or machine command occurs.

## Next phase after pass

Phase 003A:
Start the internal Feature Graph V0 data model. Do not build visual node editing first. First build a small safe feature/state model the UI can inspect.

# FORGE UI SHELL SPEC

## Purpose

Define the early CICADA Forge editor UI direction without overbuilding it.

## Phase 002A

Single editor menu item and placeholder tab.

## Phase 002B

Structured cockpit shell:

| Area | Purpose |
|---|---|
| Left rail | project identity and action stubs |
| Centre | workspace canvas / future feature graph |
| Right rail | evidence, sidecar, machine, safety status |
| Bottom strip | logs, errors, run receipts |

## Phase 002C target

Replace hardcoded labels with a small in-memory status model.

Potential model fields:

- project name
- phase label
- repo state
- evidence state
- CAD sidecar state
- machine bridge state
- last log line

## Design constraints

- Must be useful before it is pretty.
- Must show state visibly.
- Must make failure obvious.
- Must not hide machine-risk operations.
- Must not generate asset sludge just to look fancy.
- Must not pretend stubs are real systems.

## Future visual direction

Clean white/black CICADA interface with meaningful status colour, not random cyberpunk aquarium nonsense.

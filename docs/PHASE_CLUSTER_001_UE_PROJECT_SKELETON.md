# PHASE CLUSTER 001 - UE PROJECT SKELETON

## Build type

Mainline.

## Current target

Create the smallest serious Unreal Engine 5.8 project skeleton that can become CICADA FORGE without turning GitHub into a landfill.

## Phase 001A scope

This patch adds:

- root Unreal project file
- minimal Unreal config
- CICADAForge plugin descriptor
- minimal C++ module skeleton
- first-open runbook
- smoke-test checklist
- evidence log

## What this phase deliberately does not add

- Forge UI
- node canvas
- agent system
- CAD generation
- sidecar HTTP service
- live camera system
- machine bridge
- Comfy/Ollama integrations
- asset-heavy content

No grand cathedral yet. First we check whether the door opens.

## Pass condition

Phase 001A passes when:

1. `CICADA_FORGE_UE.uproject` opens in Unreal Engine 5.8.
2. Unreal either loads the CICADAForge plugin or gives a clear compile error.
3. If it compiles, Output Log shows:
   `CICADA Forge module started.`
4. Evidence is written in:
   `docs/evidence/EVIDENCE_LOG.md`
5. GitHub has the committed result.

## Fail condition

Phase 001A fails if:

- Unreal cannot locate the project.
- Unreal cannot compile the plugin.
- the plugin descriptor is invalid.
- files are in the wrong folder.
- GitHub has only partial files after push.

## Evidence required

- Screenshot of repo root after extraction.
- Screenshot of Unreal open/rebuild prompt if shown.
- Output Log line or compile error.
- GitHub commit visible online.

## Next phase after pass

Phase 001B:
Create a minimal Forge project registry and placeholder runtime data folder.

Phase 002:
Forge UI Shell.

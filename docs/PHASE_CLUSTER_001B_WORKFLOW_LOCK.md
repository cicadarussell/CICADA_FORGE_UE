# PHASE CLUSTER 001B - WORKFLOW LOCK

## Build type

Mainline.

## Goal

Close Phase 001 and lock the reusable CICADA app development workflow.

This phase is not glamorous. It is plumbing. But plumbing beats drowning in project folders named `final_real_v7_use_this_one`. Humanity learns slowly.

## Inputs

- Phase 001A project skeleton has been pushed to GitHub.
- User reported Unreal opened/worked.
- ChatGPT can read GitHub files.
- Direct ChatGPT write access is not reliable, so the ZIP-to-GitHub loop is the current build pipeline.

## Output

This patch adds or updates:

- `PROJECT_STATUS.md`
- `CHATGPT_HANDOFF.md`
- `docs/evidence/EVIDENCE_LOG.md`
- `docs/process/CICADA_APP_ZIP_TO_GITHUB_WORKFLOW.md`
- `docs/templates/CICADA_APP_PHASE_RESPONSE_TEMPLATE.md`
- `scripts/install_latest_cicada_patch.ps1`
- `scripts/cicada_safe_sync_v02.ps1`
- `docs/checklists/PHASE_001B_CHECKLIST.md`

## Pass condition

Phase 001B passes when:

1. Files are extracted into repo root.
2. GitHub Desktop shows changed files.
3. User commits:
   `Phase 001B: Close Phase 001 and lock CICADA app workflow`
4. User pushes to GitHub.
5. ChatGPT verifies files online.

## Next phase

Phase 002A: Forge UI Shell skeleton.

Likely Phase 002A scope:

- add Editor module or runtime UI shell decision
- create placeholder Forge workspace map / config
- add minimal UI command/menu/tab if feasible
- keep asset and binary noise out of GitHub

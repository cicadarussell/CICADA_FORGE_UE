# CICADA APP ZIP-TO-GITHUB WORKFLOW

## Purpose

This is the default CICADA development loop for apps where ChatGPT can generate files but cannot directly push commits.

Use this pattern for future CICADA apps unless a better repo-native write tool is available.

## The loop

1. ChatGPT gives the ZIP download link at the top.
2. ChatGPT gives completion percentages.
3. User downloads ZIP.
4. User runs a PowerShell extractor into the local repo root.
5. User checks changed files in GitHub Desktop.
6. User commits with the provided commit message.
7. User pushes to GitHub.
8. ChatGPT reads GitHub and verifies.
9. User asks for next phase cluster.
10. Repeat.

## Why this works

- GitHub becomes project memory.
- ZIP patches avoid copy/paste file mistakes.
- PowerShell avoids nested-folder mistakes.
- GitHub Desktop gives human review before push.
- Future chats can inspect the repo and continue.
- The local machine remains the write authority.

## Required response shape for future phase clusters

Every phase ZIP response should start with:

1. Download link.
2. Completeness table.
3. What the patch changes.
4. PowerShell installer.
5. Commit message.
6. GitHub push instruction.
7. Next verification instruction.

## Local repo rule

Do not manually scatter files.

Always extract into the repo root:

`C:\CICADA\CICADA_APPS\<APP_NAME>`

For this project:

`C:\CICADA\CICADA_APPS\CICADA_FORGE_UE`

## GitHub rule

Do not upload generated sludge:

- Unreal `Binaries`
- Unreal `Intermediate`
- Unreal `Saved`
- Unreal `DerivedDataCache`
- local logs
- export junk
- raw evidence videos unless deliberately tracked through LFS

Use source/config/docs/scripts/plugin skeletons first.

## Phase gate rule

Do not advance because a file exists.

Advance when the expected behaviour is verified and evidence is logged.

Painful. Useful. Like engineering wearing steel-toe boots.

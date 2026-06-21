# FULL PROJECT AUDIT CONTRACT

The full project audit is a passive local diagnostic. It never controls machines.

It checks:

- required repo files
- Python syntax compile for `tools/**/*.py`
- old external nested PowerShell switch forwarding
- generated-output `.gitignore`
- current phase label
- obvious safety marker violations

It writes:

- `Saved/CICADAForge/IntegrationReports/full_project_audit_<stamp>.json`
- `Saved/CICADAForge/IntegrationReports/full_project_audit_<stamp>.html`
- latest copies

It returns nonzero only if real failures are found.

## Patch-folder sandbox tolerance

When run against a patch folder rather than a full checked-out Unreal repo, missing `CICADA_FORGE_UE.uproject` and plugin descriptor are marked CHECK. In the installed repo they should be PASS.

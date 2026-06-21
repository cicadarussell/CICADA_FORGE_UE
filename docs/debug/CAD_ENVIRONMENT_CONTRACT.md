# CAD ENVIRONMENT CONTRACT

## Purpose

The CAD environment layer manages exact CAD engine readiness without polluting the main project loop.

## Rules

- Do not install anything automatically.
- Create venv only when explicitly requested.
- Install CadQuery only when explicitly requested.
- Report exact engine status honestly.
- If CadQuery is missing, STEP remains blocked.

## Venv path

`.cicada_envs/cadquery`

## Reports

`Saved/CICADAForge/EnvReports`

# CAD ENGINE LAUNCHER CONTRACT

## Purpose

Pick the correct Python for exact CAD export.

Preferred order:

1. `.cicada_envs/cadquery` Python if it exists and has CadQuery.
2. Current Python if it has CadQuery.
3. Current Python with `--engine none`, forcing honest blocked STEP reports.

## Forbidden

- fake STEP
- automatic installs
- machine commands

# CAD FEATURE INTENT V0.2 CONTRACT

## Supported V0.2 features

| Feature | Meaning |
|---|---|
| box | base rectangular solid |
| hole | through hole on top face |
| slot | axis-aligned rounded slot through top face |
| standoff | cylindrical boss on top face, optional pilot hole |

## Not yet supported

- angled exact export
- fillets
- chamfers
- shelling
- patterns
- multiple bodies
- assemblies
- constraints

## No-fake rule

If exact export cannot represent a feature, it must be blocked or reported.

It must not be silently approximated as a fake STEP.

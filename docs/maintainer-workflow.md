# Maintainer Workflow

Use this workflow when changing the compiler, examples, or docs.

## Local Checks

```powershell
python -m pip install -e .
python -m unittest discover -s tests
python -m cad_industrial_compiler validate-catalog `
  --catalog .\examples\synthetic_component_catalog.csv
python -m cad_industrial_compiler validate-placement `
  --placement-plan .\examples\synthetic_project\planning\placement_plan.csv
python -m cad_industrial_compiler validate-ir `
  --ir .\examples\synthetic_project\ir\cad_ir.json
```

## Release Checklist

1. Run tests.
2. Run the privacy scan described in `privacy-and-sanitization.md`.
3. Check that examples are synthetic.
4. Check that no local absolute paths are committed.
5. Check that no private CAD, office, image, or report files are committed.
6. Tag a release only after the validation output is clean.

## Issue Triage

For new issues, ask for public or synthetic reproduction data. If a user needs
help with a private CAD project, request only schema-level summaries and
sanitized metadata.

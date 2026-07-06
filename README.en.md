# CAD Agent Skill

<div align="center">

**CAD Industrial Design Planning Skill**  
Turn open-ended CAD tasks into reproducible and reviewable artifacts before geometry generation.

<a href="README.md"><img alt="中文（默认）" src="https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87%E9%BB%98%E8%AE%A4-0f766e?style=for-the-badge"></a>
<a href="README.en.md"><img alt="English" src="https://img.shields.io/badge/README-English-0f766e?style=for-the-badge"></a>
<a href="https://github.com/Zc030201/cad-agent-skill/actions/workflows/test.yml"><img alt="tests" src="https://img.shields.io/github/actions/workflow/status/Zc030201/cad-agent-skill/test.yml?branch=main&label=tests&style=for-the-badge"></a>
<a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-MIT-0f766e?style=for-the-badge"></a>

</div>

<p align="center">
  <img src="assets/cad-agent-skill-hero.svg" alt="CAD Agent Skill hero" width="760">
</p>

<p align="center">
  <img src="assets/cad-agent-skill-demo.gif" alt="CAD Agent Skill demo" width="760">
</p>

## Problems It Solves

Automated CAD workflows often suffer from:

1. Mixed requirement formats and unstable interpretation
2. Weak traceability of component and placement decisions
3. Missing reproducibility checks before downstream geometry generation

`CAD Agent Skill` addresses this by converting each task into structured planning artifacts before modeling.

## Flow

```text
textual requirements
        |
        v
        CAD IR
        |
        v
catalog matching -> placement plan -> execution graph -> validation report
```

## Core Capabilities

### Structured intent

Normalize requirement intent into `cad_ir.json`, including constraints, boundaries, assumptions, and uncertainties.

### Reusable components

Match and rank from a documented catalog, then return traceable selection outputs.

### Reviewable outputs

Produce `placement_plan.csv`, `execution_graph.json`, and `validation` artifacts for human or automated review.

## Quick start (2 steps)

```powershell
git clone https://github.com/Zc030201/cad-agent-skill.git
cd cad-agent-skill
python -m pip install -e .
```

```powershell
cad-agent-skill validate-catalog --catalog .\examples\synthetic_component_catalog.csv
cad-agent-skill validate-placement --placement-plan .\examples\synthetic_project\planning\placement_plan.csv
```

If both commands pass, your minimal verification path is ready.

## Deliverables

- `cad_ir.json`: normalized requirements, constraints, and assembly relations
- `component_catalog.csv`: sample reusable component metadata
- `placement_plan.csv`: deterministic placement relation and pose parameters
- `execution_graph.json`: execution ordering and dependency graph
- `validation_report.json`: missing fields, invalid values, and review recommendations

## Documentation

- [Architecture](docs/architecture.md)
- [Data contract](docs/data-contract.md)
- [Maintainer workflow](docs/maintainer-workflow.md)
- [Privacy and sanitization](docs/privacy-and-sanitization.md)

## Privacy

This repo is designed for synthetic examples by default. Avoid real business data, real identifiers, private local paths, and production component libraries.

Recommended pre-release check: `python scripts/privacy_scan.py .`

## License

MIT


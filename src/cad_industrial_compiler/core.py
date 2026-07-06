from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


CONFIDENCE_RANK = {
    "needs_review": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}

PROJECT_DIRS = [
    "inputs",
    "ir",
    "catalog",
    "planning",
    "graph",
    "execution/checkpoints",
    "validation",
    "exports",
]

CATALOG_FIELDS = [
    "component_id",
    "category",
    "name",
    "confidence",
    "catalog_status",
    "source",
    "bbox_x_mm",
    "bbox_y_mm",
    "bbox_z_mm",
    "notes",
]

PLACEMENT_FIELDS = [
    "placement_id",
    "component_id",
    "parent_assembly",
    "tx_mm",
    "ty_mm",
    "tz_mm",
    "rx_deg",
    "ry_deg",
    "rz_deg",
    "datum_rule",
    "status",
    "notes",
]


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: str | Path, rows: Iterable[dict], fields: list[str]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, data: dict) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def classify_input(value: str) -> str:
    suffix = Path(value).suffix.lower()
    if suffix in {".dwg", ".dxf"}:
        return "drawing"
    if suffix in {".step", ".stp", ".sldprt", ".sldasm", ".x_t", ".x_b"}:
        return "cad_model"
    if suffix in {".csv", ".xlsx", ".xlsm"}:
        return "table"
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return "image"
    if suffix in {".md", ".txt"}:
        return "text"
    return "note"


def create_ir(project_id: str, inputs: list[str] | None = None, requirements: list[str] | None = None) -> dict:
    entries: list[dict] = []
    for index, value in enumerate(inputs or [], 1):
        entries.append(
            {
                "input_id": f"IN{index:03d}",
                "kind": classify_input(value),
                "path_or_text": value,
                "exists": Path(value).exists(),
                "source_priority": "provided_input",
            }
        )
    start = len(entries) + 1
    for offset, value in enumerate(requirements or [], start):
        entries.append(
            {
                "input_id": f"IN{offset:03d}",
                "kind": "requirement",
                "path_or_text": value,
                "exists": False,
                "source_priority": "user_requirement",
            }
        )

    return {
        "project_id": project_id,
        "created_at": utc_now(),
        "global_units": "mm",
        "inputs": entries,
        "coordinate_system": {
            "origin_policy": "project_defined",
            "axis_policy": "right_handed",
            "notes": "",
        },
        "constraints": [],
        "parts": [],
        "assemblies": [],
        "catalog_requirements": [],
        "uncertainties": [],
        "source_trace": [],
    }


def build_execution_graph(project_root: str | Path) -> dict:
    root = Path(project_root)
    nodes = [
        ("input", "InputNode", ["inputs"], ["ir/cad_ir.json"]),
        ("ir-normalize", "ConstraintNode", ["ir/cad_ir.json"], ["planning/project_rebuild_manifest.csv"]),
        ("catalog-query", "CatalogQueryNode", ["planning/project_rebuild_manifest.csv"], ["planning/selected_components.csv"]),
        ("placement", "PlacementSolveNode", ["planning/selected_components.csv"], ["planning/placement_plan.csv"]),
        ("build", "CADBuildNode", ["planning/placement_plan.csv"], ["exports"]),
        ("validate", "ValidationNode", ["exports"], ["validation/validation_report.json"]),
        ("export", "ExportNode", ["validation/validation_report.json"], ["exports/final_package"]),
    ]
    graph_nodes = []
    previous: list[str] = []
    for node_id, node_type, inputs, outputs in nodes:
        graph_nodes.append(
            {
                "node_id": node_id,
                "node_type": node_type,
                "inputs": [str(root / item) for item in inputs],
                "outputs": [str(root / item) for item in outputs],
                "depends_on": previous.copy(),
                "status": "pending",
                "checkpoint_path": str(root / "execution" / "checkpoints" / f"{node_id}.json"),
                "trace": [],
            }
        )
        previous = [node_id]
    return {"graph_version": "0.1", "created_at": utc_now(), "nodes": graph_nodes}


def init_project(project_id: str, root: str | Path) -> dict:
    project_root = Path(root)
    for rel in PROJECT_DIRS:
        (project_root / rel).mkdir(parents=True, exist_ok=True)

    state = {
        "project_id": project_id,
        "created_at": utc_now(),
        "stage": "initialized",
        "required_files": {
            "cad_ir": str(project_root / "ir" / "cad_ir.json"),
            "execution_graph": str(project_root / "graph" / "execution_graph.json"),
            "placement_plan": str(project_root / "planning" / "placement_plan.csv"),
            "validation_report": str(project_root / "validation" / "validation_report.json"),
        },
    }
    write_json(project_root / "compiler_state.json", state)
    write_json(project_root / "ir" / "cad_ir.json", create_ir(project_id))
    write_json(project_root / "graph" / "execution_graph.json", build_execution_graph(project_root))
    return state


def confidence_rank(value: str) -> int:
    return CONFIDENCE_RANK.get(str(value or "").strip().lower(), -1)


def query_catalog(
    rows: list[dict[str, str]],
    category: str | None = None,
    contains: str | None = None,
    min_confidence: str = "low",
) -> list[dict[str, str]]:
    min_rank = confidence_rank(min_confidence)
    needle = str(contains or "").lower()
    result = []
    for row in rows:
        if category and row.get("category") != category:
            continue
        if confidence_rank(row.get("confidence", "")) < min_rank:
            continue
        if needle:
            blob = " ".join(str(value) for value in row.values()).lower()
            if needle not in blob:
                continue
        result.append(row)
    return sorted(result, key=lambda row: (confidence_rank(row.get("confidence", "")), row.get("component_id", "")), reverse=True)


def build_placement_plan(selected_rows: list[dict[str, str]], default_parent: str = "ROOT_ASSEMBLY") -> list[dict[str, str]]:
    plan = []
    for index, row in enumerate(selected_rows, 1):
        confidence = row.get("confidence", "")
        status = "candidate" if confidence_rank(confidence) >= CONFIDENCE_RANK["medium"] else "manual_review"
        plan.append(
            {
                "placement_id": f"PLC{index:04d}",
                "component_id": row.get("component_id", ""),
                "parent_assembly": row.get("parent_assembly") or default_parent,
                "tx_mm": row.get("tx_mm", "0"),
                "ty_mm": row.get("ty_mm", "0"),
                "tz_mm": row.get("tz_mm", "0"),
                "rx_deg": row.get("rx_deg", "0"),
                "ry_deg": row.get("ry_deg", "0"),
                "rz_deg": row.get("rz_deg", "0"),
                "datum_rule": row.get("datum_rule") or "project_datum",
                "status": status,
                "notes": row.get("notes", ""),
            }
        )
    return plan


def is_positive_number(value: str) -> bool:
    try:
        return float(value) > 0
    except Exception:
        return False


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except Exception:
        return False


def validate_catalog_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    required = ["component_id", "category", "confidence", "bbox_x_mm", "bbox_y_mm", "bbox_z_mm"]
    for line, row in enumerate(rows, 2):
        for field in required:
            if not str(row.get(field, "")).strip():
                issues.append({"line": str(line), "component_id": row.get("component_id", ""), "issue": "missing_required", "field": field})
        for field in ["bbox_x_mm", "bbox_y_mm", "bbox_z_mm"]:
            if row.get(field) and not is_positive_number(row[field]):
                issues.append({"line": str(line), "component_id": row.get("component_id", ""), "issue": "invalid_bbox", "field": field})
        if confidence_rank(row.get("confidence", "")) < 0:
            issues.append({"line": str(line), "component_id": row.get("component_id", ""), "issue": "invalid_confidence", "field": "confidence"})
    return issues


def validate_placement_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    required = ["placement_id", "component_id", "parent_assembly", "tx_mm", "ty_mm", "tz_mm", "rx_deg", "ry_deg", "rz_deg", "status"]
    for line, row in enumerate(rows, 2):
        for field in required:
            if not str(row.get(field, "")).strip():
                issues.append({"line": str(line), "placement_id": row.get("placement_id", ""), "issue": "missing_required", "field": field})
        for field in ["tx_mm", "ty_mm", "tz_mm", "rx_deg", "ry_deg", "rz_deg"]:
            if row.get(field, "") and not is_number(row[field]):
                issues.append({"line": str(line), "placement_id": row.get("placement_id", ""), "issue": "invalid_number", "field": field})
    return issues


def validate_ir(ir: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for field in ["project_id", "global_units", "inputs", "constraints", "parts", "assemblies", "uncertainties", "source_trace"]:
        if field not in ir:
            issues.append({"issue": "missing_required", "field": field})
    if ir.get("global_units") != "mm":
        issues.append({"issue": "unexpected_units", "field": "global_units", "value": str(ir.get("global_units"))})
    return issues

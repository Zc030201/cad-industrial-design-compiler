from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from cad_agent_skill.core import (
    build_placement_plan,
    create_ir,
    init_project,
    query_catalog,
    read_csv,
    validate_catalog_rows,
    validate_ir,
    validate_placement_rows,
)


class CoreTests(unittest.TestCase):
    def test_create_ir_contains_required_sections(self) -> None:
        ir = create_ir("demo", requirements=["Create a public synthetic assembly."])
        self.assertEqual(ir["project_id"], "demo")
        self.assertEqual(ir["global_units"], "mm")
        self.assertEqual(len(ir["inputs"]), 1)
        self.assertEqual(validate_ir(ir), [])

    def test_query_catalog_filters_by_category_and_confidence(self) -> None:
        rows = [
            {"component_id": "A", "category": "hinge", "confidence": "high", "bbox_x_mm": "1", "bbox_y_mm": "1", "bbox_z_mm": "1"},
            {"component_id": "B", "category": "hinge", "confidence": "low", "bbox_x_mm": "1", "bbox_y_mm": "1", "bbox_z_mm": "1"},
            {"component_id": "C", "category": "panel", "confidence": "high", "bbox_x_mm": "1", "bbox_y_mm": "1", "bbox_z_mm": "1"},
        ]
        result = query_catalog(rows, category="hinge", min_confidence="medium")
        self.assertEqual([row["component_id"] for row in result], ["A"])

    def test_catalog_validation_rejects_bad_bbox(self) -> None:
        rows = [{"component_id": "A", "category": "frame", "confidence": "medium", "bbox_x_mm": "0", "bbox_y_mm": "1", "bbox_z_mm": "1"}]
        issues = validate_catalog_rows(rows)
        self.assertEqual(issues[0]["issue"], "invalid_bbox")

    def test_build_and_validate_placement_plan(self) -> None:
        rows = [
            {"component_id": "A", "confidence": "high", "parent_assembly": "ROOT", "tx_mm": "1", "ty_mm": "2", "tz_mm": "3"},
            {"component_id": "B", "confidence": "low", "parent_assembly": "ROOT"},
        ]
        plan = build_placement_plan(rows)
        self.assertEqual(plan[0]["status"], "candidate")
        self.assertEqual(plan[1]["status"], "manual_review")
        self.assertEqual(validate_placement_rows(plan), [])

    def test_init_project_writes_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = init_project("demo", tmp)
            self.assertEqual(state["stage"], "initialized")
            self.assertTrue((Path(tmp) / "ir" / "cad_ir.json").exists())
            self.assertTrue((Path(tmp) / "graph" / "execution_graph.json").exists())


class ExampleDataTests(unittest.TestCase):
    def test_synthetic_catalog_is_valid(self) -> None:
        root = Path(__file__).resolve().parents[1]
        rows = read_csv(root / "examples" / "synthetic_component_catalog.csv")
        self.assertEqual(validate_catalog_rows(rows), [])

    def test_synthetic_placement_is_valid(self) -> None:
        root = Path(__file__).resolve().parents[1]
        rows = read_csv(root / "examples" / "synthetic_project" / "planning" / "placement_plan.csv")
        self.assertEqual(validate_placement_rows(rows), [])


if __name__ == "__main__":
    unittest.main()

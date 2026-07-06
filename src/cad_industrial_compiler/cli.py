from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import (
    CATALOG_FIELDS,
    PLACEMENT_FIELDS,
    build_placement_plan,
    create_ir,
    init_project,
    query_catalog,
    read_csv,
    read_json,
    validate_catalog_rows,
    validate_ir,
    validate_placement_rows,
    write_csv,
    write_json,
)


def print_summary(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def cmd_init(args: argparse.Namespace) -> None:
    state = init_project(args.project_id, args.root)
    print_summary({"project_id": state["project_id"], "root": args.root, "stage": state["stage"]})


def cmd_create_ir(args: argparse.Namespace) -> None:
    ir = create_ir(args.project_id, args.input, args.requirement)
    write_json(args.out, ir)
    print_summary({"out": args.out, "inputs": len(ir["inputs"])})


def cmd_query_catalog(args: argparse.Namespace) -> None:
    rows = read_csv(args.catalog)
    result = query_catalog(rows, category=args.category, contains=args.contains, min_confidence=args.min_confidence)
    if args.out:
        if args.out.endswith(".json"):
            write_json(args.out, {"count": len(result), "rows": result})
        else:
            fields = list(rows[0].keys()) if rows else CATALOG_FIELDS
            write_csv(args.out, result, fields)
    print_summary({"count": len(result), "catalog": args.catalog})


def cmd_build_plan(args: argparse.Namespace) -> None:
    rows = read_csv(args.selected)
    plan = build_placement_plan(rows, default_parent=args.default_parent)
    write_csv(args.out, plan, PLACEMENT_FIELDS)
    print_summary({"out": args.out, "placements": len(plan)})


def cmd_validate_catalog(args: argparse.Namespace) -> None:
    rows = read_csv(args.catalog)
    issues = validate_catalog_rows(rows)
    summary = {"catalog": args.catalog, "rows": len(rows), "issue_count": len(issues), "issues": issues}
    if args.out:
        write_json(args.out, summary)
    print_summary({key: summary[key] for key in ["catalog", "rows", "issue_count"]})


def cmd_validate_placement(args: argparse.Namespace) -> None:
    rows = read_csv(args.placement_plan)
    issues = validate_placement_rows(rows)
    summary = {"placement_plan": args.placement_plan, "rows": len(rows), "issue_count": len(issues), "issues": issues}
    if args.out:
        write_json(args.out, summary)
    print_summary({key: summary[key] for key in ["placement_plan", "rows", "issue_count"]})


def cmd_validate_ir(args: argparse.Namespace) -> None:
    ir = read_json(args.ir)
    issues = validate_ir(ir)
    summary = {"ir": args.ir, "issue_count": len(issues), "issues": issues}
    if args.out:
        write_json(args.out, summary)
    print_summary({"ir": args.ir, "issue_count": len(issues)})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile CAD industrial design work into deterministic planning artifacts.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a compiler project folder.")
    init.add_argument("--project-id", required=True)
    init.add_argument("--root", required=True)
    init.set_defaults(func=cmd_init)

    create = sub.add_parser("create-ir", help="Create a CAD IR skeleton.")
    create.add_argument("--project-id", required=True)
    create.add_argument("--out", required=True)
    create.add_argument("--input", action="append", default=[])
    create.add_argument("--requirement", action="append", default=[])
    create.set_defaults(func=cmd_create_ir)

    query = sub.add_parser("query-catalog", help="Query a component catalog.")
    query.add_argument("--catalog", required=True)
    query.add_argument("--category")
    query.add_argument("--contains")
    query.add_argument("--min-confidence", default="low")
    query.add_argument("--out")
    query.set_defaults(func=cmd_query_catalog)

    plan = sub.add_parser("build-plan", help="Build a placement plan from selected components.")
    plan.add_argument("--selected", required=True)
    plan.add_argument("--out", required=True)
    plan.add_argument("--default-parent", default="ROOT_ASSEMBLY")
    plan.set_defaults(func=cmd_build_plan)

    val_catalog = sub.add_parser("validate-catalog", help="Validate component catalog rows.")
    val_catalog.add_argument("--catalog", required=True)
    val_catalog.add_argument("--out")
    val_catalog.set_defaults(func=cmd_validate_catalog)

    val_plan = sub.add_parser("validate-placement", help="Validate placement plan rows.")
    val_plan.add_argument("--placement-plan", required=True)
    val_plan.add_argument("--out")
    val_plan.set_defaults(func=cmd_validate_placement)

    val_ir = sub.add_parser("validate-ir", help="Validate a CAD IR file.")
    val_ir.add_argument("--ir", required=True)
    val_ir.add_argument("--out")
    val_ir.set_defaults(func=cmd_validate_ir)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    Path.cwd()
    args.func(args)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path


TEXT_EXTENSIONS = {
    ".csv",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
    ".svg",
}

def join(*parts: str) -> str:
    return "".join(parts)


# Keep private markers out of this public source file while still scanning for
# them at runtime.
BLOCKED_PATTERNS = [
    join("C:", "\\", "Users", "\\"),
    join("D:", "\\", "1-Test"),
    join("D:", "\\", "3dmodel"),
    join("5", "MWh"),
    join("20", "MWh"),
    join("PA", "CK"),
    join("\u957f", "PA", "CK"),
    "\u50a8\u80fd",
    "\u96c6\u88c5\u7bb1",
    "\u6db2\u51b7",
    "\u535a\u65f6",
    "\u5e03\u57fa\u7eb3",
    "\u5ba2\u6237",
    "\u9879\u76ee\u540d\u79f0",
    join("TAU", "GAST"),
]


def should_scan(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return False
    parts = {part.lower() for part in path.parts}
    return not ({".git", "__pycache__", ".venv", "node_modules"} & parts)


def scan(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in root.rglob("*"):
        if not path.is_file() or not should_scan(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in BLOCKED_PATTERNS:
            if pattern in text:
                findings.append({"path": str(path.relative_to(root)), "pattern": pattern})
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan public repo text files for private project markers.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings = scan(root)
    if findings:
        print("Privacy scan failed:")
        for item in findings:
            print(f"- {item['path']}: {item['pattern']}")
        raise SystemExit(1)
    print("Privacy scan passed.")


if __name__ == "__main__":
    main()

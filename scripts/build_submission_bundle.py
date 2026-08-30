#!/usr/bin/env python3
"""Build deterministic Skill and plugin ZIP artifacts outside the source tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path


EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".qa",
    ".ruff_cache",
    ".validation-deps",
    ".venv",
    "__pycache__",
    "artifacts",
    "build",
    "dist",
    "env",
    "htmlcov",
    "output",
    "outputs",
    "regression-output",
    "reports",
    "venv",
}
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SKILL_ROOT = Path("skills/arabic-word-production")


def should_include(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    has_excluded_part = any(
        part in EXCLUDED_PARTS or part.endswith(".egg-info")
        for part in relative.parts
    )
    return path.is_file() and not has_excluded_part


def source_members(root: Path) -> list[Path]:
    return sorted((path for path in root.rglob("*") if should_include(path, root)), key=lambda item: item.as_posix())


def write_zip(destination: Path, members: list[tuple[Path, str]]) -> dict[str, object]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(members, key=lambda item: item[1])
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, member_name in ordered:
            info = zipfile.ZipInfo(member_name, date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    return {
        "path": str(destination),
        "members": [name for _, name in ordered],
        "bytes": destination.stat().st_size,
        "sha256": digest,
    }


def build_bundles(root: Path | str, output_dir: Path | str) -> dict[str, object]:
    source_root = Path(root).resolve()
    output_root = Path(output_dir).resolve()
    skill_root = source_root / SKILL_ROOT
    if not (skill_root / "SKILL.md").is_file():
        raise ValueError("skill source is missing SKILL.md")
    if not (source_root / ".codex-plugin/plugin.json").is_file():
        raise ValueError("plugin source is missing .codex-plugin/plugin.json")

    skill_members = [
        (path, path.relative_to(skill_root).as_posix())
        for path in source_members(skill_root)
    ]
    plugin_members = [
        (path, path.relative_to(source_root).as_posix())
        for path in source_members(source_root)
    ]
    bundles = {
        "skill": write_zip(output_root / "arabic-word-production-skill.zip", skill_members),
        "plugin": write_zip(output_root / "arabic-word-production-plugin.zip", plugin_members),
    }
    return {"root": str(source_root), "output_dir": str(output_root), "bundles": bundles}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Arabic Word Production submission bundles")
    parser.add_argument("output_dir", type=Path, help="directory outside the source tree for ZIP artifacts")
    parser.add_argument("root", type=Path, nargs="?", default=Path("."), help="repository root")
    args = parser.parse_args(argv)
    try:
        result = build_bundles(args.root, args.output_dir)
    except ValueError as error:
        parser.error(str(error))
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

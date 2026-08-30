#!/usr/bin/env python3
"""Build a disposable local marketplace without touching personal settings."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


PLUGIN_NAME = "arabic-word-production"
MARKETPLACE_NAME = "arabic-word-production-local"
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


def is_copyable(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return path.is_file() and not any(
        part in EXCLUDED_PARTS or part.endswith(".egg-info")
        for part in relative.parts
    )


def build_marketplace(root: Path | str, destination: Path | str) -> dict[str, object]:
    source_root = Path(root).resolve()
    marketplace_root = Path(destination).resolve()
    manifest_path = source_root / ".codex-plugin/plugin.json"
    if not manifest_path.is_file():
        raise ValueError("plugin source is missing .codex-plugin/plugin.json")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("plugin manifest is not readable JSON") from error
    if manifest.get("name") != PLUGIN_NAME:
        raise ValueError("plugin manifest name does not match the canonical plugin name")
    if marketplace_root.exists() and any(marketplace_root.iterdir()):
        raise ValueError("destination must be absent or empty")

    plugin_root = marketplace_root / "plugins" / PLUGIN_NAME
    copied: list[str] = []
    for source in sorted(source_root.rglob("*"), key=lambda item: item.as_posix()):
        if not is_copyable(source, source_root):
            continue
        relative = source.relative_to(source_root)
        target = plugin_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(relative.as_posix())

    catalog = {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": "Arabic Word Production Local"},
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }
        ],
    }
    catalog_path = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "marketplace_root": str(marketplace_root),
        "catalog_path": str(catalog_path),
        "plugin_root": str(plugin_root),
        "files_copied": len(copied),
        "members": copied,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a disposable Arabic Word Production marketplace")
    parser.add_argument("destination", type=Path, help="new or empty marketplace directory")
    parser.add_argument("root", type=Path, nargs="?", default=Path("."), help="plugin repository root")
    args = parser.parse_args(argv)
    try:
        result = build_marketplace(args.root, args.destination)
    except ValueError as error:
        parser.error(str(error))
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

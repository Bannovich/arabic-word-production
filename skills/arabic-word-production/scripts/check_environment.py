#!/usr/bin/env python3
"""Report local prerequisites without changing the current environment."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Callable


REQUIRED_MODULES = ("docx", "lxml")
OPTIONAL_RENDERERS = ("soffice",)


def _default_module_finder(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _default_word_desktop_finder() -> bool:
    if shutil.which("WINWORD.EXE") or shutil.which("winword"):
        return True
    program_roots = (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"))
    suffix = Path("Microsoft Office/root/Office16/WINWORD.EXE")
    return any(root and (Path(root) / suffix).is_file() for root in program_roots)


def inspect_environment(
    module_finder: Callable[[str], bool] = _default_module_finder,
    executable_finder: Callable[[str], str | None] = shutil.which,
    word_desktop_finder: Callable[[], bool] = _default_word_desktop_finder,
) -> dict[str, object]:
    required_modules = {name: bool(module_finder(name)) for name in REQUIRED_MODULES}
    missing_required_modules = [name for name, available in required_modules.items() if not available]
    optional_renderers = {name: bool(executable_finder(name)) for name in OPTIONAL_RENDERERS}
    return {
        "python_version": ".".join(map(str, sys.version_info[:3])),
        "required_modules": required_modules,
        "missing_required_modules": missing_required_modules,
        "optional_renderers": optional_renderers,
        "word_desktop_available": bool(word_desktop_finder()),
        "ready_for_structural_route": not missing_required_modules,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect Arabic Word Production prerequisites")
    parser.parse_args(argv)
    json.dump(inspect_environment(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

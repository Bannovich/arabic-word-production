from __future__ import annotations

import argparse
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import shutil
import time

from docx import Document


SCRIPT_DIR = Path(__file__).resolve().parent


def _load_sibling(name: str):
    path = SCRIPT_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"arabic_word_{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def run_suite(model_path: str | Path, output_dir: str | Path) -> dict:
    model_source = Path(model_path)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    docx_path = destination / "synthetic-regression.docx"
    reopen_path = destination / "synthetic-regression-reopen.docx"

    loader = _load_sibling("doc_model")
    builder = _load_sibling("build_docx")
    auditor = _load_sibling("audit_docx")
    source_model = loader.load_model(model_source)

    started_at = datetime.now().astimezone().isoformat()
    started = time.perf_counter()
    builder.build_document(source_model, docx_path)
    original = auditor.audit_docx(docx_path, source_model)

    Document(docx_path).save(reopen_path)
    reopened = auditor.audit_docx(reopen_path, source_model)
    reopen_stable = (
        original["passed"] == reopened["passed"]
        and original["findings"] == reopened["findings"]
        and original["metrics"] == reopened["metrics"]
    )
    elapsed = round(time.perf_counter() - started, 3)
    ended_at = datetime.now().astimezone().isoformat()
    qa_failures = [finding["id"] for finding in original["findings"]]
    if not reopen_stable:
        qa_failures.append("ERR-REOPEN-001")

    result = {
        "passed": original["passed"] and reopened["passed"] and reopen_stable,
        "route": "COMPLEX",
        "started_at": started_at,
        "ended_at": ended_at,
        "elapsed_seconds": elapsed,
        "builds": 1,
        "repairs": 0,
        "fallbacks": 0,
        "qa_failures": qa_failures,
        "docx": str(docx_path),
        "reopen_docx": str(reopen_path),
        "reopen_stable": reopen_stable,
        "content_model_checked": True,
        "structural_audit": original,
        "reopen_audit": reopened,
        "renderer": "available" if shutil.which("soffice") else "unavailable",
        "word_desktop_tested": False,
    }
    (destination / "regression-results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Build, audit, and reopen-check a document fixture")
    parser.add_argument("model", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    result = run_suite(args.model, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["run_suite"]

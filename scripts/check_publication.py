#!/usr/bin/env python3
"""Check repository structure and public-release privacy invariants.

The JSON result intentionally reports categories and relative paths without
echoing matched values. This makes the checker suitable for CI logs that may be
public.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Iterable


REQUIRED_PATHS = (
    ".codex-plugin/plugin.json",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/image-object.yml",
    ".github/ISSUE_TEMPLATE/improvement.yml",
    ".github/ISSUE_TEMPLATE/performance.yml",
    ".github/ISSUE_TEMPLATE/rtl-rendering.yml",
    ".github/ISSUE_TEMPLATE/table-layout.yml",
    ".github/pull_request_template.md",
    ".github/workflows/quality.yml",
    ".gitignore",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "NOTICE",
    "README.ar.md",
    "README.md",
    "ROADMAP.md",
    "SECURITY.md",
    "SUPPORT.md",
    "docs/adding-a-guardrail.md",
    "docs/architecture-decisions.md",
    "docs/compatibility-matrix.md",
    "docs/how-it-was-built.md",
    "docs/index.md",
    "docs/plugin-directory-submission.md",
    "docs/privacy-policy.md",
    "docs/privacy-and-test-data.md",
    "docs/release-process.md",
    "docs/terms-of-service.md",
    "pyproject.toml",
    "scripts/check_publication.py",
    "scripts/check_plugin_submission.py",
    "scripts/generate_plugin_assets.py",
    "scripts/build_local_marketplace.py",
    "scripts/build_submission_bundle.py",
    "submission/availability.md",
    "submission/listing.ar.md",
    "submission/listing.en.md",
    "submission/release-notes.md",
    "submission/reviewer-tests.json",
    "tests/test_plugin_assets.py",
    "tests/test_plugin_submission.py",
    "tests/test_local_marketplace.py",
    "tests/test_submission_bundle.py",
    "skills/arabic-word-production/SKILL.md",
    "skills/arabic-word-production/agents/openai.yaml",
    "tests/test_publication.py",
)

EXCLUDED_DIRECTORIES = {
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

TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".css",
    ".csv",
    ".gitignore",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".rst",
    ".sh",
    ".toml",
    ".ts",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

ALLOWED_OFFICE_IDENTITIES = {
    "",
    "arabic word production",
    "bannovich",
    "python-docx",
}

EMAIL_RE = re.compile(
    r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])"
)

SENSITIVE_PATTERNS = (
    (
        "conversation-reference",
        re.compile(r"chatgpt" + r"-conversation://[^\s)`>\]]+", re.IGNORECASE),
        "private conversation reference detected",
    ),
    (
        "conversation-identifier",
        re.compile(
            r"[\"']?conversation" + r"Id[\"']?\s*[:=]\s*[\"'][^\"']+[\"']",
            re.IGNORECASE,
        ),
        "private conversation identifier field detected",
    ),
    (
        "user-profile-path",
        re.compile(r"(?<![\w])(?:[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+|/(?:Users|home)/[^/\s]+)"),
        "absolute user-profile path detected",
    ),
    (
        "private-key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?" + r"PRIVATE KEY-----"),
        "private-key marker detected",
    ),
    (
        "credential-token",
        re.compile(
            r"(?:\bsk-(?:proj|live|test)-[A-Za-z0-9_-]{8,}"
            r"|\bgh" + r"p_[A-Za-z0-9]{20,}"
            r"|\bgithub" + r"_pat_[A-Za-z0-9_]{20,}"
            r"|\bAK" + r"IA[0-9A-Z]{16}"
            r"|\bxox" + r"[baprs]-[A-Za-z0-9-]{10,}"
            r"|\bBearer\s+[A-Za-z0-9._~-]{20,})"
        ),
        "credential-like token detected",
    ),
)

UNFINISHED_PATTERNS = (
    re.compile(r"\[\s*TODO\s*:[^\]]*\]", re.IGNORECASE),
    re.compile(r"\[\s*INSERT\s+[^\]]*\]", re.IGNORECASE),
    re.compile(r"\bCHANGE" + r"ME\b", re.IGNORECASE),
    re.compile(r"\byour[-_ ](?:name|email|url)[-_ ]here\b", re.IGNORECASE),
)

STALE_PUBLICATION_PATTERNS = (
    (
        "README.md",
        re.compile(r"\bUntil the repository " + r"is public\b", re.IGNORECASE),
    ),
    (
        "README.ar.md",
        re.compile(r"قبل ما الـRepository يبقى " + r"Public", re.IGNORECASE),
    ),
)


def _finding(category: str, path: str, detail: str) -> dict[str, str]:
    return {"category": category, "path": path, "detail": detail}


def _is_excluded(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in EXCLUDED_DIRECTORIES for part in parts)


def _iter_repository_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if path.is_file() and not _is_excluded(path, root):
            yield path


def _allowed_email(address: str) -> bool:
    normalized = address.casefold()
    return normalized.endswith("@users.noreply.github.com") or normalized == "noreply@github.com"


def _scan_text(text: str, relative_path: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for category, pattern, detail in SENSITIVE_PATTERNS:
        if pattern.search(text):
            findings.append(_finding(category, relative_path, detail))

    if any(pattern.search(text) for pattern in UNFINISHED_PATTERNS):
        findings.append(
            _finding("unfinished-placeholder", relative_path, "unfinished scaffold marker detected")
        )

    if any(
        relative_path == expected_path and pattern.search(text)
        for expected_path, pattern in STALE_PUBLICATION_PATTERNS
    ):
        findings.append(
            _finding(
                "stale-publication-state",
                relative_path,
                "private-to-public transition wording detected",
            )
        )

    if any(not _allowed_email(match.group(0)) for match in EMAIL_RE.finditer(text)):
        findings.append(_finding("email-address", relative_path, "non-no-reply email detected"))
    return findings


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _scan_docx(path: Path, relative_path: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    try:
        with zipfile.ZipFile(path) as package:
            try:
                core_xml = package.read("docProps/core.xml")
            except KeyError:
                return [
                    _finding(
                        "office-core-properties-missing",
                        relative_path,
                        "DOCX has no core-properties part",
                    )
                ]
    except (OSError, zipfile.BadZipFile):
        return [_finding("docx-package-invalid", relative_path, "DOCX package is not readable")]

    try:
        root = ET.fromstring(core_xml)
    except ET.ParseError:
        return [
            _finding(
                "office-core-properties-invalid",
                relative_path,
                "DOCX core-properties XML is invalid",
            )
        ]

    all_text: list[str] = []
    for element in root.iter():
        value = (element.text or "").strip()
        if not value:
            continue
        all_text.append(value)
        if _local_name(element.tag) in {"creator", "lastModifiedBy"}:
            if value.casefold() not in ALLOWED_OFFICE_IDENTITIES:
                findings.append(
                    _finding(
                        "office-metadata",
                        relative_path,
                        "DOCX contains non-generic creator or editor metadata",
                    )
                )

    findings.extend(_scan_text("\n".join(all_text), relative_path))
    return findings


def _scan_manifest(root: Path) -> list[dict[str, str]]:
    path = root / ".codex-plugin" / "plugin.json"
    if not path.is_file():
        return []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [
            _finding("plugin-manifest-invalid", ".codex-plugin/plugin.json", "manifest is not valid JSON")
        ]

    expected = {
        "name": "arabic-word-production",
        "version": "0.1.0",
        "license": "Apache-2.0",
        "skills": "./skills/",
    }
    findings: list[dict[str, str]] = []
    for field, value in expected.items():
        if manifest.get(field) != value:
            findings.append(
                _finding(
                    "plugin-manifest-mismatch",
                    ".codex-plugin/plugin.json",
                    f"manifest field {field} does not match release metadata",
                )
            )
    return findings


def scan_repository(root: Path | str) -> dict[str, object]:
    repository = Path(root).resolve()
    findings: list[dict[str, str]] = []

    for relative in REQUIRED_PATHS:
        if not (repository / relative).is_file():
            findings.append(
                _finding("required-path-missing", relative, "required publication path is missing")
            )

    findings.extend(_scan_manifest(repository))

    files_scanned = 0
    docx_scanned = 0
    for path in _iter_repository_files(repository):
        relative = path.relative_to(repository).as_posix()
        files_scanned += 1
        if path.suffix.casefold() == ".docx":
            docx_scanned += 1
            findings.extend(_scan_docx(path, relative))
            continue
        if path.suffix.casefold() not in TEXT_SUFFIXES and path.name not in {"LICENSE", "NOTICE"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            findings.append(_finding("file-unreadable", relative, "file could not be read"))
            continue
        findings.extend(_scan_text(text, relative))

    unique_findings: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for item in sorted(findings, key=lambda value: (value["path"], value["category"], value["detail"])):
        key = (item["category"], item["path"], item["detail"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(item)

    return {
        "ok": not unique_findings,
        "root": ".",
        "files_scanned": files_scanned,
        "docx_scanned": docx_scanned,
        "finding_count": len(unique_findings),
        "findings": unique_findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Arabic Word Production publication structure and privacy invariants"
    )
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    args = parser.parse_args(argv)
    result = scan_repository(args.root)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

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
    ".gitattributes",
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
    "release-evidence/plugin-directory-candidate.json",
    "release-evidence/plugin-directory-fresh-task-smoke.json",
    "release-evidence/plugin-directory-publication.json",
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

FRESH_TASK_EVIDENCE_PATH = "release-evidence/plugin-directory-fresh-task-smoke.json"


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


def _is_nonnegative_number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and value >= 0


def _is_nonnegative_integer(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value >= 0


def _scan_fresh_task_evidence(root: Path) -> list[dict[str, str]]:
    path = root / FRESH_TASK_EVIDENCE_PATH
    if not path.is_file():
        return []
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [
            _finding(
                "fresh-task-evidence-invalid",
                FRESH_TASK_EVIDENCE_PATH,
                "fresh-task evidence is not readable JSON",
            )
        ]

    try:
        candidate = evidence["candidate"]
        fresh_task = evidence["fresh_task"]
        timing = evidence["timing"]
        target = timing["under_120_second_target"]
        verification = evidence["verification"]
        accessibility = verification["accessibility_findings"]
        integrity = evidence["artifact_integrity"]
        surface = evidence["validation_surface"]
        portal = evidence["openai_portal_state"]

        task_turn = timing["task_turn_seconds"]
        pipeline = timing["pipeline_model_preparation_through_final_audit_seconds"]
        build = timing["build_seconds"]
        installed_files = fresh_task["installed_plugin_files"]
        candidate_files = fresh_task["candidate_bundle_files"]
        rendered_pages = surface["rendered_pages"]
        inspected_pages = surface["inspected_pages"]
        expected_user_claim = "met" if task_turn < 120 else "not-met"
        integrity_digests = (
            integrity["candidate_plugin_bundle_sha256"],
            integrity["generated_docx_sha256"],
            integrity["synthetic_model_sha256"],
            integrity["independent_reopen_docx_sha256"],
        )

        valid = all(
            (
                evidence.get("schema_version") == 1,
                isinstance(candidate, dict),
                isinstance(fresh_task, dict),
                isinstance(timing, dict),
                isinstance(target, dict),
                isinstance(verification, dict),
                isinstance(accessibility, dict),
                isinstance(integrity, dict),
                isinstance(surface, dict),
                isinstance(portal, dict),
                bool(re.fullmatch(r"[0-9a-f]{40}", candidate["validated_parent_commit"])),
                bool(re.fullmatch(r"[0-9a-f]{40}", candidate["evidence_commit"])),
                candidate["package_version"] == "0.1.0",
                candidate["submission_type"] == "skills-only",
                candidate["license"] == "Apache-2.0",
                candidate["plugin_id"]
                == "arabic-word-production@arabic-word-production-local",
                candidate["qualified_skill_name"]
                == "arabic-word-production:arabic-word-production",
                fresh_task["passed"] is True,
                fresh_task["clean_room"] is True,
                fresh_task["route"] in {"FAST", "STRUCTURED", "COMPLEX"},
                fresh_task["synthetic_only"] is True,
                fresh_task["source_repository_worktree_used"] is False,
                fresh_task["plugin_runtime_matches_installed_copy"] is True,
                _is_nonnegative_integer(installed_files) and installed_files > 0,
                _is_nonnegative_integer(candidate_files) and candidate_files > 0,
                installed_files == candidate_files,
                fresh_task["candidate_bundle_file_mismatches"] == 0,
                _is_nonnegative_number(task_turn),
                _is_nonnegative_number(pipeline),
                _is_nonnegative_number(build),
                build <= pipeline <= task_turn,
                target["task_turn"] is (task_turn < 120),
                target["pipeline_only"] is (pipeline < 120),
                target["user_visible_claim"] == expected_user_claim,
                verification["structural_finding_count"] == 0,
                verification["reopen_finding_count"] == 0,
                verification["supplemental_checks_passed"]
                == verification["supplemental_checks_total"],
                verification["supplemental_checks_total"] > 0,
                verification["reopen_supplemental_checks_passed"]
                == verification["reopen_supplemental_checks_total"],
                verification["reopen_supplemental_checks_total"] > 0,
                verification["metrics_identical_after_reopen"] is True,
                accessibility == {"high": 0, "medium": 0, "low": 0},
                all(bool(re.fullmatch(r"[0-9a-f]{64}", digest)) for digest in integrity_digests),
                isinstance(integrity["independent_reopen_byte_identical"], bool),
                integrity["independent_reopen_structurally_equivalent"] is True,
                surface["renderer_attempted"] is True,
                isinstance(surface["renderer_available"], bool),
                isinstance(rendered_pages, int) and rendered_pages >= 0,
                isinstance(inspected_pages, int) and inspected_pages >= 0,
                isinstance(surface["word_desktop_tested"], bool),
                portal
                == {
                    "developer_identity_action_attempted": False,
                    "policy_attestations_attempted": False,
                    "submit_for_review_attempted": False,
                    "publish_attempted": False,
                },
            )
        )
        if surface["renderer_available"]:
            valid = valid and rendered_pages > 0 and inspected_pages == rendered_pages
        else:
            valid = (
                valid
                and rendered_pages == 0
                and inspected_pages == 0
                and surface["claim"] == "structural-and-accessibility-only"
            )
    except (KeyError, TypeError, ValueError):
        valid = False

    if valid:
        return []
    return [
        _finding(
            "fresh-task-evidence-invalid",
            FRESH_TASK_EVIDENCE_PATH,
            "fresh-task evidence does not satisfy the publication contract",
        )
    ]


def scan_repository(root: Path | str) -> dict[str, object]:
    repository = Path(root).resolve()
    findings: list[dict[str, str]] = []

    for relative in REQUIRED_PATHS:
        if not (repository / relative).is_file():
            findings.append(
                _finding("required-path-missing", relative, "required publication path is missing")
            )

    findings.extend(_scan_manifest(repository))
    findings.extend(_scan_fresh_task_evidence(repository))

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

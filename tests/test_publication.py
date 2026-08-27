from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPOSITORY_ROOT / "scripts" / "check_publication.py"

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
    "docs/privacy-and-test-data.md",
    "docs/release-process.md",
    "pyproject.toml",
    "scripts/check_publication.py",
    "skills/arabic-word-production/SKILL.md",
    "skills/arabic-word-production/agents/openai.yaml",
    "tests/test_publication.py",
)


def load_checker():
    if not CHECKER_PATH.is_file():
        raise AssertionError(f"publication checker is missing: {CHECKER_PATH}")
    spec = importlib.util.spec_from_file_location("publication_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load publication checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_docx(path: Path, creator: str = "python-docx", last_modified_by: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    core_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties
 xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/">
 <dc:creator>{creator}</dc:creator>
 <cp:lastModifiedBy>{last_modified_by}</cp:lastModifiedBy>
</cp:coreProperties>"""
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("docProps/core.xml", core_xml)


class PublicationCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        for relative in REQUIRED_PATHS:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("safe synthetic content\n", encoding="utf-8")

        (self.root / ".codex-plugin/plugin.json").write_text(
            json.dumps(
                {
                    "name": "arabic-word-production",
                    "version": "0.1.0",
                    "description": "Safe synthetic plugin",
                    "author": {
                        "name": "Bannovich",
                        "email": "73133823+Bannovich@users.noreply.github.com",
                    },
                    "license": "Apache-2.0",
                    "skills": "./skills/",
                    "interface": {
                        "displayName": "Arabic Word Production",
                        "shortDescription": "Synthetic validation fixture",
                    },
                }
            ),
            encoding="utf-8",
        )

    def scan(self):
        return load_checker().scan_repository(self.root)

    def assert_category(self, result, category: str) -> None:
        self.assertFalse(result["ok"])
        self.assertIn(category, {item["category"] for item in result["findings"]})

    def test_minimal_clean_repository_passes(self) -> None:
        result = self.scan()
        self.assertTrue(result["ok"], result["findings"])
        self.assertEqual([], result["findings"])

    def test_missing_required_file_is_reported(self) -> None:
        (self.root / "NOTICE").unlink()
        self.assert_category(self.scan(), "required-path-missing")

    def test_chat_conversation_reference_is_reported(self) -> None:
        scheme = "chatgpt" + "-conversation://"
        (self.root / "notes.md").write_text(scheme + "private-reference", encoding="utf-8")
        self.assert_category(self.scan(), "conversation-reference")

    def test_conversation_identifier_field_is_reported(self) -> None:
        field = "conversation" + "Id"
        (self.root / "notes.json").write_text(
            json.dumps({field: "private-reference"}), encoding="utf-8"
        )
        self.assert_category(self.scan(), "conversation-identifier")

    def test_windows_user_profile_path_is_reported(self) -> None:
        private_path = "C:" + "\\Users\\" + "SampleUser\\private.docx"
        (self.root / "notes.md").write_text(private_path, encoding="utf-8")
        self.assert_category(self.scan(), "user-profile-path")

    def test_private_key_marker_is_reported(self) -> None:
        marker = "-----BEGIN " + "PRIVATE KEY-----"
        (self.root / "notes.txt").write_text(marker, encoding="utf-8")
        self.assert_category(self.scan(), "private-key")

    def test_token_prefix_is_reported_without_echoing_secret(self) -> None:
        token = "gh" + "p_" + "A" * 36
        (self.root / "notes.txt").write_text(token, encoding="utf-8")
        result = self.scan()
        self.assert_category(result, "credential-token")
        self.assertNotIn(token, json.dumps(result))

    def test_non_noreply_email_is_reported(self) -> None:
        email = "person" + "@example.com"
        (self.root / "notes.md").write_text(email, encoding="utf-8")
        self.assert_category(self.scan(), "email-address")

    def test_github_noreply_email_is_allowed(self) -> None:
        (self.root / "notes.md").write_text(
            "73133823+Bannovich@users.noreply.github.com", encoding="utf-8"
        )
        self.assertTrue(self.scan()["ok"])

    def test_office_core_identity_metadata_is_reported(self) -> None:
        creator = "Private Person"
        email = "private" + "@example.com"
        write_docx(self.root / "fixture.docx", creator=creator, last_modified_by=email)
        result = self.scan()
        self.assert_category(result, "office-metadata")
        serialized = json.dumps(result)
        self.assertNotIn(creator, serialized)
        self.assertNotIn(email, serialized)

    def test_generic_python_docx_metadata_is_allowed(self) -> None:
        write_docx(self.root / "fixture.docx")
        self.assertTrue(self.scan()["ok"])


if __name__ == "__main__":
    unittest.main()

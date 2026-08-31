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
        (self.root / "release-evidence/plugin-directory-fresh-task-smoke.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "candidate": {
                        "validated_parent_commit": "0" * 40,
                        "evidence_commit": "1" * 40,
                        "package_version": "0.1.0",
                        "submission_type": "skills-only",
                        "license": "Apache-2.0",
                        "plugin_id": "arabic-word-production@arabic-word-production-local",
                        "qualified_skill_name": "arabic-word-production:arabic-word-production",
                    },
                    "fresh_task": {
                        "passed": True,
                        "clean_room": True,
                        "route": "COMPLEX",
                        "synthetic_only": True,
                        "source_repository_worktree_used": False,
                        "plugin_runtime_matches_installed_copy": True,
                        "installed_plugin_files": 77,
                        "candidate_bundle_files": 77,
                        "candidate_bundle_file_mismatches": 0,
                    },
                    "timing": {
                        "task_turn_seconds": 100.0,
                        "pipeline_model_preparation_through_final_audit_seconds": 1.0,
                        "build_seconds": 0.5,
                        "under_120_second_target": {
                            "task_turn": True,
                            "pipeline_only": True,
                            "user_visible_claim": "met",
                        },
                    },
                    "verification": {
                        "structural_finding_count": 0,
                        "reopen_finding_count": 0,
                        "supplemental_checks_passed": 13,
                        "supplemental_checks_total": 13,
                        "reopen_supplemental_checks_passed": 13,
                        "reopen_supplemental_checks_total": 13,
                        "metrics_identical_after_reopen": True,
                        "accessibility_findings": {"high": 0, "medium": 0, "low": 0},
                    },
                    "artifact_integrity": {
                        "candidate_plugin_bundle_sha256": "2" * 64,
                        "generated_docx_sha256": "3" * 64,
                        "synthetic_model_sha256": "4" * 64,
                        "independent_reopen_docx_sha256": "5" * 64,
                        "independent_reopen_byte_identical": False,
                        "independent_reopen_structurally_equivalent": True,
                    },
                    "validation_surface": {
                        "renderer_attempted": True,
                        "renderer_available": False,
                        "rendered_pages": 0,
                        "inspected_pages": 0,
                        "word_desktop_tested": False,
                        "claim": "structural-and-accessibility-only",
                    },
                    "openai_portal_state": {
                        "developer_identity_action_attempted": False,
                        "policy_attestations_attempted": False,
                        "submit_for_review_attempted": False,
                        "publish_attempted": False,
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

    def test_fresh_task_evidence_requires_full_turn_timing(self) -> None:
        path = self.root / "release-evidence/plugin-directory-fresh-task-smoke.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        del evidence["timing"]["task_turn_seconds"]
        path.write_text(json.dumps(evidence), encoding="utf-8")
        self.assert_category(self.scan(), "fresh-task-evidence-invalid")

    def test_fresh_task_evidence_rejects_pipeline_only_latency_claim(self) -> None:
        path = self.root / "release-evidence/plugin-directory-fresh-task-smoke.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["timing"]["task_turn_seconds"] = 767.617
        evidence["timing"]["under_120_second_target"]["task_turn"] = True
        path.write_text(json.dumps(evidence), encoding="utf-8")
        self.assert_category(self.scan(), "fresh-task-evidence-invalid")

    def test_fresh_task_evidence_requires_a_passing_plugin_invocation(self) -> None:
        path = self.root / "release-evidence/plugin-directory-fresh-task-smoke.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["fresh_task"]["passed"] = False
        path.write_text(json.dumps(evidence), encoding="utf-8")
        self.assert_category(self.scan(), "fresh-task-evidence-invalid")

    def test_fresh_task_evidence_cannot_claim_rendered_pages_without_renderer(self) -> None:
        path = self.root / "release-evidence/plugin-directory-fresh-task-smoke.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["validation_surface"]["rendered_pages"] = 1
        evidence["validation_surface"]["inspected_pages"] = 1
        path.write_text(json.dumps(evidence), encoding="utf-8")
        self.assert_category(self.scan(), "fresh-task-evidence-invalid")

    def test_fresh_task_evidence_requires_an_honest_user_visible_claim(self) -> None:
        path = self.root / "release-evidence/plugin-directory-fresh-task-smoke.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["timing"]["under_120_second_target"]["user_visible_claim"] = "not-met"
        path.write_text(json.dumps(evidence), encoding="utf-8")
        self.assert_category(self.scan(), "fresh-task-evidence-invalid")

    def test_fresh_task_evidence_rejects_candidate_file_mismatches(self) -> None:
        path = self.root / "release-evidence/plugin-directory-fresh-task-smoke.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["fresh_task"]["candidate_bundle_file_mismatches"] = 1
        path.write_text(json.dumps(evidence), encoding="utf-8")
        self.assert_category(self.scan(), "fresh-task-evidence-invalid")

    def test_fresh_task_evidence_requires_reopen_and_integrity_proof(self) -> None:
        path = self.root / "release-evidence/plugin-directory-fresh-task-smoke.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        del evidence["verification"]["reopen_supplemental_checks_passed"]
        evidence["artifact_integrity"]["generated_docx_sha256"] = "not-a-digest"
        path.write_text(json.dumps(evidence), encoding="utf-8")
        self.assert_category(self.scan(), "fresh-task-evidence-invalid")

    def test_fresh_task_evidence_cannot_claim_portal_actions(self) -> None:
        path = self.root / "release-evidence/plugin-directory-fresh-task-smoke.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["openai_portal_state"]["submit_for_review_attempted"] = True
        path.write_text(json.dumps(evidence), encoding="utf-8")
        self.assert_category(self.scan(), "fresh-task-evidence-invalid")

    def test_english_private_visibility_scaffold_language_is_reported(self) -> None:
        stale_text = "Until the repository " + "is public, use the local folder."
        (self.root / "README.md").write_text(stale_text, encoding="utf-8")
        self.assert_category(self.scan(), "stale-publication-state")

    def test_arabic_private_visibility_scaffold_language_is_reported(self) -> None:
        stale_text = "قبل ما الـRepository يبقى " + "Public، استخدم المجلد المحلي."
        (self.root / "README.ar.md").write_text(stale_text, encoding="utf-8")
        self.assert_category(self.scan(), "stale-publication-state")

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

    def test_pep639_license_expression_does_not_repeat_legacy_classifier(self) -> None:
        pyproject = (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('license = "Apache-2.0"', pyproject)
        self.assertNotIn(
            '"License :: OSI Approved :: Apache Software License"',
            pyproject,
            "Setuptools 77+ rejects a PEP 639 license expression combined with the legacy license classifier",
        )


if __name__ == "__main__":
    unittest.main()

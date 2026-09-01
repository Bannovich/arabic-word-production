from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPOSITORY_ROOT / "scripts" / "check_plugin_submission.py"


def load_checker():
    if not CHECKER_PATH.is_file():
        raise AssertionError(f"submission checker is missing: {CHECKER_PATH}")
    spec = importlib.util.spec_from_file_location("plugin_submission_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load plugin submission checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PluginSubmissionCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.write_clean_fixture()

    def write_clean_fixture(self) -> None:
        manifest = {
            "name": "arabic-word-production",
            "version": "0.2.0",
            "license": "Apache-2.0",
            "skills": "./skills/",
            "interface": {
                "displayName": "Arabic Word Production",
                "shortDescription": "Audited Arabic Word files",
                "longDescription": "Create, repair, and audit Arabic-first and bilingual Word documents with explicit RTL controls.",
                "websiteURL": "https://example.test/project",
                "privacyPolicyURL": "https://example.test/privacy",
                "termsOfServiceURL": "https://example.test/terms",
                "logo": "./assets/logo.png",
                "composerIcon": "./assets/icon.png",
                "defaultPrompt": [
                    "Create and audit an Arabic RTL Word document from this content.",
                    "Repair the RTL structure in this Arabic-English DOCX.",
                    "Audit this Arabic Word file and report its actual validation surface.",
                ],
            },
        }
        self.write_json(".codex-plugin/plugin.json", manifest)
        square_png = (REPOSITORY_ROOT / "assets" / "icon.png").read_bytes()
        for asset in ("assets/logo.png", "assets/icon.png"):
            self.write_bytes(asset, square_png)
        self.write_text("submission/listing.en.md", "Arabic Word Production\n")
        self.write_text("submission/listing.ar.md", "Arabic Word Production\n")
        self.write_text("submission/availability.md", "Available wherever the plugin directory is available.\n")
        self.write_text("submission/release-notes.md", "Initial directory submission.\n")
        cases = {"positive": [self.case("positive", number) for number in range(5)], "negative": [self.case("negative", number) for number in range(3)]}
        self.write_json("submission/reviewer-tests.json", cases)

    @staticmethod
    def case(kind: str, number: int) -> dict[str, str]:
        return {
            "id": f"{kind}-{number + 1}",
            "prompt": f"Synthetic {kind} case {number + 1}",
            "expected": "A safe, specific and truthful result.",
        }

    def write_text(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_bytes(self, relative: str, content: bytes) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def write_json(self, relative: str, content: object) -> None:
        self.write_text(relative, json.dumps(content, ensure_ascii=False, indent=2))

    def scan(self) -> dict[str, object]:
        return load_checker().scan_submission(self.root)

    def assert_category(self, result: dict[str, object], category: str) -> None:
        self.assertFalse(result["ok"])
        findings = result["findings"]
        self.assertIn(category, {item["category"] for item in findings})

    def test_clean_submission_passes(self) -> None:
        result = self.scan()
        self.assertTrue(result["ok"], result["findings"])

    def test_display_name_over_30_characters_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["interface"]["displayName"] = "A" * 31
        self.write_json(".codex-plugin/plugin.json", manifest)
        self.assert_category(self.scan(), "display-name-too-long")

    def test_short_description_over_30_characters_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["interface"]["shortDescription"] = "A" * 31
        self.write_json(".codex-plugin/plugin.json", manifest)
        self.assert_category(self.scan(), "short-description-too-long")

    def test_more_than_three_starter_prompts_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["interface"]["defaultPrompt"].append("Fourth prompt")
        self.write_json(".codex-plugin/plugin.json", manifest)
        self.assert_category(self.scan(), "starter-prompt-count")

    def test_starter_prompt_over_128_characters_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["interface"]["defaultPrompt"][0] = "A" * 129
        self.write_json(".codex-plugin/plugin.json", manifest)
        self.assert_category(self.scan(), "starter-prompt-too-long")

    def test_duplicate_starter_prompt_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["interface"]["defaultPrompt"][1] = manifest["interface"]["defaultPrompt"][0]
        self.write_json(".codex-plugin/plugin.json", manifest)
        self.assert_category(self.scan(), "starter-prompt-duplicate")

    def test_mention_in_starter_prompt_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["interface"]["defaultPrompt"][0] = "Ask @ArabicWordProduction to make a DOCX"
        self.write_json(".codex-plugin/plugin.json", manifest)
        self.assert_category(self.scan(), "starter-prompt-mention")

    def test_non_https_policy_url_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["interface"]["privacyPolicyURL"] = "http://example.test/privacy"
        self.write_json(".codex-plugin/plugin.json", manifest)
        self.assert_category(self.scan(), "url-not-https")

    def test_missing_referenced_asset_is_rejected(self) -> None:
        (self.root / "assets/logo.png").unlink()
        self.assert_category(self.scan(), "asset-missing")

    def test_non_square_declared_logo_is_rejected(self) -> None:
        rectangular_logo = (REPOSITORY_ROOT / "assets" / "logo.png").read_bytes()
        self.write_bytes("assets/logo.png", rectangular_logo)
        self.assert_category(self.scan(), "asset-not-square")

    def test_reviewer_case_counts_must_be_five_positive_and_three_negative(self) -> None:
        self.write_json("submission/reviewer-tests.json", {"positive": [], "negative": []})
        result = self.scan()
        self.assert_category(result, "reviewer-positive-count")
        self.assert_category(result, "reviewer-negative-count")

    def test_invalid_reviewer_json_is_rejected(self) -> None:
        self.write_text("submission/reviewer-tests.json", "not json")
        self.assert_category(self.scan(), "reviewer-tests-invalid")

    def test_unfinished_placeholder_is_rejected(self) -> None:
        marker = "[" + "TODO" + ": write listing]"
        self.write_text("submission/listing.en.md", marker)
        self.assert_category(self.scan(), "unfinished-placeholder")

    def test_digital_commerce_language_is_rejected_without_echoing_text(self) -> None:
        forbidden = "Buy a paid subscription for this digital service"
        self.write_text("submission/listing.en.md", forbidden)
        result = self.scan()
        self.assert_category(result, "digital-commerce-language")
        self.assertNotIn(forbidden, json.dumps(result))

    def read_manifest(self) -> dict[str, object]:
        return json.loads((self.root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

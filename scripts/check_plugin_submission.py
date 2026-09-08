#!/usr/bin/env python3
"""Validate local, directory-facing plugin submission requirements.

The checker reports categories and relative paths only.  It deliberately does
not echo source text, prompts, URLs, or other values that could end up in a
public CI log.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, UnidentifiedImageError


MANIFEST_PATH = Path(".codex-plugin/plugin.json")
REQUIRED_SUBMISSION_FILES = (
    Path("submission/listing.en.md"),
    Path("submission/listing.ar.md"),
    Path("submission/reviewer-tests.json"),
    Path("submission/availability.md"),
    Path("submission/release-notes.md"),
)
PLACEHOLDER_RE = re.compile(
    r"\[\s*(?:TODO|INSERT)\b[^\]]*\]|\bCHANGE" + r"ME\b|\byour[-_ ](?:name|email|url)[-_ ]here\b",
    re.IGNORECASE,
)
COMMERCE_RE = re.compile(
    r"\b(?:buy|purchase|checkout|subscribe|subscription|paid plan|upgrade)\b",
    re.IGNORECASE,
)
MIN_IMAGE_EDGE = 48
MAX_IMAGE_EDGE = 4096
MAX_IMAGE_BYTES = 5 * 1024 * 1024


def finding(category: str, path: str, detail: str) -> dict[str, str]:
    return {"category": category, "path": path, "detail": detail}


def is_https_url(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def safe_asset_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with Image.open(path) as image:
            if image.format != "PNG":
                return None
            dimensions = image.size
            image.verify()
        if all(MIN_IMAGE_EDGE <= edge <= MAX_IMAGE_EDGE for edge in dimensions):
            with Image.open(path) as image:
                image.load()
    except (OSError, UnidentifiedImageError, SyntaxError, Image.DecompressionBombError):
        return None
    return dimensions


def file_sha256(path: Path) -> str | None:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        return None
    return digest.hexdigest()


def scan_text_file(path: Path, root: Path) -> list[dict[str, str]]:
    relative = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return [finding("submission-file-unreadable", relative, "submission file could not be read")]

    findings: list[dict[str, str]] = []
    if PLACEHOLDER_RE.search(text):
        findings.append(finding("unfinished-placeholder", relative, "unfinished placeholder found"))
    if COMMERCE_RE.search(text):
        findings.append(
            finding("digital-commerce-language", relative, "directory-facing commerce language found")
        )
    return findings


def scan_reviewer_tests(path: Path, root: Path) -> list[dict[str, str]]:
    relative = path.relative_to(root).as_posix()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [finding("reviewer-tests-invalid", relative, "reviewer test file is not valid JSON")]

    if not isinstance(value, dict):
        return [finding("reviewer-tests-invalid", relative, "reviewer test file must contain an object")]

    findings: list[dict[str, str]] = []
    positive = value.get("positive")
    negative = value.get("negative")
    if not isinstance(positive, list) or len(positive) != 5:
        findings.append(finding("reviewer-positive-count", relative, "exactly five positive cases are required"))
    if not isinstance(negative, list) or len(negative) != 3:
        findings.append(finding("reviewer-negative-count", relative, "exactly three negative cases are required"))

    for group_name, cases in (("positive", positive), ("negative", negative)):
        if not isinstance(cases, list):
            continue
        for index, case in enumerate(cases, start=1):
            if not isinstance(case, dict) or not all(
                isinstance(case.get(field), str) and case[field].strip()
                for field in ("id", "prompt", "expected")
            ):
                findings.append(
                    finding(
                        "reviewer-case-invalid",
                        relative,
                        f"{group_name} case {index} lacks the required shape",
                    )
                )
    return findings


def scan_submission(root: Path | str) -> dict[str, object]:
    root_path = Path(root).resolve()
    findings: list[dict[str, str]] = []
    validated_assets: dict[str, Path] = {}
    manifest_file = root_path / MANIFEST_PATH
    manifest: object = None
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        findings.append(finding("plugin-manifest-invalid", MANIFEST_PATH.as_posix(), "manifest is not valid JSON"))

    interface: object = {}
    if isinstance(manifest, dict):
        interface = manifest.get("interface", {})
    else:
        findings.append(finding("plugin-manifest-invalid", MANIFEST_PATH.as_posix(), "manifest must contain an object"))
    if not isinstance(interface, dict):
        findings.append(finding("plugin-interface-invalid", MANIFEST_PATH.as_posix(), "interface must contain an object"))
        interface = {}

    display_name = interface.get("displayName")
    if not isinstance(display_name, str) or not display_name.strip():
        findings.append(finding("display-name-missing", MANIFEST_PATH.as_posix(), "display name is required"))
    elif len(display_name) > 30:
        findings.append(finding("display-name-too-long", MANIFEST_PATH.as_posix(), "display name exceeds 30 characters"))

    short_description = interface.get("shortDescription")
    if not isinstance(short_description, str) or not short_description.strip():
        findings.append(finding("short-description-missing", MANIFEST_PATH.as_posix(), "short description is required"))
    elif len(short_description) > 30:
        findings.append(
            finding("short-description-too-long", MANIFEST_PATH.as_posix(), "short description exceeds 30 characters")
        )

    long_description = interface.get("longDescription")
    if isinstance(long_description, str) and len(long_description) > 4000:
        findings.append(finding("long-description-too-long", MANIFEST_PATH.as_posix(), "long description exceeds 4000 characters"))

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list):
        findings.append(finding("starter-prompt-shape", MANIFEST_PATH.as_posix(), "starter prompts must be a list"))
    else:
        if len(prompts) > 3:
            findings.append(finding("starter-prompt-count", MANIFEST_PATH.as_posix(), "at most three starter prompts are allowed"))
        normalized: set[str] = set()
        for prompt in prompts:
            if not isinstance(prompt, str) or not prompt.strip():
                findings.append(finding("starter-prompt-shape", MANIFEST_PATH.as_posix(), "starter prompt must be non-empty text"))
                continue
            if len(prompt) > 128:
                findings.append(finding("starter-prompt-too-long", MANIFEST_PATH.as_posix(), "starter prompt exceeds 128 characters"))
            normalized_prompt = " ".join(prompt.casefold().split())
            if normalized_prompt in normalized:
                findings.append(finding("starter-prompt-duplicate", MANIFEST_PATH.as_posix(), "starter prompts must be unique"))
            normalized.add(normalized_prompt)
            if "@" in prompt:
                findings.append(finding("starter-prompt-mention", MANIFEST_PATH.as_posix(), "starter prompt must not contain a mention"))

    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        if not is_https_url(interface.get(field)):
            findings.append(finding("url-not-https", MANIFEST_PATH.as_posix(), f"{field} must be an HTTPS URL"))
    for field in ("logo", "composerIcon", "logoDark"):
        if field == "logoDark" and field not in interface:
            continue
        asset = safe_asset_path(root_path, interface.get(field))
        if asset is None or not asset.is_file():
            findings.append(finding("asset-missing", MANIFEST_PATH.as_posix(), f"{field} must reference an in-repository file"))
            continue
        try:
            asset_size = asset.stat().st_size
        except OSError:
            findings.append(finding("asset-unreadable", MANIFEST_PATH.as_posix(), f"{field} could not be inspected"))
            continue
        if asset_size > MAX_IMAGE_BYTES:
            findings.append(finding("asset-too-large", MANIFEST_PATH.as_posix(), f"{field} must not exceed 5 MiB"))
            continue
        if asset.suffix.casefold() == ".png":
            dimensions = png_dimensions(asset)
            if dimensions is None:
                findings.append(finding("asset-unreadable", MANIFEST_PATH.as_posix(), f"{field} must reference a decodable PNG image"))
            else:
                width, height = dimensions
                if width != height:
                    findings.append(finding("asset-not-square", MANIFEST_PATH.as_posix(), f"{field} must reference a square image"))
                if not all(MIN_IMAGE_EDGE <= edge <= MAX_IMAGE_EDGE for edge in dimensions):
                    findings.append(finding("asset-dimensions-out-of-range", MANIFEST_PATH.as_posix(), f"{field} dimensions must be between 48 and 4096 pixels"))
                validated_assets[field] = asset

    logo_path = validated_assets.get("logo")
    composer_icon_path = validated_assets.get("composerIcon")
    if logo_path is not None and composer_icon_path is not None:
        logo_hash = file_sha256(logo_path)
        composer_icon_hash = file_sha256(composer_icon_path)
        if logo_hash is None or composer_icon_hash is None:
            findings.append(finding("asset-unreadable", MANIFEST_PATH.as_posix(), "declared assets could not be compared"))
        elif logo_hash == composer_icon_hash:
            findings.append(finding("asset-duplicate", MANIFEST_PATH.as_posix(), "logo and composerIcon must use distinct image content"))

    for relative in REQUIRED_SUBMISSION_FILES:
        path = root_path / relative
        if not path.is_file():
            findings.append(finding("submission-file-missing", relative.as_posix(), "required submission file is missing"))
            continue
        if relative.name == "reviewer-tests.json":
            findings.extend(scan_reviewer_tests(path, root_path))
        else:
            findings.extend(scan_text_file(path, root_path))

    unique = sorted(
        {(item["category"], item["path"], item["detail"]) for item in findings},
        key=lambda item: (item[1], item[0], item[2]),
    )
    serialized = [finding(category, path, detail) for category, path, detail in unique]
    return {
        "ok": not serialized,
        "root": ".",
        "finding_count": len(serialized),
        "findings": serialized,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check plugin directory submission materials")
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    args = parser.parse_args(argv)
    result = scan_submission(args.root)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

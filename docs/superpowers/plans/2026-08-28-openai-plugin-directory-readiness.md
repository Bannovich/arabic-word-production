# OpenAI Plugin Directory Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce and publicly publish a verified, portable, skills-only `arabic-word-production` submission candidate while stopping before OpenAI identity, attestation, `Submit for Review`, and `Publish` actions.

**Architecture:** Keep the GitHub repository and canonical skill as the source of truth. Add a deterministic submission-contract checker, reviewer-material files, public legal pages, portable assets, a reproducible skill ZIP builder, and clean-room marketplace tests. Generate every portal field and bundle from the exact Git commit so review fixes remain versioned and reproducible.

**Tech Stack:** OpenAI Agent Skills and Plugins, JSON/YAML/Markdown, Python 3.10+, `unittest`, `python-docx`, `lxml`, Pillow, ZIP archives, GitHub Actions, Apache-2.0.

**Spec:** `docs/superpowers/specs/2026-08-28-openai-plugin-directory-readiness-design.md`

## Global Constraints

- The initial OpenAI directory submission type is exactly `Skills only`.
- The package and skill identifier remain `arabic-word-production`; the display name remains `Arabic Word Production`.
- The public core remains Apache-2.0 and free.
- Do not add MCP, OAuth, hosted services, checkout, advertisements, subscription copy, upgrade promotion, analytics, or telemetry.
- Do not claim Word Desktop verification unless Word Desktop opened the produced file in that run.
- Use only synthetic, privacy-safe reviewer fixtures.
- Do not upload identity documents, accept attestations, select `Submit for Review`, or select `Publish` without Ahmed's explicit action-time confirmation.
- Use official OpenAI requirements fetched on the final validation date; record any drift instead of silently weakening a gate.
- Use test-first development for every new or changed executable behavior.
- Keep generated ZIPs, temporary marketplaces, rendered documents, and local environments outside the tracked source tree.

---

### Task 1: Add the directory-submission contract checker

**Files:**
- Create: `tests/test_plugin_submission.py`
- Create: `scripts/check_plugin_submission.py`
- Modify: `scripts/check_publication.py`
- Modify: `tests/test_publication.py`
- Modify: `.github/workflows/quality.yml`

**Interfaces:**
- Consumes: repository root `Path` and current `.codex-plugin/plugin.json`.
- Produces: `scan_submission(root: Path | str) -> dict[str, object]` and a CLI that prints privacy-safe JSON and exits `0` only when the submission contract passes.

- [ ] **Step 1: Write failing tests for manifest limits and required files**

Create tests with literal fixtures that require:

```python
def test_short_description_over_30_characters_is_rejected(self):
    manifest = self.valid_manifest()
    manifest["interface"]["shortDescription"] = "x" * 31
    self.assertFinding(self.scan_fixture(manifest), "short-description-too-long")

def test_missing_referenced_logo_is_rejected(self):
    manifest = self.valid_manifest()
    manifest["interface"]["logo"] = "./assets/missing.png"
    self.assertFinding(self.scan_fixture(manifest), "asset-missing")
```

Also cover display-name length, at most three unique starter prompts, 128-character prompt limits, HTTPS policy URLs, exact reviewer-test counts, unfinished placeholders, and prohibited digital-commerce copy.

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```powershell
& .\.venv\Scripts\python.exe -m unittest tests.test_plugin_submission -v
```

Expected: failure because `scripts/check_plugin_submission.py` does not exist.

- [ ] **Step 3: Implement the minimal submission checker**

Implement category-only findings without echoing potentially sensitive matched text. Parse the manifest and reviewer JSON; resolve asset paths inside the repository; validate exact numeric limits; reject non-HTTPS public URLs; and scan user-visible plugin copy for the commerce terms `buy`, `checkout`, `subscribe`, `subscription`, `upgrade`, `credits`, `pricing`, `purchase`, and their direct Arabic equivalents only in the submission-facing files, not historical policy documentation.

- [ ] **Step 4: Run focused tests and probe the real repository**

Run:

```powershell
& .\.venv\Scripts\python.exe -m unittest tests.test_plugin_submission -v
& .\.venv\Scripts\python.exe scripts\check_plugin_submission.py .
```

Expected: fixture tests pass. The real-repository command exits nonzero only for the known missing or noncompliant candidate materials that Tasks 2 and 3 add; its privacy-safe finding categories are recorded in the task checkpoint.

- [ ] **Step 5: Commit the contract gate**

```powershell
git add tests/test_plugin_submission.py scripts/check_plugin_submission.py
git commit -m "test: add plugin directory submission gates"
```

### Task 2: Add compliant listing metadata, legal pages, and brand assets

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `skills/arabic-word-production/agents/openai.yaml`
- Create: `assets/icon.png`
- Create: `assets/logo.png`
- Create: `assets/logo-dark.png`
- Create: `docs/privacy-policy.md`
- Create: `docs/terms-of-service.md`
- Create: `docs/plugin-directory-submission.md`
- Create: `docs/index.md`
- Create: `docs/_config.yml`
- Modify: `README.md`
- Modify: `README.ar.md`

**Interfaces:**
- Consumes: the limits enforced by `scan_submission` and the approved listing contract.
- Produces: a directory-compliant manifest whose local assets exist and whose public policy/support links resolve through the project website.

- [ ] **Step 1: Create and inspect the brand assets**

Generate a simple, original document-page mark that communicates Arabic RTL flow without using Microsoft, Word, OpenAI, or ChatGPT logos. Export square PNG assets with transparent backgrounds, verify image decoding and dimensions with Pillow, and inspect light/dark variants visually.

- [ ] **Step 2: Update manifest metadata**

Use these exact user-facing values unless visual review reveals a readability problem:

```json
{
  "displayName": "Arabic Word Production",
  "shortDescription": "Audited Arabic Word files",
  "developerName": "Bannovich",
  "category": "Productivity",
  "capabilities": ["Create DOCX", "Audit RTL structure"],
  "websiteURL": "https://bannovich.github.io/arabic-word-production/",
  "privacyPolicyURL": "https://bannovich.github.io/arabic-word-production/privacy-policy/",
  "termsOfServiceURL": "https://bannovich.github.io/arabic-word-production/terms-of-service/",
  "defaultPrompt": [
    "Create and audit an Arabic RTL Word document from this content.",
    "Repair the RTL structure in this Arabic-English DOCX.",
    "Audit this Arabic Word file and report its actual validation surface."
  ],
  "brandColor": "#1F4E78",
  "composerIcon": "./assets/icon.png",
  "logo": "./assets/logo.png",
  "logoDark": "./assets/logo-dark.png"
}
```

- [ ] **Step 3: Keep skill UI metadata consistent**

Set `agents/openai.yaml` to the same display name, brand color, and a 25-64 character short description. Keep `policy.allow_implicit_invocation: true` and preserve the `$arabic-word-production` default-prompt mention.

- [ ] **Step 4: Write public legal and submission-boundary pages**

Document no project-operated server or telemetry, local/sandbox processing, user-controlled output retention, synthetic testing, no warranty, Apache-2.0, backup responsibility, evidence-scoped compatibility, support boundaries, and the separation between project behavior and the OpenAI host environment. Do not add checkout or upgrade copy.

Add a minimal GitHub Pages index and `_config.yml`. Give the privacy and terms pages explicit stable permalinks matching the manifest URLs so the published links do not depend on Jekyll filename conventions.

- [ ] **Step 5: Link the pages from both READMEs**

Add a concise `Plugin Directory` section that explains the skills-only candidate, legal pages, current review status, and the exact user-only portal gates without claiming the listing is already approved.

- [ ] **Step 6: Run the metadata tests and official validators**

Run:

```powershell
$profileRoot = [Environment]::GetFolderPath('UserProfile')
$skillValidator = Join-Path $profileRoot '.codex\skills\.system\skill-creator\scripts\quick_validate.py'
$pluginValidator = Join-Path $profileRoot '.codex\skills\.system\plugin-creator\scripts\validate_plugin.py'
& .\.venv\Scripts\python.exe -m unittest tests.test_plugin_submission -v
& .\.venv\Scripts\python.exe $skillValidator skills\arabic-word-production
& .\.venv\Scripts\python.exe $pluginValidator .
```

Expected: manifest and asset tests pass; the real-repository contract may still fail only for missing reviewer materials from Task 3.

- [ ] **Step 7: Commit listing and policy material**

```powershell
git add .codex-plugin/plugin.json skills/arabic-word-production/agents/openai.yaml assets docs README.md README.ar.md
git commit -m "feat: add plugin directory listing assets"
```

### Task 3: Add the reviewer submission pack

**Files:**
- Create: `submission/listing.en.md`
- Create: `submission/listing.ar.md`
- Create: `submission/reviewer-tests.json`
- Create: `submission/availability.md`
- Create: `submission/release-notes.md`
- Modify: `CHANGELOG.md`
- Modify: `scripts/check_publication.py`
- Modify: `tests/test_publication.py`
- Modify: `.github/workflows/quality.yml`

**Interfaces:**
- Consumes: manifest listing values and the eight cases fixed in the design.
- Produces: version-controlled copy that can be transferred to the OpenAI submission portal without improvisation.

- [ ] **Step 1: Write the English and Arabic listing copy**

Include one-line title/short-description records and long descriptions that state the five observable capabilities and all validation limitations. The Arabic version retains `DOCX`, `RTL`, `Word Desktop`, `Plugin`, and `structural audit` when those terms are clearer than forced translation.

- [ ] **Step 2: Create exactly five positive reviewer cases**

Write JSON objects with IDs `POS-001` through `POS-005`. Each object contains `prompt`, `expected_route`, `expected_behavior`, `expected_result_shape`, `fixture`, and `reviewer_notes`. Use only synthetic content and repository-owned assets.

- [ ] **Step 3: Create exactly three negative reviewer cases**

Write JSON objects with IDs `NEG-001` through `NEG-003` covering false Word Desktop claims, unsanitized private fixtures, and unsupported macro/OLE editing. Each includes the expected refusal, clarification, or safe fallback and why completion would be unsafe or misleading.

- [ ] **Step 4: Add availability and release notes**

Recommend a conservative initial country selection limited to locations where English/Arabic support and the public legal pages are usable. Mark the final country choice as an Ahmed portal decision, not a code default. State this is an initial skills-only submission with no MCP, authentication, commerce, or project-operated data service.

- [ ] **Step 5: Integrate the complete contract into publication QA and CI**

Add the final submission paths to the publication inventory and its test fixture. Run `scripts/check_plugin_submission.py .` in the Windows/Ubuntu quality workflow after the publication privacy check.

- [ ] **Step 6: Run the contract checker and privacy scan**

Run:

```powershell
& .\.venv\Scripts\python.exe scripts\check_plugin_submission.py .
& .\.venv\Scripts\python.exe scripts\check_publication.py .
```

Expected: both exit `0` with zero findings.

- [ ] **Step 7: Commit reviewer materials**

```powershell
git add submission CHANGELOG.md scripts/check_publication.py tests/test_publication.py .github/workflows/quality.yml
git commit -m "docs: add plugin reviewer submission pack"
```

### Task 4: Harden clean-room and cross-platform behavior

**Files:**
- Modify: `skills/arabic-word-production/SKILL.md`
- Delete: `skills/arabic-word-production/scripts/make_test_visual.py`
- Create: `skills/arabic-word-production/scripts/check_environment.py`
- Create: `skills/arabic-word-production/tests/test_environment.py`
- Modify: `skills/arabic-word-production/references/qa-and-performance.md`
- Modify: `docs/compatibility-matrix.md`

**Interfaces:**
- Consumes: Python interpreter and import availability.
- Produces: `inspect_environment() -> dict[str, object]`, reporting Python version, required modules, optional renderer presence, and Word Desktop status without installing or changing anything.

- [ ] **Step 1: Write failing environment-diagnostic tests**

Use injected module discovery and executable lookup functions so tests can assert literal results for all-required-present, one-required-missing, optional-renderer-present, and no-Word cases without mocking the production result itself.

- [ ] **Step 2: Run the environment tests and verify RED**

Run:

```powershell
& .\.venv\Scripts\python.exe -m unittest skills.arabic-word-production.tests.test_environment -v
```

If the hyphenated path prevents module discovery, invoke the test file through `unittest discover -s skills\arabic-word-production\tests -p test_environment.py -v`. Expected: failure because the diagnostic does not exist.

- [ ] **Step 3: Implement the read-only environment diagnostic**

Check `docx`, `lxml`, and `PIL` as required modules; `soffice` as optional renderer; and report Word Desktop as unverified unless the current run supplies explicit evidence. Print JSON and return nonzero only when a required Python module is absent.

- [ ] **Step 4: Remove the unrelated visual helper**

Delete the unused Claude activation-flow generator after confirming no tracked file imports it. It is unrelated to Arabic Word production and contains a Windows-only font preference that should not ship in the public plugin.

- [ ] **Step 5: Make the general documents workflow optional**

Revise `SKILL.md` so `documents:documents` is preferred when available, while bundled `build_docx.py` and `audit_docx.py` remain the deterministic fallback. Keep the same RTL invariants and validation-surface disclosure.

- [ ] **Step 6: Run the clean-room test suite**

Create a temporary virtual environment, install the declared project dependencies, run the environment diagnostic, official validators, all repository tests, all skill tests, and one synthetic DOCX build/audit/reopen cycle with no Word Desktop assumption.

- [ ] **Step 7: Commit portability hardening**

```powershell
git add skills/arabic-word-production docs/compatibility-matrix.md
git commit -m "fix: harden skills-only plugin portability"
```

### Task 5: Build deterministic submission artifacts

**Files:**
- Create: `tests/test_submission_bundle.py`
- Create: `scripts/build_submission_bundle.py`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: repository root and output directory.
- Produces: `build_bundles(root: Path, output_dir: Path) -> dict[str, object]` with a skill ZIP, plugin-package ZIP, sorted file inventories, byte sizes, and SHA-256 digests.

- [ ] **Step 1: Write failing bundle tests**

Tests require deterministic member ordering and timestamps, `SKILL.md` at the root of the skill ZIP, no `.git`/`.venv`/cache/generated files, preservation of the DOCX template bytes, and identical SHA-256 output across two builds from the same tree.

- [ ] **Step 2: Run bundle tests and verify RED**

Run:

```powershell
& .\.venv\Scripts\python.exe -m unittest tests.test_submission_bundle -v
```

Expected: failure because the bundle builder is missing.

- [ ] **Step 3: Implement the minimal deterministic builder**

Use `zipfile.ZipFile` with sorted POSIX member names, a fixed ZIP timestamp, deflated compression, explicit exclusions, and streamed SHA-256 calculation. Write artifacts only to the caller-supplied output directory.

- [ ] **Step 4: Build the real candidate outside Git**

Write to a temporary directory, run official validators against the source tree, open each ZIP to verify inventory and CRCs, and record the resulting digests without committing the ZIPs.

- [ ] **Step 5: Commit the bundle builder**

```powershell
git add tests/test_submission_bundle.py scripts/build_submission_bundle.py .gitignore
git commit -m "build: add deterministic plugin submission bundles"
```

### Task 6: Create and test a disposable local marketplace

**Files:**
- Create: `tests/test_local_marketplace.py`
- Create: `scripts/build_local_marketplace.py`
- Modify: `docs/plugin-directory-submission.md`

**Interfaces:**
- Consumes: repository root and temporary destination.
- Produces: a disposable marketplace root with `.agents/plugins/marketplace.json` and `plugins/arabic-word-production/`, copied from the exact candidate source.

- [ ] **Step 1: Write failing marketplace tests**

Assert the catalog name, display name, plugin order, `AVAILABLE` installation policy, `ON_INSTALL` authentication policy, `Productivity` category, canonical relative source path, and byte-identical plugin copy.

- [ ] **Step 2: Run marketplace tests and verify RED**

Run:

```powershell
& .\.venv\Scripts\python.exe -m unittest tests.test_local_marketplace -v
```

Expected: failure because the builder is missing.

- [ ] **Step 3: Implement and validate the marketplace builder**

Copy only the plugin-package inventory into `plugins/arabic-word-production`, write the canonical marketplace JSON, run the official plugin validator against the copy, and leave the user's personal marketplace untouched.

- [ ] **Step 4: Perform the app installation handoff**

Add the disposable marketplace root with the supported Codex command when available, install the candidate, restart/refresh ChatGPT Desktop, and invoke the plugin in a fresh task. If the app restart or UI selection needs Ahmed, stop with that one exact action and preserve the verified marketplace path.

- [ ] **Step 5: Commit marketplace tooling**

```powershell
git add tests/test_local_marketplace.py scripts/build_local_marketplace.py docs/plugin-directory-submission.md
git commit -m "test: add clean local marketplace workflow"
```

### Task 7: Record exact-candidate evidence and publish the readiness branch

**Files:**
- Create: `release-evidence/plugin-directory-candidate.json`
- Modify: `CHANGELOG.md`
- External: push a reviewed feature branch and open/merge a GitHub pull request under the user's existing publication approval.

**Interfaces:**
- Consumes: the final source commit, official current documentation, tests, validators, generated bundles, and local marketplace result.
- Produces: a public GitHub commit with machine-readable evidence and no unperformed OpenAI portal claims.

- [ ] **Step 1: Refresh official OpenAI requirements**

Open the package, submission, submission-error, and plugin-guideline pages. Compare current limits and required materials to the spec. If a requirement changed, update tests and documentation before proceeding.

- [ ] **Step 2: Run the complete gate on the exact candidate**

Run official skill/plugin validators, repository tests, skill tests, publication checker, submission checker, environment diagnostic, deterministic bundle tests, marketplace tests, and a synthetic DOCX regression. Capture exit codes, counts, elapsed time, renderer availability, and Word Desktop status.

- [ ] **Step 3: Write evidence without circular SHA claims**

Record the validated parent commit, test counts, official-doc refresh date, bundle inventories and SHA-256 digests, marketplace result, privacy findings, renderer, and `word_desktop_tested`. Commit the evidence as the only delta, then rerun all non-circular source checks against the evidence commit.

- [ ] **Step 4: Review the branch diff and public copy**

Confirm there are no secrets, user paths, private data, checkout/upgrade copy, unrelated artifacts, broken links, or claims that the plugin is already approved by OpenAI.

- [ ] **Step 5: Push and review through GitHub**

Push `plugin-readiness-v0.2.0`, create a pull request, wait for CI, fix failures through test-first changes, and merge only after the public diff and CI evidence match the local candidate. Do not alter OpenAI Platform state.

- [ ] **Step 6: Stop at the user-only portal gate**

Provide Ahmed with the exact URLs, candidate SHA, bundle digest, validation evidence, proposed publisher identity fields, and the remaining portal actions. Request current confirmation before identity selection, attestations, `Submit for Review`, and eventual `Publish`.

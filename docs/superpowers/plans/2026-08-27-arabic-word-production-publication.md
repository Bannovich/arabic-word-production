# Arabic Word Production Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish `Bannovich/arabic-word-production` as a privacy-reviewed Apache-2.0 open-source Agent Skill and skills-only OpenAI plugin with contribution workflows, automated quality checks, and an evidence-scoped `v0.1.0` release.

**Architecture:** Keep one canonical skill under `skills/arabic-word-production/`, wrap it with a repository-level OpenAI plugin manifest, and place public-project documentation and governance outside the skill so they do not consume skill context. Add one repository quality command that validates publication structure and privacy invariants, while retaining the skill's existing DOCX builder, auditor, and regression tests as the behavioral core.

**Tech Stack:** Agent Skills (`SKILL.md`), OpenAI plugin manifest JSON, Python 3.10-3.13, `python-docx`, `lxml`, Pillow, `unittest`, GitHub Actions, GitHub Issues/Pull Requests/Releases, Apache-2.0.

**Spec:** `docs/superpowers/specs/2026-08-27-arabic-word-production-open-source-design.md`

## Global Constraints

- Repository owner and name are exactly `Bannovich/arabic-word-production`.
- Create and inspect the remote as private; make it public only after every publication gate passes.
- Use Apache-2.0 and publish the first release as `v0.1.0`.
- Preserve the existing skill behavior and automatic invocation policy.
- Do not publish raw conversations, client documents, conversation IDs, secrets, or user-profile absolute paths.
- Do not claim Word Desktop verification unless Microsoft Word Desktop actually performed the test.
- The GitHub repository is the source of truth; OpenAI universal-directory submission is not part of this release.
- Use a Python 3.10+ executable with the declared project dependencies available.
- Read the source skill from the active Codex skills directory and do not modify it in place.

---

### Task 1: Create the canonical plugin and skill tree

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `skills/arabic-word-production/**`
- Preserve: `docs/superpowers/specs/2026-08-27-arabic-word-production-open-source-design.md`
- Test: plugin scaffold validator and byte-for-byte source inventory comparison

**Interfaces:**
- Consumes: the approved design spec and the existing local skill directory.
- Produces: a plugin root with one canonical skill at `skills/arabic-word-production/`.

- [ ] **Step 1: Scaffold the plugin root with the official local helper**

Run the official scaffold helper from the parent workspace. Resolve the three
variables from the active Codex installation and workspace instead of storing
machine-specific paths in the public plan:

```powershell
& $python `
  $createBasicPlugin `
  arabic-word-production `
  --path $workspaceParent `
  --with-skills `
  --force
```

Expected: `.codex-plugin/plugin.json` and `skills/` exist without removing the committed spec.

- [ ] **Step 2: Copy the existing skill mechanically into the canonical skill folder**

Copy all 17 existing files, including the binary Word template, without editing the source directory. Compare relative paths, file counts, and SHA-256 hashes between source and destination.

Expected: every source relative path exists at the destination with the same SHA-256 hash.

- [ ] **Step 3: Replace the scaffold manifest with release metadata**

Set these exact material fields:

```json
{
  "name": "arabic-word-production",
  "version": "0.1.0",
  "description": "Create and audit Arabic-first and bilingual Microsoft Word documents with explicit RTL semantics.",
  "author": {
    "name": "Bannovich",
    "email": "73133823+Bannovich@users.noreply.github.com",
    "url": "https://github.com/Bannovich"
  },
  "homepage": "https://github.com/Bannovich/arabic-word-production",
  "repository": "https://github.com/Bannovich/arabic-word-production",
  "license": "Apache-2.0",
  "keywords": ["arabic", "bilingual", "docx", "microsoft-word", "rtl", "wordprocessingml"],
  "skills": "./skills/",
  "interface": {
    "displayName": "Arabic Word Production",
    "shortDescription": "Reliable Arabic-first and bilingual Word documents",
    "longDescription": "Build and structurally audit Arabic-first and bilingual DOCX files with explicit paragraph, run, table, and section direction rules.",
    "developerName": "Bannovich",
    "category": "Productivity",
    "capabilities": ["Write"],
    "websiteURL": "https://github.com/Bannovich/arabic-word-production",
    "defaultPrompt": [
      "Create an audited Arabic RTL Word document.",
      "Repair this bilingual DOCX for Word Desktop.",
      "Audit this Arabic Word file for RTL errors."
    ],
    "brandColor": "#1F4E78"
  }
}
```

- [ ] **Step 4: Validate the canonical skill and plugin**

Run:

```powershell
& $python $quickValidate "skills\arabic-word-production"
& $python $validatePlugin "."
```

Expected: both commands exit `0` with no unfinished scaffold markers.

- [ ] **Step 5: Commit the canonical package**

```powershell
git add .codex-plugin skills
git commit -m "feat: package Arabic Word Production skill"
```

### Task 2: Add licensing and installable project metadata

**Files:**
- Create: `LICENSE`
- Create: `NOTICE`
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `README.md`
- Create: `README.ar.md`
- Create: `CHANGELOG.md`
- Test: metadata parse, license detection, install-command review

**Interfaces:**
- Consumes: the canonical plugin tree from Task 1.
- Produces: an installable and legally reusable `v0.1.0` project with bilingual onboarding.

- [ ] **Step 1: Add the unmodified Apache License 2.0 text**

Use the official Apache License 2.0 text in `LICENSE`. Add `NOTICE` naming “Ahmed Elbanna / Bannovich” as project initiator, stating that Microsoft Word is a Microsoft trademark and OpenAI/ChatGPT/Codex are compatibility surfaces rather than owners or endorsers.

- [ ] **Step 2: Add project metadata and dependencies**

Create `pyproject.toml` with strict project version `0.1.0`, `requires-python = ">=3.10"`, and these runtime dependency ranges:

```toml
dependencies = [
  "python-docx>=1.2.0,<2",
  "lxml>=6.0,<7",
  "Pillow>=11.0,<13"
]
```

Configure setuptools with no importable top-level package because the executable scripts remain inside the Agent Skill.

- [ ] **Step 3: Add repository ignore rules**

Ignore Python caches, virtual environments, generated DOCX/PDF/PNG output, audit JSON, regression output, temporary Office lock files, local environment files, and build artifacts. Do not ignore the bundled template under `skills/arabic-word-production/assets/`.

- [ ] **Step 4: Write English and Arabic README files**

Each README must include: purpose, non-developer quick start, supported surfaces, plugin and standalone-skill installation paths, direct script usage, validation-claim vocabulary, privacy-safe issue reporting, known limitations, license, contribution links, and `v0.1.0` maturity. The Arabic README must retain technical terms such as `DOCX`, `Word Desktop`, `RTL`, `Plugin`, `Issue`, and `Pull Request` in English where clearer.

- [ ] **Step 5: Add the initial changelog**

Create `CHANGELOG.md` in Keep a Changelog style with an `Unreleased` section and a dated `0.1.0` section describing the imported skill, deterministic builder/auditor, RTL/OOXML references, tests, plugin packaging, and project governance. Do not claim universal Word compatibility.

- [ ] **Step 6: Parse metadata and review links**

Run Python `tomllib` against `pyproject.toml`, JSON parsing against `plugin.json`, and a repository search for broken local absolute paths or placeholder tokens.

- [ ] **Step 7: Commit licensing and onboarding**

```powershell
git add LICENSE NOTICE pyproject.toml .gitignore README.md README.ar.md CHANGELOG.md
git commit -m "docs: add licensing and bilingual onboarding"
```

### Task 3: Add governance, engineering history, and support documentation

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `GOVERNANCE.md`
- Create: `CODE_OF_CONDUCT.md`
- Create: `SECURITY.md`
- Create: `SUPPORT.md`
- Create: `ROADMAP.md`
- Create: `docs/how-it-was-built.md`
- Create: `docs/architecture-decisions.md`
- Create: `docs/adding-a-guardrail.md`
- Create: `docs/compatibility-matrix.md`
- Create: `docs/privacy-and-test-data.md`
- Create: `docs/release-process.md`
- Test: documentation link check and decision/claim consistency review

**Interfaces:**
- Consumes: the approved design, current error taxonomy, guardrails, and QA policy.
- Produces: a contributor-facing process in which failures become evidence-backed regression protection.

- [ ] **Step 1: Write contribution and governance rules**

Require reproduction, privacy-safe fixtures, regression evidence, scoped changes, validation-surface disclosure, and review before merge. Define `Bannovich` as initial maintainer and release authority, with a documented future path for adding maintainers.

- [ ] **Step 2: Add community safety, security, and support files**

Use Contributor Covenant 2.1 for `CODE_OF_CONDUCT.md`. Direct vulnerabilities, secrets, and private document samples away from public issues. Explain that ordinary rendering defects belong in public structured issue forms only after sanitization.

- [ ] **Step 3: Document the engineering history without hidden reasoning**

Write the history as `Problem -> Evidence -> Experiment -> Result -> Decision -> Regression protection`. Include right-alignment versus bidi semantics, logical `w:jc=start`, table `w:bidiVisual`, stable fields, one-repair limits, structural versus application verification, and performance measurement.

- [ ] **Step 4: Document architecture decisions and the guardrail workflow**

Map each accepted defect to an error ID, reproducible evidence, a failing behavioral check or manual Word protocol, minimal correction, verification, and release notes.

- [ ] **Step 5: Publish an honest compatibility matrix and roadmap**

Separate structural audit, renderer inspection, Word Desktop verification, Google Docs compatibility, and LibreOffice compatibility. Mark unperformed surfaces as `Not verified`, not as failed or supported.

- [ ] **Step 6: Document the release process**

Require exact-commit validation, privacy scan, validators, tests, remote tree comparison, visibility verification, evidence-scoped release notes, and a post-publication smoke check.

- [ ] **Step 7: Validate documentation links and claims**

Search relative Markdown links and ensure every referenced local file exists. Search for forbidden overclaims: `guaranteed`, `all Word versions`, `100% compatible`, and equivalents.

- [ ] **Step 8: Commit governance and engineering documentation**

```powershell
git add CONTRIBUTING.md GOVERNANCE.md CODE_OF_CONDUCT.md SECURITY.md SUPPORT.md ROADMAP.md docs
git commit -m "docs: define contribution and release governance"
```

### Task 4: Add publication checks, issue forms, and continuous integration

**Files:**
- Create: `scripts/check_publication.py`
- Create: `tests/test_publication.py`
- Create: `.github/ISSUE_TEMPLATE/rtl-rendering.yml`
- Create: `.github/ISSUE_TEMPLATE/table-layout.yml`
- Create: `.github/ISSUE_TEMPLATE/image-object.yml`
- Create: `.github/ISSUE_TEMPLATE/performance.yml`
- Create: `.github/ISSUE_TEMPLATE/improvement.yml`
- Create: `.github/ISSUE_TEMPLATE/config.yml`
- Create: `.github/pull_request_template.md`
- Create: `.github/CODEOWNERS`
- Create: `.github/workflows/quality.yml`
- Test: `tests/test_publication.py`, existing skill tests, YAML parse, GitHub workflow structure

**Interfaces:**
- Consumes: required file inventory, privacy rules, plugin metadata, and the existing test suite.
- Produces: `scripts/check_publication.py ROOT`, exiting `0` with a JSON summary when the repository is publishable and nonzero with finding details otherwise.

- [ ] **Step 1: Write failing tests for the publication checker**

Tests must cover: missing required file, `chatgpt-conversation://` detection, `conversationId` detection, Windows user-profile path detection, private-key marker detection, token-prefix detection, non-no-reply email detection, Office core-properties inspection, safe GitHub no-reply email allowance, and a minimal clean repository passing.

- [ ] **Step 2: Run the new tests and verify RED**

```powershell
& $python -m unittest tests.test_publication -v
```

Expected: failure because `scripts/check_publication.py` does not yet exist.

- [ ] **Step 3: Implement the minimal publication checker**

The command walks tracked project content while excluding `.git`, caches, virtual environments, and generated output. It parses text using UTF-8 with replacement, inspects `docProps/core.xml` in `.docx` ZIP packages, reports relative paths and finding categories, and never prints secret values. It also validates required repository paths and rejects unfinished scaffold markers.

- [ ] **Step 4: Run the new tests and verify GREEN**

```powershell
& $python -m unittest tests.test_publication -v
```

Expected: all publication-checker tests pass.

- [ ] **Step 5: Add structured GitHub issue forms**

Each form requires environment, Word version, locale, direction/content type, expected and actual behavior, validation surface, reproduction steps, audit output, privacy confirmation, and permission status for any attached sample. Form-specific fields cover tables, images/objects, and latency.

- [ ] **Step 6: Add PR template and ownership**

Require linked issue, reproduction evidence, red/green evidence for behavior changes, privacy confirmation, affected validation surfaces, test commands, documentation impact, and changelog impact. Set `* @Bannovich` in `CODEOWNERS`.

- [ ] **Step 7: Add GitHub Actions quality workflow**

Run on pushes and pull requests using Windows and Ubuntu with Python 3.10, 3.12, and 3.13. Install the project, run the publication checker, run the repository tests, then run the existing skill tests. Upload no private or generated DOCX artifacts.

- [ ] **Step 8: Validate YAML and run all local tests**

Parse every `.yml` file with the bundled Python YAML library when available; otherwise use a strict line/JSON-compatible validation and rely on GitHub's workflow parser after private push. Run:

```powershell
& $python -m unittest discover -s tests -v
& $python -m unittest discover -s skills\arabic-word-production\tests -v
& $python scripts\check_publication.py .
```

- [ ] **Step 9: Commit contribution automation**

```powershell
git add scripts tests .github
git commit -m "ci: add publication and contribution quality gates"
```

### Task 5: Perform the private publication audit

**Files:**
- Create: `release-evidence/v0.1.0-validation.json`
- Modify: `CHANGELOG.md` only if validation reveals a documentation correction
- Test: complete release command suite on the exact candidate commit

**Interfaces:**
- Consumes: all repository files from Tasks 1-4.
- Produces: a clean candidate commit and machine-readable release evidence suitable for private remote review.

- [ ] **Step 1: Run official skill and plugin validators**

Run both local official validators against the final candidate tree. Record command names, exit codes, and timestamps.

- [ ] **Step 2: Run every repository and skill test**

Run both `unittest` discovery commands with full verbose output. Record test counts and failures.

- [ ] **Step 3: Run the publication privacy checker**

Run `scripts/check_publication.py .` and record finding counts without recording secret contents.

- [ ] **Step 4: Run deterministic DOCX smoke build and structural audit outside the repository**

Use a temporary workspace and a synthetic Arabic/bilingual model. Build one DOCX, audit it against the model, reopen-save a copy, and re-audit. Record elapsed time and the actual renderer/Word Desktop availability. Do not commit the generated document.

- [ ] **Step 5: Inspect the bundled DOCX metadata and repository history**

Confirm the template author metadata is generic or project-owned, no absolute local paths are tracked, no ignored build artifacts are staged, and commit authors use GitHub no-reply email.

- [ ] **Step 6: Write validation evidence and commit it**

Write `release-evidence/v0.1.0-validation.json` with exact commit, timestamp, validators, test counts, smoke result, privacy scan result, renderer, and `word_desktop_tested` boolean. Commit:

```powershell
git add release-evidence/v0.1.0-validation.json
git commit -m "test: record v0.1.0 publication evidence"
```

- [ ] **Step 7: Re-run the complete gate after the evidence commit**

The evidence commit changes the candidate SHA, so rerun publication checks and tests and update the evidence to the final commit through a documented two-commit evidence convention: the evidence file names the validated parent tree, while the release tag points to the evidence commit whose only delta is that evidence record. Verify that distinction in release notes.

### Task 6: Create and verify the private GitHub repository

**Files/External state:**
- Create: private `https://github.com/Bannovich/arabic-word-production`
- Upload: exact verified local tree and history
- Configure: Issues, Discussions when available, default branch `main`, repository description, topics, and safe merge settings
- Test: private visibility, remote tree/commit parity, private Actions run

**Interfaces:**
- Consumes: the verified local repository candidate.
- Produces: a private GitHub repository that exactly represents the validated source.

- [ ] **Step 1: Create the repository through the authenticated GitHub UI**

Use owner `Bannovich`, exact name `arabic-word-production`, private visibility, and no alternate name. If the name is unavailable, stop.

- [ ] **Step 2: Upload the exact local commit**

Use the connected GitHub repository tools to create blobs, a tree, a commit, and the `main` ref without exposing authentication tokens. Preserve binary files using base64 blob encoding. Do not upload `.git`, caches, ignored outputs, or local environment files.

- [ ] **Step 3: Verify private remote parity**

Compare the remote `main` tree with the local tracked file inventory by relative path, byte size, and SHA/hash where available. Confirm the repository reports private visibility.

- [ ] **Step 4: Configure collaboration settings**

Enable Issues and Discussions when supported. Set repository description and topics. Configure merge settings and a default-branch ruleset requiring the `quality` workflow where account capabilities permit it. If a setting requires user UI interaction or is unavailable, record it explicitly.

- [ ] **Step 5: Observe the private Actions run**

Wait for the candidate workflow to finish. If it fails, keep the repository private, inspect logs, reproduce locally, fix through the test-first workflow, push a new verified commit, and rerun.

- [ ] **Step 6: Perform the private review gate**

Open the private repository as a non-code reviewer would. Check README rendering, Arabic direction, issue-form availability, license detection, release evidence, plugin manifest, and that no generated or private artifact is visible.

### Task 7: Publish the repository and `v0.1.0` release

**Files/External state:**
- Modify: repository visibility from private to public
- Create: Git tag `v0.1.0`
- Create: GitHub Release `v0.1.0`
- Create: GitHub Project board when the connected account surface permits it
- Test: anonymous public accessibility, release URL, tag/commit parity, public issue forms

**Interfaces:**
- Consumes: a passing private remote commit and completed private review.
- Produces: the public open-source project and initial release.

- [ ] **Step 1: Reconfirm the exact publication candidate**

Record the private repository URL, candidate commit SHA, successful Actions run, local verification output, privacy result, and release evidence file. Confirm no commit has appeared after validation.

- [ ] **Step 2: Change visibility to public through GitHub settings**

Use the GitHub danger-zone visibility control only for `Bannovich/arabic-word-production`. Confirm the repository name exactly before submitting the change.

- [ ] **Step 3: Verify anonymous/public accessibility**

Open the repository URL without relying on private-only API state. Confirm README, Arabic README, license, source tree, issue forms, Actions summary, and commit history are publicly accessible.

- [ ] **Step 4: Create and verify tag `v0.1.0`**

Point the tag at the exact release candidate commit. Fetch the tag through the connected GitHub surface and confirm the target SHA.

- [ ] **Step 5: Publish evidence-scoped release notes**

State included capabilities, installation paths, validator and test evidence, tested operating surfaces, whether Word Desktop was tested, known limitations, privacy policy for samples, and the Apache-2.0 license. Do not claim universal compatibility.

- [ ] **Step 6: Create the GitHub Project board when available**

Create statuses `New`, `Needs reproduction`, `Needs fixture`, `In progress`, `Word Desktop validation`, and `Released`. Add views for triage and roadmap. If account permissions or connector/UI support block this step, record exact manual steps and identify the board as pending.

- [ ] **Step 7: Perform the final public smoke check**

Verify repository visibility, release availability, tag parity, license detection, issue forms, README links, and public file inventory. Re-run local verification against the final public commit before making any completion claim.

- [ ] **Step 8: Provide the user handoff**

Return the public repository URL, release URL, exact candidate SHA, test and validator counts, renderer/Word Desktop status, installed surfaces, contribution entrypoints, and any GitHub setting that still requires one-time manual action.

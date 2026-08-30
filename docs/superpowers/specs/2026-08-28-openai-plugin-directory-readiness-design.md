# OpenAI Plugin Directory Readiness Design

**Status:** Approved in conversation on 2026-08-28 as the next phase after the public `v0.1.0` GitHub release.

## 1. Purpose

Prepare `arabic-word-production` for a public **skills-only** submission to OpenAI's universal Plugins Directory without adding a hosted service, MCP server, user accounts, checkout, or paid entitlement system. The GitHub repository remains the Apache-2.0 source of truth. This phase may prepare a portal draft and all reviewer materials, but it must stop before identity verification, policy attestations, `Submit for Review`, and `Publish` unless Ahmed gives explicit confirmation at the moment of each action.

## 2. Fixed Decisions

- The first directory submission is `Skills only`; no MCP server is introduced in this phase.
- The public core remains free and licensed under Apache-2.0.
- The publisher-facing name remains `Arabic Word Production`; the package and skill identifier remain `arabic-word-production`.
- The listing describes evidence-scoped structural DOCX generation and audit. It never promises Word Desktop verification unless Word Desktop actually opened the produced file in that run.
- The plugin does not sell, promote, or link to checkout for digital products, services, subscriptions, credits, or upgrades.
- The repository remains the maintained source; a reviewed submission bundle is generated from an exact commit rather than edited manually in the portal.
- Public examples and reviewer fixtures are synthetic and contain no client content, conversation references, secrets, local user paths, or private identity metadata.
- Automatic skill invocation remains enabled.
- Existing runtime behavior remains available directly from the GitHub skill even if public-directory review is delayed or rejected.

## 3. Official-Requirements Baseline

The implementation follows the OpenAI documentation current on 2026-08-28:

- Skills-only plugins are valid public submissions: <https://developers.openai.com/plugins/deploy/submission>
- Every plugin uses `.codex-plugin/plugin.json`, and published packages commonly include install metadata and assets: <https://developers.openai.com/plugins/build/plugins>
- Final directory metadata uses strict field limits, including a display name and short description of at most 30 characters and at most three starter prompts of at most 128 characters each: <https://developers.openai.com/plugins/deploy/submission-errors>
- Review materials include realistic starter prompts, five positive tests, three negative tests, release notes, availability, verified identity, and policy attestations: <https://developers.openai.com/plugins/deploy/submission>
- Published plugins must be stable, reliable, privacy-preserving, and useful rather than trial/demo packages: <https://developers.openai.com/plugins/app-guidelines>
- Current plugin commerce policy does not allow selling digital products or services, including subscriptions, through direct or indirect plugin upsells: <https://developers.openai.com/plugins/app-guidelines#commerce-and-monetization>

Because official requirements can change, the final pre-submission gate re-fetches these pages and records the date and constraints used.

## 4. Scope

### In scope

- Add deterministic tests for directory metadata limits and bundle completeness.
- Update the manifest with compliant descriptions, legal URLs, starter prompts, and visual asset paths.
- Create production-ready plugin icon and logo assets, including a dark-mode variant when useful.
- Publish clear Privacy Policy, Terms of Service, and support information suitable for a skills-only plugin that performs local/sandbox document processing.
- Create a machine-readable submission pack containing listing copy, starter prompts, exactly five positive reviewer cases, exactly three negative reviewer cases, release notes, proposed country availability, and a user action checklist.
- Remove unrelated or stale files that do not serve the Arabic Word workflow.
- Make platform-specific test helpers portable or clearly optional.
- Make the skill usable when the general `documents:documents` skill is available while retaining a bundled deterministic fallback when it is not.
- Build a reproducible ZIP containing only the files needed by the skills-only submission and publish its SHA-256 digest in validation evidence.
- Create a disposable local marketplace root for clean installation testing without duplicating the canonical source in Git.
- Prepare a GitHub pull request/release candidate containing the verified readiness changes.

### Out of scope

- OpenAI identity or business verification.
- Accepting legal or policy attestations for Ahmed.
- Clicking `Submit for Review` or `Publish` without action-time confirmation.
- A paid tier, checkout, subscription promotion, analytics, advertisements, or lead-generation copy inside the plugin.
- An MCP server, OAuth, cloud database, external document upload service, or hosted UI.
- Guarantees for every Microsoft Word version, operating system, preview renderer, or office suite.
- Publishing private user documents or raw conversations as test fixtures.

## 5. Repository Additions

```text
arabic-word-production/
|-- .codex-plugin/plugin.json
|-- assets/
|   |-- icon.png
|   |-- logo.png
|   `-- logo-dark.png
|-- docs/
|   |-- privacy-policy.md
|   |-- terms-of-service.md
|   `-- plugin-directory-submission.md
|-- submission/
|   |-- listing.en.md
|   |-- listing.ar.md
|   |-- reviewer-tests.json
|   |-- availability.md
|   `-- release-notes.md
|-- scripts/
|   |-- build_submission_bundle.py
|   `-- check_plugin_submission.py
|-- tests/
|   `-- test_plugin_submission.py
`-- release-evidence/
    `-- plugin-directory-candidate.json
```

The generated ZIP and disposable marketplace/install artifacts stay outside the tracked tree. Only their reproducible manifest, digest, test results, and documented commands are committed.

## 6. Listing Contract

- `displayName`: `Arabic Word Production` (22 characters).
- `shortDescription`: no more than 30 characters; proposed value `Audited Arabic Word files`.
- Category: `Productivity`.
- Capabilities must describe observable behavior and must not imply internet access, Word Desktop access, or external publication.
- At most three starter prompts, each no more than 128 characters and containing no plugin `@mention`.
- Long description distinguishes:
  - Arabic-first and bilingual DOCX creation.
  - Explicit paragraph, run, table, and section direction handling.
  - Structural audit and reopen stability checks.
  - Optional renderer inspection.
  - Word Desktop verification only when actually performed.
- Website, support, privacy, and terms links are public HTTPS URLs owned by the project publisher. GitHub Pages is the default host unless Ahmed later provides a business domain.

## 7. Reviewer-Test Contract

The submission pack contains exactly five positive and three negative cases. Every case includes an ID, synthetic prompt, expected skill route, expected behavior, expected result shape, required fixture, and reviewer notes.

### Positive cases

1. Arabic-first business document with headings, lists, and a small RTL table.
2. Bilingual Arabic-English report with URLs and technical LTR spans inside RTL paragraphs.
3. Repair and audit of a synthetic DOCX containing wrong paragraph and table direction.
4. Six-column Arabic table requiring landscape evaluation and return to portrait.
5. Arabic document with an inline image, caption adjacency, structural audit, and honest validation-surface disclosure.

### Negative cases

1. A request to claim Word Desktop verification when Word Desktop was not used; the plugin must refuse the claim and report the actual validation surface.
2. A request to include unsanitized private client or conversation data in a public fixture; the plugin must stop and request sanitized input.
3. A request outside the plugin's safe capability, such as editing macros or opaque embedded OLE objects; the plugin must preserve the source, disclose the limitation, and offer a safe supported fallback rather than corrupting the file.

## 8. Portability and Dependency Design

- The skill treats `documents:documents` as a preferred general DOCX workflow when present, not an unconditional cross-plugin dependency.
- Bundled scripts resolve paths relative to the skill directory and output to user/workspace-selected destinations.
- Font discovery checks platform-appropriate locations and installed font APIs before falling back to Pillow's default font; it must not require `C:/Windows/Fonts`.
- Rendering with LibreOffice is optional and capability-detected. Its absence is reported as `renderer: unavailable`, not a failure.
- Word Desktop is never assumed. A clean-room test must pass without Word Desktop installed.
- Required Python packages are documented and checked with a concise environment diagnostic. The diagnostic must not install software or mutate global environments.

## 9. Privacy, Legal, and Commerce Design

- The skills-only plugin sends no document to a project-owned server because this phase has no server.
- The Privacy Policy explains that ChatGPT/OpenAI runtime behavior is governed separately by the user's OpenAI plan and policies; the project itself does not operate the host runtime.
- The policy discloses any local file processing, generated artifacts, optional diagnostics, retention controlled by the user's environment, and the project's lack of telemetry.
- The Terms explain the Apache-2.0 software license, no warranty, evidence-scoped compatibility claims, user responsibility for document rights and backups, and support boundaries.
- The plugin contains no price, plan, upgrade, purchase, donation, or checkout language.
- Future paid consulting or a separate hosted service must be designed and reviewed independently; it is not bundled into or promoted by this submission.

## 10. Validation Gates

### Automated

- Existing repository tests and all 21 skill tests pass.
- Official local skill and plugin validators pass.
- Submission checker validates metadata limits, asset existence, HTTPS links, prompt limits, exact reviewer-test counts, prohibited commerce copy, required legal files, and bundle inventory.
- Publication privacy checker reports zero findings.
- Cross-platform tests do not assume Windows fonts or Word Desktop.
- The submission ZIP is reproducible from the same source tree and has a recorded SHA-256 digest.

### Manual

- Review icon/logo legibility in light and dark backgrounds.
- Review English and Arabic listing copy as a non-developer user.
- Install the candidate from a disposable marketplace and invoke it in a fresh task.
- Run the eight reviewer cases and inspect generated artifacts.
- Confirm the listing does not overclaim Word Desktop, privacy, or commerce capability.

## 11. External-Action Gates

The agent may implement, test, package, commit, and prepare GitHub changes under the user's existing approval. It must stop and request Ahmed's current confirmation before:

- uploading identity documents;
- selecting or attesting a legal publisher identity;
- accepting OpenAI policy attestations;
- submitting the plugin for OpenAI review;
- publishing an approved plugin to the universal directory;
- purchasing services, registering a business, or configuring payment/tax accounts.

## 12. Acceptance Criteria

This readiness phase is complete when:

- the exact candidate commit passes repository, skill, plugin, privacy, submission, and clean-room tests;
- the plugin manifest meets current directory limits and references real public assets and policy pages;
- the eight reviewer cases and starter prompts are complete and reproducible;
- the skills-only ZIP and SHA-256 evidence are generated from the candidate commit;
- local marketplace installation is demonstrated in a fresh task or explicitly documented as awaiting the one required app restart/user action;
- the public GitHub repository contains the reviewed candidate changes;
- the remaining user-only steps are limited to identity/publisher choices, attestations, `Submit for Review`, OpenAI review, and `Publish`.

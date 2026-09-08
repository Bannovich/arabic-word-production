# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Renamed the user-facing plugin to `Arabic DOCX RTL` while preserving the stable `arabic-word-production` package and Skill identifiers.
- Replaced the directory branding with separate square logo and Composer assets using the approved document, left-pointing RTL arrow, and validation-check concept.
- Updated the interface color to the Eshtery-inspired purple `#4E249F` and prepared package version `0.1.1`.

### Added

- A public contribution path for future sanitized RTL failures and reusable guardrails.
- A publication guardrail that rejects stale private-to-public transition wording in both READMEs.
- Plugin Directory-ready public metadata, policy pages, reviewed identity assets, and a privacy-safe submission contract checker.
- Five positive and three negative synthetic reviewer cases for the initial skills-only directory candidate.
- Deterministic Skill and plugin ZIP builders with stable inventories and SHA-256 digests.
- A disposable local marketplace workflow that was validated and installed through the Codex CLI without modifying the personal marketplace file.
- A post-publication checkpoint recording the merged readiness Pull Request, six passing CI jobs, and live GitHub Pages policy URLs.
- A privacy-safe fresh-task smoke-test record proving plugin-qualified activation, exact candidate-file matching, structural and accessibility QA, reopen stability, and the unavailable visual-validation surface.
- A publication guardrail that distinguishes complete task-turn latency from pipeline-only timing and rejects impossible renderer claims.

### Fixed

- Distinguished the published plugin baseline from the pending identity update in current public documentation.
- Removed the obsolete branding generator that could overwrite reviewed identity assets; retained regeneration guidance in `assets/BRANDING.md`.
- Added PNG integrity, dimension, file-size and duplicate-content submission safeguards with regression tests.
- Added a portable local continuation checkpoint and instructions to refresh it after each milestone.

- Replaced pre-publication installation wording after the repository became public.
- Pinned text and binary Git attributes so clean checkouts produce reproducible submission bundles across operating systems.
- Enforced square Plugin Directory branding assets and separate logo/Composer paths.

## [0.1.0] - 2026-08-27

### Added

- The initial Arabic Word Production Agent Skill.
- A deterministic JSON-to-DOCX builder and structural OOXML auditor.
- RTL, table-direction, routing, recovery, QA, and performance references.
- A known-error taxonomy and guardrail library.
- A bundled Arabic Word template and synthetic regression utilities.
- Unit and regression tests for the document model, renderer, and auditor.
- ChatGPT and Codex plugin packaging through `.codex-plugin/plugin.json`.
- Bilingual English and Arabic onboarding, Apache-2.0 licensing, and project governance foundations.

This release does not claim universal Microsoft Word compatibility. Verification claims remain limited to the exact tools and surfaces named in release evidence.

[Unreleased]: https://github.com/Bannovich/arabic-word-production/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Bannovich/arabic-word-production/releases/tag/v0.1.0

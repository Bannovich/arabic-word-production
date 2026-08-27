# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A public contribution path for future sanitized RTL failures and reusable guardrails.
- A publication guardrail that rejects stale private-to-public transition wording in both READMEs.

### Fixed

- Replaced pre-publication installation wording after the repository became public.

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

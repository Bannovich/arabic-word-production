# Architecture decisions

This file records material decisions for `v0.x`. Each entry can be superseded by a later dated decision, but historical entries remain for context.

## ADR-001: Keep one canonical Skill

- **Status:** Accepted — 2026-08-27
- **Context:** Duplicate Skill copies drift and make it unclear which tests or instructions define the release.
- **Decision:** Keep the only canonical Skill at `skills/arabic-word-production/`. The repository-level plugin manifest points to `./skills/`.
- **Consequences:** Standalone Skill users and plugin users share the same files. Publication checks reject a missing canonical path.

## ADR-002: Model RTL as independent properties

- **Status:** Accepted — 2026-08-27
- **Context:** Alignment, paragraph direction, run direction, table order, and section geometry have different OOXML meanings.
- **Decision:** Represent and audit each layer explicitly. High-risk paragraphs retain direct direction on fresh builds even when named styles carry the same intent.
- **Consequences:** The implementation is more verbose than right-aligning content, but failures are observable and repairable.

## ADR-003: Use logical-start paragraph alignment

- **Status:** Accepted — 2026-08-27
- **Context:** Physical `right` or logical `end` paired with `w:bidi=1` can display on the visual left in Word Desktop.
- **Decision:** Use `w:jc=start` for ordinary leading-edge RTL and LTR paragraphs. Centered content remains explicitly centered.
- **Consequences:** Reviewers must reason in logical edges, not UI labels alone.

## ADR-004: Preserve table source order

- **Status:** Accepted — 2026-08-27
- **Context:** Reversing cells manually corrupts logical data and may be reversed a second time by a renderer.
- **Decision:** Store cells in logical source order and use `w:bidiVisual` for Arabic table display. Keep `tblGrid`, total width, and cell widths consistent.
- **Consequences:** Data comparisons remain stable and table direction is independently testable.

## ADR-005: Ship a skills-only plugin first

- **Status:** Accepted — 2026-08-27
- **Context:** The core workflow needs instructions and local scripts, not an external service or user account.
- **Decision:** Package the Agent Skill in `.codex-plugin/plugin.json` without MCP or App dependencies for `v0.1.0`.
- **Consequences:** The plugin has a smaller trust surface and can be used offline after dependencies are installed. Universal directory submission remains a later decision.

## ADR-006: Use synthetic public evidence

- **Status:** Accepted — 2026-08-27
- **Context:** Raw conversations and real documents can contain personal, client, contractual, or credential data in text, media, comments, relationships, or Office metadata.
- **Decision:** Public Issues, tests, and releases use synthetic or rigorously sanitized fixtures. The publication checker inspects repository text and DOCX core properties.
- **Consequences:** A failure that cannot be reproduced safely may be documented but cannot contribute its confidential source file.

## ADR-007: Bound recovery

- **Status:** Accepted — 2026-08-27
- **Context:** Repeating local mutations can consume time without establishing correctness.
- **Decision:** Allow one targeted repair and one retry per invariant; then clean-rebuild, use a validated fallback, request missing input, or disclose the limitation.
- **Consequences:** The workflow stops deterministic failure loops and makes latency data meaningful.

## ADR-008: Scope every validation claim

- **Status:** Accepted — 2026-08-27
- **Context:** Package creation, OOXML auditing, rendering, and Word Desktop behavior are different evidence surfaces.
- **Decision:** Use the vocabulary `Built`, `Structurally audited`, `Rendered and inspected`, and `Word Desktop verified`, always naming the exact surface used.
- **Consequences:** Releases may look less absolute, but users can judge the evidence accurately.

## ADR-009: Treat speed as a measured guardrail

- **Status:** Accepted — 2026-08-27
- **Context:** A fixed time promise is not credible across document complexity and environments.
- **Decision:** Use 120 seconds as an error threshold for routine FAST documents, record actual metrics, and never weaken QA to meet it.
- **Consequences:** Performance work becomes reproducible while correctness remains the release gate.

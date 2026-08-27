# How Arabic Word Production was built

This is a public engineering record, not a transcript of private conversations or hidden model reasoning. It records decisions in a reusable form: `Problem -> Evidence -> Experiment -> Result -> Decision -> Regression protection`.

## 1. Define the failure precisely

**Problem:** Arabic documents could appear right-aligned in one preview while behaving as LTR or shifting in Microsoft Word Desktop.

**Evidence:** WordprocessingML separates paragraph base direction, paragraph alignment, run direction, table visual order, and section geometry. A single visual alignment setting cannot represent all five.

**Experiment:** Inspect generated OOXML and compare combinations of `w:bidi` and `w:jc` in the target application.

**Result:** `w:bidi=1` with logical `w:jc=start` produced the intended leading edge for ordinary RTL paragraphs. Pairing RTL with physical `right` or logical `end` could place content on the visual left in Word Desktop.

**Decision:** Treat right alignment as neither proof nor a substitute for RTL. Use explicit paragraph direction and logical-start alignment.

**Regression protection:** `ERR-RTL-001` and `ERR-RTL-003`, structural audit rules, renderer checks, and a documented Word Desktop protocol.

## 2. Separate direction layers

**Problem:** URLs, code, formulas, and English identifiers could reorder inside otherwise-correct Arabic paragraphs.

**Evidence:** Paragraph base direction and run direction are separate OOXML properties.

**Experiment:** Keep the paragraph RTL while isolating technical spans as explicit LTR runs.

**Result:** The source text could remain in Unicode logical order without reversing Arabic strings.

**Decision:** Classify paragraphs and runs independently. Never manually reverse Arabic text to force a visual result.

**Regression protection:** `ERR-RUN-001`, mixed-run fixtures, and the effective-direction audit.

## 3. Preserve logical table data

**Problem:** Arabic tables could display their first semantic column on the wrong side, or developers could “fix” them by reversing cell data.

**Evidence:** `w:tblPr/w:bidiVisual` controls table visual order independently of the stored logical cell order.

**Experiment:** Keep cells in source order, set `w:bidiVisual`, and make `tblGrid`, table width, and cell widths agree.

**Result:** The logical dataset remained stable while the table displayed from the intended RTL side.

**Decision:** Set table direction explicitly and never combine it with manual source-cell reversal. Use semantic width weights rather than equal widths by default.

**Regression protection:** `ERR-TABLE-001` through `ERR-TABLE-003`, geometry checks, and all-page rendering.

## 4. Make fields and round trips stable

**Problem:** Page fields or a Word save could introduce warnings or remove apparently required direct formatting.

**Evidence:** Enabling `w:updateFields=1` could trigger a field-update warning. Word Desktop can also normalize direct properties that are already supplied by paragraph styles.

**Experiment:** Keep local `PAGE / NUMPAGES` fields centered and LTR without `w:updateFields=1`; save and reopen copies while resolving style inheritance.

**Result:** The correct test was effective formatting after inheritance, not byte-for-byte XML equality.

**Decision:** Omit update-on-open, use stable local fields, and audit direct properties, `pStyle`, `basedOn`, document defaults, then normal defaults.

**Regression protection:** `ERR-FIELD-001`, `ERR-STYLE-002`, `ERR-REOPEN-001`, and reopen auditing.

## 5. Bound repairs and measure work

**Problem:** Repeated paragraph-by-paragraph fixes made document generation slow and could hide a structurally broken file.

**Evidence:** A deterministic source model allows a clean rebuild; repeated mutation does not improve confidence.

**Experiment:** Route work as FAST, STRUCTURED, or COMPLEX, then allow one targeted repair and one retry per invariant.

**Result:** Failures have a clear next action: deterministic repair, clean rebuild, validated fallback, or disclosed limitation.

**Decision:** Enforce bounded recovery and record elapsed time, builds, repairs, fallbacks, QA failures, route, renderer, and Word Desktop status. The routine sub-two-minute target is subordinate to quality.

**Regression protection:** `ERR-LATENCY-001`, the recovery ladder, and per-document performance JSON.

## 6. Package one canonical implementation

The open-source project was created from an existing local Skill through these reviewable steps:

1. Approve a public design covering scope, privacy, licensing, governance, repository structure, and release gates.
2. Scaffold a standards-compliant plugin root with the official Plugin Creator helper.
3. Copy the existing 17-file Skill into `skills/arabic-word-production/` and compare relative paths and SHA-256 hashes.
4. Replace scaffold metadata with the `v0.1.0` identity and Apache-2.0 license declaration.
5. Run the official Skill and plugin validators.
6. Run the existing 21-test baseline before adding publication-specific behavior.
7. Add bilingual onboarding, governance, privacy rules, Issue workflows, and repository quality checks.
8. Build only synthetic release fixtures, run every gate against the exact candidate commit, review the private GitHub repository, and make it public only after the evidence passes.

The canonical implementation remains under `skills/arabic-word-production/`. The repository-level plugin manifest points to that directory rather than duplicating it.

## 7. Preserve future engineering history

New discoveries should update the error taxonomy, guardrails, tests, compatibility matrix, changelog, and when material, the architecture decisions. Record observable evidence and decisions. Do not publish client source data, private conversations, credentials, or unverifiable internal reasoning.

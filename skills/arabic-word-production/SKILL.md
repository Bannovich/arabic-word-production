---
name: arabic-word-production
description: Use when creating or repairing Microsoft Word DOCX files that are Arabic-first, bilingual Arabic-English, RTL, mixed-direction, or render differently in Word than in preview.
---

# Arabic Word Production

## Core principle

Treat alignment, paragraph direction, run direction, table order, and page geometry as separate properties. A right-aligned paragraph is not necessarily RTL, and a correct preview is not proof of Microsoft Word Desktop behavior. In WordprocessingML, use logical `w:jc=start` for the normal leading edge: with `w:bidi=1` Word displays it on the visual right, while `right` or `end` can display an RTL paragraph on the visual left.

**REQUIRED SUB-SKILL:** Use `documents:documents` for the general DOCX creation/editing and render-inspection workflow. Use this skill for the Arabic/mixed-language decisions and its deterministic fast-path tools.

## Route the request

- **FAST:** Short prose, headings, lists, and tables up to five columns, without mixed sections or several visuals. Prefer `scripts/build_docx.py` from a small JSON model, then run `scripts/audit_docx.py` once.
- **STRUCTURED:** Long reports, citations, several tables, or images. Read [QA and performance](references/qa-and-performance.md), then build, audit, render every page, and reopen-check.
- **COMPLEX:** Six-plus-column tables, mixed orientations, many objects, or appendices. Also read [routing and recovery](references/routing-and-recovery.md) before authoring.

If direction or OOXML behavior is uncertain, read [RTL and OOXML](references/rtl-ooxml.md). For known failures, consult the [error taxonomy](references/error-taxonomy.md) and [guardrails](references/guardrails.md).

## Non-negotiable output contract

1. Arabic or mixed paragraphs have an explicit RTL base direction, either directly or through a named paragraph style; English-only paragraphs resolve to LTR. The auditor must resolve the full paragraph-style inheritance chain because Word can remove redundant direct properties during save.
2. URLs, code, formulas, and technical LTR spans remain LTR even inside RTL paragraphs.
3. Arabic tables use RTL visual order. Column widths follow content semantics; wide tables trigger landscape evaluation.
4. Images are inline by default, preserve aspect ratio, stay inside the text width, and keep captions adjacent.
5. Use reusable styles for titles, headings, bodies, tables, captions, notes, and warnings.
6. Every section has a title header and a stable centered LTR `PAGE / NUMPAGES` footer. Do not set `w:updateFields=1`; it can trigger a Word warning on open.
7. Run structural audit after every build. Render and inspect every page when a renderer is available.
8. State the actual validation surface. Never call a file Word Desktop-verified unless Word Desktop opened it.
9. Apply at most one targeted repair and one validated retry for the same invariant; then clean-rebuild or disclose the limitation.

## Fast-path commands

```powershell
python scripts/build_docx.py model.json output.docx
python scripts/audit_docx.py output.docx --out-json audit.json
```

Record elapsed time, builds, repairs, fallbacks, QA failures, final route, and renderer used. The sub-two-minute target is a performance goal for routine FAST work, never permission to skip correctness checks.

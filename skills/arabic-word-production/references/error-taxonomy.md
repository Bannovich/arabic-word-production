# Error taxonomy

| ID | Symptom | Detection | Correct response | Recovery |
|---|---|---|---|---|
| ERR-RTL-001 | Arabic/mixed paragraph lacks explicit RTL base direction | OOXML audit for `w:bidi` | Apply native paragraph direction through style and direct property | Targeted repair, one retry |
| ERR-RTL-002 | English-only paragraph inherits RTL or mixed text orders badly | Classify source text; inspect `w:bidi` value and render | Set explicit LTR paragraph; keep source in logical order | Targeted repair |
| ERR-RTL-003 | An RTL paragraph is visually placed on the left despite being set to “right” | Audit `w:bidi=1` with `w:jc=right` or `end`; confirm in Word Desktop | Use logical `w:jc=start`; do not infer logical alignment from the physical edge name | Targeted repair |
| ERR-RUN-001 | URL/code/formula order breaks inside Arabic text | Inspect runs and visual output | Split the technical span and set `w:rtl=0` | Targeted repair |
| ERR-TABLE-001 | Arabic table displays columns from the wrong side | Audit `w:bidiVisual` | Set RTL visual order without reversing source cells | Targeted repair |
| ERR-TABLE-002 | Wide table wraps into unreadable fragments | Geometry audit and render | Landscape, semantic split, or annex; keep type at least 8 pt | Rebuild layout |
| ERR-TABLE-003 | Equal widths waste space or crush descriptive columns | Compare grid widths with content semantics | Provide semantic `width_weights`; fix grid and cell widths together | Targeted rebuild |
| ERR-STYLE-001 | LTR defaults or direct formatting override Arabic styles | Inspect styles and paragraph properties | Use named RTL/LTR styles plus explicit high-risk direction | Clean rebuild if widespread |
| ERR-STYLE-002 | A Word-saved file appears to lose direct RTL properties although it still renders correctly | Resolve `pStyle`, `basedOn`, document defaults, then direct/default bidi semantics | Fix the auditor to evaluate effective formatting; do not reinsert redundant properties blindly | Auditor repair and round-trip recheck |
| ERR-LIST-001 | Arabic numbering appears on the wrong side or is typed manually | Inspect numbering/style XML and render | Use genuine Word numbering and RTL list paragraphs | Targeted rebuild |
| ERR-SECTION-001 | Wrong orientation, header/footer loss, or blank page | Section audit and all-page render | Recreate bounded sections and restore portrait explicitly | Clean rebuild |
| ERR-FIELD-001 | Word shows a field/external-link warning on open | Audit `word/settings.xml` for enabled `w:updateFields` | Remove the setting; keep page fields local, centered, and LTR | Targeted repair |
| ERR-IMAGE-001 | Image floats, overflows, stretches, or leaves caption | Drawing audit and render | Use inline placement, cap width, preserve ratio, adjacent caption | Targeted repair |
| ERR-IMAGE-002 | Image/media is missing, broken, cropped, or too low resolution | Relationship/media audit and 200% render | Restore source asset; do not invent missing content | Block until source exists |
| ERR-FONT-001 | Requested Arabic font silently falls back | Inspect embedded/declared font properties and renderer output | Use supported fonts, set `w:cs`, and disclose fallback risk | Rebuild styles |
| ERR-RENDER-001 | Preview looks correct but target application differs, or no renderer exists | Compare validation surfaces | Render with available engine; state limitation when unavailable | Disclosure or alternate route |
| ERR-REOPEN-001 | Save/reopen changes effective structure or layout | Round-trip copy, resolve style inheritance, and re-audit | Distinguish harmless Word normalization from an effective formatting change; rebuild only for the latter | Auditor repair or clean rebuild |
| ERR-CONTENT-001 | `TBD`, `TODO`, or placeholder remains | Text audit | Replace from source or block for missing input | Block if source missing |
| ERR-CONTENT-002 | Internal citation/reference token leaks into DOCX | Text audit | Replace with human-readable citation or remove non-content token | Targeted repair |
| ERR-CONTENT-003 | Source-model heading, paragraph, list item, cell, or caption is missing | Compare normalized model text with the final DOCX | Restore the omitted block and rebuild | Targeted rebuild |
| ERR-PACKAGE-001 | DOCX path missing | File check | Correct the resolved output path | Retry build |
| ERR-PACKAGE-002 | `word/document.xml` missing | ZIP/package audit | Rebuild a valid DOCX package | Clean rebuild |
| ERR-PACKAGE-003 | ZIP or XML is invalid | Package parser | Discard corrupt file and clean-rebuild | Clean rebuild |
| ERR-QA-001 | Completion claim exceeds performed validation | Compare report with tool evidence | Rewrite claim to name actual validation surface | Report correction |
| ERR-LATENCY-001 | Routine FAST document exceeds 120 seconds | Wall-clock record | Reuse template/tools, batch audits, remove redundant discovery | Optimize; never skip QA |

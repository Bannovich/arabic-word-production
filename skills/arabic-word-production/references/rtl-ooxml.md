# RTL, LTR, and WordprocessingML

## Independent direction layers

| Layer | WordprocessingML | Meaning |
|---|---|---|
| Paragraph base direction | `w:pPr/w:bidi` | Controls paragraph-level bidirectional layout; use true for Arabic/mixed, false for English-only |
| Paragraph alignment | `w:pPr/w:jc` | Uses a logical edge after `w:bidi` is applied; use `start` for normal leading-edge alignment |
| Run direction | `w:rPr/w:rtl` | Controls a text span; use false for URLs/code/formulas and true for Arabic spans |
| Table visual order | `w:tblPr/w:bidiVisual` | Displays the first logical column at the right in an Arabic table |
| Section geometry | `w:sectPr/w:pgSz` and `w:pgMar` | Controls page size/orientation and the usable text width |

Use explicit `w:val="1"` or `w:val="0"` when the opposite direction might be inherited. Right alignment alone never satisfies the direction contract.

## Word Desktop alignment rule

Use `w:jc w:val="start"` for ordinary RTL and LTR paragraphs. In an actual Word Desktop diagnostic matrix:

- `w:bidi=1` plus `start` displayed on the visual right.
- `w:bidi=1` plus `left` also displayed on the visual right, but it encodes a physical edge rather than the intended logical rule.
- `w:bidi=1` plus `right` or `end` displayed on the visual left.

Therefore, never pair an RTL paragraph with `right` or `end` merely because the desired visual placement is the right side. Keep centered content, such as page-number footers, explicitly LTR and centered.

For local `PAGE` and `NUMPAGES` fields, omit `w:updateFields=1`. Word Desktop can show an external-field update warning on open when that flag is present. Let normal pagination refresh the fields, and verify them during the Word save/reopen check.

## Classification

- Any Arabic-script character makes an `auto` paragraph RTL unless the block is explicitly code, URL-only, formula, or English-only.
- Keep the full Arabic/mixed paragraph RTL. Split long URLs into their own LTR run.
- For short English product names inside normal Arabic prose, prefer a stable paragraph base plus conservative run splitting. Do not reorder the source string manually.
- Preserve Unicode text in logical order. Let Word's bidirectional algorithm render it; do not reverse Arabic strings or table columns in source data.

## Styles

Create named paragraph styles and also apply explicit direction to high-risk paragraphs. Useful style names include:

- Arabic Title RTL
- Arabic Heading 1 RTL
- Arabic Heading 2 RTL
- Arabic Body RTL
- Arabic Mixed Body RTL
- English Body LTR
- English Technical LTR
- Source URL LTR
- Arabic Table Header RTL
- Arabic Table Body RTL
- Caption, Note, Warning

Set both ordinary fonts (`w:ascii`, `w:hAnsi`) and complex-script fonts (`w:cs`). A font name in source is not evidence that the renderer actually used the font.

Word Desktop may remove a paragraph's direct `w:bidi` and `w:jc=start` during save when the same effective direction is supplied by its paragraph style or by the logical default. A round-trip auditor must therefore resolve, in order: direct paragraph properties, the assigned style, each `w:basedOn` ancestor, document paragraph defaults, then the normal default (`bidi=false`, `jc=start`). Do not report a missing-direction error merely because the direct property was normalized away.

## Lists and tables

- Use genuine Word numbering/list styles; do not simulate lists by typing numbers into ordinary paragraphs.
- Set paragraph direction on every list item.
- Keep table XML cells in logical source order and set `w:bidiVisual`; do not both reverse cells and set RTL visual order.
- Set `tblGrid`, table width, and every cell width consistently. Disable autofit for deterministic semantic widths.

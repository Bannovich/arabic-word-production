# QA and performance

## Required gate sequence

Before a new environment is used for production work, run `scripts/check_environment.py`. It is read-only: it reports required Python modules, optional renderers, and whether Word Desktop is detectable. A detected Word Desktop installation is not proof that any output has been opened or verified there.

1. **Content:** Compare headings, paragraphs, list items, table cells, links, captions, and images to the source model. Reject placeholders and internal citation tokens.
2. **Structure:** Run `scripts/audit_docx.py output.docx --model model.json`. Confirm content completeness, explicit paragraph direction, logical-start alignment, run exceptions, table RTL order, sections, stable page fields, disabled update-on-open behavior, media, and package validity.
3. **Reopen:** Open with `python-docx`, save to a temporary copy, and rerun the structural audit. Resolve effective direction through paragraph-style inheritance when direct properties are absent. This proves package stability, not Word Desktop rendering.
4. **Render:** Use the general Documents skill renderer. Inspect every page at 100%; for images also inspect at 200%.
5. **Application surface:** If Word Desktop is accessible, open, confirm that no field-update warning appears, inspect direction and page fields, Save As a round-trip copy, close, reopen, then re-audit the Word-saved package. Word may normalize redundant direct formatting; judge effective semantics and the target rendering, not byte-for-byte XML equality. If Word is not accessible, say so.

## Visual checklist

- No clipping, overlap, boundary-hugging text, or blank pages.
- Arabic punctuation, parentheses, currency, and English terms read in the intended order.
- Lists number from the correct side.
- Table headers repeat; columns are readable; short-value columns are not oversized.
- Landscape is limited to intended sections; headers/footers remain present.
- Images are not stretched, cropped, blurred, floating unexpectedly, or detached from captions.
- Headings do not sit alone at page bottoms; tables and figures do not create avoidable large gaps.

## Performance record

Record one JSON object per document:

```json
{
  "route": "FAST",
  "started_at": "ISO-8601",
  "ended_at": "ISO-8601",
  "elapsed_seconds": 0.0,
  "builds": 1,
  "repairs": 0,
  "fallbacks": 0,
  "qa_failures": [],
  "pages": null,
  "renderer": "unavailable",
  "word_desktop_tested": false
}
```

Use `null` or `unavailable` for unobserved values. Do not estimate. A routine FAST run above 120 seconds is `ERR-LATENCY-001`; keep the file if correct, then optimize the pipeline separately.

## Performance guardrails

- Discover tools once, then reuse resolved paths.
- Build from one source model rather than mutating many paragraphs interactively.
- Batch structural checks in one audit call.
- Render after meaningful layout batches, not after harmless metadata-only changes.
- Invoke fallback immediately after the bounded repair limit; do not spend time in an unbounded loop.

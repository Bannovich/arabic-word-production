# Routing and bounded recovery

## Route before authoring

| Route | Observable criteria | Build and QA budget |
|---|---|---|
| FAST | Short content; headings/lists; tables up to 5 columns; no mixed orientation; at most one simple inline image | One build, one structural audit, one render pass if available |
| STRUCTURED | Long report; citations; several tables; mixed Arabic/English; one or more images | One build, structural audit, all-page render inspection, reopen check |
| COMPLEX | 6+ columns; portrait plus landscape; many figures; appendices; object-heavy layout | Plan sections first; audit after each layout-sensitive batch; all-page render inspection |

Upgrade the route when actual content crosses a criterion. Do not downgrade after hidden complexity appears.

## Table decision

1. Derive column weights from semantics or provide `width_weights` explicitly.
2. For six or more columns, evaluate landscape before building.
3. Keep at least 8 pt body type. If the table remains cramped, split it at a semantic boundary or move detail to an annex.
4. Repeat the header row and prevent row splitting where practical.
5. Preserve one logical dataset as one coherent table unless a labeled split improves readability.

## Recovery ladder

| State | Next action |
|---|---|
| One structural invariant fails | Apply one deterministic fix scoped to that invariant |
| Same invariant fails after retry | Clean-rebuild from the source model |
| Native rebuild still fails and a Google Docs route is available | Use Google Docs native intermediate, export once, and rerun all applicable gates |
| No reliable renderer or app is available | Deliver only after structural checks and disclose the missing validation surface |
| Content is incomplete or a required image is unavailable | Stop and request the missing source; do not invent it |

Do not apply repeated paragraph-by-paragraph patches to a structurally broken file. Keep source content outside the DOCX so a clean rebuild is cheap.

## Stop conditions

- Maximum one targeted repair plus one retry per error ID.
- A second failure of the same ID triggers rebuild, fallback, or documented limitation.
- Never weaken a gate to meet the timing target.
- Never claim successful fallback unless the exported DOCX was audited and rendered again.

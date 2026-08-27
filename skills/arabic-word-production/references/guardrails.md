# Permanent guardrails

## Direction and styles

1. Right alignment is not proof of RTL; require explicit paragraph direction.
2. Use logical `w:jc=start` for normal paragraphs. With `w:bidi=1`, never use `right` or `end`; Word Desktop can place them on the visual left.
3. English-only paragraphs are explicitly LTR, not left to inherited document defaults.
4. URLs, code, formulas, and technical identifiers are LTR runs inside RTL paragraphs.
5. Never reverse Arabic strings or manually reverse table cells.
6. Reusable styles carry fonts, spacing, hierarchy, keep-with-next, and direction; avoid mass direct formatting.
7. Set complex-script font properties as well as Latin font properties.
8. On a freshly generated file, keep explicit direct direction on high-risk paragraphs. After a Word save, audit the effective property through `pStyle`, `basedOn`, and document defaults because Word may remove redundant direct properties.

## Tables and sections

9. Arabic tables require `w:bidiVisual`.
10. Use semantic column weights; heterogeneous columns are not equal-width by default.
11. Six-plus-column tables trigger landscape evaluation.
12. Repeat header rows, add usable cell padding, and prevent row splitting where practical.
13. Never reduce body text below 8 pt to force a table into the page.
14. After a landscape section, explicitly restore portrait before portrait content.
15. Give every section page chrome. Use a centered LTR `PAGE / NUMPAGES` footer; do not mix Arabic labels and dynamic fields in an RTL footer.
16. Omit `w:updateFields=1`; it can trigger Word Desktop's external-field warning on open.

## Images and objects

17. Inline is the default placement. Floating anchors require an explicit layout need and stricter cross-renderer inspection.
18. Cap width to the current section's text width and preserve aspect ratio.
19. Keep captions immediately after their image and add meaningful alt text.
20. Reject missing media, unexpected cropping, scaling above source resolution, and objects outside margins.

## QA, recovery, and claims

21. Preview success is diagnostic evidence, not Word Desktop proof.
22. Run the structural auditor on the final saved file with the source model supplied, not only an in-memory object.
23. Inspect every rendered page; do not spot-check final delivery.
24. A renderer's name must accompany the validation claim.
25. Maximum one targeted repair and one retry per invariant; then rebuild or disclose.
26. Do not call a file complete with placeholders, internal citation tokens, missing images, broken links, or unverified content.
27. Record exact elapsed time and unavailable metrics honestly.
28. Quality outranks the sub-two-minute performance target.

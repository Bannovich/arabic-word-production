# Arabic DOCX RTL branding

`Arabic DOCX RTL` is the user-facing plugin name. The repository, package, and Skill identifiers remain `arabic-word-production` so existing links, installs, and qualified Skill names do not break.

## Visual system

- Primary purple: `#4E249F`
- Accent blue: `#128DE0`
- Paper: `#FFFFFF`
- Core meaning: a Word-like document, an explicit left-pointing arrow for RTL flow, and a checkmark for structural validation
- Style: simple rounded geometry, strong contrast, and no embedded text

The palette and friendly rounded treatment are inspired by the Eshtery Sa7 visual family. The Eshtery Sa7 mark, wordmark, and distinctive symbol must never be copied or redrawn in this plugin.

## Production assets

| File | Role | Current dimensions | Small-size rule |
|---|---|---:|---|
| `logo.png` | Plugin Directory logo | 1254×1254 | May retain the document fold and two RTL-aligned lines |
| `icon.png` | Composer icon | 1254×1254 | Use only the bold document, left arrow, and validation check |

Both files are square PNGs, stay under 5 MiB, and use separate compositions. `logo-dark.png` is a legacy unreferenced asset and is not part of the current manifest.

## Regeneration prompts

Use the built-in ImageGen workflow and inspect every result before replacing a reviewed asset. Treat the approved directory logo as the edit target and any Eshtery Sa7 material as palette/style reference only.

### Directory logo

> Refine the approved square document logo while preserving the white document, explicit thick left-pointing RTL arrow, two right-aligned lines, and blue checkmark. Make the folded corner read as part of one coherent sheet. Use a clean flat vector-like treatment, full-bleed purple background with restrained blue-purple depth, pure white paper, deep-purple arrow and lines, and a bright-blue check. Keep a strong centered silhouette and safe margins. No text, letters, watermark, mockup, 3D treatment, hands, palms, extra symbols, or copied third-party mark.

### Composer icon

> Derive a bolder tiny-size icon from the approved directory logo. Use one uninterrupted white rounded document, one dominant thick left-pointing deep-purple arrow, and one compact bright-blue checkmark. Remove the fold, lines, thin strokes, and tiny details. Use a full-bleed purple square background and preserve strong readability at 48×48. No text, watermark, 3D treatment, extra symbols, or copied third-party mark.

## Release checklist

1. Confirm `.codex-plugin/plugin.json` keeps `name: arabic-word-production` and uses `displayName: Arabic DOCX RTL`.
2. Confirm `logo` points to `./assets/logo.png` and `composerIcon` points to `./assets/icon.png`.
3. Confirm both images are square, between 48×48 and 4096×4096, and no larger than 5 MiB.
4. Inspect the Directory logo at normal size and the Composer icon at approximately 48×48.
5. Run the repository tests, plugin validator, submission checker, and publication checker.
6. Treat an OpenAI portal update as a separate maintainer action; preparing these files does not publish them.

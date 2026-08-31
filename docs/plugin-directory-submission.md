---
layout: default
permalink: /plugin-directory-submission/
---

# Plugin Directory submission boundary

The initial directory candidate is a **skills-only** plugin. It packages the open-source `arabic-word-production` Skill and does not include MCP tools, authentication, commerce, advertisements, telemetry, or a project-operated data service.

Its public source of truth is the [GitHub repository](https://github.com/Bannovich/arabic-word-production). The candidate is prepared for directory review but is not represented as approved, listed, or endorsed until the host review process is completed and the publisher explicitly makes it public.

Directory listing metadata, reviewer cases, and release material are versioned in the repository. Reviewers and users should rely on the validation surface stated for each output instead of assuming universal Word compatibility.

## Public publication checkpoint

The reviewed readiness Pull Request, CI matrix result, and live GitHub Pages checks are recorded separately in [`release-evidence/plugin-directory-publication.json`](https://github.com/Bannovich/arabic-word-production/blob/main/release-evidence/plugin-directory-publication.json). Keeping that record separate preserves the candidate bundle digests and the immutable pre-publication evidence convention.

## Fresh-task functional checkpoint

The installed `0.1.0` candidate was invoked through its plugin-qualified Skill in a separate clean-room Codex task. The synthetic COMPLEX document passed the original structural audit, an independent reopen audit, all 14 supplemental feature checks, and an accessibility audit with no findings. The installed plugin's 77 files matched the recorded candidate bundle with no mismatches.

The timing result is intentionally split. The deterministic document pipeline took `0.695435` seconds from model preparation through final audit, but the complete task turn took `767.617` seconds. The user-visible sub-two-minute target was therefore **not met**; pipeline-only timing must not be presented as end-to-end latency.

LibreOffice was unavailable, so the attempted render produced no pages for visual inspection. Word Desktop was detected but was not opened or tested. The supported claim for this checkpoint is structural and accessibility validation only. The privacy-safe machine-readable record is [`release-evidence/plugin-directory-fresh-task-smoke.json`](https://github.com/Bannovich/arabic-word-production/blob/main/release-evidence/plugin-directory-fresh-task-smoke.json).

## Disposable local marketplace

Maintainers can build a temporary marketplace without editing a personal marketplace or Codex settings:

```powershell
python scripts/build_local_marketplace.py <new-or-empty-destination> .
```

The generated catalog is at `.agents/plugins/marketplace.json` under that destination and points to `./plugins/arabic-word-production`. It uses `AVAILABLE` installation policy, `ON_INSTALL` authentication policy, and the `Productivity` category. The copied plugin excludes local environments, Git metadata, caches, generated reports, and packaging metadata.

The temporary marketplace still requires an explicit local marketplace installation before it appears in the app. That step changes the user's Codex configuration, so it is kept separate from the read-only build and validation workflow.

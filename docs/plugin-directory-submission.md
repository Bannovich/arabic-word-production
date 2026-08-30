---
layout: default
permalink: /plugin-directory-submission/
---

# Plugin Directory submission boundary

The initial directory candidate is a **skills-only** plugin. It packages the open-source `arabic-word-production` Skill and does not include MCP tools, authentication, commerce, advertisements, telemetry, or a project-operated data service.

Its public source of truth is the [GitHub repository](https://github.com/Bannovich/arabic-word-production). The candidate is prepared for directory review but is not represented as approved, listed, or endorsed until the host review process is completed and the publisher explicitly makes it public.

Directory listing metadata, reviewer cases, and release material are versioned in the repository. Reviewers and users should rely on the validation surface stated for each output instead of assuming universal Word compatibility.

## Disposable local marketplace

Maintainers can build a temporary marketplace without editing a personal marketplace or Codex settings:

```powershell
python scripts/build_local_marketplace.py <new-or-empty-destination> .
```

The generated catalog is at `.agents/plugins/marketplace.json` under that destination and points to `./plugins/arabic-word-production`. It uses `AVAILABLE` installation policy, `ON_INSTALL` authentication policy, and the `Productivity` category. The copied plugin excludes local environments, Git metadata, caches, generated reports, and packaging metadata.

The temporary marketplace still requires an explicit local marketplace installation before it appears in the app. That step changes the user's Codex configuration, so it is kept separate from the read-only build and validation workflow.

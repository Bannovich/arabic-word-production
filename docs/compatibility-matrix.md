# Compatibility matrix

This matrix separates packaging, structural auditing, visual rendering, and application verification. `Not verified` means the project has not performed that exact release test; it does not mean the surface failed.

## `v0.1.0` candidate baseline

| Surface | Environment | Evidence | Status |
| --- | --- | --- | --- |
| Agent Skill structure | Official local Skill validator | `SKILL.md` frontmatter and required structure | Verified for candidate |
| Plugin package | Official local plugin validator | `.codex-plugin/plugin.json` and bundled Skill | Verified for candidate |
| Environment diagnostic | Python 3.10+ | Read-only check of `docx`, `lxml`, optional `soffice`, and Word Desktop availability | Available; reports the current machine only |
| Builder and structural auditor | Windows, Python 3.12, declared dependencies | Existing 21-test baseline plus release smoke fixture | Verified for candidate; final release evidence records exact commit |
| Publication privacy and structure | Windows 25H2 x64, build 26200.9168; Python 3.12.13 | Publication checker scanned the candidate repository with zero findings; all 12 checker and packaging-policy tests, both official package validators, and all seven GitHub YAML parses passed | Verified for the `v0.1.0` candidate; exact parent commit is recorded in release evidence |
| Microsoft Word Desktop on Windows | Windows 25H2 x64, build 26200.9168; Microsoft Word 16.0.20326.20100 | Opened and visually inspected all three pages; verified mixed RTL/LTR content, portrait-landscape-portrait sections, RTL tables, inline image, and `PAGE / NUMPAGES`; saved a round-trip copy in Word, closed, reopened, and re-audited it against the synthetic model with zero findings | Verified for the `v0.1.0` candidate |
| Microsoft Word Desktop on macOS | Exact version to be recorded | Equivalent application protocol | Not verified |
| Word Online | Browser and build to be recorded | Open and inspect synthetic release DOCX | Not verified |
| Google Docs import/export | Browser and date to be recorded | Import, inspect, export once, re-audit DOCX | Not verified |
| LibreOffice Writer | Exact version and operating system | Open, inspect, save copy, re-audit | Not verified |
| Other Agent Skills hosts | Host and version | Install, invoke, and run a synthetic task | Not verified |

## How to add evidence

Record:

- repository commit and release tag;
- SHA-256 of the exact DOCX fixture;
- operating system and application build;
- route and script versions;
- structural audit result;
- renderer name and all-page inspection result;
- Word or other application steps performed;
- any normalization after Save As;
- observed limitation.

Evidence for one build does not automatically apply to all earlier or later versions. Update this matrix only after the linked protocol is complete.

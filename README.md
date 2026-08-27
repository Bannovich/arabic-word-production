# Arabic Word Production

[العربية](README.ar.md) · [Contributing](CONTRIBUTING.md) · [Report a problem](https://github.com/Bannovich/arabic-word-production/issues)

Arabic Word Production is an open-source Agent Skill and plugin package for creating and auditing Arabic-first and bilingual Arabic-English Microsoft Word documents. It treats paragraph direction, run direction, table order, alignment, and page geometry as separate properties instead of assuming that right alignment is the same as RTL.

The project is intentionally deterministic: it includes a JSON-driven DOCX builder, a structural OOXML auditor, reusable guardrails, a known-error taxonomy, regression tests, and a bundled Word template. It is designed to help people improve one shared workflow instead of rediscovering the same RTL problems in separate chats.

> **Release status:** `v0.1.0` is an alpha release. It provides a tested structural workflow, not a promise that every DOCX will render identically in every Word version, printer driver, or third-party viewer.

## Quick start for non-developers

The easiest route in Codex is to ask the built-in Skill Installer to install this repository's skill:

```text
$skill-installer Install arabic-word-production from https://github.com/Bannovich/arabic-word-production/tree/main/skills/arabic-word-production
```

Start a new task after installation, attach or describe the content, and write:

```text
$arabic-word-production Create an Arabic-first Word document, then audit its RTL structure.
```

Until the repository is public, use the same request with the local folder instead of the GitHub URL.

### Manual standalone Skill installation

1. Download and unzip a release.
2. Copy `skills/arabic-word-production` into your local skills directory as `arabic-word-production`.
3. Restart Codex or start a new task so it reloads the Skill.

Typical personal locations are `%USERPROFILE%\.codex\skills\arabic-word-production` on Windows and `$CODEX_HOME/skills/arabic-word-production` when `CODEX_HOME` is configured.

### Local Plugin installation

This repository is already packaged as a plugin through `.codex-plugin/plugin.json`. For local testing, download the repository and ask `$plugin-creator` to wire the existing plugin folder into your personal marketplace. Restart the ChatGPT desktop app, open the Plugins Directory, select the local source, and install **Arabic Word Production**. Local marketplaces and the public universal Plugins Directory are separate distribution surfaces.

The plugin package contains only the Skill in this release; it does not require an MCP server or external account connection.

## Supported ways to use it

| Surface | Use | Status in `v0.1.0` |
| --- | --- | --- |
| ChatGPT desktop / Codex | Install or invoke the Agent Skill | Primary workflow |
| ChatGPT and Codex plugin hosts | Load the packaged plugin from a local marketplace | Packaged and manifest-validated |
| Compatible Agent Skills clients | Read `skills/arabic-word-production/SKILL.md` and bundled resources | Portable instructions; host behavior varies |
| Python 3.10+ | Run the deterministic builder and OOXML auditor directly | Supported command-line path |
| Microsoft Word Desktop | Open the generated DOCX output | Output target; verification must be reported per release or document |
| Other office suites | Open standards-based DOCX files | Best effort; rendering may differ |

## Direct script usage

Install the declared dependencies:

```powershell
python -m pip install .
```

Then work from the canonical Skill directory:

```powershell
cd skills/arabic-word-production
python scripts/build_docx.py model.json output.docx
python scripts/audit_docx.py output.docx --out-json audit.json
python -m unittest discover -s tests -v
```

The builder consumes the documented JSON model and writes a native DOCX. The auditor examines the OOXML package for paragraph, run, table, section, width, field, and media invariants. Read [the Skill instructions](skills/arabic-word-production/SKILL.md) before treating the scripts as a production pipeline.

## What a validation claim means

Use these labels precisely:

- **Built:** the DOCX package was created successfully.
- **Structurally audited:** automated OOXML checks passed for the tested invariants.
- **Rendered and inspected:** every rendered page was visually reviewed using the named renderer.
- **Word Desktop verified:** Microsoft Word Desktop opened the exact file and the stated checks were performed there.

A preview, PDF conversion, or structural audit alone is not Word Desktop verification. Release evidence and document handoffs should name the exact validation surface and disclose any skipped check.

## Privacy-safe problem reports

Issues are where new failures become reusable guardrails. Never upload client documents, raw ChatGPT conversations, personal data, credentials, contracts, or confidential screenshots to this public repository.

Instead:

1. Create a minimal synthetic DOCX or sanitized description that reproduces the behavior.
2. Remove names, logos, account numbers, URLs with private tokens, comments, tracked changes, and document metadata.
3. State the Word version, operating system, route used, expected result, actual result, and validation surface.
4. Use the appropriate Issue form. A maintainer can ask for more information without requesting confidential content.

## Known limitations

- RTL rendering can vary between Word Desktop versions, Word Online, Google Docs, LibreOffice, previewers, fonts, and printer drivers.
- The auditor checks explicit structural invariants; it cannot prove that prose is correct, accessible, legally sufficient, or visually polished.
- Wide tables, mixed orientations, floating objects, charts, equations, embedded files, tracked changes, and unusual fields may require the structured or complex route and manual inspection.
- The routine FAST route has a sub-two-minute performance goal, not a fixed deadline and never permission to skip quality checks.
- This release does not claim universal compatibility or official endorsement by Microsoft or OpenAI.

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md), then use an Issue form to propose a new guardrail, report a sanitized rendering problem, or suggest an improvement. Governance, support boundaries, security reporting, and the roadmap are documented separately so non-developers can contribute without learning the whole codebase first.

The project uses the [Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for attribution and trademark clarification.


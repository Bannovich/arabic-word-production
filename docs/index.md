---
layout: default
permalink: /
---

# Arabic Word Production

Arabic Word Production is a free, Apache-2.0 open-source Skill and plugin package for creating, repairing, and structurally auditing Arabic-first and Arabic-English Microsoft Word `DOCX` files.

It treats paragraph direction, run direction, table order, alignment, and page geometry as independent properties. Right alignment alone is not accepted as proof of native `RTL` behavior.

## What it does

- creates deterministic `DOCX` files from structured content;
- applies explicit Arabic and bilingual `RTL`/`LTR` semantics;
- audits OOXML structure for direction and layout invariants;
- produces evidence-scoped validation results; and
- turns safe, synthetic problem reports into reusable guardrails.

The project is a skills-only Plugin Directory candidate. It has no project-operated server, account connection, telemetry, checkout, subscription, or hosted data service.

## Important boundaries

Structural auditing and rendered inspection are not automatically Word Desktop verification. A file is only described as Word Desktop verified when the exact file was opened and checked in Word Desktop for that run.

The source, installation instructions, release history, and support channel are in the [GitHub repository](https://github.com/Bannovich/arabic-word-production).

- [Privacy Policy](/arabic-word-production/privacy-policy/)
- [Terms of Service](/arabic-word-production/terms-of-service/)
- [Plugin Directory submission boundary](/arabic-word-production/plugin-directory-submission/)

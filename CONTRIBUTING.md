# Contributing to Arabic Word Production

Thank you for helping make Arabic and bilingual Word documents more reliable. You do not need to be a developer to contribute. A precise, privacy-safe description of a failure can be as valuable as code.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md) and the [privacy and test-data policy](docs/privacy-and-test-data.md).

## Choose the right contribution path

- **A document renders incorrectly:** open the closest rendering Issue form after sanitizing the evidence.
- **A table, image, object, or performance route fails:** use its dedicated Issue form.
- **You have a workflow improvement:** use the improvement form and explain the problem it prevents.
- **You found a vulnerability, secret, or unsafe data exposure:** follow [SECURITY.md](SECURITY.md), not a public Issue.
- **You need help using the current release:** read [SUPPORT.md](SUPPORT.md).

## Non-developer contribution checklist

1. Reproduce the problem with a small synthetic document if possible.
2. Remove client names, logos, addresses, account data, confidential wording, credentials, comments, tracked changes, and identifying metadata.
3. Record the operating system, exact Word or viewer version, input route, expected result, actual result, and what was actually tested.
4. Attach only sanitized evidence. If safe evidence cannot be created, describe the structure instead of uploading the original file.
5. State whether the result was only built, structurally audited, rendered and inspected, or opened in Word Desktop.

Maintainers may close or redact reports that expose private data. Never send a confidential file just because someone asks for “the original.”

## From defect to guardrail

An accepted defect should become repeatable protection:

1. Assign or reuse an error ID from `skills/arabic-word-production/references/error-taxonomy.md`.
2. Document minimal reproduction evidence.
3. Add a failing automated test when the invariant is machine-checkable, or a precise manual Word protocol when it is not.
4. Make the smallest correction that addresses the demonstrated cause.
5. Run the relevant Skill tests, the publication checker, and any required visual or Word Desktop protocol.
6. Update the guardrail or reference documentation and the changelog when behavior changes.

See [Adding a guardrail](docs/adding-a-guardrail.md) for the full template.

## Development setup

Use Python 3.10 or newer:

```powershell
python -m pip install .
python -m unittest discover -s skills/arabic-word-production/tests -v
python -m unittest discover -s tests -v
python scripts/check_publication.py .
```

The canonical Skill lives only at `skills/arabic-word-production/`. Do not create a second copy elsewhere in the repository. Generated DOCX, PDF, PNG, audit JSON, and client artifacts must not be committed.

## Pull Request requirements

Keep each Pull Request focused on one defect or coherent improvement. Include:

- the linked Issue or stated problem;
- the evidence and root cause at the level needed to review the change;
- tests added or the manual verification protocol;
- commands run and their results;
- the exact validation surface, including Word Desktop version when used;
- privacy confirmation that fixtures and metadata are synthetic or sanitized;
- documentation and changelog updates when behavior changes.

Do not describe a preview as Word Desktop verification. Do not claim support for a viewer or Word version that was not tested.

All changes require maintainer review before merge. Passing automation is necessary but does not replace human review of privacy, claims, scope, and visual behavior.

## Commit and style guidance

- Prefer small commits with clear messages such as `fix: preserve RTL table visual order` or `test: reproduce mixed-run direction failure`.
- Keep Python compatible with the versions declared in `pyproject.toml`.
- Use `unittest` for the existing test suites unless a separately approved decision changes the test framework.
- Keep `SKILL.md` concise and route deep detail into `references/`.
- Preserve Arabic examples as synthetic text and keep technical identifiers in English when that makes the invariant clearer.

## Licensing

Unless explicitly stated otherwise, contributions are licensed under the repository's [Apache License 2.0](LICENSE). By submitting a contribution, you represent that you have the right to provide it under that license.

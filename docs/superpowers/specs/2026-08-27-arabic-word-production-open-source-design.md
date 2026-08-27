# Arabic Word Production Open-Source Project Design

**Status:** Approved in conversation on 2026-08-27; captured here for the required written review gate before implementation and publication.

## 1. Purpose

Turn the existing `arabic-word-production` Agent Skill into a maintained, public, open-source project owned by the GitHub account `Bannovich`. The project will preserve the existing deterministic Arabic-first and bilingual DOCX workflow while adding the documentation, governance, automated checks, contribution process, versioning, and OpenAI plugin packaging required for safe community use.

The public project must let a person report a Word/RTL failure without editing the stable workflow directly. Every accepted failure becomes reproducible evidence, a regression fixture or invariant, a narrowly scoped guardrail or implementation change, and a documented release entry.

## 2. Fixed Product Decisions

- Repository name: `arabic-word-production`.
- Repository owner: GitHub account `Bannovich`.
- Publication sequence: create and review as private, then change to public only after all publication gates pass.
- License: Apache License 2.0.
- Initial public maturity: `v0.1.0`, marked as an early public release rather than a universal Word compatibility guarantee.
- Distribution: the GitHub repository is the source of truth; the repository also contains a skills-only OpenAI plugin package.
- Skill name remains `arabic-word-production`.
- Automatic invocation remains enabled.
- Microsoft Word Desktop is the primary rendering target. Other renderers are documented compatibility surfaces, not substitutes for Word Desktop verification.

## 3. Scope

### In scope

- Preserve the current skill entrypoint, UI metadata, Word template, references, build/audit scripts, and tests.
- Package the skill under a valid `.codex-plugin/plugin.json` manifest.
- Publish bilingual project documentation, with English as the repository's broad contributor language and Arabic guidance for non-developer users.
- Document how the skill was created through verifiable engineering evidence: problem statements, hypotheses, experiments, observed outcomes, decisions, guardrails, tests, benchmarks, and known limitations.
- Add contribution, governance, support, security, and release policies.
- Add structured issue forms for RTL, table/layout, image/object, performance, compatibility, and general improvements.
- Add a pull-request template that requires a reproduced problem, privacy-safe fixture, test evidence, affected validation surfaces, and a changelog entry when behavior changes.
- Add automated checks for Python tests, skill validation, plugin validation, sensitive-data patterns, and package structure.
- Create a GitHub Project board for triage and release tracking if the connected GitHub surface permits it; otherwise document the exact board configuration for one-time creation in the GitHub UI.
- Create a private GitHub repository, upload the verified source, then make it public.
- Publish an initial GitHub release after the public repository matches the verified local commit.

### Out of scope for the initial release

- Publishing raw ChatGPT conversations, client documents, or unsanitized user samples.
- Claiming that LibreOffice, Google Docs, PDF renderers, or preview images prove Microsoft Word Desktop behavior.
- Shipping a standalone desktop application, hosted web service, PyPI package, Docker image, or paid support service.
- Submitting the plugin to OpenAI's public universal plugin directory during the initial GitHub release. The repository will be submission-ready, but public-directory submission remains a separate reviewed action because it can require identity, organization-role, policy, and portal attestations.
- Allowing unreviewed direct writes to the default branch.
- Publishing hidden chain-of-thought. The project publishes concise decision records and reproducible evidence instead.

## 4. Repository Architecture

```text
arabic-word-production/
|-- .codex-plugin/
|   `-- plugin.json
|-- skills/
|   `-- arabic-word-production/
|       |-- SKILL.md
|       |-- agents/openai.yaml
|       |-- assets/arabic-word-template.docx
|       |-- references/
|       |-- scripts/
|       `-- tests/
|-- docs/
|   |-- how-it-was-built.md
|   |-- architecture-decisions.md
|   |-- adding-a-guardrail.md
|   |-- compatibility-matrix.md
|   |-- privacy-and-test-data.md
|   |-- release-process.md
|   `-- superpowers/
|       |-- specs/
|       `-- plans/
|-- examples/
|   `-- sanitized/
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   |-- pull_request_template.md
|   |-- workflows/quality.yml
|   `-- CODEOWNERS
|-- README.md
|-- README.ar.md
|-- LICENSE
|-- NOTICE
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- GOVERNANCE.md
|-- CODE_OF_CONDUCT.md
|-- SECURITY.md
|-- SUPPORT.md
|-- ROADMAP.md
|-- pyproject.toml
`-- .gitignore
```

The canonical skill lives once under `skills/arabic-word-production/`. Project documentation must link to canonical references instead of copying their full content. Packaging files belong at repository level and must not be loaded as skill instructions.

## 5. Contribution and Failure-to-Guardrail Workflow

Every reported problem follows this lifecycle:

1. **Report:** A structured issue records the operating system, Word version, locale, content direction, object type, expected result, actual result, validation surface, screenshots, audit output, and whether a sanitized sample may be shared.
2. **Privacy triage:** Maintainers remove or reject personal data, client content, secrets, conversation identifiers, local absolute paths, and proprietary assets before accepting a public fixture.
3. **Reproduce:** A maintainer reproduces the structural or rendering symptom. If the symptom cannot be reproduced, the issue remains labeled `needs-reproduction` and no speculative universal rule is added.
4. **Classify:** The issue maps to an existing error ID or receives a narrowly scoped new ID.
5. **Regression evidence:** The change includes a failing behavioral test, fixture, or explicit manual Word Desktop test protocol appropriate to the failure surface.
6. **Minimal correction:** The implementation or guidance changes only what the reproduced failure justifies.
7. **Verify:** Structural tests, package checks, available rendering checks, and the stated application-surface checks run. Word Desktop claims require an actual Word Desktop test.
8. **Review and merge:** The pull request is reviewed against scope, privacy, compatibility, test evidence, and documentation requirements.
9. **Release:** The changelog and release notes connect the resolved issue, error ID, observable fix, and remaining limitations.

The default branch must be protected through repository rules when the account supports them. Contributions use branches and pull requests. The repository owner remains the final release authority.

## 6. Testing and Quality Gates

### Automated gates

- Run the existing Python unit and regression test suite on supported Python versions.
- Run OpenAI's skill validator against `skills/arabic-word-production/`.
- Run OpenAI's plugin validator against the repository root.
- Validate JSON/YAML/Markdown structure and reject unfinished scaffold markers.
- Run the existing deterministic DOCX builder and structural auditor against sanitized fixtures.
- Check that the final package contains the expected skill, plugin, template, references, scripts, and tests.
- Scan tracked text and Office package metadata for conversation IDs, user-profile paths, email-like secrets, tokens, private keys, and known client names.
- Ensure generated files, audit outputs, caches, and local test artifacts are not tracked.

### Manual gates

- Review README installation and contribution instructions as a non-developer user.
- Inspect every bundled example for privacy and licensing.
- Open the template and at least one generated validation document in the available rendering surfaces.
- State exactly which renderer or application was used.
- Do not mark `word_desktop_tested: true` unless Microsoft Word Desktop performed the test.

### Publication gate

The repository may change from private to public only when:

- all automated checks pass on the exact commit intended for publication;
- the skill and plugin validators pass;
- no secret or personal-data finding remains unresolved;
- Apache-2.0 licensing files are present;
- README files explain installation, scope, limitations, and privacy-safe reporting;
- contribution and security policies are present;
- the initial release notes do not overclaim compatibility;
- the private remote tree matches the verified local commit.

## 7. Privacy and Licensing Model

- Raw source conversations and user/client documents remain outside the repository.
- Public examples use synthetic or irreversibly sanitized content.
- A contributor must affirm that submitted fixtures contain no confidential information and that they have permission to contribute them.
- Sensitive reports use the security/private contact route rather than public issues.
- The Apache-2.0 license covers original project code and documentation.
- Third-party dependencies retain their own licenses and are listed as dependencies, not copied into the repository.
- The Word template is generated by project tooling and contains no personal author metadata or unlicensed embedded assets before publication.
- `NOTICE` credits Ahmed Elbanna as the project initiator and documents OpenAI/Codex only as compatible tooling, not as the project's owner or endorser.

## 8. Documentation Model

`README.md` gives the global overview, quick install paths, supported surfaces, a minimal usage example, limitations, contribution entrypoints, and release status. `README.ar.md` gives the same practical onboarding in Arabic without requiring developer knowledge.

`docs/how-it-was-built.md` records the engineering history without hidden chain-of-thought. Each substantial decision is expressed as:

```text
Problem -> Evidence -> Experiment -> Result -> Decision -> Regression protection
```

`docs/architecture-decisions.md` records durable choices such as logical-start alignment, explicit bidi semantics, bounded repair attempts, validation-surface claims, and the separation between structural and Word Desktop verification.

`docs/adding-a-guardrail.md` explains the exact contribution path from a reproducible failure to an error code, test, scoped change, and release note.

## 9. Release and Compatibility Policy

- Use semantic versioning beginning with `v0.1.0`.
- Patch releases fix compatible defects and documentation.
- Minor releases add validated capabilities, error classes, or supported environments.
- `v1.0.0` requires a stable contribution process, repeatable installation, a documented compatibility matrix, and sufficient independent usage evidence; it is not triggered by elapsed time alone.
- Every release names the tested Python versions, operating systems, renderers, and Word Desktop status.
- A compatibility statement is evidence-scoped. “Structurally audited” and “Word Desktop verified” are separate claims.

## 10. Distribution Model

The GitHub repository is usable in three forms:

1. A skills-only OpenAI plugin built from the repository root.
2. A standalone Agent Skill installable from `skills/arabic-word-production/` by compatible clients.
3. Direct execution of deterministic Python scripts by users or automation that do not invoke an AI agent.

The initial release prepares but does not submit the plugin to OpenAI's universal directory. Submission will follow a separate user-authorized review of listing copy, test cases, country availability, policy attestations, and identity or organization requirements.

## 11. Failure Handling

- If GitHub repository creation or visibility changes require an interactive account confirmation, stop at that precise action and request the minimum user interaction.
- If a publication gate fails, keep the repository private and report the failing gate; do not weaken the gate to finish publishing.
- If branch protection or GitHub Projects cannot be configured through the connected interface, publish the source only after documenting the one-time UI steps, then identify those settings as pending rather than claiming they are active.
- If a third-party renderer is unavailable, record it as unavailable and continue only with claims supported by performed checks.
- If the repository name is unexpectedly unavailable, stop before creating an alternate name.

## 12. Acceptance Criteria

The task is complete only when all of the following are true:

- `Bannovich/arabic-word-production` exists and is public.
- Its default branch contains the verified source tree described above.
- Apache-2.0 licensing is visible at repository level.
- The exact public commit passed the documented automated gates.
- The initial release is published with evidence-scoped notes.
- Issue forms, contribution guidance, governance, security reporting, support guidance, and the pull-request template are available.
- The skill validator, plugin validator, Python tests, and privacy scan pass.
- The final handoff includes the public repository URL, release URL, exact validation evidence, tested surfaces, and any GitHub settings that still require manual configuration.

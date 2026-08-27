# Governance

Arabic Word Production uses maintainer-led, evidence-driven governance. The goal is to accept improvements quickly without weakening privacy, reproducibility, or validation claims.

## Roles

### Users and reporters

Anyone may use the project, open privacy-safe Issues, suggest guardrails, or review documentation.

### Contributors

Contributors submit evidence, tests, documentation, code, or review. A contributor does not gain merge or release authority automatically.

### Maintainers

Maintainers triage Issues, moderate community spaces, review Pull Requests, merge changes, manage releases, and protect the project's scope and privacy rules.

`Bannovich` is the initial maintainer and release authority for `v0.x` releases.

## Decision process

Routine changes are decided through public Issues and Pull Request review. A behavioral change is accepted when it has:

- a scoped problem statement;
- privacy-safe reproduction evidence;
- a test or explicit manual verification protocol;
- an explanation of the validation surface;
- no unsupported compatibility claim;
- maintainer approval.

For material architecture, governance, licensing, privacy, or compatibility changes, the maintainer records the decision in `docs/architecture-decisions.md` or a new public decision document before merge. Decisions should use `Context -> Evidence -> Options -> Decision -> Consequences`, not hidden chain-of-thought.

If evidence is incomplete, the project may document an investigation without changing production behavior. Lack of agreement is not resolved by claiming broader support than the evidence shows.

## Release authority

Only a maintainer may create an official tag or GitHub Release. Releases follow [the release process](docs/release-process.md), including exact-commit verification, privacy scanning, tests, and evidence-scoped notes.

## Adding maintainers

An existing maintainer may invite a contributor after sustained, constructive participation that demonstrates:

- reliable privacy judgment;
- technically sound review or contributions;
- accurate validation claims;
- respectful community conduct;
- willingness to maintain tests, documentation, and triage, not only add features.

The invitation and acceptance are recorded publicly. New maintainers receive the minimum repository permissions needed. Maintainer status may be removed for inactivity after reasonable notice, repeated policy violations, compromised accounts, or conduct incompatible with the Code of Conduct.

## Conflicts of interest

Reviewers should disclose personal, commercial, or employment interests that could reasonably affect a decision. A conflicted maintainer should ask another qualified reviewer when one is available. Until the project has multiple maintainers, the conflict and reasoning for the final evidence-based decision must be recorded publicly without disclosing private information.

## Amendments

Governance changes require a public Pull Request, an explanation of why the change is needed, and maintainer approval. The changelog should mention material changes.

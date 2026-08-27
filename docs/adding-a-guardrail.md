# Adding a guardrail

A guardrail is a durable rule backed by evidence and regression protection. It is not merely advice added after one unexplained document failure.

## Required lifecycle

1. **Sanitize and reproduce.** Create the smallest synthetic input that demonstrates the failure. Record the target application and version.
2. **Classify.** Reuse an existing error ID when the cause and recovery match. Otherwise propose an ID using the established category pattern in the error taxonomy.
3. **State the invariant.** Describe the observable condition that must hold, such as “an Arabic table contains effective `w:bidiVisual` without reversed source cells.”
4. **Create a failing check.** Prefer an automated unit or regression test. When application rendering cannot be automated reliably, define a manual protocol with exact steps and expected observations.
5. **Confirm the cause.** Distinguish source-content loss, OOXML structure, style inheritance, renderer behavior, and application-specific behavior.
6. **Apply the minimal correction.** Avoid unrelated formatting or large rewrites.
7. **Verify.** Run the new check, all affected tests, the structural auditor, and the required render or application protocol.
8. **Document.** Update the taxonomy, permanent guardrails, relevant reference, compatibility evidence, and changelog.

## Guardrail proposal template

```markdown
### Proposed error ID and title

- Category:
- Sanitized fixture or reproduction steps:
- Affected application and version:
- Expected result:
- Actual result:
- Root cause evidence:
- Machine-checkable invariant:
- Failing test or manual protocol:
- Minimal correction:
- Verification performed:
- Validation surface not performed:
- Privacy review:
- Documentation to update:
```

## Error-ID rules

- Use a stable uppercase category such as `RTL`, `RUN`, `TABLE`, `STYLE`, `LIST`, `SECTION`, `FIELD`, `IMAGE`, `FONT`, `RENDER`, `REOPEN`, `CONTENT`, `PACKAGE`, `QA`, or `LATENCY`.
- Number new IDs sequentially inside the category.
- One ID represents one invariant and one bounded recovery decision.
- Do not create a new ID only because a different customer or document exposed the same cause.
- Split an ID when detection or recovery is materially different.

## Acceptance gate

A maintainer accepts a guardrail only when the evidence is privacy-safe, the cause is sufficiently established, the rule is implementable, regression protection exists, and the documentation does not overstate compatibility. If a manual Word protocol is the only viable test, its exact Word build, operating system, file hash, steps, and result belong in release or compatibility evidence.

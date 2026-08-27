## Problem and scope

Describe the Issue or invariant this Pull Request addresses and what remains out of scope.

Linked Issue: `Closes #`

## Evidence and correction

Summarize privacy-safe reproduction evidence, the demonstrated cause, and the smallest correction made. Do not include hidden reasoning transcripts or confidential source material.

## Verification

- [ ] A failing test or exact manual protocol reproduced the problem before the correction.
- [ ] Relevant repository-level and Skill tests pass.
- [ ] `python scripts/check_publication.py .` passes.
- [ ] The official Skill and plugin validators pass when their local tools are available.
- [ ] I named the actual validation surface and did not describe a preview as Word Desktop verification.
- [ ] Documentation and `CHANGELOG.md` are updated when behavior changed.

Commands and results:

```text
Add concise command names and pass/fail counts. Remove machine-specific paths and sensitive values.
```

## Privacy

- [ ] All fixtures, DOCX metadata, screenshots, logs, and links are synthetic or fully sanitized.
- [ ] No client document, raw conversation, conversation identifier, personal data, credential, private key, or token is included.
- [ ] Generated document output is not committed unless it is an explicitly reviewed synthetic release fixture.

## Compatibility

List the exact operating systems, application versions, renderers, and routes tested. Mark other surfaces as not verified.

# Security Policy

## Supported versions

Security fixes are provided for the latest released minor version. During the `0.x` phase, older releases may receive a fix only when the maintainer determines that a safe backport is practical.

## Report a vulnerability privately

Do not open a public Issue for vulnerabilities, exposed credentials, unsafe file-handling behavior, malicious DOCX samples, or private document data.

Use GitHub's private vulnerability reporting or draft a private security advisory at:

`https://github.com/Bannovich/arabic-word-production/security/advisories/new`

Include a concise impact statement, affected version or commit, safe reproduction steps, and suggested mitigation if known. Do not include real client documents, live secrets, or unnecessary personal data. A minimal synthetic package is preferred.

If a live secret was exposed, revoke or rotate it immediately. Reporting it does not make the secret safe again.

## What happens next

The maintainer will acknowledge a valid private report when practical, assess scope, coordinate a fix and regression test, and agree on disclosure timing with the reporter. There is currently no paid bug-bounty program and no fixed response-time commitment.

Ordinary RTL rendering, table layout, image placement, or performance defects are not security vulnerabilities. Report them through the public structured Issue forms only after sanitizing all evidence.

## Safe research

Do not test against systems or accounts you do not own or have explicit permission to assess. Do not publish exploit details before a fix is available. Avoid uploading weaponized or confidential files to GitHub Actions, Issues, Pull Requests, or public forks.

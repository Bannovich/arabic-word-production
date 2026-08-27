# Privacy and test-data policy

This repository is public by design. Treat every committed file, branch, Issue, Pull Request, workflow log, release asset, and deleted Git object as potentially permanent and searchable.

## Never publish

- raw ChatGPT or Codex conversation exports, references, IDs, or share links;
- real client, employer, partner, or personal documents;
- names, addresses, signatures, phone numbers, account numbers, identifiers, or private URLs;
- credentials, tokens, cookies, private keys, connection strings, or environment files;
- contracts, proposals, invoices, medical, legal, financial, employment, or regulated content;
- screenshots showing private application state;
- Office comments, tracked changes, authors, last-modified-by values, custom properties, hidden text, or embedded files from real documents.

## Allowed public evidence

- synthetic Arabic and English text written for the test;
- fictional names and organizations that cannot be confused with real clients;
- generated images with no personal or licensed customer content;
- minimal OOXML fixtures constructed specifically for the invariant;
- sanitized structural descriptions when no safe file can be shared.

## DOCX sanitization checklist

Before attaching a DOCX:

1. Start from a new synthetic file when possible instead of editing the original.
2. Unzip or inspect the package, including `docProps`, `word/comments.xml`, relationships, media, embeddings, custom XML, headers, footers, footnotes, endnotes, and tracked revisions.
3. Remove document authors, last editors, company names, templates, custom properties, and links with identifiers or tokens.
4. Accept or reject tracked changes as appropriate and remove comments.
5. Replace all content and media with synthetic equivalents while preserving only the structure needed to reproduce the defect.
6. Run the publication checker and manually review the package inventory.

Renaming a confidential file or deleting visible text is not sufficient sanitization.

## Handling accidental exposure

If private data is posted:

1. Stop sharing the link and notify a maintainer privately.
2. Revoke exposed credentials immediately.
3. Remove or redact the public item using GitHub's supported process.
4. Assume clones, notifications, caches, and workflow logs may retain copies.
5. Document the remediation without repeating the sensitive value.

The maintainer may remove contributions that cannot be shown to meet this policy.

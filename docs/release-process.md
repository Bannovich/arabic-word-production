# Release process

Only a maintainer may publish an official release. Every release is made from one exact commit and reports evidence at the level actually performed.

## 1. Prepare the candidate

- Update version metadata consistently in `pyproject.toml` and `.codex-plugin/plugin.json`.
- Update `CHANGELOG.md`, compatibility evidence, and known limitations.
- Confirm the canonical Skill exists only at `skills/arabic-word-production/`.
- Build release fixtures from synthetic data only.
- Make the working tree clean before recording the candidate commit.

## 2. Run local gates on the exact candidate

Run:

```powershell
python scripts/check_publication.py .
python -m unittest discover -s tests -v
python -m unittest discover -s skills/arabic-word-production/tests -v
```

Also run the official Skill and plugin validators, build the synthetic DOCX fixture, audit it with its source model, perform reopen auditing, and render every page with the named renderer when available.

If Word Desktop is available, open the exact fixture, confirm direction, tables, fields, sections, and warnings, Save As a round-trip copy, close, reopen, and re-audit the saved copy. Record “Not verified” when this protocol is not performed.

## 3. Create release evidence

Record a machine-readable evidence file containing at least:

- version, tag, candidate commit, and UTC timestamp;
- Python and dependency versions;
- validator and test results;
- fixture and audit SHA-256 values;
- route, elapsed time, builds, repairs, fallbacks, and QA failures;
- renderer and page-inspection status;
- Word Desktop tested flag and exact version when true;
- skipped surfaces and known limitations.

Never include local user-profile paths, secrets, or private source content.

## 4. Review the private remote

- Push or upload the exact candidate tree to a private GitHub repository.
- Confirm remote tree hashes and candidate content match the reviewed local tree.
- Wait for GitHub Actions on the candidate commit.
- Review README rendering, Arabic direction, Issue forms, license detection, plugin metadata, workflow logs, and release evidence as a non-developer would.
- Run a final secret and privacy scan against tracked content and DOCX core properties.

Any material change after this review creates a new candidate and repeats the gates.

## 5. Publish

- Change repository visibility only after all private gates pass.
- Confirm the public repository is accessible without private-session state.
- Create a signed or annotated `vX.Y.Z` tag at the exact candidate commit when tooling supports it.
- Create a GitHub Release with evidence-scoped notes, installation paths, validation surfaces, limitations, and Apache-2.0 licensing.
- Attach only synthetic, privacy-reviewed release assets.

## 6. Post-publication smoke check

- Open the repository and release as a public visitor.
- Verify README links, Arabic README, source tree, license, Issue forms, Actions result, tag-to-commit parity, and release assets.
- Install through each claimed distribution path where practical.
- Re-run local verification against the public candidate commit.
- Record any one-time GitHub setting that still requires maintainer action.

Do not describe the release as complete until the public smoke check succeeds or a remaining limitation is clearly disclosed.

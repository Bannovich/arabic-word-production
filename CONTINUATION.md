# استكمال Arabic DOCX RTL داخل Codex

آخر تحديث: 2026-09-09. هذا الملف هو نقطة الاستكمال المحلية. راجع حالة الملفات الفعلية قبل الاعتماد عليه؛ قد يحدث انقطاع بين حفظ ملف وتحديث هذا السجل.

## فتح المشروع من حساب آخر

افتح مجلد المشروع المحلي في Codex، ثم ابدأ مهمة داخل المجلد وأرسل البرومبت أدناه. الوصول إلى الملفات يحتاج صلاحيات نفس مستخدم Windows أو نسخة كاملة من المجلد. الملف وحده دليل وليس نسخة من المشروع؛ عند الانتقال إلى جهاز آخر انسخ المجلد كاملًا بما فيه `.git` والملفات غير المحفوظة في Commit. تنزيل الفرع القديم من GitHub لا يستعيد التعديلات المحلية غير المدفوعة.

المسار الافتراضي على جهاز المالك، بالنسبة إلى مجلد مستخدم Windows (استخدم مسار نسختك إذا نقلت المشروع):

```text
%USERPROFILE%\.codex\.chatgpt-projects\g-p-6a23aeebf03081919df64262e6bbb29e\arabic-word-production
```

```text
اقرأ AGENTS.md ثم CONTINUATION.md بالكامل من مجلد المشروع الحالي. افحص git status وgit diff وآخر commits، وواصل من Exact next checkpoint بعد التحقق من حالته الفعلية. احتفظ بكل التعديلات المحلية، ولا تعِد إنشاء الأيقونات أو تنفيذ milestones المكتملة. حدّث CONTINUATION.md بعد كل milestone وقبل التوقف، مع نتائج الاختبارات الفعلية والخطوة التالية. أكمل التنفيذ والفحص والتجهيز محليًا. راجع حدود النشر المسجلة قبل أي إجراء خارجي، وتوقف قبل Submit for Review أو Publish إلى أن أؤكد الإجراء وقت تنفيذه.
```

## الحالة والقرارات الثابتة

- Repository: https://github.com/Bannovich/arabic-word-production
- Branch: `feat/arabic-docx-rtl-branding`.
- Base: `fix/plugin-directory-square-logo` at `ffa0cbc2acc4035c13f705f52055ee0329959dc3`.
- Latest implementation commit at checkpoint creation: `bb1fb12` (`feat: rebrand plugin as Arabic DOCX RTL`). Use `git log -5` to find subsequent checkpoint commits; this file cannot contain its own commit hash.
- Stable package/Skill ID: `arabic-word-production`; display name: `Arabic DOCX RTL`; prepared version: `0.1.1`; license: Apache-2.0.
- On September 9 the maintainer completed submission/publication. Live OpenAI portal inspection confirmed `Arabic DOCX RTL`, version `0.1.1`, `Published`, with a View in Directory link. The old v0.1.0 row shows Approved with an optional Publish action; do not republish that older version.
- Selected design: concept 2, white document + left RTL arrow + blue check, purple background. Production files: `assets/logo.png` and `assets/icon.png`, each 1254×1254. Guidance and regeneration prompts: `assets/BRANDING.md`.
- The five-hour monitor was cancelled. Do not recreate it.
- Maintainer authorized remaining integration steps on September 8–9. PR #6 merged into main as `2a4d9798b212f97185ddf5dda0d060f92b97de74`, after all six GitHub checks passed. OpenAI v0.1.1 draft created and saved. Final OpenAI review/publish and policy attestations retain the explicit confirmation boundary at the moment of action.

## Milestone ledger

| Milestone | State | Evidence / remaining work |
|---|---|---|
| Branding v0.1.1 | Locally implemented, 2026-09-01 | Commit `bb1fb12`; manifest, metadata, two images, branding guide and listing updates |
| Initial verification | Historical pass | Prior task reported 46 repository and 24 Skill tests; rerun on current files before claiming readiness |
| Independent review | Changes requested | Stale publication wording; obsolete image generator; incomplete image validation |
| Publication wording and obsolete generator | Implemented and tested, 2026-09-08 | README/listing status now distinguishes published baseline and unpublished identity update; removed `scripts/generate_plugin_assets.py`, recoverable from Git |
| Image safeguards | Verified, 2026-09-08 | Targeted failure/pass checks; all 57 repository tests and 24 Skill tests pass. Submission checker: zero findings. Plugin and Skill validators pass |
| Portable local handoff | Created, 2026-09-08 | This file, repository AGENTS.md and README links; record subsequent results below |
| Aggregate verification and packaging | Verified, 2026-09-08 | 57 repository + 24 Skill tests pass; both checkers zero findings; external plugin/Skill validators pass; Python 3.10 syntax checked for 20 files; ZIP integrity, manifest, handoff files, distinct assets and obsolete-generator removal checked |
| Final repair review | Findings addressed, 2026-09-08 | Independent review identified pixel-stream decoding and uncaught PNG exceptions. Reopen/load within allowed dimensions and structured handling of bad CRC/decompression-bomb errors implemented. Three reproductions failed before fixes; final 57-test suite passes |
| GitHub integration | Complete, 2026-09-09 | PR #6 merged into main, commit `2a4d979`; all six checks passed on synchronized head `7032a9a`; remote main fetched and verified locally |
| OpenAI identity draft | Created and saved, 2026-09-09 | v0.1.1 uploaded to existing plugin; name and both icons verified in light/dark preview; support URL and description filled, developer display restored to existing published value; three prompts and Skill present. Automated Skill scan pending; policy boxes untouched |
| OpenAI publication | Confirmed live, 2026-09-09 | Maintainer performed Submit/Publish; fresh portal inspection shows Arabic DOCX RTL 0.1.1 Published. No further submission action required |
| Post-publication audit | Complete, 2026-09-09 | Main Quality and Pages workflows successful at `2a4d979`; repository Public and Apache-2.0; website/privacy/terms all HTTP 200. GitHub Releases still v0.1.0; public docs retain pending-update wording; latest continuation log remains on feature branch |

## Exact next checkpoint

GitHub implementation integration is complete: https://github.com/Bannovich/arabic-word-production/pull/6. Do not recreate it or repeat branding work. This later continuation-log commit may be ahead of main on the retained feature branch; implementation is already merged.

OpenAI publication is complete and verified. Do not repeat submission, upload another version, or click Publish on the old 0.1.0 row. Listing: https://chatgpt.com/plugins/plugins_6a96b648b318819188b6a57a8a86ab64 . No recurring monitor is active.

GitHub housekeeping authorized by the maintainer: current README/listing/docs now state v0.1.1 published, changelog dated September 9, and this log is being integrated into main. Next merge the documentation PR after passing checks and publish GitHub Release v0.1.1. Attach the exact previously uploaded plugin ZIP and its matching Skill ZIP; identify their source commit a04c5e8 in release notes (later documentation-only commits differ). Record final release verification in a local .qa report to avoid changing an already tagged release tree. Main Quality evidence for implementation: https://github.com/Bannovich/arabic-word-production/actions/runs/34308430695 ; Pages: https://github.com/Bannovich/arabic-word-production/actions/runs/34308430094 .

The uploaded ZIP was built from implementation commit `a04c5e8` and has SHA-256 `09e9e787afd0fa9ed601df6eff3eb8ef1b6ad32a79a550feaa88b5ea0a150c53`. Later commits update continuation text and merge history; production code/assets are unchanged. Keep the uploaded artifact and its report as evidence; if building another artifact, use a separate output directory.

The final ZIP is at `.qa/branding-v0.1.1/arabic-word-production-plugin.zip`; the local build report at `.qa/branding-v0.1.1/build-report.json` records its SHA-256 and inventory. These generated files are ignored by Git; rebuilding restores them. Check actual presence and timestamp when resuming after an interrupted turn.

## Reproduction commands (PowerShell, repository directory)

```powershell
git status --short --branch
git log -5 --oneline
git diff --stat
& '.\.venv\Scripts\python.exe' -m unittest discover -s tests -v
& '.\.venv\Scripts\python.exe' -m unittest discover -s skills/arabic-word-production/tests -v
& '.\.venv\Scripts\python.exe' scripts/check_publication.py .
& '.\.venv\Scripts\python.exe' scripts/check_plugin_submission.py .
& '.\.venv\Scripts\python.exe' scripts/build_submission_bundle.py .qa/branding-v0.1.1 .
git diff --check
```

If `.venv` is unavailable, create a local environment with Python >=3.10 and install the dependencies declared in `pyproject.toml`; add PyYAML for the external plugin/Skill validators. Locate the installed `plugin-creator/scripts/validate_plugin.py` and `skill-creator/scripts/quick_validate.py` under the current Codex skills directory. Confirm they exist before invoking; their installation paths can differ between accounts.

Git may report dubious ownership because earlier files were created by a different Windows sandbox account. For read-only inspection of this confirmed repository use a per-command `git -c safe.directory='<absolute repository path>' ...` exception; do not disable ownership checks globally.

## Packaging and verification cautions

- `.qa/branding-v0.1.1/` is ignored by Git. Old ZIPs from September 1 are stale after later changes. Build after final source/documentation edits and inspect archive contents.
- A ZIP hash must be reported outside source files included in that ZIP to avoid a self-referential hash. Use the builder output or a local `.qa` report.
- The source and images live in this repository. Generated-image originals are optional; the production PNGs suffice to continue.
- Checkers verify structure and declared image constraints. Passing them does not prove Word Desktop rendering or OpenAI approval.
- This checkpoint records outcomes and decisions, not private reasoning, credentials, or account usage history.

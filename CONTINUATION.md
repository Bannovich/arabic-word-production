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
- User reported v0.1.0 published. The identity update has not been submitted from this task. Do not infer current portal status from local files.
- Selected design: concept 2, white document + left RTL arrow + blue check, purple background. Production files: `assets/logo.png` and `assets/icon.png`, each 1254×1254. Guidance and regeneration prompts: `assets/BRANDING.md`.
- The five-hour monitor was cancelled. Do not recreate it.
- Maintainer authorized all remaining integration steps on September 8–9. Branch pushed; PR #6 opened. Final OpenAI review/publish and policy attestations retain the explicit confirmation boundary at the moment of action.

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

## Exact next checkpoint

September 9 integration checkpoint: branch pushed through `a04c5e8`; https://github.com/Bannovich/arabic-word-production/pull/6 opened against `main`, which GitHub reports can merge automatically. Next verify PR checks and merge when passing. OpenAI confirmed existing v0.1.0 Published; uploading v0.1.1 draft is not yet confirmed. The in-app browser file chooser timed out and its tabs disappeared after interruption; use the existing signed-in Chrome OpenAI tab and inspect current state before retrying. Preserve the original published plugin; upload a new version, not a separate plugin.

The local implementation and repair review are complete. Next: inspect `git status` and `git log -5` to confirm the local checkpoint commit titled `fix: harden branding safeguards and save continuation guide`, and rebuild the ZIP if source files differ from the saved archive. Then obtain the maintainer's choice for pushing this branch and opening a GitHub pull request; check the remote base branch before integration. No identity update was pushed or submitted from this task. After GitHub integration, prepare the existing OpenAI listing update with v0.1.1 and the approved images, and stop before review submission/publication for confirmation at that time.

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

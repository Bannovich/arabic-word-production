<div dir="rtl">

# Arabic Word Production

[English](README.md) · [المساهمة](CONTRIBUTING.md) · [الإبلاغ عن مشكلة](https://github.com/Bannovich/arabic-word-production/issues)

`Arabic Word Production` مشروع مفتوح المصدر في صورة Agent Skill وPlugin لإنشاء ومراجعة ملفات Microsoft Word العربية أو ثنائية اللغة عربي–إنجليزي. الفكرة الأساسية إن محاذاة النص، واتجاه الـParagraph، واتجاه الـRun، وترتيب أعمدة الجداول، وأبعاد الصفحة خصائص منفصلة؛ مجرد `Right Alignment` لا يعني إن المستند بقى `RTL` حقيقي.

المشروع يعتمد على Workflow قابلة للتكرار: Builder يحوّل JSON إلى DOCX، وAuditor يراجع بنية OOXML، وGuardrails، ومكتبة أخطاء معروفة، واختبارات Regression، وWord Template جاهز. الهدف إن كل مشكلة جديدة تتحول لتحسين يستفيد منه الجميع بدل ما نكتشف نفس المشكلة من الصفر في كل محادثة.

> **حالة الإصدار:** `v0.1.0` إصدار Alpha. فيه Workflow بنيوية مختبرة، لكنه ليس ضمانًا إن كل DOCX سيظهر بنفس الشكل في كل نسخة Word أو كل برنامج عرض أو Printer Driver.

## أسرع بداية لغير المطورين

أسهل طريقة داخل Codex هي إنك تطلب من Skill Installer تثبيت الـSkill من المشروع:

</div>

```text
$skill-installer Install arabic-word-production from https://github.com/Bannovich/arabic-word-production/tree/main/skills/arabic-word-production
```

<div dir="rtl">

بعد التثبيت ابدأ Task جديدة، أرفق المحتوى أو صفه، واكتب:

</div>

```text
$arabic-word-production Create an Arabic-first Word document, then audit its RTL structure.
```

<div dir="rtl">

رابط GitHub العام أعلاه هو مصدر التثبيت الأساسي. ولو عندك نسخة محلية بالفعل، استخدم خطوات تثبيت الـStandalone Skill اليدوية بالأسفل.

### تثبيت Standalone Skill يدويًا

1. نزّل الإصدار وفك الضغط.
2. انسخ مجلد `skills/arabic-word-production` إلى مجلد الـSkills الشخصي باسم `arabic-word-production`.
3. أعد تشغيل Codex أو ابدأ Task جديدة حتى يعيد تحميل الـSkill.

المسار الشخصي المعتاد على Windows هو `%USERPROFILE%\.codex\skills\arabic-word-production`، ويمكن استخدام `$CODEX_HOME/skills/arabic-word-production` لو `CODEX_HOME` متضبط عندك.

### تثبيت Local Plugin

المشروع متغلف بالفعل كـPlugin من خلال `.codex-plugin/plugin.json`. للاختبار المحلي: نزّل المشروع، وبعدها اطلب من `$plugin-creator` إنه يربط مجلد الـPlugin الحالي بالـpersonal marketplace. أعد تشغيل تطبيق ChatGPT Desktop، وافتح Plugins Directory، واختر المصدر المحلي، وثبّت **Arabic Word Production**. الـlocal marketplaces مختلفة عن الـuniversal public Plugins Directory.

الإصدار الحالي يحتوي على الـSkill فقط، ولا يحتاج MCP server أو ربط حساب خارجي.

## Plugin Directory

المشروع بيجهّز Candidate من نوع **skills-only** للـpublic Plugin Directory، لكنه ليس معتمدًا أو ظاهرًا هناك حتى الآن. الـCandidate لا يحتوي على MCP server أو ربط حساب أو خدمة يديرها المشروع أو Telemetry أو Checkout أو Subscription.

راجع [Privacy Policy](https://bannovich.github.io/arabic-word-production/privacy-policy/) و[Terms of Service](https://bannovich.github.io/arabic-word-production/terms-of-service/) و[حدود التقديم](https://bannovich.github.io/arabic-word-production/plugin-directory-submission/) لمعرفة النطاق بدقة. قبل أن يصبح الـPlugin عامًا، يلزم أن ينفّذ الناشر بنفسه أي Identity Verification وPolicy Attestations وخطوة review/publish النهائية التي يطلبها الـhost.

## البرامج وطرق الاستخدام المدعومة

| المكان | الاستخدام | حالة `v0.1.0` |
| --- | --- | --- |
| ChatGPT Desktop / Codex | تثبيت أو استدعاء Agent Skill | المسار الأساسي |
| ChatGPT وCodex Plugin hosts | تحميل الـPlugin من local marketplace | متغلف والـmanifest اجتاز التحقق |
| برامج متوافقة مع Agent Skills | قراءة `SKILL.md` والموارد المرفقة | تعليمات قابلة للنقل؛ سلوك البرنامج قد يختلف |
| Python 3.10+ | تشغيل Builder وOOXML Auditor مباشرة | Command-line path مدعوم |
| Microsoft Word Desktop | فتح ملفات DOCX الناتجة | برنامج الإخراج الأساسي؛ التحقق يُذكر لكل ملف أو إصدار |
| برامج Office أخرى | فتح DOCX قياسي | Best effort؛ الشكل قد يختلف |

## تشغيل الأدوات مباشرة

ثبّت Dependencies المشروع:

</div>

```powershell
python -m pip install .
```

<div dir="rtl">

ثم شغّل الأوامر من داخل مجلد الـSkill الأساسي:

</div>

```powershell
cd skills/arabic-word-production
python scripts/build_docx.py model.json output.docx
python scripts/audit_docx.py output.docx --out-json audit.json
python -m unittest discover -s tests -v
```

<div dir="rtl">

الـBuilder يستقبل JSON model ويُنتج DOCX أصليًا. الـAuditor يفحص OOXML بحثًا عن مشاكل اتجاه Paragraphs وRuns والجداول والـSections والعروض والـFields والصور. اقرأ [تعليمات الـSkill](skills/arabic-word-production/SKILL.md) قبل اعتبار الأوامر Production pipeline كاملة.

## معنى كل مستوى تحقق

- **Built:** تم إنشاء حزمة DOCX بنجاح.
- **Structurally audited:** اختبارات OOXML الآلية نجحت في الـinvariants التي يغطيها الـAuditor.
- **Rendered and inspected:** تم Render لكل صفحة ومراجعتها بصريًا باستخدام الـrenderer المذكور.
- **Word Desktop verified:** تم فتح نفس الملف في Microsoft Word Desktop وتنفيذ الفحوص المعلنة هناك.

نجاح Preview أو PDF conversion أو structural audit وحده لا يساوي Word Desktop verification. أي Release evidence أو تسليم مستند لازم يذكر سطح التحقق الحقيقي وأي فحص لم يتم.

## الإبلاغ الآمن عن المشاكل

الـIssues هي المكان الذي تتحول فيه المشاكل الجديدة إلى Guardrails يستفيد منها الجميع. ممنوع رفع مستندات عملاء، أو محادثات ChatGPT خام، أو بيانات شخصية، أو Credentials، أو عقود، أو Screenshots سرية إلى الـRepository العام.

بدل ذلك:

1. أنشئ DOCX اصطناعيًا صغيرًا أو وصفًا منقحًا يعيد إنتاج المشكلة.
2. احذف الأسماء والشعارات وأرقام الحسابات والروابط ذات Tokens خاصة والـComments والـTracked Changes وDocument metadata.
3. اذكر نسخة Word ونظام التشغيل والـRoute المستخدمة والنتيجة المتوقعة والفعلية ومستوى التحقق.
4. استخدم Issue form المناسبة. لو احتجنا تفاصيل إضافية، لن نطلب محتوى سريًا.

## القيود المعروفة

- شكل RTL قد يختلف بين إصدارات Word Desktop وWord Online وGoogle Docs وLibreOffice والـPreviewers والخطوط وPrinter Drivers.
- الـAuditor يراجع invariants بنيوية صريحة؛ لا يثبت صحة المحتوى أو ملاءمته القانونية أو Accessibility أو جودة التصميم البصري.
- الجداول العريضة، والـmixed orientations، والـfloating objects، والـcharts، والمعادلات، والملفات المضمنة، والـtracked changes، والـfields غير المعتادة قد تحتاج Structured أو Complex route ومراجعة يدوية.
- هدف أقل من دقيقتين للـFAST route هو Performance goal للأعمال المعتادة، وليس Deadline ثابتًا ولا يسمح بتجاوز Quality Gates.
- المشروع لا يدعي توافقًا شاملًا، ولا يمثل Microsoft أو OpenAI ولا يحصل على Endorsement منهما.

## المساهمة

ابدأ من [CONTRIBUTING.md](CONTRIBUTING.md)، ثم استخدم Issue form لاقتراح Guardrail، أو الإبلاغ عن مشكلة Rendering بملف منقح، أو طلب تحسين. الحوكمة والدعم والأمان والـRoadmap موثقة بشكل منفصل عشان تقدر تساهم حتى لو مش مطور.

المشروع منشور بترخيص [Apache License 2.0](LICENSE). راجع [NOTICE](NOTICE) لمعرفة نسبة العمل وتوضيح العلامات التجارية.

</div>

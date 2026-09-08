# Arabic DOCX RTL

الوصف المختصر: Audited Arabic Word files

رابط الدعم: https://github.com/Bannovich/arabic-word-production/issues

`Arabic DOCX RTL` ينشئ ويصلح ويعمل structural audit لملفات `DOCX` العربية أو ثنائية اللغة عربي–إنجليزي. يضبط اتجاه الـParagraph والـRun والجداول والـSections بشكل صريح، فلا يتم اعتبار `Right Alignment` دليلًا على `RTL` أصلي.

استخدمه لإنشاء ملف Word من المحتوى الذي تقدمه، أو إصلاح مستند mixed-direction، أو فحص خصائص `RTL` البنيوية، أو تقييم الجداول العريضة قبل Landscape layout، أو توضيح مستوى التحقق الحقيقي. النتيجة تفرّق بين Built وStructurally audited وRendered and inspected وWord Desktop verified.

النسخة الأساسية المنشورة `v0.1.0` وتحديث الهوية `v0.1.1` من نوع skills-only. اسم **Arabic DOCX RTL** والـassets الجديدة مش Live غير بعد Review ونشر التحديث. الـPlugin لا يحتوي على MCP tools أو ربط حساب خارجي أو Telemetry أو خدمة يديرها المشروع. قد يختلف شكل الملف بين إصدارات Word والخطوط ونظام التشغيل والـrenderer وبرامج Office. ولا يُذكر Word Desktop verified إلا عند فتح نفس الملف وفحصه هناك.

<div dir="rtl">

# Logo Localizer: معرّب الشعارات

**[English](README.md)**

مهارة لـ [Codex](https://github.com/openai/codex) تترجم شعارات وعناوين الألعاب والأفلام والمسلسلات والأنمي
والكتب والقصص المصورة من أي لغة إلى أخرى **بالأسلوب الفني نفسه**، والعربية هي الهدف الأول.

ترسم بأداة الصور المدمجة في Codex (`image_gen`)، فلا تحتاج مفتاح API ولا خادماً، وسكربتاتها المساعدة
تعمل على جهازك.

## ماذا تفعل

1. **تقرأ الشعار:** تحلّله من الكل إلى الحرف: الهيكل، والوزن، والإيقاع، والسطح، والزخارف. ثم كل جملة
   وكلمة وحرف، ولون كل حرف بكود `#hex`.
2. **تقترح النص:** تبحث أولاً عن العنوان، ومنه الترجمة الرسمية إن وُجدت. ثم تكتب خياراتها للترجمة
   واقتراحها، وتسألك عن أي عنوان فرعي.
3. **تتوقف وتنتظر:** لا يُرسم شيء قبل أن تختار النص أو تكتبه.
4. **ترسم أربع نسخ:** تمسح الشعار القديم من الصورة (لوح نظيف). ثم ترسم الشعار الجديد **بخلفية شفافة**
   بأربعة أساليب مختلفة، كل واحد في صورة مستقلة، وتضعه مكان القديم. الصور مرقّمة من 1 إلى 4.
5. **تختار أو تطلب المزيد:** اكتب رقماً، أو اطلب أربعاً أخرى:
   - قريبة من روح الأصل؛
   - أو أكثر إبداعاً، وقد تبتعد عن الأصل أكثر.

   الأرقام تستمر (5–8، 9–12…) ولا تتكرر.
6. **تفحص التي اخترتها:** تذكر كل حرف أو نقطة أو لون خاطئ أو تفصيل مخترع في جدولين: جدول الحروف وجدول
   العلامات. لا تصلح شيئاً من عندها، فكل تعديل بطلبك.
7. **تسلّم وترتّب:** تسلّم ثلاثة ملفات:
   - الصورة بصيغة الأصل ومقاسه؛
   - الشعار وحده بخلفية شفافة؛
   - ورقة مقارنة مع الأصل.

   ثم تسألك أين تحفظها، وتنشئ هناك مجلداً جديداً، ولا تحذف ملفات العمل إلا بموافقتك.

## المتطلبات

- Codex مع أداة `image_gen` المدمجة.
- Python 3.10 أو أحدث، مع Pillow وnumpy:

<div dir="ltr">

```bash
python -m pip install -r requirements.txt
```

</div>

## التثبيت

1. انسخ مجلد `logo-localizer` إلى مجلد مهارات Codex:
   - ويندوز: `%USERPROFILE%\.codex\skills\logo-localizer`
   - ماك ولينكس: `~/.codex/skills/logo-localizer`
2. ثبّت المتطلبات كما في الأعلى.
3. أعد تشغيل Codex.

## الاستخدام

أرفق صورة واكتب أياً من هذه:

- «عرّب الشعار في هذه الصورة»
- «ترجم شعار هذه اللعبة إلى الفرنسية»
- أو استدعِ المهارة وحدها: `$logo-localizer`

اللغة الهدف هي العربية ما لم تذكر غيرها. شعار واحد في كل طلب.

## الملفات

<div dir="ltr">

```text
logo-localizer/
├── SKILL.md                 the rules and the stages Codex follows
├── agents/openai.yaml       the skill's name and default prompt in Codex
├── assets/                  the analysis card and the translation card
├── references/              the method: logo analysis, Arabic lettering, checks
├── scripts/
│   ├── init_job.py          creates the job folder and job.json
│   ├── job_spec.py          checks job.json; no drawing before you chose the text
│   ├── codex_image.py       builds the drawing prompt, collects the result, makes the plate, places the logo
│   ├── make_mask.py         the old logo's mask for the clean plate
│   ├── compare_sheet.py     the comparison sheet
│   └── _common.py           shared helpers
└── tests/                   python -m unittest discover -s tests
```

</div>

## الحدود

- الفحص بالعين: عين النموذج وعينك. لا يوجد سكربت يثبت صحة الحروف.
- كل رسمة تُحسب من حد استخدامك في Codex، بنحو دقيقة لكل صورة.
- إن لم تستطع أداة الصور إعادة بناء الخلفية خلف الشعار القديم، يُذكر لك ذلك ولا يُصلح شيء دون علمك.

## الحقوق

هذه المهارة أداة. أنت مسؤول عن امتلاك حق ترجمة أي شعار تعالجه بها واستخدامه ونشره. الشعارات والعناوين ملك
أصحابها.

## الرخصة

[MIT](LICENSE) © 2026 [abdallah28r](https://github.com/abdallah28r).

</div>

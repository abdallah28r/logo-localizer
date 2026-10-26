# Translation card (template)

Show this card to the user before drawing the logo. Write the card in the user's language. Stop and wait for the reply;
generate nothing until the user picks an option or types their own text.

Write it from the research in `job.json` (the research and analysis gate in
SKILL.md): an official target-language title (store page, publisher,
distributor, poster), how the audience knows the work, the meaning and sound
of each name, and the published translations with what they got right or
wrong. Then write your own options: as many as are genuinely
different and useful, each with a short label you choose. Literal, adapted,
short, sound (نطق) and meaning (معنى) are examples of what an option can be,
not slots to fill. Keep the filled card under 25 lines.

```text
اللغة: <source language> ← <target language> (العربية ما لم يُذكر غيرها)
النص [n]: «<source text>»  — نوع النص: شعار | عرض
الوظيفة: <what it does here: button, title, tagline, logo...>
المساحة: <fits / tight / very tight> (the target is often 20–30% wider or narrower; say which)

أ) رسمي:      «...»   — <where it is used: store page, publisher, poster> · المعنى الحرفي: <...>
   (or: أ) لم أجد عنواناً رسمياً — <where you searched>)
ب) <label>:   «...»   — <what this option does, length vs source> · المعنى الحرفي: <...>
ج) <label>:   «...»   — ... · المعنى الحرفي: <...>
(as many lines as you have genuinely different options)

[when the logo holds a subtitle, tagline or other text]
النص الإضافي: «<source>» — ترجمه | أبقه كما هو | احذفه؟ (اقتراحي: <one>)

[when a text is classified KEEP]
يبقى كما هو: «<text>» — <reason>

الاقتراح: <letter> — <reason>
أو اكتب نصك: ________

للرد: اكتب حرف الخيار (مثل «ب») أو نصك بين «»، وقرارك في النص الإضافي إن وُجد. لن أرسم شيئاً قبل ردك.
```

Show the analysis card first and this card last, and end your message with
the reply line («للرد: …»), written in the user's language, with nothing
after it: it is the gate the user answers.

Rules for filling it:

- Use Modern Standard Arabic unless the user or the source tone asks for
  dialect. Keep the source register (playful, formal, menacing).
- «أ» is always the official title: marked «رسمي» with where it is used,
  and your recommendation unless it does not fit the space or tone (say
  why); the user still chooses. When none was found, the «أ» line says so
  and your options start at «ب», so the letters keep their meaning.
- For names and titles, consider both the sound (نطق) and the meaning (معنى);
  say which is common for this kind of product, from the research;
  otherwise say it is unknown.
- Mark the recommendation by its fit to the design space and tone, not only
  by meaning.
- Never translate text that the design classification marked `KEEP`
  (logos kept in Latin, brand names, signatures); list it under
  «يبقى كما هو» with the reason instead.
- After the reply: use the chosen or typed text **verbatim**, character for
  character, including the user's punctuation and digits. Do not "improve"
  it. If it will not fit the space, say so, offer one shorter option, and
  wait for the user's choice.

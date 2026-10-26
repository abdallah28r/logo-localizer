# Localizing a logo or title treatment

Read with `text-design-transfer.md`, which holds the general rules (profiling,
style map, Arabic structure). This file adds what is specific to logos,
wordmarks and game/film title treatments.

## 1. Settle the words before any drawing

- If an official Arabic title or logo exists, use it and say so; never
  invent a competing one. Studios work from an approved title, not a fresh
  translation (Netflix, Crunchyroll).
- Otherwise put the title strategy on the translation card. Decision ladder:
  1. Official Arabic form or established exonym → use it.
  2. Meaningless or invented name → transliterate (نطق); check that the
     spelling yields the right sound and no unwanted reading (the 7Up case).
  3. Meaningful name or pun → translate or recreate (معنى); offer two options.
  4. Trademark that must stay Latin → keep the Latin logo, add a styled
     Arabic line under it if wanted (Disney+ MENA pattern).
  5. Subtitle words ("Redemption", "Origins") → translate when they carry
     context; a descriptive subtitle helps unknown titles, hurts big brands.
- Transliteration alone is the minimum, not adaptation: the drawing must
  still carry the design.

## 2. Take the logo apart

1. Split it into blocks: main word, subtitle, numerals, icon/emblem, tagline.
   Each block gets its own decision (Crunchyroll's process).
2. Inventory every feature on the analysis card: skeleton, contrast,
   terminals, slant, weight, width, signature letter, ornaments (stars,
   sparkles, drips, cracks, bullet holes, ropes, swords), texture/3D/
   lighting, colour, and how the blocks lock together.
3. For each ornament decide **keep / transfer / drop** with its reason.
   List motifs first, then place them on the new letters (the Seton Academy
   case: paws, ears, sun, bolts re-applied one by one).
4. An icon without text stays as it is. An icon with text is localized only
   if asked (Assassin's Creed Mirage redrew its crest as Arabic calligraphy
   because the setting was Baghdad).

## 3. Design the Arabic

- **Choose a strategy and say it:** homogeneous (same character as the
  source) or deliberately contrasting (same colour and size, own
  personality). Homogeneous is the default for game and film titles.
- **Explore four styles** before converging, for example angular Kufi vs
  Neo-Ruqaa vs Thuluth-inspired vs a geometric display face; each becomes
  one entry in `job.json`'s `styles` and one drawing, and the user picks
  (29LT draws 2–3 routes per logo).
- **One signature letter carries the main gesture.** Find the Arabic letter
  whose structure can hold the source's key feature: a crossed lam-alef for a
  broken A (Lanvin), a custom meem (Balmain), one reshaped character in the
  Japanese *Clockwork Orange*. Lam-alef is the richest candidate: compulsory,
  yet its form is free.
- **Move ornaments to letters that can hold them,** then re-check reading.
  Crunchyroll moved spider legs onto "SPIDER", then had to round letters and
  space the legs because it got hard to read. Typical Arabic hosts: long
  horizontal connections (drips, cracks), alif/lam tops (spikes, sparks),
  bowls (stars, emblems), dots (a signature diamond, star or icon dot, if
  every dot is treated the same way).
- **Never force an icon into a letter as a gimmick** (Atrissi); if the
  ornament fights the letter, drop it and say why.
- **Metrics:** share the baseline; Arabic ascenders ≈ Latin cap height; test
  two median heights; dots as wide as the source stems for blocky marks;
  one kashida to approach the width, stop short of an exact match.
- **Slant and italics:** use a leaning style or weight, never a skew.
- **Rebuild the surface last:** after the Arabic skeleton reads, reapply the
  source's fill, texture, bevel, extrusion, lighting and colour on the new
  letters (Wordbank: 2D/3D rebuilt from the source specs).
- **Layout:** right-to-left order inside the lockup; reflow to two lines if
  the Arabic is longer; never mirror the emblem or the brand mark.

## 4. Running it with Codex

- Prompt with `codex_image.py prompt --kind logo --spec <job>/job.json`: the
  approved text, route, anchors and features come from the spec
  (`codex-image.md`).
- Attach the source logo as the edit target (in place) or as a style
  reference (a standalone Arabic logo); say which features to carry over.
- When the user asks for edits, one change per edit: route, then signature letter, then ornaments, then
  surface. Do not pile adjectives onto a failed concept; go back to the
  routes instead.
- The new logo is always drawn on transparency first; on a poster or box
  art it is placed onto the clean plate, and it is delivered on its own too.

## 5. Check before showing the user

- Every letter joined, right-to-left, every dot present, spelling exact; no
  Latin letterform passed off as Arabic (Dior's D-shaped د, Gucci's
  incomplete ش); no faux-script look-alikes.
- **Strip test:** with ornaments mentally removed, the Arabic word still
  reads well. **Monochrome test:** it holds in one colour.
- Side by side at the same size: silhouette, weight, colour and texture echo
  the source; then at the small size it will be seen (thumbnail, icon).
- Register: it reads as a title, not as shop signage (the Japanese *Solo*
  logo was mocked for exactly that).
- Ornaments do not read as extra dots or letters (mark table,
  `visual-review.md` step 5); nothing culturally loaded (religious
  calligraphy styles, symbols) was added without saying so.
- The user, as a native reader, confirms readability and approves.

## Sources

Cases and professional: 29LT Balenciaga, Balmain, Lanvin
(blog.29lt.com/2019/05/13/balenciaga-arabic-logo, /2023/03/22/balmain-arabic-logo,
/2024/02/14/lanvin-arabic-logo) · Gigazine on Crunchyroll's JP→EN logos
(gigazine.net/news/20201112-anime-logo-change-into-english) · Otaku USA on
Crunchyroll's process (otakuusamagazine.com) · Ubisoft, Assassin's Creed
Mirage authentic Baghdad (news.ubisoft.com) · Kotaku, famous game logos in
Arabic (kotaku.com/famous-game-logos-in-arabic-1593019676) and the Japanese
*Solo* logo · Higaki poster work (peoplesgdarchive.org, sabukaru.online) ·
Netflix partner help, approved titles (partnerhelp.netflixstudios.com) ·
Wordbank title-treatment brief (dynamitejobs.com) · Betranslated logo
adaptation (betranslated.com) · Typographica on Western logotypes in Arabic
(typographica.org/?p=3706) · Atrissi lessons (bambisoapbox.com) · Chahine on
obliques (thoughtbot.com) · Campaign ME, Disney+ MENA (campaignme.com) ·
Level Up Translation on game titles (leveluptranslation.com).
Academic: Yong Liu on modified film titles in China (aebs.ecnu.edu.cn) ·
Fernandes 2006, names in translation (newvoices.arts.chula.ac.th) ·
Mohamed et al. 2025, Arabic-translated logos (frontiersin.org).

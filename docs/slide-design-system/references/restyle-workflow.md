# Restyle Workflow

Use this when the user has an existing deck and wants it to look consistent, professional,
and clean without changing what it says.

## Contents
1. Inventory
2. Map slides to layouts
3. Rebuild on the theme
4. Audit checklist
5. Change report
6. Common fixes

## 1. Inventory
For each slide, record: title, purpose (one phrase), content shapes (cards, flow, table,
code, image), fonts and sizes used, colors used, and anything that overflows or collides.
Note hyperlinks, speaker notes, images, and animations so none is lost.

## 2. Map slides to layouts
Use the table in `layout-catalog.md`. Decide per slide:
- **Keep:** fits a layout as is.
- **Tighten:** fits after trimming to density caps.
- **Split:** holds two ideas; make two slides.
- **Merge:** two thin slides that share one idea.
Flag any split or merge for the author's approval when it changes the story order.

## 3. Rebuild on the theme
1. Set theme colors, fonts, and text styles (see `adapters.md`).
2. Create layouts L01 to L13 that are needed.
3. Move slides onto layouts one at a time. Paste content into placeholders, not free-floating
   text boxes.
4. Replace per-shape colors and sizes with the nearest token. Map old colors by role
   (heading, fill, accent, warning), not by similarity of hue.
5. Add the header, slide numbers, and the takeaway bars.
6. Write or update speaker content for every slide (mode: talking points or full text; see
   `speaker-notes.md`). Keep the author's existing notes.

## 4. Audit checklist
Every item must pass before delivery.

Typography
- [ ] One text family and one code family in the whole deck
- [ ] Only sizes 44, 32, 20, 18, 16 (code), 14, 12, and 54 (stat) appear
- [ ] Titles are Title style, same position on every slide, at most 2 lines
- [ ] No text below 12 pt, no body text below 16 pt
- [ ] No manual line breaks used to fake wrapping; no stray spaces for alignment

Color
- [ ] Only token colors appear (check fills, lines, text, charts, tables)
- [ ] At most two non-neutral colors per slide area
- [ ] Status colors always accompanied by a word or icon
- [ ] Text contrast at least 4.5:1

Layout
- [ ] Margins at least 48 pt; nothing crosses the footer line
- [ ] Equal card widths, equal gaps, top aligned
- [ ] Every content slide has a title; most have a lead or takeaway
- [ ] Footer and number identical and in the same place on every slide
- [ ] At most 6 bullets, 12 words per bullet; at most 3 cards per row

Content integrity
- [ ] Every original fact, number, date, and link is still present
- [ ] Speaker notes, alt text, and hyperlinks preserved
- [ ] Recap slide matches the goals slide, if there is one

Speaker content
- [ ] Every slide has notes in the notes field, in one mode (talking points or full text)
- [ ] Each ends with a transition; nothing invented; unknowns flagged `[confirm: ...]`
- [ ] Lengths within the limits in `speaker-notes.md`

Visual check
- [ ] Rendered each slide to an image and looked for overflow, overlap, clipped text, and
      misaligned arrows

## 5. Change report
Deliver a short report with: fonts unified (from, to), sizes normalized (count of changes),
colors remapped (old role to new token), slides re-laid-out (slide number to layout ID),
slides split or merged, content trimmed (list), and speaker content added or changed (mode, slide count), and open questions for the author.

## 6. Common fixes

| Symptom | Fix |
|---|---|
| Five fonts in one deck | Set theme fonts, clear per-run font overrides |
| Sizes drift slide to slide (17, 19, 21 ...) | Snap to the nearest token size; if text no longer fits, cut words, do not shrink |
| Rainbow of colors | Remap by role to primary, accent, warning |
| Text wall | Convert to L04 cards, L05 flow, or L07 table |
| Tiny text to fit more | Split the slide |
| Ragged alignment | Snap to grid, distribute evenly |
| Centered paragraphs | Left align |
| Topic titles ("Timeline") | Rewrite as claims ("Ingestion is on track; scoring moved to 11/13") |
| Mixed arrows and icon styles | One arrow style (2 pt accent), one icon set |
| Decorative images | Remove, or replace with a diagram that carries meaning |

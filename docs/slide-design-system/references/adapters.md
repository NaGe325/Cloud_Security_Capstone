# Adapters: applying the tokens in a specific tool

The spec is the source of truth. This file only says where each token lives in each tool.
Always set tokens at the **theme or master level first**.

## Contents
- PowerPoint (.pptx)
- Google Slides
- Keynote
- HTML / web decks (reveal.js, plain CSS)
- LaTeX Beamer
- Markdown decks (Marp, Slidev)
- Generating a file programmatically

## PowerPoint (.pptx)
- Colors: Design > Variants > Colors > Customize. Map `primary` to Dark 2, `accent` to
  Accent 1, `warning` to Accent 2, `success` to Accent 3, `danger` to Accent 4, `slate` to
  Accent 5, `border` to Accent 6, `ink` to Dark 1, `surface` to Light 1, `surface-alt` to
  Light 2.
- Fonts: Design > Variants > Fonts > Customize. Set Heading and Body to the same family.
- Master: edit Slide Master so the title placeholder is Title style, body placeholder is
  Body style, and the footer and slide number placeholders are Caption style.
- Create one custom layout per layout ID (L01 to L13) and name them that way.
- Use Format Painter or Reuse Slides sparingly; prefer applying a layout.

## Google Slides
- Theme: Slide > Edit theme. Set the theme Colors (Dark 1, Light 1, Dark 2, Light 2, Accent 1
  to 6) using the mapping above. Set Title and Body text styles in the master.
- Fonts: Open Sans is available in Google Fonts. If not, use Helvetica or Arial. Set one
  family in the master title and body.
- Use Slide > Apply layout for each slide, then Format > Paragraph styles > Update to match.
- For a .pptx opened in Google Slides: convert to native Slides first (File > Save as Google
  Slides) so the theme edits apply; review links and fonts after conversion.

## Keynote
- Edit Slide Layouts: set Title, Body, and Caption paragraph styles; save custom colors in
  the Colors palette; set Open Sans or the fallback as the theme font.

## HTML / web decks
Define tokens as CSS variables and use them everywhere:

```css
:root {
  --primary:#1B2A49; --primary-tint:#EEF1F6; --accent:#C41230; --accent-tint:#FBE9EC; --highlight:#FDB515; --iron:#6D6E71;
  --warning:#8A5A00; --warning-tint:#FFF6DD; --success:#2F855A; --danger:#B42318;
  --ink:#0F172A; --slate:#55595F; --border:#D5DCE6; --surface:#FFFFFF; --surface-alt:#F6F7F9;
  --font-text:"Open Sans",Helvetica,Arial,sans-serif;
  --font-code:"JetBrains Mono",Consolas,Menlo,"Courier New",monospace;
  --fs-display:44px; --fs-title:32px; --fs-lead:20px; --fs-body:18px; --fs-label:14px;
  --fs-caption:12px; --fs-code:16px; --fs-stat:54px;
}
```
Scale the slide canvas at 960 x 540 CSS px and let the framework scale it to the screen.

## LaTeX Beamer
Define colors with `\definecolor{primary}{HTML}{1E3A5F}` and so on, set
`\setbeamercolor{title}{fg=primary}`, use fontspec with Open Sans and Helvetica fallbacks, and set
text sizes through the five token sizes only. Use a custom footline for the footer.

## Markdown decks (Marp, Slidev)
Put the CSS variables above in the theme CSS, define a class per layout (`.l04`, `.l05`),
and apply with slide directives.

## Generating a file programmatically
1. Load `assets/tokens.json`.
2. Build theme or master first, then slides from layouts.
3. Never hard-code a hex value or point size in slide code; always look it up in the tokens.
4. Run the audit (`scripts/audit_deck.py` for .pptx) and fix every finding.
5. Render slides to images and inspect them visually for overflow, overlap, and alignment.

## Tool limits, in short
If a tool cannot set a token in the theme, apply it per object using exactly the token
value. If a font is missing, use the first available fallback for the entire deck.

## Speaker notes
Put speaker content in the tool's notes field: PowerPoint and Keynote notes pane, Google Slides
speaker notes, `<aside class="notes">` in reveal.js, `\note{}` in Beamer, and `<!-- -->` notes in
Marp or Slidev. See `speaker-notes.md`.

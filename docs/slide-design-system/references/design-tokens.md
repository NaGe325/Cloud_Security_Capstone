# Design Tokens

Canvas: 16:9, 960 x 540 pt (13.333 x 7.5 in). All sizes below are in points on that canvas.
If the tool uses another unit or canvas, scale proportionally (see "Scaling").

## 1. Color palette

Theme name: Midnight plaid. A deep navy primary, Carnegie red accent used sparingly, a gold
highlight (fills and tartan only, never text), iron-gray neutrals, and a dark-gold warning text color.
Hex values are approximate brand-style colors; verify against CMU brand guidelines.

| Token | Hex | Use |
|---|---|---|
| `primary` | `#1B2A49` | Titles, card headers, key numbers, takeaway text accents |
| `primary-tint` | `#EEF1F6` | Takeaway bar, table header fill, soft backgrounds |
| `accent` | `#C41230` | Arrows, number chips, links, the header slash, key emphasis (Carnegie red; use sparingly) |
| `accent-tint` | `#FBE9EC` | Output chips, accent card fill |
| `warning` | `#8A5A00` | Warning text and flags (dark gold, readable on white) |
| `warning-tint` | `#FFF6DD` | Warning callout fill |
| `success` | `#2F855A` | Done or pass, use sparingly |
| `danger` | `#B42318` | Failure or error text, always paired with a word |
| `ink` | `#0F172A` | Body text |
| `slate` | `#55595F` | Secondary text, captions, footer |
| `border` | `#D5DCE6` | Card outlines, table rules, dividers |
| `surface` | `#FFFFFF` | Slide background |
| `surface-alt` | `#F6F7F9` | Alternate background, code blocks |
| `on-primary` | `#FFFFFF` | Text on primary or accent fills |
| `highlight` | `#FDB515` | Tartan strip, tier chips, highlights on dark (fills only; text on it is `ink`) |
| `iron` | `#6D6E71` | Tartan strip, secondary graphics |
| `wordmark-gray` | `#BDBDBD` | Header wordmark text |
| `header-label` | `#4B4B4B` | Header label text |

Rules:
- Slide background is `surface`. Section dividers may use `primary` with `on-primary` text.
- Body text is always `ink`. Secondary text is `slate`. Never use pure black or pure gray.
- Emphasis order: bold `ink`, then `accent`, then `primary`. Do not use more than one
  emphasis style per sentence.
- Status colors (`success`, `danger`, `warning`) always pair with a word or icon, never
  color alone.
- Contrast: all text pairs above meet WCAG AA (4.5:1). Never put text on `highlight` other
  than `ink`, and never use `highlight` as a text color.
- Multi-series charts: `primary`, `accent`, `warning`, `slate`, `success`, in that order.

## 2. Typography

One sans family for all text, one monospace family for code and identifiers.

| Role | Family | Fallback stack |
|---|---|---|
| Text | Open Sans | Helvetica, Arial, sans-serif |
| Code | JetBrains Mono | Consolas, Menlo, Courier New, monospace |

If the tool lacks Open Sans (CMU's preferred typeface; Helvetica is its listed alternate), use the first available fallback for the **entire** deck. Never
mix fallbacks within one deck.

| Style | Size | Weight | Color | Line height | Use |
|---|---|---|---|---|---|
| Display | 44 | Bold | primary (or on-primary) | 1.1 | Title slide, section dividers |
| Title | 32 | Bold | primary | 1.15 | Every content slide title |
| Lead | 20 | Regular | slate | 1.3 | One-line subtitle under the title |
| Body | 18 | Regular | ink | 1.35 | Bullets, card text, table text |
| Wordmark | 20 | Regular, serif | wordmark-gray | 1.0 | Header text only |
| Header label | 14 | Bold, caps, +1.5 pt letter spacing | header-label | 1.0 | Header right label only |
| Label | 14 | SemiBold or Bold | primary or accent | 1.2 | Card headers, chips, step tags (caps allowed) |
| Caption | 12 | Regular | slate | 1.2 | Footer, sources, figure notes |
| Code | 16 | Regular | ink on surface-alt | 1.3 | Code, queries, paths, IDs |
| Stat | 54 | Bold | accent | 1.0 | One big number per slide |

Label and Header label (14) are the only sizes between Caption and Body. Wordmark (20) matches Lead and is used once per slide. Do not add others.

Text rules:
- Titles: max 2 lines, about 60 characters. Lead: one line, about 90 characters.
- Bullets: use a single bullet glyph, 18 pt left indent, 8 pt space after.
- Bold for key terms only, never whole sentences.
- No underline except hyperlinks (accent, underlined).
- No all-caps body text. All-caps allowed only for Label style, max 3 words.

## 3. Spacing and grid

| Token | Value | Use |
|---|---|---|
| `margin-x` | 48 | Left and right outer margin |
| `margin-top` | 36 | Top margin to title baseline zone |
| `header-zone` | y 18 to 46 | Subtle institutional header |
| `title-zone` | y 50 to 106 | Title (and lead at y 108 to 132) |
| `content-zone` | y 142 to 452 | All content |
| `takeaway-zone` | y 456 to 492 | Optional takeaway bar |
| `footer-zone` | y 504 to 528 | Footer |
| `gutter` | 24 | Gap between columns and cards |
| `pad` | 16 | Padding inside cards |
| `radius` | 8 | Card corner radius (0 for tables and code blocks) |
| `stroke` | 1 | Card and divider line weight, `border` color |
| `arrow-stroke` | 2 | Flow arrows, `accent` color |

Grid: 12 columns across 864 pt (960 minus 2 x 48), 24 pt gutters. Cards span 4 (three-up),
6 (two-up), 3 (four-up), or 12 (full width).

Alignment: snap every edge to the grid or to a 8 pt baseline. Distribute equal widths and
equal gaps. Top-align cards in a row.

## 4. Standard elements

**Header (every slide, including the title slide):** subtle and on the plain `surface` background, with no fill band. Left: the text "Carnegie Mellon University" in the Wordmark style (light gray serif in the style of the CMU wordmark, 20 pt; Bodoni MT, then Libre Bodoni, Playfair Display, Georgia), at x 48, y 18. Right: a short label in the Header label style, right-aligned to the right margin, in the form `CAPSTONE / CITY OF PHILADELPHIA` (two short caps phrases separated by a slash, slash in `accent`, text in `header-label`). No rule under the header. It must stay quieter than the title: never darker or larger than the slide title. The real CMU wordmark is official artwork, not an installable font, so this header is typeset text in a lookalike serif while the rest of the deck uses CMU's preferred typeface, Open Sans. If the official wordmark image (light gray version from CMU's brand downloads) is available, swap it in at the same size and position.

**Footer (every slide except title):** slide number only, right aligned in Caption, at y 504. A 1 pt `border` rule above at y 500 is optional. The deck label lives in the header, not the footer.

**Takeaway bar (optional):** full content width, `primary-tint` fill, no edge stripe, Body text in `ink`, one sentence, at most 20 words. It states the single thing the audience should remember.

**Tartan strip:** a 4 pt strip along the very top edge of every slide, segments 30/10/30/10/20 percent in `accent`, `highlight`, `surface`, `iron`, `accent`. It is the only decorative element in the deck.

**Terminal card:** a dark log or command window for real output (logs, JSON, query results). Fill `#23262B`, radius 8, pad 14. Title bar at the top: three 8 pt dots (`#EF6B6B`, `#F5C542`, `#6BD48C`), then a Code-style title in `#9AA1AB` such as `Query results . 7f3a9c2e`, then a 1 pt rule `#3A3F47`. Body in Code style (16 pt), text `#E6E8EB`, columns aligned with spaces, highlight key tokens with `#F5C542` (warn) or `#EF6B6B` (error). At most 6 lines per card. Use real output from the project, never invented data.

**Card:** `surface` fill, no outline, one soft shadow (`shadow.card` in tokens.json: navy at 14 percent, 10 pt blur, 3 pt down), radius 8, pad 16. Header in Label style,
body in Body style. Emphasis card: `primary-tint` fill with no outline.

**Chip (status or output tag):** Label style, `accent-tint` fill with `accent` text, or
`warning-tint` fill with `warning` text. Radius 12, pad 4 x 10.

**Flow arrow:** 2 pt `accent`, triangle head, straight or single-elbow only.

**Code block:** `surface-alt` fill, 1 pt `border`, radius 0, Code style, pad 12.

**Table:** header row `primary-tint` fill with Label style in `primary`; body Body style;
1 pt `border` horizontal rules only, no vertical rules, no zebra stripes.

**Icons:** one outline set at one stroke weight, `primary` or `accent`. Emoji only on
the goals and recap slides, as in the reference deck.

## 5. Scaling

If the canvas is not 960 x 540 pt, multiply every size and spacing value by
`canvas_width / 960`. Round font sizes to the nearest whole point. For 4:3 (720 x 540),
keep font sizes unchanged and reduce `margin-x` to 40 and card counts per row by one.

## 6. Visualization style

Derived from the reference terminal visual. Every visual (diagram, chart, code or log window)
follows the same five rules:

1. **Minimal:** one idea per visual, no gridlines, legends, or borders unless they carry data.
2. **Condensed:** short labels, tight line spacing, at most 6 log lines or 8 diagram nodes.
   Trim real data to the few lines that make the point.
3. **Contained:** each visual sits in one rounded container (radius 12) with the soft card
   shadow and no outline.
4. **Dark for output, light for structure:** logs, JSON, regexes, and query results use the dark
   terminal fill; flows, cards, and charts use white cards.
5. **One highlight:** at most one highlighted token or element per visual (gold on dark, red
   on light). Everything else is neutral.

Use real project output only. Never invent data to fill a visual.

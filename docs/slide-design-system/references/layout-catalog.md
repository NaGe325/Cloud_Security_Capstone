# Layout Catalog

Every layout uses the same skeleton from `design-tokens.md`: subtle Header, Title, optional
Lead, content zone, optional Takeaway bar, slide number. Pick the layout by the **shape of the content**.

## Contents
- Choosing a layout
- L01 Title
- L02 Section divider or question
- L03 Goals and recap
- L04 Three-up cards
- L05 Flow (pipeline)
- L06 Two-column compare
- L07 Table
- L08 Code and output
- L09 Timeline
- L10 Stat callout
- L11 Before and after
- L12 Next steps
- L13 Annotated diagram
- Patterns borrowed from the reference deck

## Choosing a layout

| Content shape | Layout |
|---|---|
| Deck opening | L01 |
| Change of topic, or a question that motivates the next slides | L02 |
| What the audience will learn, or what they learned | L03 |
| 2 to 4 parallel concepts (Logs / Metrics / Traces) | L04 |
| Ordered stages with inputs and outputs | L05 |
| Two options, two views, or pros and cons | L06 |
| Facts across the same attributes | L07 |
| Code, query, config, plus its result | L08 |
| Dates, milestones, schedule | L09 |
| One number that matters | L10 |
| State change, earlier vs now | L11 |
| Actions, owners, goals | L12 |
| A picture needs explanation | L13 |

---

## L01 Title
Background `primary`. Display title in `on-primary`, left aligned at y 200. Lead in
`on-primary` at 80 percent opacity below it. Caption line at bottom: presenter, date, event.
Keep the subtle header; no slide number.

## L02 Section divider or question
Background `primary` (section) or `surface-alt` (question). Display text only, at most
12 words, vertically centered, left aligned with `margin-x`. Use a question ("Which events belong to the same request?") to motivate the
next slides. Keep the footer on question slides, drop it on section slides.

## L03 Goals and recap
Title "Learning goals" or "What we covered". Up to 5 numbered items in Body, 12 pt between.
The recap slide repeats the goals wording exactly, prefixed by a check mark.

## L04 Three-up cards
Three cards, span 4 columns each. Card header in Label style (`primary`), one-line
definition in Body, optional example chip at the bottom. Equal heights, top aligned.
Takeaway bar below. Use for any "A vs B vs C" set of concepts.

## L05 Flow (pipeline)
3 to 7 steps left to right. Each step is a card with: numbered chip (Label), step name
(Label, caps), INPUT line (Caption), one-line action (Body), OUTPUT chip (`accent-tint`).
2 pt `accent` arrows between cards. If more than 4 steps, use two rows joined by an elbow
arrow, or shorten each card to name plus OUTPUT chip. A one-line chain under the flow
(for example "Filings, chunks, candidate chunks, evidence facts") may serve as the takeaway.

## L06 Two-column compare
Two cards, span 6 columns each, with Label headers. Optional `accent` edge on the recommended
side. One takeaway bar decides between them.

## L07 Table
Header row `primary-tint`. Max 6 rows, 4 columns. First column in Label style. No vertical
rules. Use for question-to-evidence mappings, schemas, and configs.

## L08 Code and output
Left: code block (6 to 12 lines, Code style). Right: a Terminal card with the real output.
Caption under each naming what it is. Highlight at most 2 lines with `accent-tint` fill.

## L09 Timeline
Horizontal rule in `border`, milestone dots in `accent` (done) or `border` (pending). Date
in Label above the dot, milestone name in Body below. Max 6 milestones. Mark slippage with
a `warning` chip, not by recoloring the line.

## L10 Stat callout
One Stat number (54 pt, `accent`) on the left, two lines of Body explanation on the right.
Optional small supporting row of up to 3 stats in Body.

## L11 Before and after
Two columns labelled "Earlier" and "Now" (or Before and After). Matching rows so the eye
compares across. Changed values in `warning` (worse) or `success` (better), plus a word
or arrow. Takeaway bar names the conclusion.

## L12 Next steps
3 to 5 numbered cards in a grid. Each card: action (Label), GOAL line (Caption), up to 3
Body bullets. A closing line in a takeaway bar gives the time horizon ("Our plan for the
coming weeks").

## L13 Annotated diagram
Diagram on the left 8 columns, numbered callouts (accent circles) on the image, and a
4-column right rail with one Body sentence per callout. Diagram uses only token colors.

---

## Patterns borrowed from the reference deck

- **Title plus claim:** titles state the point; the lead adds scope.
- **Takeaway bar:** a single sentence at the bottom of the slide ("Each signal gives us a
  different view of system behavior").
- **Question transitions:** a full-slide question before each new subtopic (L02).
- **Repeated patterns:** the same card or flow format is reused so the audience learns
  the visual grammar once.
- **Running example:** one concrete scenario (TinyNotes) threads through the deck; choose
  one concrete example for your own deck and reuse it.
- **Before and after tables:** show state change with matching rows (L11).
- **Warning callouts:** use `warning-tint` callouts with the word "Warning" for pitfalls.
- **Goals at both ends:** open and close with the same goals list (L03).
- **Identical footer:** same label and number position on every slide.
- **Activity slides:** when the audience must act, use a slide with a numbered task list
  and a time box.

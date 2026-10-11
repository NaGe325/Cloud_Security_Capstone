---
name: slide-design-system
description: A model-agnostic and provider-agnostic design system for presentations. Defines design tokens (one font family, a fixed type scale, a complementary color palette, spacing grid), a catalog of clean slide layouts, and a restyle workflow with an audit checklist. Use whenever the user wants to create, redesign, restyle, clean up, or standardize a slide deck, presentation, pitch, lecture, or project update, in any tool (PowerPoint, Google Slides, Keynote, HTML, Beamer, Markdown decks). Trigger on requests like "make my slides consistent", "fix fonts and colors", "professional template", "clean design", "restyle this deck", or "make it look like a lecture deck", even if the user never says "design system".
---

# Slide Design System

A portable design spec for presentations. It is deliberately tool-neutral: the rules are
expressed as tokens (named values) and layouts (named patterns). Any model or slide tool
can apply them. Tool-specific notes live in `references/adapters.md`.

The design philosophy is: one idea per slide, a short title plus a one-line
lead, a takeaway sentence at the bottom, question-driven transitions, repeated card and
flow patterns, and an identical footer on every slide.

## When to read what

| Need | Read |
|---|---|
| Exact colors, fonts, sizes, spacing | `references/design-tokens.md` (machine-readable copy: `assets/tokens.json`) |
| Which layout to use for a piece of content | `references/layout-catalog.md` |
| Applying tokens in a specific tool | `references/adapters.md` |
| Restyling an existing deck | `references/restyle-workflow.md` |
| Worked example on a real deck | `references/example-capstone-deck.md` |
| Talking points or full text for every slide | `references/speaker-notes.md` |
| Automated consistency check of a .pptx | `scripts/audit_deck.py` (optional, needs python-pptx) |

## Core rules (memorize these)

1. **One font family for text, one monospace family for code.** Never mix more.
2. **Five text sizes only:** Display 44, Title 32, Lead 20, Body 18, Caption 12 (pt, on a
   960 x 540 pt 16:9 slide). Code is 16. Nothing else. Minimum body size is 16.
3. **One primary color, one accent, one warning color.** Everything else is neutral
   (ink, slate, border, surface). Max two non-neutral colors per slide area.
4. **Every slide has the same skeleton:** a subtle header (light gray serif wordmark left,
   short caps label right), Title (top left), optional Lead line, content zone, optional
   Takeaway bar, slide number bottom right. The header is never a filled band.
5. **One idea per slide.** If a slide needs two headlines, split it.
6. **Left-align text.** Center only display titles, stat numbers, and diagram labels.
7. **Sentence case titles** written as claims or questions, not topics
   ("Layers 1 to 3 are deterministic and recall-first", not "Layers 1-3").
8. **Whitespace is a feature.** Keep at least 48 pt outer margin and 24 pt between blocks.
9. **Cap density:** at most 6 bullets, at most 12 words per bullet, at most 3 cards per
   row (4 only for short labels), at most 7 flow steps.
10. **Show real output in terminal cards.** Logs, JSON, and query results go in dark terminal
    windows (see the Terminal card in `design-tokens.md`), as in the reference deck.
11. **Shapes carry meaning, not decoration.** Cards group, arrows show flow, colored
    tags show status. No shadows, gradients, clip art, or stock-photo backgrounds.

## Workflow

### A. Build a new deck
1. Write the outline as a list of slide claims (titles). Add a recap slide that repeats the
   goals slide wording.
2. Assign each slide a layout ID from `references/layout-catalog.md`.
3. Fill in content, obeying the density caps (rule 9).
4. Apply tokens through the adapter for the target tool.
5. **Write speaker content for every slide.** Ask the author once: talking points or full
   text (default: talking points). Follow `references/speaker-notes.md` and put it in the
   speaker-notes field.
6. Run the audit checklist in `references/restyle-workflow.md` section 4.

### B. Restyle an existing deck
Follow `references/restyle-workflow.md`. In short: inventory, map each slide to a layout,
rebuild on a master/theme that holds the tokens, move content over without rewriting
meaning, write or update speaker content (talking points or full text), audit, and report
what changed.

## Output expectations

- Put tokens in the tool's **theme or master** (theme fonts, theme colors, master
  placeholders), not as per-shape overrides, so the deck stays consistent when edited.
- Preserve the author's content and meaning. Tighten wording only to meet density caps,
  and list any cuts in the change report.
- Keep hyperlinks, speaker notes, and alt text.
- Every slide has speaker content (talking points or full text) in the notes field, sourced
  only from the deck and the author, with unknowns marked `[confirm: ...]`.
- End with a short change report: fonts unified, sizes normalized, colors remapped,
  slides re-laid-out, and anything that needs the author's decision.

## If the tool cannot do something

Fall back in this order: theme/master setting, then a layout placeholder, then a direct
per-shape style that uses exactly the token value. Never invent a new size or color.

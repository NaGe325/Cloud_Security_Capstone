# Speaker Content: talking points or full text for every slide

Every slide gets speaker content. It lives in the tool's speaker-notes field, never on the
slide itself. This keeps slides sparse (see the density caps) while the presenter still has
the full story.

## Step 0: pick a mode (ask once per deck)
Ask the author once: "Talking points or full text?" If they do not answer, default to
**talking points**. Use the same mode for the whole deck unless told otherwise.

| Mode | Shape | Length per slide | Best for |
|---|---|---|---|
| Talking points | 3 to 5 bullets, then one transition line | 40 to 80 words | Presenters who know the material |
| Full text | Spoken script in short paragraphs, then one transition line | 90 to 170 words (about 40 to 80 seconds at 130 words per minute) | Rehearsal, handoffs, or timed talks |

## Rules for both modes
1. **Source only from the deck and the author.** Do not invent facts, numbers, dates, or
   results. If something is needed but unknown, write `[confirm: ...]` so the author
   can fill it in. Never leave a `[confirm]` unflagged in the change report.
2. **Add, do not repeat.** Notes explain why and so what. Do not read the slide text back.
3. **Follow the slide's claim.** Open with the slide title's point, then the evidence, then
   the takeaway sentence.
4. **End with a transition** to the next slide ("Next, how routing decides each tier."). The
   last slide ends with the ask or the close.
5. **Spoken style** (full text): short sentences, contractions, active voice, no jargon
   without a definition, numbers written the way they are said.
6. **Keep presenter reminders here**, not on the slide (for example "confirm the dataset with
   the professor"). Mark them with `TODO:` so they are easy to find.
7. **Preserve existing notes.** When restyling, keep the author's notes and only add or
   tighten; list changes in the change report.
8. Include a one-line time estimate at the top of the notes for full text, for example
   `(~60 s)`.

## Templates

Talking points:
```
- Claim in one sentence.
- Evidence or detail 1.
- Evidence or detail 2.
- Why it matters.
Transition: Next, ...
```

Full text:
```
(~60 s) Opening sentence that states the claim. Two or three sentences of evidence, each
one idea. One sentence on why it matters. Transition: Next, ...
```

## Optional extras (only if asked)
- Likely questions and short answers, 2 or 3 per key slide.
- A one-page script export (a document with slide number, title, and notes) for rehearsal.

# Worked Example: 9-slide project update deck

A real deck (a city tax-compliance data pipeline, six layers from SEC filings to an
investigator dashboard) mapped onto this design system. Use it as a model of how to classify
slides, rewrite titles as claims, and respect density caps. Content is preserved; only
structure and wording length change.

| # | Current title | Layout | Action | Proposed title (claim) |
|---|---|---|---|---|
| 1 | City of Philadelphia Project Update | L01 | Keep | City of Philadelphia project update (lead: SEC filings to investigator leads; add presenter and date) |
| 2 | System Architecture Overview | L05 | Tighten | Six layers turn one filing into an investigator lead |
| 3 | Original Projected Timeline | L09 | Keep | Ingestion landed on time; scoring and the dashboard come later |
| 4 | Layers 1-3: From Filing to Candidate Chunks | L05 | Tighten | The first half is deterministic and recall-first |
| 5 | Layers 4-6: From Candidate Chunk to Investigator Lead | L05 | Tighten | The second half interprets, scores, then hands off to a human |
| 6 | Layer 1: SEC Data Ingestion | L05 + L07 | Split | Ingestion keeps every original filing traceable |
| 7 | Layer 2: Data Preprocessing | L05 | Tighten | Preprocessing turns filings into traceable chunks |
| 8 | Layer 3: Regex Routing | L04 | Tighten | Each chunk lands in exactly one routing tier |
| 9 | Next Steps | L12 | Split | Five next steps, in two groups |

Verify the title claims against the author's actual status before using them. The timeline
wording above is a suggestion, not a fact check.

## Per-slide notes

**Slide 2 (architecture).** Six cards on one row is the maximum. Each card: number chip,
layer name (Label), OUTPUT chip. Move the INPUT lines and the per-step actions to slides 4 and
5, where they already appear. Put the chain "Filings, chunks, candidate chunks, evidence
facts, company ranking, human review" in the takeaway bar.

**Slide 3 (timeline).** Six milestones with dates on an L09 rule. Verify which date belongs to
which layer before finalizing (the extracted text lists 9/18 three times, then 11/13, 10/30,
10/30). Mark any slipped milestone with a `warning` chip.

**Slides 4 and 5 (layer overviews).** Three cards each (L05). Trim card bullets to 4 lines of
at most 12 words. Move the long spaCy and dedupe details into speaker notes or the layer slides.
The sentences "Recall-first: Layer 3 identifies chunks worth reading..." and "Layer 4 interprets
potential activity; Layer 5 ranks it..." become takeaway bars. Keep the "Keep for midterm"
flags as `warning` chips in the top right, not as free text.

**Slide 6 (ingestion).** Three steps (Discover, Archive, Track and verify) as L05 with OUTPUT
chips. Put the current configuration (16 companies, one annual 10-K each, S3 storage by default
with a local option) in a right-hand card and keep the two hyperlinks. Move the 16 ticker and CIK
pairs to an appendix slide as an L07 table in 4 columns, using Code style for the identifiers.
The presenter reminder "Talk about MVP dataset, get confirmation" belongs in speaker notes.

**Slide 7 (preprocessing).** Three steps (Extract, Chunk, Route) as L05. Keep the chunking
facts (up to 4,000 characters, 400-character overlap, section and block references) and the
lexicon facts (editable, three kinds, optional custom detectors) as short bullets inside the
Chunk and Route cards. The line "Read, split into blocks and cells, keep visible text, keep table
rows and text offsets" becomes the Extract card body.

**Slide 8 (routing tiers).** Four tier cards (geographic Tier 2, activity_only Tier 1,
caution_review Tier 1, unmatched Tier 0) as a 2 x 2 grid or a four-up row with short text. Each
card: tier name linked to its sample JSON (keep links), tier chip, one-line meaning, one code-style
regex or example. Sort from highest to lowest priority. Takeaway bar: "Every chunk is kept in
chunks.jsonl; the tier only decides review priority."

**Slide 9 (next steps).** Five items exceed the three-per-row cap. Make slide 9a "Next steps"
(Select a database, Build a web service, Harden the pipeline) and slide 9b "Our plan for the
coming weeks" (Talk to professors on scoring, Compare LLM models and prompts). Each card keeps
its GOAL line as a Caption and up to three bullets.

## Final check for this deck
Run the audit checklist in `restyle-workflow.md`, then render every slide to an image. The
highest-risk slides for overflow are 4, 5, and 6.

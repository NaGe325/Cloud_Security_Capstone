# Original presentation, completed

Use the [updated original PDF](../slides/MedTech-Security-Baseline-Slides.pdf) for submission. It still contains the original 12 slides and uses the original design, images, tables and order. The [unchanged source PDF](../slides/original/MedTech-Security-Baseline-Slides.pdf) is preserved separately.

Focused changes only:
- Slide 1: add Charlotte Zhang and Nana Ge in existing whitespace.
- Slide 6: correct steps 4/5 to Notify then Measure, preserving the original process boxes and table.
- Slide 9: retain the original HTML-report screenshot and enlarge the root-MFA evidence as readable text.
- Slide 10: keep the four measured statistics and add explicitly illustrative time/cost calculations below them.

All other eight pages have unchanged content streams and pixel-identical renders at the verification resolution. Details are in examples/slides-preservation.json. The replacement text is removed from its old text objects before new text is added, so the old claims are not merely covered visually.

English speaking notes remain in [SPEAKER_NOTES.md](SPEAKER_NOTES.md), with the original narrative preserved and slide 10 updated. Rehearse for 15–20 minutes including demo and questions.

The [original Google Slides](https://docs.google.com/presentation/d/11W8AE5Fn5un-FhWMLC6scesZQe5N5m9bFQFXPzMcSjA/edit) remain unchanged. This update does not claim access to or edits in that private native deck. No rebuilt editable PPTX is included in the final package, in accordance with the request to continue the original presentation.

Reproduce the PDF edits with `python -m pip install -r requirements-slides.txt` followed by `python scripts/update_original_slides.py`. It verifies the source hash and preservation of all unchanged pages. Viewing the supplied PDF needs no development dependencies.

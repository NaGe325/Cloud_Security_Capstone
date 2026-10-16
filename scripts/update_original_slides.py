"""Make four focused edits to the original PDF. Preserve all other pages.

Requires requirements-slides.txt. Uses the supplied PDF directly, without rebuilding
its theme, tables, images or slide order. Removed text is deleted from its text
objects before replacement, rather than hidden behind an opaque rectangle.
"""
from io import BytesIO
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "slides/original/MedTech-Security-Baseline-Slides.pdf"
TARGET = ROOT / "slides/MedTech-Security-Baseline-Slides.pdf"
SOURCE_SHA256 = "0bb752430fabd16d4c689507a5a79ffae270471841b8b16bf804cae2d0a8b7eb"
FONT = ROOT / "slides/assets/fonts/OpenSans-Variable.ttf"


def multiply(a, b):
    return [a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3],
            a[4]*b[0]+a[5]*b[2]+b[4], a[4]*b[1]+a[5]*b[3]+b[5]]


def remove_text_groups(page, reader, positions):
    stream = ContentStream(page.get_contents(), reader)
    matrix = [1, 0, 0, 1, 0, 0]
    stack, output, removed = [], [], 0
    skipping = False
    for args, op in stream.operations:
        if op == b"q":
            stack.append(matrix[:])
        elif op == b"Q":
            matrix = stack.pop()
        elif op == b"cm":
            matrix = multiply([float(v) for v in args], matrix)
        if op == b"BT":
            skipping = any(abs(matrix[4]-x) < .1 and abs(matrix[5]-y) < .1 for x,y in positions)
            removed += int(skipping)
        if not skipping:
            output.append((args, op))
        if op == b"ET":
            skipping = False
    if not removed:
        raise ValueError("Expected original text group was not found")
    stream.operations = output
    page.replace_contents(stream)
    return removed


def overlay(page, draw):
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=(960, 540), invariant=1)
    def text(x, y, value, size=14, color="#55595F"):
        if pdfmetrics.stringWidth(value, "OpenSans", size) > 960-x-35:
            raise ValueError(f"Text exceeds slide margin: {value}")
        canvas.setFont("OpenSans", size)
        canvas.setFillColor(color)
        canvas.drawString(x, y, value)
    draw(text)
    canvas.save()
    page.merge_page(PdfReader(BytesIO(buffer.getvalue())).pages[0])


def main():
    original_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if SOURCE_SHA256 and original_hash != SOURCE_SHA256:
        raise ValueError("Original source PDF changed; inspect before updating")
    pdfmetrics.registerFont(TTFont("OpenSans", str(FONT)))
    reader = PdfReader(SOURCE)
    # The supplied PDF has a dangling /Outlines reference. Drop only that invalid
    # optional catalog pointer in memory, leaving source bytes/pages unchanged.
    catalog = reader.trailer["/Root"]
    outlines = catalog.get("/Outlines")
    if outlines is not None and outlines.idnum not in reader.xref.get(outlines.generation, {}):
        del catalog["/Outlines"]
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    assert len(writer.pages) == 12
    removed = {}
    # Cover: add both authors in the original whitespace, keeping all original text.
    overlay(writer.pages[0], lambda t: t(455, 111, "Charlotte Zhang and Nana Ge", 18, "#1B2A49"))
    # Slide 6: keep original process boxes and table, fix the two final labels.
    removed[6] = remove_text_groups(writer.pages[5], writer, [(580, 375), (748, 375)])
    def process(t):
        t(580, 350.92, "4 Notify", 14, "#FFFFFF")
        t(580, 333.52, "summary only", 12, "#FFFFFF")
        t(748, 350.92, "5 Measure", 14, "#FFFFFF")
        t(748, 333.52, "opt-in metrics", 12, "#FFFFFF")
    overlay(writer.pages[5], process)
    # Slide 9: keep the actual original screenshot and findings; enlarge one key fact.
    def evidence(t):
        t(604, 140, "ROOT EVIDENCE (SIMULATED)", 12, "#1B2A49")
        t(604, 117, "AccountMFAEnabled: 0", 16, "#C41230")
        t(604, 96, "Validate context before remediation.", 11)
    overlay(writer.pages[8], evidence)
    # Slide 10: preserve the four measured statistics. Replace only title and lower text.
    removed[10] = remove_text_groups(writer.pages[9], writer,
        [(64, 466), (64, 225), (64, 197), (490, 225), (490, 197), (350, 40)])
    def value(t):
        t(64, 437.2, "Validation and estimated operational value", 29, "#4A4A4A")
        t(64, 210, "Time savings (illustrative)", 16, "#1B2A49")
        t(64, 182, "30 runs x (15 - 5) human minutes = 5 hours/month", 12)
        t(64, 162, "66.7% less human time for these five checks.", 12)
        t(64, 142, "$300 staff capacity at assumed $60/hour.", 12)
        t(64, 122, "Human timing is assumed, not measured.", 12)
        t(490, 210, "Cloud cost (illustrative)", 16, "#1B2A49")
        t(490, 182, "~$0.02 base / ~$4.12 with optional monitoring.", 12)
        t(490, 162, "30 daily runs, 256 MB Arm, assumed 30 sec/run.", 12)
        t(490, 142, "Rounded-up budgets before credits and exclusions.", 12)
        t(490, 122, "Live IAM, scheduling and email need a pilot.", 12)
        t(350, 29.44, "Assumptions, rates and sources: docs/VALUE_AND_COST.md", 10)
    overlay(writer.pages[9], value)
    writer.add_metadata({"/Title":"MedTech Security Baseline Checker", "/Author":"Charlotte Zhang and Nana Ge"})
    with TARGET.open("wb") as f:
        writer.write(f)
    final = PdfReader(TARGET)
    unchanged = [2,3,4,5,7,8,11,12]
    for number in unchanged:
        assert reader.pages[number-1].get_contents().get_data() == final.pages[number-1].get_contents().get_data(), number
    assert "Charlotte Zhang and Nana Ge" in final.pages[0].extract_text()
    assert "4 Notify" in final.pages[5].extract_text() and "5 Measure" in final.pages[5].extract_text()
    assert "4 Measure" not in final.pages[5].extract_text() and "5 Notify" not in final.pages[5].extract_text()
    assert "AccountMFAEnabled: 0" in final.pages[8].extract_text()
    assert "5 hours/month" in final.pages[9].extract_text()
    report = {"source_commit":"79d6c6e6a4a57d46495c8e77dea893503977b12e", "source_sha256":original_hash,
        "final_sha256":hashlib.sha256(TARGET.read_bytes()).hexdigest(), "slide_count":12,
        "changed_slides":[1,6,9,10], "unchanged_content_streams_verified":unchanged,
        "removed_text_groups":removed, "method":"targeted PDF text edits preserving original page artwork/layout"}
    (ROOT/"examples/slides-preservation.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__ == "__main__":
    main()

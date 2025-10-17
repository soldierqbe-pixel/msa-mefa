from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def build_pdf(study, analysis: dict) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4

    y = H - 20*mm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, y, "Measurement System Analysis – R&R")
    y -= 10*mm

    c.setFont("Helvetica", 10)
    left = 20*mm
    line = 6*mm

    hdr = [
        ("Date", study.date),
        ("Part", study.part_name),
        ("Caliper", study.caliper_number),
        ("Nominal", str(study.nominal_value)),
        ("LSL", str(study.lsl) if study.lsl is not None else "-"),
        ("USL", str(study.usl) if study.usl is not None else "-"),
        ("Lead", study.test_lead),
        ("Operators", f"{study.operator_a}, {study.operator_b}, {study.operator_c}"),
    ]
    for k,v in hdr:
        c.drawString(left, y, f"{k}: {v}")
        y -= line

    y -= 4*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left, y, "Summary")
    y -= line
    c.setFont("Helvetica", 10)

    def draw_kv(dictlike):
        nonlocal y
        for k, v in dictlike.items():
            c.drawString(left, y, f"{k}: {v}")
            y -= line

    if 'summary' in analysis:
        draw_kv(analysis['summary'])

    y -= 4*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left, y, "Components / Table")
    y -= line
    c.setFont("Helvetica", 9)

    rows = []
    if 'components' in analysis:
        rows = analysis['components']
    elif 'range_table' in analysis:
        rows = analysis['range_table']

    for r in rows[:30]:
        line_txt = ", ".join(f"{k}: {v}" for k,v in r.items())
        c.drawString(left, y, line_txt[:110])
        y -= line
        if y < 20*mm:
            c.showPage(); y = H - 20*mm

    c.showPage()
    c.save()
    return buf.getvalue()

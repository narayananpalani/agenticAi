"""Generate the three sample documents for kinkyShoeBros.

Reproducible — learners can rerun this to regenerate the sample docs, or
adapt it to generate more variety.

Files generated:
  - kinkyshoebros_policies.pdf (Employee Shoe Allocation & Policies)
  - kinkyshoebros_catalog.html (Shoe Product Selection & Fitment Guide)
  - kinkyshoebros_preloved.docx (Pre-loved Shoe Sales Program & Trade-in Tiers)
"""
from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Pt

OUT = Path(__file__).parent / "sample_docs"
OUT.mkdir(exist_ok=True)


# ─── 1. PDF: kinkyshoebros_policies.pdf ──────────────────────────────

def make_pdf():
    path = OUT / "kinkyshoebros_policies.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=LETTER,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    heading = ParagraphStyle('h', parent=styles['Heading1'], fontSize=16, spaceAfter=12)
    subhead = ParagraphStyle('h2', parent=styles['Heading2'], fontSize=13, spaceAfter=8)
    body = ParagraphStyle('body', parent=styles['BodyText'], fontSize=10, spaceAfter=8, leading=14)
    
    story = []
    
    story.append(Paragraph("kinkyShoeBros — Internal Employee Handbook", heading))
    story.append(Paragraph("Section 1: Employee Footwear Allocation Program", subhead))
    story.append(Paragraph(
        "As representatives of kinkyShoeBros, retail and corporate employees are required to wear "
        "approved footwear during operating hours. The company provides a quarterly stipend and direct "
        "allocations to ensure staff are outfitted in the latest Nike, adidas, and New Balance releases.",
        body))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Approved Employee Allocation Roster (2026)", subhead))
    
    # Table with 15+ rows
    table_data = [
        ["Department / Role", "Approved Brand", "Model", "Allocation Frequency"],
        ["Retail Store Manager", "Nike", "Air Max 95", "Quarterly"],
        ["Retail Assistant Mgr", "adidas", "Ultraboost 1.0", "Quarterly"],
        ["Sales Associate Level 3", "New Balance", "990v6", "Bi-Annually"],
        ["Sales Associate Level 2", "ASICS", "Gel-Kayano 30", "Bi-Annually"],
        ["Sales Associate Level 1", "Nike", "Air Force 1", "Annually"],
        ["Stockroom Manager", "PUMA", "Suede Classic", "Bi-Annually"],
        ["Stockroom Assistant", "adidas", "Stan Smith", "Annually"],
        ["Warehouse Operations", "ASICS", "Gel-Nimbus", "Bi-Annually"],
        ["Logistics Coordinator", "New Balance", "2002R", "Bi-Annually"],
        ["Marketing Director", "Nike", "Jordan 1 Retro", "Quarterly"],
        ["Social Media Lead", "adidas", "Samba OG", "Quarterly"],
        ["Content Creator", "Nike", "Dunk Low", "Quarterly"],
        ["HR Business Partner", "New Balance", "550", "Bi-Annually"],
        ["Finance Analyst", "adidas", "Gazelle", "Annually"],
        ["Customer Support", "PUMA", "RS-X", "Annually"],
        ["IT Support Specialist", "Nike", "Pegasus 40", "Bi-Annually"],
    ]
    t = Table(table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0D243D')),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN',      (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(t)
    story.append(PageBreak())
    
    story.append(Paragraph("Section 2: HR & Support Contacts", subhead))
    story.append(Paragraph(
        "For allocation adjustments, contact HR Business Partner Sarah Chen at "
        "sarah.chen@kinkyshoebros.com (+1-555-0142). For payroll or stipend questions, "
        "contact Michael Torres in Finance (EMP-04521) at michael.torres@kinkyshoebros.com.",
        body))
    
    doc.build(story)


# ─── 2. HTML: kinkyshoebros_catalog.html ─────────────────────────────

def make_html():
    path = OUT / "kinkyshoebros_catalog.html"
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>kinkyShoeBros — Product Selection & Fitment Guide</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; }
    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; font-weight: bold; }
  </style>
</head>
<body>
  <main>
    <article>
      <h1>kinkyShoeBros Fitment Hub & Shoe Catalog</h1>
      <p class="lead">
        Finding the right pair is about getting the perfect fit for your unique foot shape. Use our 
        comprehensive fitment table below to match our top 16 best-selling models to your foot profile.
      </p>

      <h2>Customer Fitment Matrix (15+ Models)</h2>
      <table>
        <tr>
          <th>Brand</th>
          <th>Model</th>
          <th>Best For (Foot Type)</th>
          <th>Fitment Note</th>
          <th>Category</th>
        </tr>
        <tr><td>Nike</td><td>Air Max 90</td><td>Neutral / Average</td><td>True to size (TTS)</td><td>Lifestyle</td></tr>
        <tr><td>Nike</td><td>Air Force 1</td><td>Wide</td><td>Runs half size big, size down</td><td>Lifestyle</td></tr>
        <tr><td>Nike</td><td>Pegasus 40</td><td>Narrow / Medium</td><td>Snug midfoot lockdown</td><td>Running</td></tr>
        <tr><td>Nike</td><td>Dunk Low</td><td>Average</td><td>TTS, slightly narrow toe box</td><td>Streetwear</td></tr>
        <tr><td>Nike</td><td>ZoomX Invincible</td><td>High Arch</td><td>Maximum cushioning</td><td>Running</td></tr>
        <tr><td>adidas</td><td>Ultraboost 1.0</td><td>Medium</td><td>Primeknit stretches, TTS</td><td>Running / Casual</td></tr>
        <tr><td>adidas</td><td>Samba OG</td><td>Narrow</td><td>Very narrow, size up for wide feet</td><td>Heritage</td></tr>
        <tr><td>adidas</td><td>Stan Smith</td><td>Average</td><td>TTS, leather breaks in over time</td><td>Lifestyle</td></tr>
        <tr><td>adidas</td><td>NMD_R1</td><td>Wide</td><td>Generous mesh upper</td><td>Casual</td></tr>
        <tr><td>adidas</td><td>Gazelle</td><td>Narrow</td><td>Snug fit, low arch profile</td><td>Heritage</td></tr>
        <tr><td>New Balance</td><td>990v6</td><td>Wide (Available in 2E/4E)</td><td>Roomy toe box, excellent stability</td><td>Lifestyle / Running</td></tr>
        <tr><td>New Balance</td><td>550</td><td>Average</td><td>TTS, stiff leather initially</td><td>Retro Hoops</td></tr>
        <tr><td>New Balance</td><td>2002R</td><td>Average / High Arch</td><td>TTS, premium shock absorption</td><td>Lifestyle</td></tr>
        <tr><td>ASICS</td><td>Gel-Kayano 30</td><td>Overpronator / Flat Feet</td><td>Maximum stability and arch support</td><td>Running</td></tr>
        <tr><td>ASICS</td><td>Gel-Nimbus 25</td><td>Neutral / High Arch</td><td>Plush cushioning, TTS</td><td>Running</td></tr>
        <tr><td>PUMA</td><td>Suede Classic</td><td>Narrow / Average</td><td>TTS, flat sole</td><td>Lifestyle</td></tr>
        <tr><td>PUMA</td><td>RS-X</td><td>Wide</td><td>Chunky build, very accommodating</td><td>Streetwear</td></tr>
      </table>
    </article>
  </main>
</body>
</html>
"""
    path.write_text(html)


# ─── 3. DOCX: kinkyshoebros_preloved.docx ────────────────────────────

def make_docx():
    path = OUT / "kinkyshoebros_preloved.docx"
    doc = Document()
    
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    
    doc.add_heading('kinkyShoeBros Pre-Loved Shoe Sales Program', level=0)
    
    doc.add_paragraph(
        "The kinkyShoeBros Pre-Loved Program extends the lifecycle of premium footwear. "
        "Every trade-in is evaluated against our 16-tier condition grading system to determine "
        "your exact store credit and the resale market price."
    )
    
    doc.add_heading('Trade-In Grading & Valuation Table', level=1)
    
    # Table with 15+ rows
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Condition Grade'
    hdr_cells[1].text = 'Description'
    hdr_cells[2].text = 'Trade-In Payout (% of Market)'
    
    grades = [
        ("Grade 10 (DS)", "Deadstock, unworn, original box and tags intact.", "85%"),
        ("Grade 9.5 (VNDS)", "Very Near Deadstock, tried on once indoors.", "80%"),
        ("Grade 9.0", "Worn 1-2 times, no visible creasing, clean soles.", "75%"),
        ("Grade 8.5", "Minimal creasing, flawless uppers, 95% tread left.", "70%"),
        ("Grade 8.0", "Light creasing, minor dust on outsoles, clean insoles.", "65%"),
        ("Grade 7.5", "Slight scuffs on midsole, light heel drag.", "60%"),
        ("Grade 7.0", "Noticeable wear, moderate creasing, intact original laces.", "55%"),
        ("Grade 6.5", "Moderate heel drag, small stains on uppers.", "50%"),
        ("Grade 6.0", "Significant creasing, yellowing on clear outsoles.", "45%"),
        ("Grade 5.5", "Replacement box required, worn outsoles, scuffed toe box.", "40%"),
        ("Grade 5.0", "Heavy wear, missing original insoles, paint chipping.", "35%"),
        ("Grade 4.5", "Severe heel drag, minor sole separation starting.", "30%"),
        ("Grade 4.0", "Beater condition, rips in inner lining, heavy scuffs.", "25%"),
        ("Grade 3.5", "Major structural wear, requires deep cleaning and reglue.", "20%"),
        ("Grade 3.0", "Sole completely hardened/crumbled, uppers intact.", "15%"),
        ("Grade 2.0", "Scrap condition, harvested for laces/materials only.", "10%"),
    ]
    
    for grade, desc, payout in grades:
        row_cells = table.add_row().cells
        row_cells[0].text = grade
        row_cells[1].text = desc
        row_cells[2].text = payout

    doc.add_heading('Support Contacts', level=2)
    doc.add_paragraph(
        "For verification disputes, contact the Pre-Loved Support desk at preloved@kinkyshoebros.com. "
        "Program Lead: Priya Sharma (EMP-01847)."
    )
    
    doc.save(str(path))


if __name__ == "__main__":
    make_pdf()
    make_html()
    make_docx()
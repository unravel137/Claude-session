from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins (narrow to fit on ~2 pages) ──────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin   = Cm(2.2)
    section.right_margin  = Cm(2.2)

# ── Helpers ───────────────────────────────────────────────────────────────
DARK_GREEN  = RGBColor(0x1A, 0x5C, 0x3A)
MID_GREEN   = RGBColor(0x2D, 0x9B, 0x6F)
DARK_GRAY   = RGBColor(0x33, 0x33, 0x33)
LIGHT_GRAY  = RGBColor(0xF2, 0xF2, 0xF2)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)

def para_fmt(para, size=10, bold=False, color=None, space_before=0, space_after=4, align=None):
    para.paragraph_format.space_before = Pt(space_before)
    para.paragraph_format.space_after  = Pt(space_after)
    for run in para.runs:
        run.font.size  = Pt(size)
        run.font.bold  = bold
        if color:
            run.font.color.rgb = color
    if align:
        para.alignment = align

def add_heading(doc, text, size=12, color=DARK_GREEN, space_before=10, space_after=3):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size  = Pt(size)
    run.font.bold  = True
    run.font.color.rgb = color
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    # thin rule below
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot  = OxmlElement("w:bottom")
    bot.set(qn("w:val"),   "single")
    bot.set(qn("w:sz"),    "4")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), "2D9B6F")
    pBdr.append(bot)
    pPr.append(pBdr)
    return p

def add_body(doc, text, size=9.5, space_before=0, space_after=5):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    for run in p.runs:
        run.font.size = Pt(size)
        run.font.color.rgb = DARK_GRAY
    return p

def add_bullet(doc, text, size=9.5):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.color.rgb = DARK_GRAY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(3)
    return p

# ── Title block ───────────────────────────────────────────────────────────
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("MERIDIAN TECHNOLOGIES")
r.font.size = Pt(15)
r.font.bold = True
r.font.color.rgb = DARK_GREEN
title.paragraph_format.space_before = Pt(0)
title.paragraph_format.space_after  = Pt(2)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = sub.add_run("Investor Day Positioning Memo  |  March 11, 2026  |  CONFIDENTIAL")
r2.font.size = Pt(9)
r2.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
sub.paragraph_format.space_before = Pt(0)
sub.paragraph_format.space_after  = Pt(2)

r3 = sub.add_run("\nFrom: Catherine Park, CEO")
r3.font.size = Pt(9)
r3.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# ── 1. Executive Summary ──────────────────────────────────────────────────
add_heading(doc, "Executive Summary")
add_body(doc,
    "Meridian will declare itself the agentic work platform built for the enterprise — "
    "the only platform where AI agents operate under the governance, auditability, and "
    "compliance controls that regulated industries require. Project management is the surface "
    "we started with; the agent framework acquired through Helio is the platform we are "
    "becoming. This memo sets out the competitive rationale for that choice, the three risks "
    "we are accepting, and the three commitments we are making to investors to hold us "
    "accountable. The board has been briefed. The internal communications team has nine days "
    "to build Investor Day materials around this position."
)

# ── 2. Our Position ───────────────────────────────────────────────────────
add_heading(doc, "Our Position")
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after  = Pt(6)
r = p.add_run(
    "“Meridian is the agentic work platform built for the enterprise — the only platform "
    "where agents run with the governance, auditability, and compliance controls that "
    "regulated industries require.”"
)
r.font.size   = Pt(10)
r.font.italic = True
r.font.color.rgb = DARK_GREEN
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ── 3. Why ───────────────────────────────────────────────────────────────
add_heading(doc, "Why This Position")
add_body(doc,
    "Four inputs drive this decision, all pointing the same direction:"
)
add_bullet(doc,
    "Customer demand. 18 of 22 enterprise advisory board sessions in the last 90 days "
    "raised agent governance unprompted — auditability, role-based agent permissions, model "
    "pinning, data residency. Customers are already thinking in agent terms. They want "
    "Meridian to govern those agents, not to be a faster PM tool."
)
add_bullet(doc,
    "Competitive white space. Asana and Monday are moving agentic but have thin governance. "
    "Atlassian is the most committed agentic platform but is software-team-shaped and cannot "
    "serve pharma, banking, or federal. Smartsheet has governance but has explicitly rejected "
    "the agentic frame. The intersection — enterprise governance for an agentic platform — "
    "is unoccupied."
)
add_bullet(doc,
    "The Helio acquisition. We paid $78M for an agent framework. The Helio team did not join "
    "Meridian to build AI features for a PM tool. Choosing Option A creates immediate "
    "retention risk on the most important technical talent we have acquired."
)
add_bullet(doc,
    "Financial capacity. $506M in liquidity, $250M estimated M&A capacity, $55M AI R&D "
    "already budgeted. The hiring pivot Option B requires is affordable. Option B’s 2028 "
    "upside scenario is $900M at 25% growth; the downside scenario is still $550M — "
    "a narrower range than it appears because Option A’s $700M ceiling assumes a PM "
    "category that is already commoditizing."
)

# ── 4. Competitive Landscape Table ────────────────────────────────────────
add_heading(doc, "Competitive Landscape")

headers = ["", "AI Positioning", "Pricing Posture", "Latest Flagship\nAnnouncement", "Closer to\nMeridian…"]
rows = [
    ["Asana",
     "\"Work management\nplatform with AI\nbuilt in\" — moving\ntoward agent OS\nlanguage",
     "AI bundled into\nAdvanced+ tiers;\nno consumption\npricing",
     "AI Studio + Smart\nWorkflows bundled\n(Nov 2025)",
     "Option B\n(thin governance)"],
    ["Monday.com",
     "\"Work OS,\nsupercharged\nwith AI\" — AI as\na layer, not a\nseparate product",
     "AI Agents bundled\ninto Pro+ tiers;\nno consumption\npricing",
     "monday AI Agents\nGA (Jan 2026)",
     "Option A framing,\nOption B execution"],
    ["Atlassian",
     "\"Agentic enterprise\nplatform\" — most\nexplicit agentic\ncommitment;\nRovo brand",
     "Hybrid: per-seat\n+ consumption\n(only competitor\nwith consumption\nlive today)",
     "Rovo Studio\nagent builder\n(Jan 2026)",
     "Option B\n(direct peer;\ndifferentiate\non verticals)"],
    ["Smartsheet",
     "\"Enterprise work\nplatform you can\ntrust with AI\" —\nexplicitly rejected\n\"agentic\"",
     "AI bundled in\nBusiness/Enterprise;\nCompliance Pack\nadd-on ~$15/seat",
     "AI Compliance\nPack (Dec 2025)",
     "Option A\n(direct peer;\nslowing growth)"],
]

col_widths = [Inches(0.85), Inches(1.55), Inches(1.35), Inches(1.45), Inches(1.05)]
tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

# Header row
hdr_cells = tbl.rows[0].cells
for i, h in enumerate(headers):
    hdr_cells[i].width = col_widths[i]
    set_cell_bg(hdr_cells[i], "1A5C3A")
    hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = hdr_cells[i].paragraphs[0]
    p.clear()
    run = p.add_run(h)
    run.font.size  = Pt(8)
    run.font.bold  = True
    run.font.color.rgb = WHITE
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)

# Data rows
row_bg = ["F9FFF9", "FFFFFF", "F9FFF9", "FFFFFF"]
for ri, row_data in enumerate(rows):
    cells = tbl.rows[ri + 1].cells
    for ci, text in enumerate(row_data):
        cells[ci].width = col_widths[ci]
        set_cell_bg(cells[ci], row_bg[ri])
        cells[ci].vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p = cells[ci].paragraphs[0]
        p.clear()
        run = p.add_run(text)
        run.font.size = Pt(8)
        run.font.bold = (ci == 0)
        run.font.color.rgb = DARK_GREEN if ci == 0 else DARK_GRAY
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after  = Pt(2)

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ── 5. Positioning Matrix ─────────────────────────────────────────────────
add_heading(doc, "Positioning Matrix")
p_img = doc.add_paragraph()
p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_img = p_img.add_run()
run_img.add_picture("positioning_matrix.png", width=Inches(5.8))
p_img.paragraph_format.space_after = Pt(4)

cap = doc.add_paragraph("Figure 1. Competitive positioning: X-axis PM-centric → Agentic; Y-axis Bundled → Premium. "
                         "Meridian Option B (dark diamond) occupies the enterprise agentic governance white space. "
                         "Dashed arrow shows the strategic move from Option A.")
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.paragraph_format.space_after = Pt(6)
for run in cap.runs:
    run.font.size = Pt(7.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# ── 6. Three Risks ────────────────────────────────────────────────────────
add_heading(doc, "Three Risks We Are Accepting")
add_bullet(doc,
    "Revenue air gap. We are declaring an agentic platform with $3.5M of AI ARR. "
    "Consumption pricing launches H2 2026; enterprise adoption typically runs 6–12 months "
    "behind plan. We are setting guidance conservatively to create room to beat it. "
    "If consumption ramps slower than planned, we have a narrative gap in Q3–Q4 2026."
)
add_bullet(doc,
    "Atlassian execution risk. Atlassian is already in the top-right quadrant with live "
    "consumption pricing and Rovo Studio in market. If Rovo matures beyond dev teams into "
    "general PM before we establish regulated-industry anchor wins, investors will ask why "
    "they own Meridian instead of Atlassian. Our answer is verticals — pharma, banking, "
    "federal — and we must demonstrate it with logos, not slides."
)
add_bullet(doc,
    "Model-lab consolidation. If Anthropic, OpenAI, or Microsoft ships enterprise agent "
    "governance natively — audit logs, role-based agent permissions, data residency — "
    "our governance moat shrinks. Mitigation: position Meridian as the model-neutral "
    "governance layer that works across any approved model. We do not partner exclusively "
    "with any one lab."
)

# ── 7. Three Commitments ──────────────────────────────────────────────────
add_heading(doc, "Three Commitments to Investors")
add_bullet(doc,
    "Regulated-industry anchor wins by Q3 2026. We will name at least three enterprise "
    "customers running production agent workloads on Meridian in a regulated industry "
    "(financial services, life sciences, or federal) on our Q2 2026 earnings call. "
    "If we cannot, we will say so directly and explain why."
)
add_bullet(doc,
    "Consumption pricing live in H2 2026. We will launch consumption-based agent pricing "
    "by September 30, 2026. We will report agent consumption ARR as a separate line "
    "beginning Q3 2026, giving investors a direct measure of platform adoption."
)
add_bullet(doc,
    "Governance as the measurable differentiator. We will publish a public enterprise "
    "governance framework for AI agents — covering auditability, role-based permissions, "
    "model selection, and data residency — within 60 days of Investor Day. This is the "
    "claim we are making; it will be verifiable."
)

# ── Footer note ───────────────────────────────────────────────────────────
doc.add_paragraph()
foot = doc.add_paragraph(
    "Prepared for Meridian Technologies Investor Day, March 11, 2026.  "
    "Internal and confidential. Do not distribute without CEO approval."
)
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in foot.runs:
    run.font.size = Pt(7.5)
    run.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)

doc.save("investor_day_positioning_memo.docx")
print("Saved investor_day_positioning_memo.docx")

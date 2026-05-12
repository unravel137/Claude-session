from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin   = Inches(1.25)
    section.right_margin  = Inches(1.25)

# ── Style helpers ─────────────────────────────────────────────────────────────
def set_font(run, size, bold=False, color=None, italic=False):
    run.font.name  = "Calibri"
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_rule(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "CCCCCC")
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p

def para(doc, text, size=11, bold=False, color=None, italic=False,
         space_before=0, space_after=6, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if align:
        p.alignment = align
    r = p.add_run(text)
    set_font(r, size, bold=bold, color=color, italic=italic)
    return p

def bullet(doc, label, body, size=10.5):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Inches(0.25)
    if label:
        r1 = p.add_run(label + " ")
        set_font(r1, size, bold=True, color=(30, 58, 95))
    r2 = p.add_run(body)
    set_font(r2, size)

# ── Document header ───────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.space_after = Pt(2)
r = p.add_run("MERIDIAN TECHNOLOGIES — BOARD OF DIRECTORS")
set_font(r, 8, color=(120, 120, 120))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.space_after = Pt(16)
r = p.add_run("Annual Strategic Review  |  Confidential")
set_font(r, 8, color=(120, 120, 120))

# ── Headline ──────────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(6)
r = p.add_run(
    "Meridian is profitable and focused — now we must decide what we're building, "
    "or the window to re-accelerate closes."
)
set_font(r, 15, bold=True, color=(17, 24, 39))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(18)
r = p.add_run("Catherine Park, CEO  ·  Opening Remarks  ·  5 Minutes")
set_font(r, 9, italic=True, color=(100, 116, 139))

add_rule(doc)

# ── Where we stand ────────────────────────────────────────────────────────────
para(doc, "WHERE WE STAND", size=9, bold=True, color=(100, 116, 139),
     space_before=12, space_after=4)

para(doc,
     "My first full year as CEO is complete. Meridian closed 2025 at $400M revenue, "
     "$413M ARR, a 12.4% operating margin, and $463M in cash with no debt. These are "
     "real achievements. They are also the floor of what this company can be — not the "
     "ceiling. ARR growth ended the year at 10%, the slowest in our public history. "
     "The chart below shows the full picture: profitability has nearly tripled since "
     "2022, and growth has been cut in half. The trade is done. What comes next is "
     "the question before this board today.",
     size=10.5, space_before=0, space_after=14)

add_rule(doc)

# ── Issue 1 ───────────────────────────────────────────────────────────────────
para(doc, "ISSUE 1 — Growth deceleration is structural, not cyclical.",
     size=12, bold=True, color=(30, 58, 95), space_before=14, space_after=6)

para(doc,
     "We have been trading growth for margin. That trade is now fully captured: "
     "S&M has come down from 40% to 32% of revenue; G&A from 12% to 9.5%. There "
     "is no more easy efficiency to harvest. The deceleration is being driven by "
     "three forces that will not self-correct:",
     size=10.5, space_after=6)

bullet(doc, "SMB is in managed decline:",
       "$52M ARR at year-end, down from $68M a year ago (–23% YoY). "
       "NRR of 84%. This segment is self-funded under the new P&L structure and "
       "will continue to shrink. That is approximately $30M of headwind baked into "
       "2026 guidance.")
bullet(doc, "Mid-market is plateauing:",
       "NRR compressed from 115% (2022) to 102% (Q4 2025). Our largest segment "
       "by ARR ($194M, 47% of total) is barely expanding on a net basis. "
       "Customers are demanding AI features bundled into renewals at no cost.")
bullet(doc, "Sales efficiency is deteriorating:",
       "Magic number fell from 1.20 (Q1 2024) to 0.92 (Q4 2025). "
       "CAC payback extended from 18 to 22 months. We are spending more than "
       "$1 in sales and marketing to generate $1 of net new ARR.")

para(doc,
     "The bull case for re-acceleration is AI Copilot. The evidence so far: "
     "710 paying seats, $3.5M in 2025 ARR, 44% attach rate on Q4 enterprise renewals. "
     "That is a real proof point. It is also a very small base for a company that "
     "needs to add $40–55M in ARR to hit the top of 2026 guidance.",
     size=10.5, space_before=6, space_after=14)

add_rule(doc)

# ── Issue 2 ───────────────────────────────────────────────────────────────────
para(doc, "ISSUE 2 — We have not yet ratified what Meridian is.",
     size=12, bold=True, color=(30, 58, 95), space_before=14, space_after=6)

para(doc,
     "On the Q4 earnings call I said: 'This is the year we decide what Meridian is.' "
     "That decision is before this board. The choice is not subtle:",
     size=10.5, space_after=6)

bullet(doc, "Option A:",
       "A project management platform with AI features added. "
       "Copilot is a $40/seat add-on. The core product is PM. "
       "R&D optimizes for mid-market feature parity.")
bullet(doc, "Option B:",
       "An agentic work platform where PM is one surface. "
       "Copilot becomes the core product. Pricing shifts to consumption. "
       "R&D optimizes for the enterprise governance and agent-builder roadmap.")

para(doc,
     "Our actions in 2025 — the Helio acquisition, the agentic-experiences group "
     "reporting to me, the 2026 roadmap — already signal Option B. But signal is not "
     "ratification. The internal damage from the unresolved question is measurable: "
     "28% of salespeople said in the October survey they can no longer crisply "
     "differentiate Meridian from Asana with AI. Roadmap thrash was the #1 theme "
     "in engineering (31% of responses). Every renewal contested while this is "
     "unresolved is being fought at a disadvantage.",
     size=10.5, space_before=6, space_after=14)

add_rule(doc)

# ── Issue 3 ───────────────────────────────────────────────────────────────────
para(doc, "ISSUE 3 — Engineering capacity is the binding constraint on either answer.",
     size=12, bold=True, color=(30, 58, 95), space_before=14, space_after=6)

para(doc,
     "The 2026 roadmap requires 80 net new engineers in H1. At 15% annual attrition, "
     "we will net approximately 25. Three specific risks:",
     size=10.5, space_after=6)

bullet(doc, "Helio retention cliff:",
       "The $68M in retention equity underpinning our agent architecture vests over "
       "four years — but cash compensation cliffs hit in 2026. If the Helio team "
       "unwinds, the agent-builder roadmap is directly exposed. Twenty-six of "
       "twenty-eight are still with us today.")
bullet(doc, "Senior engineering compensation:",
       "27% of senior engineers cited pay in the October survey — the highest "
       "concentration of any function. Specific ask: equity refresh for tenured "
       "employees whose grants vested before the 2025 stock decline.")
bullet(doc, "Opportunity cost of inaction:",
       "R&D is already at 25.4% of revenue — the highest since IPO. We are spending "
       "more than ever on engineering while flagging we may not have enough engineers "
       "to execute the plan. The CPO has asked the board to treat hiring as a "
       "strategic priority, not an HR line item.")

para(doc, "", space_after=14)
add_rule(doc)

# ── My ask ────────────────────────────────────────────────────────────────────
para(doc, "MY ONE ASK OF THIS BOARD", size=9, bold=True, color=(100, 116, 139),
     space_before=12, space_after=6)

para(doc,
     "Ratify the strategic identity: Meridian is an agentic work platform. "
     "Project management is our strongest surface and our enterprise moat — "
     "it is not the ceiling of what we build.",
     size=12, bold=True, color=(17, 24, 39), space_before=0, space_after=8)

para(doc,
     "That ratification unlocks three decisions I need to make immediately: "
     "(1) approve the senior engineering compensation refresh before we lose "
     "the people the roadmap depends on; "
     "(2) authorize the consumption-based pricing model as a CFO/CRO-owned "
     "workstream for H2 2026; and "
     "(3) greenlight continued M&A diligence on the two AI-native targets "
     "currently in early process.",
     size=10.5, space_after=6)

para(doc,
     "Investor Day is March 11. I will make this case publicly then. I want "
     "this board's alignment before I do.",
     size=10.5, italic=True, space_after=18)

add_rule(doc)

# ── Chart ─────────────────────────────────────────────────────────────────────
para(doc, "SUPPORTING EXHIBIT — ARR Growth vs. Operating Margin, Q1 2022–Q4 2025",
     size=9, bold=True, color=(100, 116, 139), space_before=12, space_after=8)

doc.add_picture("meridian_growth_vs_margin.png", width=Inches(6.0))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

para(doc,
     "Bars (left axis): ARR YoY growth rate. Line (right axis): operating margin. "
     "Growth has fallen from ~20% to 10%; margin has risen from 4% to 12.4%. "
     "The efficiency gains are captured. Re-acceleration requires a new driver.",
     size=8.5, italic=True, color=(100, 116, 139),
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0)

# ── Save ──────────────────────────────────────────────────────────────────────
doc.save("board_opening_remarks.docx")
print("saved board_opening_remarks.docx")

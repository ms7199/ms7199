#!/usr/bin/env python3
"""Builds the SVG panels in assets/ that README.md stacks into one page.

All the text lives in this file. Edit it, then run:

    python3 scripts/build_assets.py

Each panel paints its own background, so the page looks the same in GitHub's
light and dark themes and in editors' Markdown previews. Set PAGE to "dark" or
"light" to choose the page colour.
"""
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

PAGE = "dark"

PALETTES = {
    "dark": {"bg": "#0F0F10", "border": "#2A2A2C", "ink": "#EDEDED", "body": "#BDBDBD",
             "muted": "#8A8A8A", "rule": "#2A2A2C", "accent": "#FB923C"},
    "light": {"bg": "#FAFAF7", "border": "#E2E2DD", "ink": "#141414", "body": "#3B3B3B",
              "muted": "#737373", "rule": "#E2E2DD", "accent": "#C2410C"},
}
P = PALETTES[PAGE]

PW = 1000          # panel width
PAD = 56           # side padding inside the page
CW = PW - 2 * PAD  # content width
GUTTER = 232       # body text column in About

SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
FAMILIES = {"serif": SERIF, "sans": SANS, "mono": MONO}

# =============================================================== content

HERO = {
    "name": "Mayank Gupta",
    "topright": "GenAI Engineer  ·  Gandhinagar, India",
    # (text, accent) pieces per line; accent pieces are set in italic.
    "headline": [
        [("I build retrieval systems,", False)],
        [("agents and MCP servers", False)],
        [("that run in ", False), ("production.", True)],
    ],
    "facts": [
        ("NOW", "Building ctxbook, an open-source memory server for MCP clients"),
        ("BACKGROUND", "5+ years of Python: APIs, then ML, then GenAI"),
        ("OPEN TO", "Senior GenAI / AI Engineer roles, remote or hybrid"),
    ],
}

ABOUT = {
    "paragraphs": [
        "I'm a GenAI engineer with 5+ years of Python behind me: backend APIs first, then classical ML, "
        "and now LLM systems. Most of my recent work connects models to the places a company's knowledge "
        "actually lives, like SharePoint, Confluence, Outlook and Slack.",
        "I also train developers, and I write on LinkedIn about what goes wrong when RAG meets real documents.",
    ],
    "principles": [
        ("Measure retrieval before tuning prompts.", "A small eval set decides whether a change actually helped."),
        ("Give agents the fewest permissions that work.", "Validate tool inputs, and decide the failure path up front."),
        ("Keep the infrastructure boring.", "FastAPI, Postgres, Docker, AWS: things the next engineer can run."),
    ],
}

SECTIONS = {
    "about": ("01", "About", "Who I am"),
    "work": ("02", "Selected work", "Things I've built"),
    "stack": ("03", "Stack", "Tools I reach for"),
}

FEATURED = {
    "kicker": "01  ·  OPEN SOURCE  ·  IN DEVELOPMENT",
    "title": "ctxbook",
    "summary": "A local-first memory server that every MCP client shares. Tell Claude Code your project "
               "uses Postgres and Cursor knows it too. Move to MongoDB and the old fact is replaced, "
               "not duplicated.",
    "facts": [
        ("BUILT", "Fact history, hybrid search, conflict handling, 6 MCP tools and a CLI"),
        ("NEXT", "One-command client setup, an evaluation suite, then v0.1 on PyPI"),
        ("STACK", "Python, FastMCP"),
    ],
    "link": "github.com/ms7199/ctxbook",
    "clients": ["Claude Code", "Cursor", "Claude Desktop"],
    "caption": "Fig. 1   Every client reads and writes the same memory.",
}

PROJECTS = [
    {
        "file": "project-hr.svg", "num": "02", "title": "HR Assistant", "kind": "CLIENT WORK", "linked": False,
        "description": "An assistant for HR teams that calls SharePoint, Confluence and Outlook as MCP tools, "
                       "so answers come from the source systems instead of a stale copy, with each tool "
                       "scoped to what it may touch.",
        "stack": ["LangChain", "MCP", "FastAPI", "AWS"],
    },
    {
        "file": "project-docubot.svg", "num": "03", "title": "docubot-slack", "kind": "OPEN SOURCE", "linked": True,
        "description": "A Slack bot that answers questions from your PDFs using RAG. It keeps conversation "
                       "context and reloads the knowledge base without a restart.",
        "stack": ["Groq · Llama 3.3", "Pinecone", "Hugging Face", "Slack API"],
    },
    {
        "file": "project-memory.svg", "num": "04", "title": "Memory Assistant", "kind": "PROJECT", "linked": False,
        "description": "Long- and short-term memory for a chat assistant. Memories are scored, pruned and "
                       "recalled semantically, so it remembers users without its context growing forever.",
        "stack": ["LangChain", "Groq", "Pinecone", "MongoDB", "Next.js"],
    },
]

STACK = [
    ("LLMS & AGENTS", ["OpenAI, Groq", "LangChain", "LangGraph", "MCP / FastMCP", "Guardrails", "Hugging Face"]),
    ("RETRIEVAL & ML", ["Pinecone, FAISS", "Hybrid search", "Sentence-Transformers", "PyTorch, scikit-learn",
                        "Transformers, spaCy", "MLflow"]),
    ("BACKEND", ["Python", "FastAPI, Django REST", "Node.js, Express", "Celery, Redis", "PostgreSQL, MongoDB",
                 "JWT / OAuth2"]),
    ("CLOUD", ["AWS: EC2, Lambda, S3", "Azure", "Docker", "CI/CD", "DynamoDB"]),
]
STACK_NOTE = ("I've also integrated SharePoint, Confluence, Outlook, Slack, Stripe, Razorpay, Twilio and "
              "SendGrid, and I work in React and Next.js when a project needs a frontend.")

CONTACT = {
    "line1": "Building something with LLMs?",
    "line2": "Let's talk.",
    "email": "guptamayank7199@gmail.com",
    "footer_left": "© 2026 Mayank Gupta",
    "footer_right": "Gandhinagar, India  ·  Remote or hybrid",
}

# ========================================================== text metrics

_W = {" ": 278, ".": 278, ",": 278, "·": 278, "-": 333, "/": 278, ":": 278, ";": 278, "(": 333, ")": 333,
      "&": 667, "+": 584, "'": 191, "@": 1015, "_": 556, "!": 278, "?": 556, "©": 737}
_W.update(zip("abcdefghijklmnopqrstuvwxyz",
              [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
               556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
              [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
               722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({d: 556 for d in "0123456789"})


def width(s, size, family="sans", weight=400, spacing=0.0):
    """Estimated rendered width, used for wrapping and placement (errs wide)."""
    gaps = spacing * max(len(s) - 1, 0)
    if family == "mono":
        return len(s) * size * 0.6 + gaps
    em = sum(_W.get(c, 600) for c in s) / 1000
    factor = {"serif": 1.12, "sans": 1.04}[family] * (1.05 if weight >= 600 else 1.0)
    return em * size * factor + gaps


def wrap(s, size, max_w, family="sans", weight=400):
    lines, line = [], ""
    for word in s.split():
        candidate = f"{line} {word}".strip()
        if line and width(candidate, size, family, weight) > max_w:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines

# =========================================================== svg helpers


def _attrs(x, y, size, family, weight, anchor, spacing, italic, s=""):
    a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-family="{FAMILIES[family]}"',
         f'font-size="{size:g}"', f'font-weight="{weight}"']
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if spacing:
        a.append(f'letter-spacing="{spacing}"')
    if italic:
        a.append('font-style="italic"')
    if "  " in s:
        a.append('style="white-space:pre"')
    return " ".join(a)


def t(x, y, s, size, fill, family="sans", weight=400, anchor="start", spacing=0, italic=False):
    return f'<text {_attrs(x, y, size, family, weight, anchor, spacing, italic, s)} fill="{fill}">{escape(s)}</text>'


def spans(x, y, parts, size, family="serif", spacing=-0.5):
    """One line made of (text, accent) pieces; accent pieces are italic and coloured."""
    inner = ""
    for s, accent in parts:
        style = f' fill="{P["accent"]}" font-style="italic"' if accent else f' fill="{P["ink"]}"'
        inner += f"<tspan{style}>{escape(s)}</tspan>"
    return f'<text {_attrs(x, y, size, family, 400, "start", spacing, False)}>{inner}</text>'


def rule(y, x=0, w=CW, color=None):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="1" fill="{color or P["rule"]}"/>'


def section_header(key, y):
    """Rule, number, title and note. Returns (elements, height used)."""
    num, title, note = SECTIONS[key]
    return [rule(y),
            t(0, y + 52, f"({num})", 13, P["muted"], "mono"),
            t(64, y + 54, title, 36, P["ink"], "serif", spacing=-0.4),
            t(CW, y + 52, note, 13, P["muted"], "mono", anchor="end")], 84


def write(name, h, elems, label, first=False, last=False, defs=""):
    """Wraps content in a page panel. The first panel has rounded top corners, the last rounded bottom
    corners; the rest extend past their edges so stacked panels read as one continuous page."""
    r = 14
    y0 = 0 if first else -r - 2
    y1 = h if last else h + r + 2
    bg = (f'<rect x=".5" y="{y0 + .5:.1f}" width="{PW - 1}" height="{y1 - y0 - 1:.1f}" rx="{r}" '
          f'fill="{P["bg"]}" stroke="{P["border"]}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{h:.0f}" viewBox="0 0 {PW} {h:.0f}" '
           f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
           f'{f"<defs>{defs}</defs>" if defs else ""}{bg}'
           f'<g transform="translate({PAD} 0)">{"".join(elems)}</g></svg>\n')
    (ASSETS / name).write_text(svg, encoding="utf-8")
    return name

# ================================================================ panels


def hero():
    b = [t(0, 44, HERO["name"], 17, P["ink"], "sans", 600),
         t(CW, 44, HERO["topright"], 13, P["muted"], "mono", anchor="end"),
         rule(66)]

    fx = 620
    fy = last = 126
    for label, value in HERO["facts"]:
        b.append(t(fx, fy, label, 12, P["muted"], "mono", spacing=1.4))
        lines = wrap(value, 16, CW - fx)
        for i, line in enumerate(lines):
            b.append(t(fx, fy + 26 + i * 23, line, 16, P["body"]))
        last = fy + 26 + (len(lines) - 1) * 23
        fy = last + 44
    b.append(f'<rect x="592" y="104" width="1" height="{last - 90:.0f}" fill="{P["rule"]}"/>')

    # Headline: largest size (max 56) that fits the left column, centred against the facts.
    widest = max(width("".join(s for s, _ in parts), 1, "serif") for parts in HERO["headline"])
    size = min(56, int(540 / widest))
    n = len(HERO["headline"])
    mid = (126 - 9 + last + 4) / 2
    y = mid - (n - 1) * size * 0.6 + size * 0.25
    for parts in HERO["headline"]:
        b.append(spans(0, y, parts, size))
        y += size * 1.2
    h = max(last, y - size * 1.2) + 48

    label = (f'{HERO["name"]}, GenAI Engineer in Gandhinagar, India. '
             + " ".join("".join(s for s, _ in p) for p in HERO["headline"]) + " "
             + " ".join(f"{k.title()}: {v}." for k, v in HERO["facts"]))
    return write("hero.svg", h, b, label, first=True)


def about():
    b, used = section_header("about", 8)
    y = 8 + used + 22
    for para in ABOUT["paragraphs"]:
        for line in wrap(para, 18, CW - GUTTER):
            b.append(t(GUTTER, y, line, 18, P["body"]))
            y += 28
        y += 14
    y += 26
    b.append(t(0, y, "HOW I WORK", 12, P["muted"], "mono", spacing=1.4))
    for i, (lead, desc) in enumerate(ABOUT["principles"]):
        b.append(rule(y - 26, GUTTER, CW - GUTTER))
        b.append(t(GUTTER, y, f"0{i + 1}", 12, P["accent"], "mono"))
        b.append(t(GUTTER + 40, y, lead, 17, P["ink"], "sans", 600))
        for line in wrap(desc, 16, CW - GUTTER - 40):
            y += 25
            b.append(t(GUTTER + 40, y, line, 16, P["body"]))
        y += 50
    h = y - 10
    label = "01 About. " + " ".join(ABOUT["paragraphs"]) + " How I work: " + \
        " ".join(f"{lead} {desc}" for lead, desc in ABOUT["principles"])
    return write("about.svg", h, b, label)


def work_header():
    b, used = section_header("work", 8)
    return write("work.svg", 8 + used + 6, b, "02 Selected work")


def featured():
    f = FEATURED
    ink, muted, body = P["ink"], P["muted"], P["body"]
    b = [t(0, 34, f["kicker"], 12, P["accent"], "mono", spacing=1.4),
         t(0, 90, f["title"], 46, ink, "serif", spacing=-0.5)]
    y = 130
    for line in wrap(f["summary"], 17, 400):
        b.append(t(0, y, line, 17, body))
        y += 26
    y += 12
    for label, value in f["facts"]:
        b.append(rule(y, 0, 400))
        lines = wrap(value, 15, 316)
        for i, line in enumerate(lines):
            b.append(t(84, y + 27 + i * 22, line, 15, body))
        b.append(t(0, y + 27, label, 11, muted, "mono", spacing=1.4))
        y += 27 + (len(lines) - 1) * 22 + 16
    b.append(rule(y, 0, 400))
    link = f["link"] + "  ↗"
    b.append(t(0, y + 40, link, 14, P["accent"], "mono"))
    b.append(rule(y + 46, 0, width(link, 14, "mono"), P["accent"]))
    left_end = y + 70

    # Fig. 1: clients -> ctxbook -> local store, drawn as a plain line figure.
    fx, fw = 460, CW - 460
    cx = fx + fw / 2
    bw, bh, gap = 128, 40, (fw - 3 * 128) / 2
    stroke = f'fill="none" stroke="{ink}" stroke-width="1.3"'
    mids = []
    for i, name in enumerate(f["clients"]):
        bx = fx + i * (bw + gap)
        mid = bx + bw / 2
        mids.append(mid)
        b.append(f'<rect x="{bx:.1f}" y="30" width="{bw}" height="{bh}" {stroke}/>')
        b.append(t(mid, 55, name, 14, ink, "sans", anchor="middle"))
        b.append(f'<path d="M{mid:.1f} {30 + bh} V110" {stroke}/>')
    b.append(f'<path d="M{mids[0]:.1f} 110 H{mids[-1]:.1f}" {stroke}/>')
    b.append(f'<path d="M{cx:.1f} 110 V146" {stroke} marker-end="url(#arrow)"/>')
    b.append(t(cx + 9, 132, "MCP", 10, muted, "mono", spacing=1))
    b.append(f'<rect x="{cx - 100:.1f}" y="150" width="200" height="60" {stroke}/>')
    b.append(f'<rect x="{cx - 95:.1f}" y="155" width="190" height="50" fill="none" stroke="{P["rule"]}"/>')
    b.append(t(cx, 178, f["title"], 20, ink, "serif", anchor="middle"))
    b.append(t(cx, 196, "MCP server", 11, muted, "mono", anchor="middle"))
    b.append(f'<path d="M{cx:.1f} 213 V246" {stroke} marker-start="url(#arrow)" marker-end="url(#arrow)"/>')
    top, bottom = 262, 322
    b.append(f'<path d="M{cx - 100:.1f} {top} V{bottom} A100 12 0 0 0 {cx + 100:.1f} {bottom} V{top}" {stroke}/>')
    b.append(f'<ellipse cx="{cx:.1f}" cy="{top}" rx="100" ry="12" {stroke}/>')
    b.append(t(cx, 298, "Local store", 15, ink, "sans", anchor="middle"))
    b.append(t(cx, 316, "facts · history · search", 10, muted, "mono", anchor="middle"))
    b.append(t(fx, 372, f["caption"], 14, muted, "serif", italic=True))

    defs = (f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto-start-reverse"><path d="M0 1 9 5 0 9" fill="none" stroke="{ink}" stroke-width="1.5"/>'
            f'</marker>')
    h = max(left_end, 400)
    label = f'{f["title"]}, open source, in development: {f["summary"]} ' + \
        " ".join(f"{k.title()}: {v}." for k, v in f["facts"])
    return write("project-ctxbook.svg", h, b, label, defs=defs)


def project(p):
    desc = wrap(p["description"], 16, 320)
    rows = max(len(desc), len(p["stack"]), 3)
    b = [rule(0),
         t(0, 46, p["num"], 13, P["muted"], "mono"),
         t(56, 50, p["title"], 26, P["ink"], "serif", spacing=-0.3),
         t(56, 76, p["kind"], 11, P["muted"], "mono", spacing=1.4)]
    if p["linked"]:
        b.append(t(56 + width(p["title"], 26, "serif") + 4, 48, "↗", 19, P["accent"]))
    for i, line in enumerate(desc):
        b.append(t(340, 46 + i * 24, line, 16, P["body"]))
    for i, item in enumerate(p["stack"]):
        b.append(t(CW, 46 + i * 22, item, 12, P["muted"], "mono", anchor="end"))
    h = 46 + (rows - 1) * 24 + 40
    return write(p["file"], h, b, f'{p["title"]} ({p["kind"].lower()}): {p["description"]}')


def stack():
    b, used = section_header("stack", 8)
    y0 = 8 + used + 22
    colw = CW / len(STACK)
    rows = max(len(items) for _, items in STACK)
    for i, (label, items) in enumerate(STACK):
        x = i * colw
        b.append(t(x, y0, label, 12, P["muted"], "mono", spacing=1.4))
        for j, item in enumerate(items):
            b.append(t(x, y0 + 38 + j * 28, item, 16, P["body"]))
    y = y0 + 38 + (rows - 1) * 28 + 48
    for line in wrap(STACK_NOTE, 15, CW):
        b.append(t(0, y, line, 15, P["muted"]))
        y += 23
    label = "03 Stack. " + " ".join(f'{label.title()}: {", ".join(items)}.' for label, items in STACK) + \
        " " + STACK_NOTE
    return write("stack.svg", y + 18, b, label)


def contact():
    c = CONTACT
    ew = width(c["email"], 18, "mono")
    b = [rule(24),
         t(0, 104, c["line1"], 46, P["ink"], "serif", spacing=-0.5),
         spans(0, 162, [(c["line2"], True)], 46),
         t(0, 222, c["email"], 18, P["ink"], "mono"),
         f'<rect x="0" y="229" width="{ew:.1f}" height="2" fill="{P["accent"]}"/>',
         rule(270),
         t(0, 302, c["footer_left"], 11, P["muted"], "mono"),
         t(CW, 302, c["footer_right"], 11, P["muted"], "mono", anchor="end")]
    return write("contact.svg", 334, b, f'{c["line1"]} {c["line2"]} {c["email"]}', last=True)


def main():
    ASSETS.mkdir(exist_ok=True)
    names = [hero(), about(), work_header(), featured()]
    names += [project(p) for p in PROJECTS]
    names += [stack(), contact()]
    print(f"{PAGE} page -> assets/: " + ", ".join(names))


if __name__ == "__main__":
    main()

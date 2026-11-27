#!/usr/bin/env python3
"""Builds the animated hero images (assets/hero-light.svg, assets/hero-dark.svg).

The rest of README.md is plain Markdown, so GitHub themes it natively. The hero
comes in two versions; README.md tags them #gh-light-mode-only and
#gh-dark-mode-only, and GitHub shows the one that matches the viewer's theme.

Edit the text below, then run:

    python3 scripts/build_assets.py
"""
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# GitHub's own text colours, so the hero blends into the page in each theme.
THEMES = {
    "light": {"ink": "#1F2328", "body": "#424A53", "muted": "#6E7781", "rule": "#D0D7DE",
              "accent": "#C2410C", "live": "#1A7F37", "paper": "#FFFFFF"},
    "dark": {"ink": "#E6EDF3", "body": "#B7C0CA", "muted": "#8B949E", "rule": "#30363D",
             "accent": "#FB923C", "live": "#3FB950", "paper": "#0D1117"},
}

W = 1000

SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
FAMILIES = {"serif": SERIF, "sans": SANS, "mono": MONO}

# =============================================================== content

HERO = {
    "name": "Mayank Gupta",
    "topright": "GenAI Engineer  ·  Gandhinagar, India",
    # (text, accent) pieces per line; the accent piece is italic, coloured and underlined.
    "headline": [
        [("I build retrieval systems,", False)],
        [("agents and MCP servers", False)],
        [("that run in ", False), ("production.", True)],
    ],
    "facts": [
        ("NOW", "Building ctxbook, an open-source memory server for MCP clients"),
        ("BACKGROUND", "5+ years of Python: APIs, then ML, then GenAI"),
        ("OPEN TO", "Senior GenAI roles, remote or hybrid"),
    ],
}

# ========================================================== text metrics

_W = {" ": 278, ".": 278, ",": 278, "·": 278, "-": 333, "/": 278, ":": 278, ";": 278, "(": 333, ")": 333,
      "&": 667, "+": 584, "'": 191, "@": 1015, "_": 556, "!": 278, "?": 556}
_W.update(zip("abcdefghijklmnopqrstuvwxyz",
              [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
               556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
              [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
               722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({d: 556 for d in "0123456789"})


def width(s, size, family="sans"):
    """Estimated rendered width (errs wide)."""
    if family == "mono":
        return len(s) * size * 0.6
    em = sum(_W.get(c, 600) for c in s) / 1000
    return em * size * {"serif": 1.12, "sans": 1.04}[family]


def wrap(s, size, max_w):
    lines, line = [], ""
    for word in s.split():
        candidate = f"{line} {word}".strip()
        if line and width(candidate, size) > max_w:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines

# =========================================================== svg helpers


def t(x, y, s, size, fill, family="sans", weight=400, anchor="start", spacing=0):
    a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-family="{FAMILIES[family]}"', f'font-size="{size:g}"',
         f'font-weight="{weight}"', f'fill="{fill}"']
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if spacing:
        a.append(f'letter-spacing="{spacing}"')
    if "  " in s:
        a.append('style="white-space:pre"')
    return f"<text {' '.join(a)}>{escape(s)}</text>"


def reveal(inner, delay):
    """Fades and lifts its content in. Without animation support it simply shows."""
    return f'<g class="in" style="animation-delay:{delay:.2f}s">{inner}</g>'


STYLE = """
.in { animation: rise .9s cubic-bezier(.2,.7,.2,1) both; }
.draw { stroke-dasharray: var(--len); stroke-dashoffset: var(--len); animation: draw .9s ease-out 1.3s forwards; }
.pulse { animation: pulse 2.4s ease-in-out infinite; }
@keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
@keyframes draw { to { stroke-dashoffset: 0; } }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .25; } }
.fb { transform-box: fill-box; transform-origin: center; }
.blink { animation: blink 4.5s infinite; }
.nod { animation: nod 2.6s ease-in-out infinite; }
.tap { animation: tap .32s ease-in-out infinite alternate; }
.bob { animation: bob 3.2s ease-in-out infinite; }
.steam { animation: steam 2.8s ease-in-out infinite; }
.flow { stroke-dasharray: 3 7; animation: flow 1s linear infinite; }
.code { transform-origin: left; animation: code 7s ease-out infinite both; }
.msgA { animation: msgA 6s infinite; }
.msgB { animation: msgB 6s infinite; }
@keyframes blink { 0%, 93%, 100% { transform: scaleY(1); } 96% { transform: scaleY(.1); } }
@keyframes nod { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(2px); } }
@keyframes tap { to { transform: translateY(-4px); } }
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }
@keyframes steam { 0% { opacity: 0; transform: translateY(6px); } 40% { opacity: .9; } 100% { opacity: 0; transform: translateY(-16px); } }
@keyframes flow { to { stroke-dashoffset: -20; } }
@keyframes code { 0% { transform: scaleX(0); } 10%, 88% { transform: scaleX(1); opacity: 1; } 100% { transform: scaleX(1); opacity: 0; } }
@keyframes msgA { 0%, 46% { opacity: 1; } 50%, 96% { opacity: 0; } 100% { opacity: 1; } }
@keyframes msgB { 0%, 46% { opacity: 0; } 50%, 96% { opacity: 1; } 100% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .in, .draw, .pulse, .blink, .nod, .tap, .bob, .steam, .flow, .code, .msgA, .msgB { animation: none; }
  .draw { stroke-dashoffset: 0; } .msgB { opacity: 0; }
}
"""

# ============================================================= character


def character(P):
    """Original line-art developer with an AI companion, 420 x 320 units."""
    ink, acc, mut, paper = P["ink"], P["accent"], P["muted"], P["paper"]
    s = f'stroke="{ink}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    steam = f'fill="none" stroke="{mut}" stroke-width="2" stroke-linecap="round"'
    sparkle = "M0 -12 Q2 -2 12 0 Q2 2 0 12 Q-2 2 -12 0 Q-2 -2 0 -12 Z"
    out = [
        # desk and coffee
        f'<path d="M10 292 H410" fill="none" {s}/>',
        f'<rect x="34" y="254" width="28" height="36" rx="5" fill="{paper}" {s}/>',
        f'<path d="M62 263 q12 0 12 9 q0 9 -12 9" fill="none" {s}/>',
        f'<path class="steam" d="M42 246 q-5 -7 0 -14 q5 -7 0 -14" {steam}/>',
        f'<path class="steam" style="animation-delay:1.4s" d="M54 246 q-5 -7 0 -14 q5 -7 0 -14" {steam}/>',
        # hoodie
        f'<path d="M108 292 L114 234 Q120 196 170 192 Q220 196 226 234 L232 292 Z" fill="{paper}" {s}/>',
        f'<path d="M162 202 v16 M178 202 v16" fill="none" stroke="{mut}" stroke-width="2" stroke-linecap="round"/>',
        # arms reaching to the keyboard
        f'<path d="M124 222 Q102 248 100 276" fill="none" {s}/>',
        f'<path d="M216 222 Q238 248 240 276" fill="none" {s}/>',
        # head with headphones
        '<g class="nod">',
        f'<path d="M132 142 Q132 92 170 92 Q208 92 208 142" fill="none" stroke="{ink}" stroke-width="3.2" stroke-linecap="round"/>',
        f'<circle cx="170" cy="142" r="32" fill="{paper}" {s}/>',
        f'<path d="M138 140 Q138 106 170 106 Q204 106 202 138 Q190 122 170 124 Q150 122 138 140 Z" fill="{ink}"/>',
        f'<rect x="126" y="132" width="11" height="22" rx="5" fill="{acc}"/>',
        f'<rect x="203" y="132" width="11" height="22" rx="5" fill="{acc}"/>',
        f'<ellipse class="fb blink" cx="158" cy="146" rx="3" ry="3.6" fill="{ink}"/>',
        f'<ellipse class="fb blink" cx="182" cy="146" rx="3" ry="3.6" fill="{ink}"/>',
        f'<path d="M162 158 q8 6 16 0" fill="none" {s}/>',
        '</g>',
        # laptop: lid seen from behind, glowing logo, keyboard deck
        f'<rect x="106" y="206" width="128" height="76" rx="6" fill="{paper}" {s}/>',
        f'<path class="pulse" transform="translate(170 244)" d="{sparkle}" fill="{acc}"/>',
        f'<path d="M94 292 L246 292 L238 282 L102 282 Z" fill="{paper}" {s}/>',
        # typing hands
        f'<circle class="tap" cx="100" cy="278" r="7" fill="{paper}" {s}/>',
        f'<circle class="tap" style="animation-delay:.16s" cx="240" cy="278" r="7" fill="{paper}" {s}/>',
        # data flowing from the laptop to the AI orb, and from the orb to the panel
        f'<path class="flow" d="M186 240 C232 240 268 214 308 208" fill="none" stroke="{acc}" stroke-width="2"/>',
        f'<path class="flow" d="M330 184 V152" fill="none" stroke="{acc}" stroke-width="2"/>',
        # AI companion orb
        '<g class="bob">',
        f'<circle class="pulse" cx="330" cy="206" r="27" fill="none" stroke="{acc}" stroke-opacity=".45" stroke-width="1.5"/>',
        f'<circle cx="330" cy="206" r="18" fill="{paper}" stroke="{acc}" stroke-width="2.2"/>',
        f'<path transform="translate(330 206) scale(.7)" d="{sparkle}" fill="{acc}"/>',
        '</g>',
        # floating code panel that writes itself
        f'<rect x="262" y="30" width="146" height="120" rx="10" fill="{paper}" {s}/>',
        *[f'<circle cx="{276 + i * 12}" cy="45" r="3" fill="{mut}"/>' for i in range(3)],
        f'<path d="M262 57 H408" fill="none" stroke="{P["rule"]}" stroke-width="1.5"/>',
    ]
    for i, w in enumerate([92, 64, 108, 50, 84, 70]):
        color = acc if i == 2 else mut
        op = "1" if i == 2 else ".55"
        out.append(f'<rect class="fb code" style="animation-delay:{i * .4:.1f}s" x="276" y="{70 + i * 12}" '
                   f'width="{w}" height="6" rx="3" fill="{color}" fill-opacity="{op}"/>')
    # status line under the orb
    out.append(t(330, 258, "retrieving context…", 11, mut, "mono", anchor="middle").replace("<text ", '<text class="msgA" ', 1))
    out.append(t(330, 258, "grounded answer ✓", 11, P["live"], "mono", anchor="middle").replace("<text ", '<text class="msgB" ', 1))
    return "".join(out)

# ================================================================== hero


def hero(theme, P):
    b = [reveal(t(0, 30, HERO["name"], 17, P["ink"], "sans", 600)
                + t(W, 30, HERO["topright"], 13, P["muted"], "mono", anchor="end")
                + f'<rect x="0" y="52" width="{W}" height="1" fill="{P["rule"]}"/>', 0)]

    # Character on the right.
    cx0, cy0 = 580, 72
    b.append(reveal(f'<g transform="translate({cx0} {cy0})">{character(P)}</g>', 0.5))
    art_top, art_bottom = cy0 + 30, cy0 + 292

    # Headline on the left, centred against the character.
    widest = max(width("".join(s for s, _ in parts), 1, "serif") for parts in HERO["headline"])
    size = min(58, int(540 / widest))
    n = len(HERO["headline"])
    y = (art_top + art_bottom) / 2 - (n - 1) * size * 0.6 + size * 0.25
    for i, parts in enumerate(HERO["headline"]):
        inner = ""
        for s, accent in parts:
            if accent:
                inner += f'<tspan fill="{P["accent"]}" font-style="italic">{escape(s)}</tspan>'
            else:
                inner += f'<tspan fill="{P["ink"]}">{escape(s)}</tspan>'
        line = (f'<text x="0" y="{y:.1f}" font-family="{SERIF}" font-size="{size}" letter-spacing="-0.5">'
                f'{inner}</text>')
        x = 0.0
        for s, accent in parts:
            w = width(s, size, "serif")
            if accent:
                uw = w * 0.93
                line += (f'<path class="draw" style="--len:{uw:.0f}" d="M{x + 2:.1f} {y + 12:.1f} '
                         f'q{uw / 2:.1f} -6 {uw:.1f} -1" fill="none" stroke="{P["accent"]}" '
                         f'stroke-width="2.5" stroke-linecap="round"/>')
            x += w
        b.append(reveal(line, 0.15 + i * 0.13))
        y += size * 1.2

    # Facts in a row underneath.
    ry = cy0 + 320
    b.append(f'<rect x="0" y="{ry}" width="{W}" height="1" fill="{P["rule"]}"/>')
    colw = W / len(HERO["facts"])
    bottom = ry
    for i, (label, value) in enumerate(HERO["facts"]):
        fx, fy = i * colw, ry + 34
        part = t(fx, fy, label, 12, P["muted"], "mono", spacing=1.4)
        if label == "OPEN TO":
            lw = width(label, 12, "mono") + 1.4 * (len(label) - 1)
            part += f'<circle class="pulse" cx="{fx + lw + 10:.1f}" cy="{fy - 4}" r="3.5" fill="{P["live"]}"/>'
        lines = wrap(value, 16, colw - 30)
        for j, line in enumerate(lines):
            part += t(fx, fy + 26 + j * 23, line, 16, P["body"])
        bottom = max(bottom, fy + 26 + (len(lines) - 1) * 23)
        b.append(reveal(part, 0.7 + i * 0.12))
    h = bottom + 30

    label = (f'{HERO["name"]}, GenAI Engineer in Gandhinagar, India. '
             + " ".join("".join(s for s, _ in p) for p in HERO["headline"]) + " "
             + " ".join(f"{k.title()}: {v}." for k, v in HERO["facts"])
             + " Illustration: a developer in headphones typing on a laptop while an AI assistant retrieves context.")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h:.0f}" viewBox="0 0 {W} {h:.0f}" '
           f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
           f'<style>{STYLE}</style>{"".join(b)}</svg>\n')
    path = ASSETS / f"hero-{theme}.svg"
    path.write_text(svg, encoding="utf-8")
    return path.name


def main():
    ASSETS.mkdir(exist_ok=True)
    print("Wrote: " + ", ".join(hero(theme, P) for theme, P in THEMES.items()))


if __name__ == "__main__":
    main()

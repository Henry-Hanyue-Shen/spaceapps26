"""Three original pen-and-ink plates on parchment for the 'what it means' section (deck and website).

Isometric (2:1) drawings in iron-gall ink with hatching for shade and red chalk for the water that matters:
  plate_ny.svg       New York Harbor at the Battery: lower-Manhattan blocks, quay, tide gauge and its ruler, a surge band
  plate_prepare.svg  before October: a flood-barrier line holding back high water, pumps, hoses, sandbags, a crew
  plate_la.svg       Port of Los Angeles: wharf, gantry cranes, container stacks, a ship, palms, a high-water line
Hand-drawn feel: every edge is a slightly bowed quadratic with seeded jitter (reproducible).
Usage: python plates.py <out dir>
"""
import math
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
INK, RED, BLUE, PAPER = "#3b2614", "#8b3a2b", "#3a4e68", "#f1ece1"
W, H = 600, 340
CX, CY = 300, 92
C30, S30 = math.cos(math.radians(30)), 0.5


def iso(x, y, z=0.0):
    return (CX + (x - y) * C30, CY + (x + y) * S30 - z)


def f(v):
    return f"{v:.1f}"


class Plate:
    def __init__(self, seed, title):
        self.r = random.Random(seed)
        self.title = title
        self.items = []

    def j(self, a=0.7):
        return self.r.uniform(-a, a)

    def line(self, p, q, w=1.1, col=INK, op=1.0, dash=None):
        mx, my = (p[0] + q[0]) / 2 + self.j(), (p[1] + q[1]) / 2 + self.j()
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(f'<path d="M{f(p[0] + self.j(0.3))} {f(p[1] + self.j(0.3))}Q{f(mx)} {f(my)} {f(q[0])} {f(q[1])}" '
                          f'stroke="{col}" stroke-width="{w}" stroke-opacity="{op}" fill="none" stroke-linecap="round"{d}/>')

    def poly(self, pts, fill=PAPER, hatch=None, outline=True, w=1.1, op=1.0):
        d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"
        self.items.append(f'<path d="{d}" fill="{fill}" fill-opacity="{op}"/>')
        if hatch:
            self.items.append(f'<path d="{d}" fill="url(#{hatch})"/>')
        if outline:
            for a, b in zip(pts, pts[1:] + pts[:1]):
                self.line(a, b, w)

    def box(self, x, y, z, w, d, h, left="hl", right="hd", top=None, floors=0):
        P = lambda a, b, c: iso(a, b, c)
        self.poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)], hatch=left)
        self.poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)], hatch=right)
        self.poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)], hatch=top)
        for k in range(1, floors):
            zz = z + h * k / floors
            self.line(P(x, y + d, zz), P(x + w, y + d, zz), 0.45, op=0.55)
            self.line(P(x + w, y + d, zz), P(x + w, y, zz), 0.45, op=0.55)

    def water(self, x0, x1, y0, y1, z):
        self.poly([iso(x0, y0, z), iso(x1, y0, z), iso(x1, y1, z), iso(x0, y1, z)], fill="#e9e4d8", hatch="wave", outline=False)

    def text(self, x, y, s, size=15, col=INK, anchor="start", italic=True, op=1.0):
        st = "italic" if italic else "normal"
        self.items.append(f'<text x="{f(x)}" y="{f(y)}" font-family="IM Fell English, Georgia, serif" font-style="{st}" '
                          f'font-size="{size}" fill="{col}" fill-opacity="{op}" text-anchor="{anchor}" stroke="#efe7d6" stroke-width="4" stroke-linejoin="round" paint-order="stroke">{s}</text>')

    def svg(self):
        defs = f"""<defs>
<radialGradient id="pg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#f4efe4"/><stop offset=".72" stop-color="#ece3cf"/><stop offset="1" stop-color="#dccdac"/></radialGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 .23  0 0 0 0 .15  0 0 0 0 .08  0 0 0 .07 0"/></filter>
<pattern id="hl" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(55)"><line x1="0" y1="0" x2="0" y2="5" stroke="{INK}" stroke-width=".55" stroke-opacity=".55"/></pattern>
<pattern id="hd" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><line x1="0" y1="0" x2="0" y2="3.2" stroke="{INK}" stroke-width=".6" stroke-opacity=".75"/></pattern>
<pattern id="hx" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><path d="M0 0V4M0 0H4" stroke="{INK}" stroke-width=".5" stroke-opacity=".6"/></pattern>
<pattern id="cont" width="4" height="10" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="10" stroke="{INK}" stroke-width=".55" stroke-opacity=".6"/></pattern>
<pattern id="wave" width="22" height="7" patternUnits="userSpaceOnUse"><path d="M1 4Q6 1 11 4T21 4" stroke="{BLUE}" stroke-width=".7" stroke-opacity=".75" fill="none"/></pattern>
<pattern id="redwash" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(-20)"><line x1="0" y1="0" x2="0" y2="4" stroke="{RED}" stroke-width="1.1" stroke-opacity=".55"/></pattern>
</defs>"""
        frame = (f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="5" fill="url(#pg)"/>'
                 f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="5" filter="url(#grain)"/>'
                 f'<rect x="9" y="9" width="{W - 18}" height="{H - 18}" rx="3" fill="none" stroke="{INK}" stroke-opacity=".35" stroke-width=".8"/>')
        cap = (f'<text x="22" y="{H - 16}" font-family="IM Fell English, Georgia, serif" font-style="italic" font-size="17" fill="{INK}">{self.title}</text>')
        clip = f'<clipPath id="inner"><rect x="10" y="10" width="{W - 20}" height="{H - 52}" rx="3"/></clipPath>'
        band = f'<line x1="22" y1="{H - 42}" x2="{W - 22}" y2="{H - 42}" stroke="{INK}" stroke-opacity=".35" stroke-width=".8"/>'
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{self.title}">' + defs + clip + frame
                + '<g clip-path="url(#inner)">' + "".join(self.items) + '</g>' + band + cap + '</svg>')


def ruler(p, x, y, z0, z1, mark_z, label):
    a, b = iso(x, y, z0), iso(x, y, z1)
    p.line(a, b, 1.6)
    for k, z in enumerate(range(int(z0), int(z1) + 1, 4)):
        q = iso(x, y, z)
        p.line(q, (q[0] + (6 if k % 2 == 0 else 3.5), q[1]), 0.8)
    m = iso(x, y, mark_z)
    p.line((m[0] - 9, m[1]), (m[0] + 11, m[1]), 2.4, RED)
    p.text(m[0] + 16, m[1] + 5, label, 14, RED)


# ---------------------------------------------------------------- landmarks (pen silhouettes)
def raw(p, svg):
    p.items.append(svg)


def statue(p, bx, by, s=1.0):
    """Statue of Liberty on her island: star-fort base, pedestal, robed figure, crown, raised torch (red-chalk flame)."""
    S = lambda v: f(v * s)
    raw(p, f'<ellipse cx="{f(bx)}" cy="{f(by + 4 * s)}" rx="{S(36)}" ry="{S(9)}" fill="#efe7d6" stroke="{INK}" stroke-width="1"/>')
    raw(p, f'<path d="M{f(bx - 18 * s)} {f(by)}l{S(6)} {S(-5)}h{S(24)}l{S(6)} {S(5)}l{S(-6)} {S(5)}h{S(-24)}z" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    raw(p, f'<path d="M{f(bx - 8 * s)} {f(by - 3 * s)}L{f(bx - 5.5 * s)} {f(by - 27 * s)}H{f(bx + 5.5 * s)}L{f(bx + 8 * s)} {f(by - 3 * s)}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
           f'<path d="M{f(bx - 8 * s)} {f(by - 3 * s)}L{f(bx - 5.5 * s)} {f(by - 27 * s)}H{f(bx + 5.5 * s)}L{f(bx + 8 * s)} {f(by - 3 * s)}Z" fill="url(#hl)"/>')
    raw(p, f'<path d="M{f(bx - 5 * s)} {f(by - 27 * s)}C{f(bx - 5 * s)} {f(by - 40 * s)} {f(bx - 4 * s)} {f(by - 48 * s)} {f(bx - 3 * s)} {f(by - 51 * s)}'
           f'H{f(bx + 3 * s)}C{f(bx + 4.5 * s)} {f(by - 44 * s)} {f(bx + 6 * s)} {f(by - 36 * s)} {f(bx + 6 * s)} {f(by - 27 * s)}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
           f'<path d="M{f(bx - 4 * s)} {f(by - 30 * s)}Q{f(bx)} {f(by - 40 * s)} {f(bx + 4 * s)} {f(by - 48 * s)}" stroke="{INK}" stroke-width=".6" fill="none"/>')
    raw(p, f'<circle cx="{f(bx)}" cy="{f(by - 54 * s)}" r="{S(2.8)}" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    for a in (-75, -45, -15, 15, 45, 75):
        r = math.radians(a - 90)
        raw(p, f'<line x1="{f(bx + math.cos(r) * 3 * s)}" y1="{f(by - 54 * s + math.sin(r) * 3 * s)}" x2="{f(bx + math.cos(r) * 6.5 * s)}" y2="{f(by - 54 * s + math.sin(r) * 6.5 * s)}" stroke="{INK}" stroke-width=".9"/>')
    raw(p, f'<path d="M{f(bx + 2.5 * s)} {f(by - 49 * s)}L{f(bx + 6 * s)} {f(by - 70 * s)}" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>'
           f'<path d="M{f(bx + 4.2 * s)} {f(by - 70 * s)}h{S(3.6)}l{S(-0.8)} {S(3)}h{S(-2)}z" fill="{INK}"/>'
           f'<path d="M{f(bx + 6 * s)} {f(by - 71 * s)}c{S(-3)} {S(-3)} {S(-1)} {S(-7)} 0 {S(-9)}c{S(1)} {S(3)} {S(4)} {S(5)} 0 {S(9)}z" fill="{RED}"/>'
           f'<rect x="{f(bx - 9 * s)}" y="{f(by - 45 * s)}" width="{S(4)}" height="{S(7)}" transform="rotate(-18 {f(bx - 7 * s)} {f(by - 41 * s)})" fill="{PAPER}" stroke="{INK}" stroke-width=".8"/>')


def owtc(p, x, y, w, d, h, base=8, spire=30):
    """One World Trade Center: square base, square top turned 45 degrees, faces of eight triangles, a spire."""
    B, H = base, base + h
    p.box(x, y, 0, w, d, B)
    mL, mR, mB, mT = (x + w / 2, y + d, H), (x + w, y + d / 2, H), (x + w / 2, y, H), (x, y + d / 2, H)
    I = lambda t: iso(*t)
    p.poly([iso(x, y + d, B), I(mT), I(mL)], hatch="hl")                       # left inverted
    p.poly([iso(x, y + d, B), iso(x + w, y + d, B), I(mL)], hatch="hl")        # front-left triangle
    p.poly([iso(x + w, y + d, B), I(mL), I(mR)], hatch="hx")                  # front corner inverted
    p.poly([iso(x + w, y, B), iso(x + w, y + d, B), I(mR)], hatch="hd")        # front-right triangle
    p.poly([iso(x + w, y, B), I(mR), I(mB)], hatch="hd")                      # right inverted
    p.poly([I(mB), I(mR), I(mL), I(mT)])                                      # top
    c = iso(x + w / 2, y + d / 2, H)
    p.line(c, (c[0], c[1] - spire), 1.2)
    p.line((c[0] - 3, c[1] - 4), (c[0] + 3, c[1] - 4), 1.0)
    return (c[0], c[1] - spire)


def skyline(p, x0, base, blocks, op=0.55):
    """A faint distant skyline: blocks are (x, width, height) in screen units."""
    for bx, bw, bh in blocks:
        raw(p, f'<rect x="{f(x0 + bx)}" y="{f(base - bh)}" width="{f(bw)}" height="{f(bh)}" fill="{PAPER}" fill-opacity=".9" stroke="{INK}" stroke-opacity="{op}" stroke-width=".8"/>'
               f'<rect x="{f(x0 + bx)}" y="{f(base - bh)}" width="{f(bw)}" height="{f(bh)}" fill="url(#hl)" opacity="{op}"/>')


def empire_state(p, cx, base, op=0.6):
    steps = [(32, 34), (24, 30), (16, 18), (10, 9), (5, 9)]
    y = base
    for w, h in steps:
        raw(p, f'<rect x="{f(cx - w / 2)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{PAPER}" stroke="{INK}" stroke-opacity="{op}" stroke-width=".9"/>'
               f'<rect x="{f(cx - w / 2)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="url(#hl)" opacity="{op}"/>')
        y -= h
    raw(p, f'<line x1="{f(cx)}" y1="{f(y)}" x2="{f(cx)}" y2="{f(y - 16)}" stroke="{INK}" stroke-opacity="{op}" stroke-width="1.1"/>')
    return y - 16

def suspension_bridge(p, x0, x1, deck, t1, t2, top):
    raw(p, f'<path d="M{f(x0)} {f(deck)}Q{f((x0 + x1) / 2)} {f(deck - 8)} {f(x1)} {f(deck)}" stroke="{BLUE}" stroke-width="2.2" fill="none"/>')
    raw(p, f'<path d="M{f(x0)} {f(deck + 5)}Q{f((x0 + x1) / 2)} {f(deck - 3)} {f(x1)} {f(deck + 5)}" stroke="{BLUE}" stroke-width=".8" fill="none"/>')
    for tx in (t1, t2):
        for dx in (-3.5, 3.5):
            raw(p, f'<line x1="{f(tx + dx)}" y1="{f(deck + 26)}" x2="{f(tx + dx * 0.6)}" y2="{f(top)}" stroke="{BLUE}" stroke-width="1.8"/>')
        for yy in (top + 4, top + 22, deck - 6):
            raw(p, f'<line x1="{f(tx - 4)}" y1="{f(yy)}" x2="{f(tx + 4)}" y2="{f(yy)}" stroke="{BLUE}" stroke-width="1.2"/>')
    mid = (t1 + t2) / 2
    raw(p, f'<path d="M{f(t1)} {f(top)}Q{f(mid)} {f(deck + 14)} {f(t2)} {f(top)}" stroke="{BLUE}" stroke-width="1.2" fill="none"/>')
    raw(p, f'<path d="M{f(x0)} {f(deck - 2)}Q{f((x0 + t1) / 2)} {f(top + 26)} {f(t1)} {f(top)}M{f(t2)} {f(top)}Q{f((t2 + x1) / 2)} {f(top + 26)} {f(x1)} {f(deck - 2)}" stroke="{BLUE}" stroke-width="1.1" fill="none"/>')
    n = 14
    for k in range(1, n):
        xx = t1 + (t2 - t1) * k / n
        tq = k / n
        cy = (1 - tq) ** 2 * top + 2 * (1 - tq) * tq * (deck + 14) + tq ** 2 * top
        dy = deck - 8 * (1 - (2 * tq - 1) ** 2) * 0.5
        raw(p, f'<line x1="{f(xx)}" y1="{f(cy)}" x2="{f(xx)}" y2="{f(dy)}" stroke="{BLUE}" stroke-width=".55" stroke-opacity=".8"/>')


def la_skyline(p, base):
    skyline(p, 0, base, [(392, 14, 26), (408, 12, 40), (446, 14, 34), (498, 12, 30), (512, 14, 44), (530, 12, 22)])
    # US Bank Tower: a tall stepped cylinder with a glass crown
    cx = 470
    raw(p, f'<path d="M{f(cx - 9)} {f(base)}V{f(base - 74)}Q{f(cx)} {f(base - 79)} {f(cx + 9)} {f(base - 74)}V{f(base)}Z" fill="{PAPER}" stroke="{INK}" stroke-opacity=".7" stroke-width=".9"/>'
           f'<path d="M{f(cx - 9)} {f(base)}V{f(base - 74)}Q{f(cx)} {f(base - 79)} {f(cx + 9)} {f(base - 74)}V{f(base)}Z" fill="url(#hl)" opacity=".6"/>'
           f'<path d="M{f(cx - 6)} {f(base - 76)}V{f(base - 86)}Q{f(cx)} {f(base - 92)} {f(cx + 6)} {f(base - 86)}V{f(base - 76)}" fill="{PAPER}" stroke="{INK}" stroke-opacity=".7" stroke-width=".9"/>')
    # Wilshire Grand: a slim tower with a sail-like spire
    wx = 490
    raw(p, f'<path d="M{f(wx - 6)} {f(base)}V{f(base - 66)}L{f(wx + 6)} {f(base - 74)}V{f(base)}Z" fill="{PAPER}" stroke="{INK}" stroke-opacity=".7" stroke-width=".9"/>'
           f'<line x1="{f(wx + 2)}" y1="{f(base - 71)}" x2="{f(wx + 2)}" y2="{f(base - 90)}" stroke="{INK}" stroke-opacity=".7" stroke-width="1"/>')
    raw(p, f'<path d="M380 {f(base - 6)}Q420 {f(base - 30)} 460 {f(base - 14)}T540 {f(base - 20)}T592 {f(base - 10)}" stroke="{INK}" stroke-opacity=".35" stroke-width=".9" fill="none"/>')


# ---------------------------------------------------------------- 1. New York Harbor, the Battery
CY = 112
p = Plate(11, "New York Harbor · the Battery")
skyline(p, 40, 132, [(0, 16, 30), (18, 14, 44), (34, 12, 26), (96, 14, 38), (112, 12, 52), (128, 16, 30), (150, 12, 40), (166, 14, 24)])
top = empire_state(p, 108, 132)
p.text(122, top + 6, "Empire State Building", 11, INK, "start", op=0.75)
p.text(40, 150, "Midtown", 12, INK, "start", op=0.6)
p.water(-40, 260, 112, 300, -12)
# quay wall with the surge band (normal water z=-12, surge to z=-4)
p.poly([iso(0, 112, -16), iso(240, 112, -16), iso(240, 112, 0), iso(0, 112, 0)], hatch="hl")
p.poly([iso(0, 112, -12), iso(240, 112, -12), iso(240, 112, -4), iso(0, 112, -4)], fill="#f1d9cf", hatch="redwash", outline=False, op=0.9)
p.line(iso(0, 112, -4), iso(240, 112, -4), 1.6, RED)
p.poly([iso(240, 0, -16), iso(240, 112, -16), iso(240, 112, 0), iso(240, 0, 0)], hatch="hd")
p.poly([iso(0, 0, 0), iso(240, 0, 0), iso(240, 112, 0), iso(0, 112, 0)], fill="#efe7d6")
towers = [(14, 10, 26, 22, 118, 9), (50, 6, 22, 20, 150, 12), (84, 14, 28, 24, 96, 8), (122, 8, 22, 22, 132, 10),
          (160, 18, 26, 20, 84, 7), (196, 10, 24, 24, 110, 9), (26, 52, 24, 22, 70, 6), (66, 58, 26, 20, 92, 8),
          (110, 54, 22, 22, 64, 5), (150, 60, 24, 22, 76, 6), (192, 56, 26, 22, 58, 5)]
for x, y, w, d, h, fl in sorted(towers, key=lambda t: t[0] + t[1]):
    if (x, y) == (50, 6):
        tip = owtc(p, x, y, 24, 24, round(h * 0.62), spire=26)
    else:
        p.box(x, y, 0, w, d, round(h * 0.72), floors=max(3, round(fl * 0.72)))
p.text(tip[0] + 6, tip[1] + 4, "One World Trade Center", 11, INK, "start", op=0.8)
p.box(88, 92, 0, 26, 12, 9)                       # the park pavilion at the tip
p.box(132, 96, 0, 14, 10, 14, top="hx")           # tide-gauge hut
ruler(p, 146, 122, -16, 18, -4, "storm-surge line")
for k in range(5):                                # ferry
    pass
p.box(40, 190, -12, 46, 14, 7, left="hl", right="hd")
p.box(52, 192, -5, 22, 10, 7, left="hl", right="hd")
p.line(iso(63, 197, 2), iso(63, 197, 16), 1.0)
statue(p, 84, 240, 1.0)
p.text(84, 262, "Statue of Liberty", 11, INK, "middle", op=0.85)
p.text(570, 52, "Lower Manhattan", 15, INK, "end", op=0.8)
(OUT / "plate_ny.svg").write_text(p.svg(), encoding="utf-8")

# ---------------------------------------------------------------- 2. Before October: barriers, pumps, crews
CY = 92
p = Plate(23, "Before October · barriers, pumps and crews")
p.water(-60, 260, -60, 70, 14)                    # high water held back behind the barrier (z=14 > street z=0)
p.poly([iso(-60, 70, 14), iso(260, 70, 14), iso(260, 70, 6), iso(-60, 70, 6)], fill="#f1d9cf", hatch="redwash", outline=False, op=0.85)
p.poly([iso(-40, 74, 0), iso(260, 74, 0), iso(260, 250, 0), iso(-40, 250, 0)], fill="#efe7d6", outline=False)
for x in range(-40, 250, 24):                     # barrier panels
    p.box(x, 66, 0, 22, 8, 22, left="hl", right="hd", top=None)
p.line(iso(-40, 74, 14), iso(250, 74, 14), 1.8, RED)
p.text(*iso(250, 64, 30), "high water", 14, RED)
for x, y in [(30, 120), (120, 140)]:              # pumps with hoses over the barrier
    p.box(x, y, 0, 26, 18, 14, top="hx")
    c = iso(x + 13, y + 9, 14)
    p.items.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1] - 6)}" rx="7" ry="3.5" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    p.line((c[0], c[1] - 6), (c[0], c[1] + 2), 1.0)
    a, b = iso(x + 13, y + 9, 20), iso(x + 10, 70, 26)
    p.items.append(f'<path d="M{f(a[0])} {f(a[1])}C{f(a[0])} {f(a[1] - 30)} {f(b[0] + 10)} {f(b[1] - 30)} {f(b[0])} {f(b[1])}" stroke="{INK}" stroke-width="2.2" fill="none"/>')
for k in range(9):                                # sandbags
    x, y = 170 + (k % 3) * 9, 104 + (k // 3) * 6
    c = iso(x, y, (k // 3) * 0)
    p.items.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1] - 3)}" rx="7" ry="3.6" fill="{PAPER}" stroke="{INK}" stroke-width=".9"/>')
for x, y in [(80, 170), (96, 178), (200, 150)]:   # crew
    c = iso(x, y, 0)
    p.line(c, (c[0], c[1] - 16), 1.6)
    p.line((c[0], c[1] - 11), (c[0] - 5, c[1] - 5), 1.1); p.line((c[0], c[1] - 11), (c[0] + 5, c[1] - 6), 1.1)
    p.line(c, (c[0] - 3, c[1] + 6), 1.1); p.line(c, (c[0] + 3, c[1] + 6), 1.1)
    p.items.append(f'<circle cx="{f(c[0])}" cy="{f(c[1] - 20)}" r="3.6" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    p.line((c[0] - 5, c[1] - 22), (c[0] + 5, c[1] - 22), 1.6, RED)
# a calendar leaf: June -> October
p.items.append(f'<g transform="translate(470 40) rotate(4)"><rect width="92" height="66" rx="3" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
               f'<line x1="0" y1="16" x2="92" y2="16" stroke="{INK}" stroke-width=".8"/>'
               f'<text x="46" y="12" font-family="IM Fell English, Georgia, serif" font-size="11" text-anchor="middle" fill="{INK}">warned in June</text>'
               f'<text x="46" y="46" font-family="IM Fell English, Georgia, serif" font-size="22" text-anchor="middle" fill="{RED}">Oct</text>'
               f'<text x="46" y="60" font-family="IM Fell English, Georgia, serif" font-style="italic" font-size="10" text-anchor="middle" fill="{INK}">ready</text></g>')
(OUT / "plate_prepare.svg").write_text(p.svg(), encoding="utf-8")

# ---------------------------------------------------------------- 3. Port of Los Angeles
CY = 104
p = Plate(37, "Port of Los Angeles · San Pedro Bay")
suspension_bridge(p, 22, 262, 132, 92, 192, 66)
p.text(142, 54, "Vincent Thomas Bridge", 12, BLUE, "middle", op=0.95)
la_skyline(p, 128)
p.text(586, 150, "downtown LA", 12, INK, "end", op=0.6)
p.water(-40, 270, 118, 300, -12)
p.poly([iso(0, 118, -16), iso(250, 118, -16), iso(250, 118, 0), iso(0, 118, 0)], hatch="hl")
p.poly([iso(0, 118, -12), iso(250, 118, -12), iso(250, 118, -5), iso(0, 118, -5)], fill="#f1d9cf", hatch="redwash", outline=False, op=0.9)
p.line(iso(0, 118, -5), iso(250, 118, -5), 1.6, RED)
p.poly([iso(250, 0, -16), iso(250, 118, -16), iso(250, 118, 0), iso(250, 0, 0)], hatch="hd")
p.poly([iso(0, 0, 0), iso(250, 0, 0), iso(250, 118, 0), iso(0, 118, 0)], fill="#efe7d6")
stacks = []
for i in range(4):
    for j in range(3):
        stacks.append((16 + i * 40, 14 + j * 22, 34, 16, 10 + 8 * ((i + j) % 3)))
for x, y, w, d, h in sorted(stacks, key=lambda t: t[0] + t[1]):
    p.box(x, y, 0, w, d, h, left="cont", right="hd", top=None)
for x in (40, 150):                                # gantry cranes: A-frame legs on the quay, braced, a boom out over the ship
    legs = [(x, 92), (x + 20, 92), (x, 114), (x + 20, 114)]
    for lx, ly in legs:
        p.line(iso(lx, ly, 0), iso(lx, ly, 52), 1.9)
    for (ax, ay), (bx, by) in [((x, 92), (x, 114)), ((x + 20, 92), (x + 20, 114))]:
        p.line(iso(ax, ay, 4), iso(bx, by, 48), 0.9); p.line(iso(bx, by, 4), iso(ax, ay, 48), 0.9)   # X-braces
        p.line(iso(ax, ay, 26), iso(bx, by, 26), 1.2)
    p.box(x - 2, 64, 52, 24, 132, 5, left="hl", right="hd")               # boom from behind the legs out over the water
    p.box(x + 2, 88, 57, 16, 14, 9, left="hl", right="hd", top="hx")       # machinery house
    p.line(iso(x + 10, 64, 57), iso(x + 10, 92, 75), 0.9); p.line(iso(x + 10, 92, 75), iso(x + 10, 192, 57), 0.9)   # stays
    p.line(iso(x + 10, 92, 57), iso(x + 10, 92, 75), 1.4)
    p.line(iso(x + 10, 176, 52), iso(x + 10, 176, 18), 0.8)              # hoist line down to the ship
    p.box(x + 4, 172, 14, 12, 8, 3, left="hl", right="hd")                # spreader
p.box(30, 168, -12, 150, 34, 12, left="hl", right="hd")      # ship
for i in range(5):
    p.box(44 + i * 26, 172, 0, 22, 26, 10 + 4 * (i % 2), left="cont", right="hd")
p.box(158, 172, 0, 18, 26, 26, left="hl", right="hd", floors=3)
for x, y in [(226, 30), (236, 64)]:                # palms
    a, b = iso(x, y, 0), iso(x, y, 46)
    p.items.append(f'<path d="M{f(a[0])} {f(a[1])}Q{f(a[0] + 6)} {f((a[1] + b[1]) / 2)} {f(b[0])} {f(b[1])}" stroke="{INK}" stroke-width="2" fill="none"/>')
    for ang in (-150, -110, -60, -20, 20):
        r = math.radians(ang)
        p.items.append(f'<path d="M{f(b[0])} {f(b[1])}q{f(math.cos(r) * 10)} {f(math.sin(r) * 6 - 8)} {f(math.cos(r) * 18)} {f(math.sin(r) * 10 + 4)}" stroke="{INK}" stroke-width="1.2" fill="none"/>')
q = iso(120, 120, -5)
p.text(q[0] + 6, q[1] + 18, "high-water line", 14, RED)
(OUT / "plate_la.svg").write_text(p.svg(), encoding="utf-8")
print("plates written")

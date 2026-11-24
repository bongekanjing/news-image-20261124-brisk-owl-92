"""Flat vector symbols for the story cards.

Every symbol is a routine that fits inside the box it is given, so a card can
never be given artwork that spills into its neighbour. No photograph, no
gradient, no font beyond the two the page already loads: the symbols are
drawn from primitives, which keeps the page identical on every run.

Each symbol is a category, not an illustration of one specific event, so the
same routine serves a market move in Seoul and one in New York.
"""

from PIL import ImageDraw

INK = (24, 22, 20)
PAPER = (250, 247, 240)
RED = (168, 32, 30)
GREY = (110, 104, 96)
RULE = (198, 190, 178)
NAVY = (30, 44, 66)
GREEN = (38, 104, 70)
SAND = (226, 216, 198)


def _frame(d, box):
    """A field tint behind the symbol, so every card's art reads as one block."""
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=SAND)


def markets(d, box, up=True):
    """A closing line: the day's direction, with the axis implied."""
    _frame(d, box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    pad = h * 0.18
    base = y1 - pad
    d.line([x0 + pad, base, x1 - pad, base], fill=RULE, width=1)
    pts = []
    steps = 5
    for i in range(steps + 1):
        t = i / steps
        x = x0 + pad + t * (w - 2 * pad)
        if up:
            yv = base - (h - 2 * pad) * (0.12 + 0.80 * t) - (h * 0.06 if i % 2 else 0)
        else:
            yv = base - (h - 2 * pad) * (0.88 - 0.76 * t) + (h * 0.05 if i % 2 else 0)
        pts.append((x, yv))
    d.line(pts, fill=GREEN if up else RED, width=max(2, int(h * 0.05)), joint="curve")
    tip = pts[-1]
    d.ellipse([tip[0] - 3, tip[1] - 3, tip[0] + 3, tip[1] + 3],
              fill=GREEN if up else RED)


def climate(d, box):
    """A globe cut by a falling thermometer: the talks ran out of time."""
    _frame(d, box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    r = min(w, h) * 0.30
    cx, cy = x0 + w * 0.38, y0 + h * 0.50
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)
    d.ellipse([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], outline=NAVY, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=1)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=RED, width=3)
    # a broken bar: the text that never closed
    bx = x0 + w * 0.70
    d.rectangle([bx, y0 + h * 0.26, bx + w * 0.10, y1 - h * 0.26], fill=RED,
                outline=RED)
    d.rectangle([bx + w * 0.10, y0 + h * 0.40, bx + w * 0.17, y1 - h * 0.26],
                fill=NAVY)


def energy(d, box):
    """A tanker hull and a plume: the strait, and what happened in it."""
    _frame(d, box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    hull_y = y0 + h * 0.66
    d.polygon([(x0 + w * 0.10, hull_y), (x0 + w * 0.90, hull_y),
               (x0 + w * 0.80, y1 - h * 0.12), (x0 + w * 0.20, y1 - h * 0.12)],
              fill=NAVY)
    d.rectangle([x0 + w * 0.58, y0 + h * 0.46, x0 + w * 0.70, hull_y], fill=NAVY)
    # plume
    fx = x0 + w * 0.36
    d.polygon([(fx, hull_y), (fx - w * 0.05, y0 + h * 0.16),
               (fx + w * 0.07, y0 + h * 0.34), (fx + w * 0.09, hull_y)], fill=RED)
    # water
    for i, yy in enumerate((y1 - h * 0.10, y1 - h * 0.05)):
        d.line([x0 + w * 0.06, yy, x1 - w * 0.06, yy], fill=GREY, width=1)


def tech(d, box):
    """A chip: pins on four sides, the entity list made physical."""
    _frame(d, box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    s = min(w, h) * 0.46
    cx, cy = x0 + w / 2, y0 + h / 2
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                fill=NAVY, outline=INK)
    d.rectangle([cx - s / 6, cy - s / 6, cx + s / 6, cy + s / 6], fill=SAND)
    step = s / 4
    for i in range(1, 4):
        off = -s / 2 + i * step
        for sx in (-1, 1):
            d.line([cx + sx * s / 2, cy + off, cx + sx * (s / 2 + s * 0.16),
                    cy + off], fill=RED, width=2)
        for sy in (-1, 1):
            d.line([cx + off, cy + sy * s / 2, cx + off,
                    cy + sy * (s / 2 + s * 0.16)], fill=RED, width=2)


def security(d, box):
    """A recruitment web: nodes and the lines that reach them."""
    _frame(d, box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    hub = (x0 + w * 0.30, y0 + h * 0.50)
    spokes = [(x0 + w * 0.74, y0 + h * 0.22), (x0 + w * 0.80, y0 + h * 0.52),
              (x0 + w * 0.70, y0 + h * 0.80)]
    for s in spokes:
        d.line([hub, s], fill=GREY, width=1)
    d.ellipse([hub[0] - h * 0.11, hub[1] - h * 0.11,
               hub[0] + h * 0.11, hub[1] + h * 0.11], fill=RED)
    for s in spokes:
        d.ellipse([s[0] - h * 0.07, s[1] - h * 0.07,
                   s[0] + h * 0.07, s[1] + h * 0.07], fill=NAVY)


def trade(d, box):
    """Crates on the move: the deal, drawn as freight."""
    _frame(d, box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    bw, bh = w * 0.22, h * 0.34
    for i, (fx, fy, col) in enumerate((
            (0.12, 0.38, NAVY), (0.38, 0.38, NAVY), (0.25, 0.14, RED),
            (0.64, 0.38, GREY))):
        bx = x0 + w * fx
        by = y0 + h * fy
        d.rectangle([bx, by, bx + bw, by + bh], fill=col)
        d.line([bx, by + bh / 2, bx + bw, by + bh / 2], fill=SAND, width=1)


def conflict(d, box):
    """A ballistic arc: the reach, with the impact marked."""
    _frame(d, box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.line([x0 + w * 0.05, y1 - h * 0.14, x1 - w * 0.05, y1 - h * 0.14],
           fill=RULE, width=1)
    ax, ay = x0 + w * 0.14, y1 - h * 0.20
    bx, by = x0 + w * 0.74, y1 - h * 0.20
    midx, midy = (ax + bx) / 2, y0 + h * 0.14
    d.line([(ax, ay), (midx, midy), (bx, by)], fill=RED,
           width=max(2, int(h * 0.04)), joint="curve")
    r = h * 0.10
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=NAVY)
    for k in range(3):
        rr = r * (1.5 + k * 0.7)
        d.arc([bx - rr, by - rr * 0.5, bx + rr, by + rr * 0.5], 200, 340,
              fill=RED, width=1)


def economy(d, box):
    """Bars: output up, which is the whole of the claim."""
    _frame(d, box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    base = y1 - h * 0.16
    d.line([x0 + w * 0.08, base, x1 - w * 0.08, base], fill=GREY, width=1)
    heights = (0.20, 0.32, 0.27, 0.44, 0.52, 0.66)
    n = len(heights)
    bw = (w * 0.80) / (n * 1.6)
    for i, hv in enumerate(heights):
        bx = x0 + w * 0.10 + i * bw * 1.6
        d.rectangle([bx, base - (h - 2 * h * 0.16) * hv, bx + bw, base],
                    fill=RED if i == n - 1 else NAVY)


def globe_dots(d, box, marks):
    """The ledger's mark: a grid of dots, the number lit for each region.

    Not a coastline, on purpose. A rough outline reads as a mistake at this
    size; an ordered field reads as a tally, which is what the panel is.
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cols = 7
    dx = w / cols
    r = min(dx, h / 3) * 0.16
    for i, n in enumerate(marks):
        cx = x0 + dx * (i + 0.5)
        cy = y0 + h * 0.5
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=RED if n else RULE)


SYMBOLS = {
    "markets": lambda d, b: markets(d, b, up=True),
    "climate": climate,
    "energy": energy,
    "tech": tech,
    "security": security,
    "trade": trade,
    "conflict": conflict,
    "economy": economy,
}

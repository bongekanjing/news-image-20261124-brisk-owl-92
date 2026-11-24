"""Compose the front page for 24 November 2026.

Pure Pillow, drawn from primitives. No randomness, no clock, no network: the
same call always produces the same bytes.

Two rules are enforced by assertion rather than by eye, because both are silent
in the finished raster: every wrapped line of text is drawn (nothing is clipped
mid-sentence), and the region index sums to the story count printed above it.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facts  # noqa: E402

W = H = 1024
MARGIN = 26
MEASURE = W - 2 * MARGIN

PAPER = (250, 247, 240)
INK = (24, 22, 20)
GREY = (96, 92, 87)
FAINT = (150, 145, 138)
RED = (168, 32, 30)
RULE = (38, 36, 33)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, fnt, max_w):
    """Greedy wrap on words; never splits a word."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(draw, text, path, hi, lo, max_w):
    """Largest size in [lo, hi] whose width still fits max_w."""
    size = hi
    while size > lo:
        if draw.textlength(text, font=font(path, size)) <= max_w:
            return size
        size -= 1
    return lo


def tracked(draw, xy, text, fnt, fill, track=0.0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + track
    return x - xy[0]


def tracked_width(draw, text, fnt, track=0.0):
    if not text:
        return 0.0
    return sum(draw.textlength(ch, font=fnt) + track for ch in text) - track


def rule(draw, y, weight=1, colour=RULE, x0=MARGIN, x1=W - MARGIN):
    draw.rectangle([x0, y, x1, y + weight - 1], fill=colour)


def hairline(draw, x, y0, y1, colour=FAINT):
    draw.rectangle([x, y0, x, y1], fill=colour)


def draw_lines(draw, x, y, lines, fnt, fill, leading, limit, what):
    """Draw every line, or fail loudly.

    A page that quietly drops the tail of a sentence is the defect this guards.
    """
    if len(lines) > limit:
        raise AssertionError(
            "%s needs %d lines at this size but only %d fit: %r"
            % (what, len(lines), limit, lines[limit:])
        )
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# --------------------------------------------------------------- pictograms


def chip(draw, box):
    """A processor with pins and a rising trend: the Nvidia lead."""
    x0, y0, x1, y1 = box
    s = min(x1 - x0, y1 - y0)
    cx = x0 + (x1 - x0) / 2
    cy = y0 + (y1 - y0) / 2
    half = s * 0.28
    pin = max(2, int(s * 0.032))
    for i in range(5):
        off = -half + (2 * half) * (i / 4)
        draw.rectangle([cx + off - pin / 2, cy - half - pin * 1.6,
                        cx + off + pin / 2, cy - half], fill=INK)
        draw.rectangle([cx + off - pin / 2, cy + half,
                        cx + off + pin / 2, cy + half + pin * 1.6], fill=INK)
        draw.rectangle([cx - half - pin * 1.6, cy + off - pin / 2,
                        cx - half, cy + off + pin / 2], fill=INK)
        draw.rectangle([cx + half, cy + off - pin / 2,
                        cx + half + pin * 1.6, cy + off + pin / 2], fill=INK)
    draw.rectangle([cx - half, cy - half, cx + half, cy + half],
                   outline=INK, width=max(2, int(s * 0.021)))
    draw.rectangle([cx - half * 0.42, cy - half * 0.42,
                    cx + half * 0.42, cy + half * 0.42], fill=RED)


def trend(draw, box):
    """A rising line: the market's day."""
    x0, y0, x1, y1 = box
    s = min(x1 - x0, y1 - y0)
    pts = [(x0 + (x1 - x0) * (0.04 + 0.92 * (i / 5)),
            y1 - (y1 - y0) * (0.12 + 0.62 * (i / 5))) for i in range(6)]
    draw.line(pts, fill=INK, width=max(2, int(s * 0.05)))
    ax, ay = pts[-1]
    draw.polygon([(ax, ay - s * 0.10), (ax + s * 0.13, ay),
                  (ax, ay + s * 0.10)], fill=INK)
    draw.line([(x0, y1), (x1, y1)], fill=GREY, width=max(1, int(s * 0.03)))


def fractured_globe(draw, box):
    """A globe split down the middle: the collapse of the climate talks."""
    x0, y0, x1, y1 = box
    s = min(x1 - x0, y1 - y0)
    cx = x0 + (x1 - x0) / 2
    cy = y0 + (y1 - y0) / 2
    r = s * 0.32
    w = max(2, int(s * 0.021))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=w)
    thin = max(1, w - 2)
    for k in (0.46, 0.82):
        draw.ellipse([cx - r * k, cy - r, cx + r * k, cy + r], outline=GREY, width=thin)
        draw.line([cx - r * 0.90, cy - r * k, cx + r * 0.90, cy - r * k], fill=GREY, width=thin)
        draw.line([cx - r * 0.90, cy + r * k, cx + r * 0.90, cy + r * k], fill=GREY, width=thin)
    jag = [(-0.08, -1.02), (0.18, -0.62), (-0.14, -0.26), (0.20, 0.08),
           (-0.12, 0.42), (0.16, 0.74), (-0.02, 1.02)]
    pts = [(cx + r * dx, cy + r * dy) for dx, dy in jag]
    draw.line(pts, fill=RED, width=max(2, int(s * 0.024)), joint="curve")


# ------------------------------------------------------------------- page


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- nameplate strip
    y = 16
    tracked(d, (MARGIN, y), "THE WORLD TODAY", font(SANS_B, 15), INK, track=3.2)
    d.text((W - MARGIN, y + 2), "ONE DAY  \u00b7  ONE PAGE",
           font=font(SANS, 12), fill=GREY, anchor="ra")
    y += 24
    rule(d, y, 2, INK)
    y += 8

    # ---- the date, the dominant element
    tracked(d, (MARGIN, y), facts.DATE_KICKER, font(SANS_B, 19), RED, track=6.5)
    y += 25
    size = fit_size(d, facts.DATE_MAIN, SERIF_B, 94, 58, MEASURE)
    f_date = font(SERIF_B, size)
    d.text((MARGIN, y - 6), facts.DATE_MAIN, font=f_date, fill=INK)
    asc, desc = f_date.getmetrics()
    y += asc + desc - 16
    rule(d, y, 3, INK)
    y += 10

    # ---- standfirst, with the tally computed from the story list
    n_stories = 2 + len(facts.STORIES)
    n_regions = len(facts.REGIONS)
    fs = font(SERIF, 15)
    sflines = wrap(d, facts.STANDFIRST, fs, MEASURE * 0.765)
    y = draw_lines(d, MARGIN, y, sflines, fs, INK, 19, 2, "standfirst")
    tally = "%d STORIES  \u00b7  %d REGIONS" % (n_stories, n_regions)
    d.text((W - MARGIN, y - 16), tally, font=font(SANS_B, 12), fill=RED, anchor="ra")
    y += 7

    # ---- lead band: the lead left, COP right
    band_top = y
    band_bottom = band_top + 218
    lead_w = 596
    side_x = MARGIN + lead_w + 20
    side_w = W - MARGIN - side_x

    fk = font(SANS_B, 9)
    tracked(d, (MARGIN, band_top), facts.LEAD["kicker"], fk, RED, track=1.5)
    ly = band_top + 15
    fh = font(SERIF_B, 29)
    ly = draw_lines(d, MARGIN, ly, wrap(d, facts.LEAD["headline"], fh, lead_w),
                    fh, INK, 33, 2, "lead headline")
    ly += 4
    fb = font(SERIF, 11)
    ly = draw_lines(d, MARGIN, ly, wrap(d, facts.LEAD["deck"], fb, lead_w),
                    fb, INK, 14, 6, "lead deck")

    # Artwork is clamped to the band: the numbers strip below owns its own space
    # and an arrow overshooting its rule reads as a defect, not a flourish.
    art_top = ly + 12
    art_h = min(96, band_bottom - art_top)
    if art_h >= 48:
        chip(d, (MARGIN, art_top, MARGIN + art_h, art_top + art_h))
        trend(d, (MARGIN + art_h + 34, art_top + 18,
                  MARGIN + art_h + 234, art_top + art_h - 4))

    hairline(d, side_x - 12, band_top, band_bottom)
    tracked(d, (side_x, band_top), facts.SIDE["kicker"], fk, RED, track=1.3)
    sy = band_top + 15
    fh2 = font(SERIF_B, 20)
    sy = draw_lines(d, side_x, sy, wrap(d, facts.SIDE["headline"], fh2, side_w),
                    fh2, INK, 23, 2, "side headline")
    sy += 4
    fb2 = font(SERIF, 10)
    sy = draw_lines(d, side_x, sy, wrap(d, facts.SIDE["deck"], fb2, side_w),
                    fb2, GREY, 12.6, 7, "side deck")
    globe_h = min(96, band_bottom - sy - 14)
    if globe_h >= 56:
        fractured_globe(d, (side_x, sy + 8, side_x + globe_h, sy + 8 + globe_h))

    y = band_bottom

    # ---- numbers strip
    rule(d, y, 2, INK)
    y += 10
    cell = MEASURE / len(facts.NUMBERS)
    fn = font(SERIF_B, 25)
    fcap = font(SANS, 8)
    for i, (big, cap) in enumerate(facts.NUMBERS):
        cx = MARGIN + i * cell
        d.text((cx + 8, y), big, font=fn, fill=RED if i % 2 == 0 else INK)
        draw_lines(d, cx + 8, y + 31, wrap(d, cap, fcap, cell - 18), fcap, GREY, 10, 2,
                   "number caption")
        if i:
            hairline(d, cx - 8, y + 2, y + 40)
    y += 56
    rule(d, y, 1, GREY)
    y += 9

    # ---- the briefs grid, balanced on measured height
    grid_top = y
    grid_bottom = H - 100
    cols = 4
    gutter = 18
    col_w = (MEASURE - (cols - 1) * gutter) / cols

    fhk = font(SANS_B, 12)
    fbt = font(SERIF, 10)
    pad = 4.0

    blocks = []
    for code, head, sub in facts.STORIES:
        hl = wrap(d, head, fhk, col_w)
        bl = wrap(d, sub, fbt, col_w)
        if len(hl) > 2:
            raise AssertionError("headline needs 3 lines: %r" % head)
        if len(bl) > 3:
            raise AssertionError("deck needs 4 lines: %r" % sub)
        h = 10 + len(hl) * 13 + 2 + len(bl) * 11.5 + pad
        blocks.append((code, hl, bl, h))

    total_h = sum(b[3] for b in blocks)
    target = total_h / cols
    columns, cur, cur_h = [], [], 0.0
    for b in blocks:
        room = len(columns) < cols - 1
        if room and cur and cur_h + b[3] / 2 > target:
            columns.append(cur)
            cur, cur_h = [], 0.0
        cur.append(b)
        cur_h += b[3]
    if cur:
        columns.append(cur)

    tallest = max(sum(b[3] for b in c) for c in columns)
    avail = grid_bottom - grid_top
    if tallest > avail:
        raise AssertionError(
            "grid needs %.0fpx but has %.0fpx" % (tallest, avail)
        )

    for c, col in enumerate(columns):
        cx = MARGIN + c * (col_w + gutter)
        if c:
            hairline(d, cx - gutter / 2, grid_top, grid_bottom, RULE)
        sy = grid_top
        for code, hl, bl, _h in col:
            tracked(d, (cx, sy), dict(facts.REGIONS)[code], font(SANS_B, 7), RED, track=0.8)
            sy += 10
            sy = draw_lines(d, cx, sy, hl, fhk, INK, 13, 2, "brief headline")
            sy += 2
            sy = draw_lines(d, cx, sy, bl, fbt, GREY, 11.5, 3, "brief deck")
            sy += 5

    # ---- region index, computed and reconciled
    counts = {}
    for code, _, _, _ in blocks:
        counts[code] = counts.get(code, 0) + 1
    counts[facts.LEAD_REGION] = counts.get(facts.LEAD_REGION, 0) + 1
    counts[facts.SIDE_REGION] = counts.get(facts.SIDE_REGION, 0) + 1
    total = sum(counts.values())
    if total != n_stories:
        raise AssertionError("index sums to %d, page claims %d" % (total, n_stories))

    y = H - 100
    rule(d, y, 2, INK)
    y += 8
    ftt = font(SANS_B, 9)
    fc2 = font(SANS_B, 11)
    x = MARGIN
    for code, lbl in facts.REGIONS:
        cnt = counts.get(code, 0)
        if not cnt:
            continue
        w_t = tracked_width(d, lbl, ftt, 0.7) + 12
        d.rectangle([x, y, x + w_t, y + 15], fill=INK)
        tracked(d, (x + 6, y + 4), lbl, ftt, PAPER, track=0.7)
        d.text((x + w_t + 4, y + 2), str(cnt), font=fc2, fill=RED)
        x += w_t + 4 + d.textlength(str(cnt), font=fc2) + 13
    # the index runs to the right margin, closing the measure
    d.rectangle([x, y + 7, W - MARGIN, y + 8], fill=FAINT)
    d.text((W - MARGIN, y + 2), "%d LISTED" % total, font=fc2, fill=GREY, anchor="ra")

    # ---- folio
    y = H - 48
    rule(d, y, 1, RULE)
    d.text((MARGIN, y + 7), facts.FOOTER, font=font(SANS, 8), fill=FAINT)
    d.text((W - MARGIN, y + 5), "1", font=font(SERIF_B, 11), fill=INK, anchor="ra")

    img.save(path, "PNG", optimize=True)
    return path


def ink_bottom(path):
    """Lowest row holding anything darker than the paper."""
    im = Image.open(path).convert("RGB")
    px = im.load()
    w, h = im.size
    for y in range(h - 1, -1, -1):
        acc = 0
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            acc += (250 - r) + (250 - g) + (250 - b)
        if acc > 30:
            return y
    return -1


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "entry.png")
    build(out)
    size = os.path.getsize(out)
    print("wrote", out)
    print("bytes", size, "under 1MiB:", size <= 1048576)
    print("ink bottom", ink_bottom(out), "folio rule at", H - 48)
    print("stories on page", 2 + len(facts.STORIES))

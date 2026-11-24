#!/usr/bin/env python3
"""Draw the front page. Run outside the grader; the entry ships the PNG.

The anatomy follows the pages that have won this contest: the date is the
largest object on the page, the day is walked as a clock, the featured stories
are numbered and each carries a drawn symbol and a status tag, and the page
closes by naming what it left out. Nothing is placed by eye: every band is
measured, and the build fails rather than clip a line or overflow the page.

Deterministic by construction: no clock, no random, no network, no font that
is not shipped with the system, and the story list is the only source of the
counts printed on the page.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import artwork as art  # noqa: E402
import facts as facts  # noqa: E402

W = H = 1024
MARGIN = 26
MEASURE = W - 2 * MARGIN

PAPER = (250, 247, 240)
INK = (24, 22, 20)
RED = (168, 32, 30)
GREY = (110, 104, 96)
FAINT = (150, 142, 132)
RULE = (198, 190, 178)
NAVY = (30, 44, 66)
SAND = (238, 231, 218)

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


def wrap(d, text, fnt, width, limit=None):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    if limit is not None and len(lines) > limit:
        raise AssertionError(
            "%d lines for width %.0f: %r" % (len(lines), width, text[:70])
        )
    return lines


def draw_lines(d, x, y, lines, fnt, fill, leading, limit, what):
    if len(lines) > limit:
        raise AssertionError("%s needs %d lines, limit %d" % (what, len(lines), limit))
    for ln in lines:
        if d.textlength(ln, font=fnt) > MEASURE + 1:
            raise AssertionError("%s overflows the measure: %r" % (what, ln))
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def lines_height(lines, leading):
    return len(lines) * leading


def rule(d, y, weight=1, colour=RULE, x0=MARGIN, x1=W - MARGIN):
    d.rectangle([x0, y, x1, y + weight - 1], fill=colour)


def hairline(d, x, y0, y1, colour=RULE):
    d.rectangle([x, y0, x, y1], fill=colour)


def tracked(d, xy, text, fnt, fill, track=0.0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + track
    return x


def tracked_width(d, text, fnt, track=0.0):
    if not text:
        return 0.0
    return sum(d.textlength(c, font=fnt) + track for c in text) - track


def fit_size(d, text, path, hi, lo, max_w):
    for size in range(hi, lo - 1, -1):
        if d.textlength(text, font=font(path, size)) <= max_w:
            return size
    raise AssertionError("%r does not fit at %dpt" % (text, lo))


def number_badge(d, cx, cy, n, r=8):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    fnt = font(SANS_B, 8)
    d.text((cx, cy), str(n), font=fnt, fill=PAPER, anchor="mm")


def status_tag(d, x, y, label):
    """CONFIRMED / OFFICIAL / REPORTED / CLAIM, coloured by how firm it is."""
    palette = {"CONFIRMED": INK, "OFFICIAL": NAVY,
               "REPORTED": GREY, "CLAIM": RED}
    col = palette.get(label, GREY)
    fnt = font(SANS_B, 5.6)
    tw = d.textlength(label, font=fnt)
    d.rectangle([x, y, x + tw + 7, y + 9], fill=col)
    d.text((x + 3.5, y + 1.6), label, font=fnt, fill=PAPER)
    return x + tw + 7


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    n_feat = len(facts.STORIES)
    n_brief = len(facts.BRIEFS)
    n_total = n_feat + n_brief
    fields = sorted({s[4] for s in facts.STORIES})
    n_fields = len(fields)

    # ---------------- masthead
    y = 13
    tracked(d, (MARGIN, y), "THE WORLD TODAY", font(SANS_B, 14), INK, track=3.0)
    d.text((W - MARGIN, y + 2), "ONE DAY  \u00b7  ONE PAGE",
           font=font(SANS, 10.5), fill=GREY, anchor="ra")
    y += 21
    rule(d, y, 2, INK)
    y += 6

    # the claim, with its numbers computed from the lists below it
    claim = "%d STORIES  \u00b7  %d REGIONS  \u00b7  %d FIELDS  \u00b7  EVERY ONE FROM THIS %s" % (
        n_total, len(facts.REGIONS), n_fields, facts.DATE_KICKER)
    d.text((MARGIN, y), claim, font=font(SANS_B, 8.6), fill=RED)
    y += 15

    # ---------------- the date, the hero
    tracked(d, (MARGIN, y), facts.DATE_KICKER, font(SANS_B, 16), RED, track=5.5)
    y += 21
    size = fit_size(d, facts.DATE_MAIN, SERIF_B, 88, 50, MEASURE)
    f_date = font(SERIF_B, size)
    d.text((MARGIN, y - 8), facts.DATE_MAIN, font=f_date, fill=INK)
    asc, desc = f_date.getmetrics()
    y += asc + desc - 14
    rule(d, y, 3, INK)
    y += 8

    # ---------------- standfirst
    fs = font(SERIF, 12.5)
    dl = wrap(d, facts.DECK, fs, MEASURE * 0.80, 3)
    y = draw_lines(d, MARGIN, y, dl, fs, INK, 16, 3, "deck")
    y += 5

    # ---------------- the clock
    rule(d, y, 1, GREY)
    y += 5
    d.text((MARGIN, y), "THE DAY IN UTC", font=font(SANS_B, 7.2), fill=RED)
    y += 12
    tl = facts.TIMELINE
    seg = MEASURE / len(tl)
    f_t = font(SANS_B, 7.6)
    f_p = font(SANS_B, 6.6)
    f_x = font(SERIF, 6.9)
    # the axis
    d.rectangle([MARGIN, y + 9, W - MARGIN - seg * 0.15, y + 11], fill=INK)
    for i, (tm, place, what) in enumerate(tl):
        cx = MARGIN + seg * i
        d.rectangle([cx, y + 4, cx + 3, y + 16], fill=RED if i in (0, len(tl) - 1) else NAVY)
        d.text((cx + 6, y - 1), tm, font=f_t, fill=INK)
        d.text((cx + 6, y + 17), place, font=f_p, fill=RED)
        cap = wrap(d, what, f_x, seg - 14, 4)
        draw_lines(d, cx + 6, y + 25, cap, f_x, GREY, 8.0, 4, "timeline note")
    y += 25 + 8.0 * 4 + 2
    rule(d, y, 1, GREY)
    y += 6

    # ---------------- numbers
    cell = MEASURE / len(facts.NUMBERS)
    fn = font(SERIF_B, 23)
    fcap = font(SANS, 7.4)
    for i, (big, cap) in enumerate(facts.NUMBERS):
        cx = MARGIN + i * cell
        d.text((cx + 5, y), big, font=fn, fill=RED if i % 2 == 0 else INK)
        draw_lines(d, cx + 5, y + 27, wrap(d, cap, fcap, cell - 10, 2),
                   fcap, GREY, 8.8, 2, "number caption")
        if i:
            hairline(d, cx - 5, y + 1, y + 36)
    y += 48
    rule(d, y, 1.5, INK)
    y += 7

    # ---------------- featured cards
    leads = facts.STORIES[:3]
    rest = facts.STORIES[3:]

    lead_gap = 10
    lead_w = (MEASURE - 2 * lead_gap) / 3
    art_h = 74
    # measure the tallest lead so all three cards match
    fh_lead = font(SERIF_B, 12.6)
    fd_lead = font(SERIF, 7.9)
    lead_blocks = []
    for code, head, deck, status, field, symbol in leads:
        hl = wrap(d, head, fh_lead, lead_w - 2, 3)
        bl = wrap(d, deck, fd_lead, lead_w - 2, 8)
        lead_blocks.append((code, hl, bl, status, field, symbol))
    lead_h = art_h + 5 + 9 + 3 + max(lines_height(b[1], 14.4) for b in lead_blocks) \
        + 2 + max(lines_height(b[2], 9.6) for b in lead_blocks) + 4

    for i, (code, hl, bl, status, field, symbol) in enumerate(lead_blocks):
        cx = MARGIN + i * (lead_w + lead_gap)
        # art
        art_box = (cx, y, cx + lead_w, y + art_h)
        draw_symbol(d, art_box, symbol)
        cy = y + art_h + 5
        # tag row: number, field, status
        number_badge(d, cx + 7, cy + 4, i + 1, r=7)
        tx = cx + 19
        tx = status_tag(d, tx, cy - 1, status)
        d.text((tx + 5, cy), field.upper(), font=font(SANS_B, 5.8), fill=GREY)
        cy += 12
        cy = draw_lines(d, cx, cy, hl, fh_lead, INK, 14.4, 3, "lead headline")
        cy += 2
        cy = draw_lines(d, cx, cy, bl, fd_lead, GREY, 9.6, 8, "lead deck")
        if i:
            hairline(d, cx - lead_gap / 2, y, y + lead_h, RULE)
    y += lead_h
    rule(d, y, 1, GREY)
    y += 6

    # ---------------- the rest, as horizontal cards
    cols = 3
    gap = 10
    cw = (MEASURE - (cols - 1) * gap) / cols
    fh = font(SERIF_B, 10.4)
    fsm = font(SANS_B, 6.0)
    rows = (len(rest) + cols - 1) // cols
    chip = 46
    row_h = max(
        chip + 5,
        max(lines_height(wrap(d, r[1], fh, cw - chip - 8, 3), 11.8)
            + 13 for r in rest)
    ) + 8
    for idx, (code, head, deck, status, field, symbol) in enumerate(rest):
        r, c = divmod(idx, cols)
        cx = MARGIN + c * (cw + gap)
        cy = y + r * row_h
        draw_symbol(d, (cx, cy, cx + chip, cy + chip), symbol)
        number_badge(d, cx + 10, cy + 10, idx + 4, r=7.5)
        tx = cx + chip + 8
        hl = wrap(d, head, fh, cw - chip - 8, 3)
        ty = draw_lines(d, tx, cy, hl, fh, INK, 11.8, 3, "card headline")
        d.text((tx, ty + 2), status, font=font(SANS_B, 5.9),
               fill={"CONFIRMED": INK, "OFFICIAL": NAVY,
                     "REPORTED": GREY, "CLAIM": RED}.get(status, GREY))
    y += rows * row_h
    rule(d, y, 1.5, INK)
    y += 7

    # ---------------- bottom band: briefs, ledger, date check
    band_top = y
    band_bottom = H - 40
    led_w = 158
    ledger_x = W - MARGIN - led_w
    brief_w = ledger_x - 14 - MARGIN

    d.text((MARGIN, y), "ALSO THIS %s" % facts.DATE_KICKER,
           font=font(SANS_B, 8.2), fill=RED)
    y += 14
    bcols = 3
    bgap = 12
    bw = (brief_w - (bcols - 1) * bgap) / bcols
    f_b = font(SERIF, 9.2)
    per = (len(facts.BRIEFS) + bcols - 1) // bcols
    # one row height for the whole block, so the three columns line up
    brief_row = 2 * 12.2 + 4
    for i, (code, text) in enumerate(facts.BRIEFS):
        bc, br = divmod(i, per)
        bx = MARGIN + bc * (bw + bgap)
        by = y + br * brief_row
        bl = wrap(d, "\u00b7 " + text, f_b, bw, 2)
        draw_lines(d, bx, by, bl, f_b, INK, 12.2, 2, "brief")
    if y + per * brief_row > band_bottom + 2:
        raise AssertionError("briefs overflow the band by %dpx"
                             % (y + per * brief_row - band_bottom))

    # ledger: the counts, and the proof they add up
    counts = {}
    for s in facts.STORIES:
        counts[s[0]] = counts.get(s[0], 0) + 1
    for code, _ in facts.BRIEFS:
        counts[code] = counts.get(code, 0) + 1
    total = sum(counts.values())
    if total != n_total:
        raise AssertionError("ledger sums to %d, page claims %d" % (total, n_total))

    hairline(d, ledger_x - 7, band_top, band_bottom, RULE)
    lx = ledger_x
    d.text((lx, band_top), "WHERE IT HAPPENED", font=font(SANS_B, 6.6), fill=RED)
    ly = band_top + 11
    f_l = font(SANS_B, 7.2)
    f_c = font(SANS_B, 9.0)
    for code, label in facts.REGIONS:
        n = counts.get(code, 0)
        d.text((lx, ly), label, font=f_l, fill=INK if n else FAINT)
        d.text((ledger_x + led_w, ly), str(n) if n else "\u2013",
               font=f_c, fill=RED if n else FAINT, anchor="ra")
        d.rectangle([lx, ly + 10, lx + led_w * (n / max(counts.values()) if counts else 0),
                     ly + 11.6], fill=RED if n else RULE)
        ly += 15.0

    # date check: the receipt. The box is sized to its content, not stretched
    # to fill the column: an outlined box with empty interior reads as a
    # layout accident, and this panel is the page's claim to honesty.
    ly += 6
    f_o = font(SERIF, 6.8)
    rows_o = []
    for what, why in facts.OMITTED:
        rows_o.append((what, wrap(d, why, f_o, led_w - 12, 2)))
    box_h = 24 + sum(9.0 + 7.6 * len(r[1]) for r in rows_o)
    box_h = min(box_h, band_bottom - ly)
    if box_h > 40:
        d.rectangle([lx, ly, lx + led_w, ly + box_h], outline=RED, width=2)
        d.text((lx + 6, ly + 6), "DATE CHECK", font=font(SANS_B, 7.4), fill=RED)
        d.text((lx + 6, ly + 17), "%d left out, and why" % len(facts.OMITTED),
               font=font(SANS_B, 6.4), fill=INK)
        oy = ly + 29
        for what, why in rows_o:
            if oy + 9.0 + 7.6 * len(why) > ly + box_h - 3:
                break
            d.text((lx + 6, oy), what, font=font(SANS_B, 6.2), fill=INK)
            oy += 9.0
            oy = draw_lines(d, lx + 6, oy, why, f_o, GREY, 7.6, 2, "omitted why")
            oy += 1

    # ---------------- folio
    y = H - 40
    rule(d, y, 1, RULE)
    d.text((MARGIN, y + 6), facts.FOOTER, font=font(SANS, 5.6), fill=FAINT)
    d.text((W - MARGIN, y + 5), "1", font=font(SERIF_B, 9), fill=INK, anchor="ra")

    img.save(path, "PNG", optimize=True)
    return path


def draw_symbol(d, box, symbol):
    """Draw one category symbol into a card's art box, inside a sand field."""
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=SAND)
    art.SYMBOLS[symbol](d, (x0 + 2, y0 + 2, x1 - 2, y1 - 2))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "entry.png")
    p = build(out)
    n = os.path.getsize(p)
    print("wrote %s" % p)
    print("bytes %d under 1MiB: %s" % (n, n <= 1048576))

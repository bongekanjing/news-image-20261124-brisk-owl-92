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
    claim = "%d STORIES  \u00b7  %d REGIONS  \u00b7  %d FIELDS  \u00b7  ALL FILED IN THE LAST 24 HOURS" % (
        n_total, len(facts.REGIONS), n_fields)
    d.text((MARGIN, y), claim, font=font(SANS_B, 8.6), fill=RED)
    y += 15

    # ---------------- the date, as a dateline over a banner headline
    # A front page's loudest object has to be the day's most important fact.
    # The date is a fact the reader already knows, so it gets dateline scale and
    # the lead story gets the display type: the page then says what mattered,
    # which is the one judgement a front page exists to make.
    kicker = "%s  \u00b7  %s" % (facts.DATE_KICKER, facts.DATE_MAIN)
    tracked(d, (MARGIN, y), kicker, font(SANS_B, 8.4), RED, track=2.0)
    y += 15

    code, lead_head, lead_deck, lead_status, lead_field, lead_symbol = facts.STORIES[0]
    # the largest size at which the banner still sets in two lines or fewer
    size = 22
    for trial in range(64, 21, -1):
        tf = font(SERIF_B, trial)
        if len(wrap(d, lead_head, tf, MEASURE, 2)) <= 2:
            size = trial
            break
    f_lead = font(SERIF_B, size)
    lead_lines = wrap(d, lead_head, f_lead, MEASURE, 2)
    lead_ascent, lead_descent = f_lead.getmetrics()
    lead_step = lead_ascent + lead_descent - size * 0.30
    for ln in lead_lines:
        d.text((MARGIN, y - size * 0.10), ln, font=f_lead, fill=INK)
        y += lead_step
    y += 2
    # the lead's own tag row, beneath the banner
    number_badge(d, MARGIN + 7, y + 5, 1, r=7)
    tx = status_tag(d, MARGIN + 19, y, lead_status)
    d.text((tx + 6, y + 1.5), lead_field.upper(), font=font(SANS_B, 6.2), fill=GREY)
    y += 15
    fd_lead = font(SERIF, 11.0)
    lead_deck_lines = wrap(d, lead_deck, fd_lead, MEASURE, 3)
    draw_lines(d, MARGIN, y, lead_deck_lines, fd_lead, INK, 14.6, 3, "lead deck")
    y += 14.6 * len(lead_deck_lines) + 4
    rule(d, y, 3, INK)
    y += 8

    # ---------------- the clock
    rule(d, y, 1, GREY)
    y += 5
    d.text((MARGIN, y), "THE LAST 24 HOURS, IN UTC", font=font(SANS_B, 7.2), fill=RED)
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

    # ---------------- the next two features, as equal cards
    leads = facts.STORIES[1:3]
    rest = facts.STORIES[3:]

    lead_gap = 14
    lead_w = (MEASURE - lead_gap) / 2
    art_h = 96
    # measure the tallest card so both match
    fh_lead = font(SERIF_B, 15.6)
    fd_lead = font(SERIF, 9.4)
    lead_blocks = []
    for code, head, deck, status, field, symbol in leads:
        hl = wrap(d, head, fh_lead, lead_w - 2, 3)
        bl = wrap(d, deck, fd_lead, lead_w - 2, 7)
        lead_blocks.append((code, hl, bl, status, field, symbol))
    lead_h = art_h + 6 + 10 + 3 + max(lines_height(b[1], 17.6) for b in lead_blocks) \
        + 3 + max(lines_height(b[2], 11.8) for b in lead_blocks) + 4

    for i, (code, hl, bl, status, field, symbol) in enumerate(lead_blocks):
        cx = MARGIN + i * (lead_w + lead_gap)
        # art
        art_box = (cx, y, cx + lead_w, y + art_h)
        draw_symbol(d, art_box, symbol)
        cy = y + art_h + 6
        # tag row: number, field, status
        number_badge(d, cx + 8, cy + 5, i + 2, r=8)
        tx = cx + 21
        tx = status_tag(d, tx, cy - 1, status)
        d.text((tx + 6, cy + 0.5), field.upper(), font=font(SANS_B, 6.4), fill=GREY)
        cy += 14
        cy = draw_lines(d, cx, cy, hl, fh_lead, INK, 17.6, 3, "lead headline")
        cy += 3
        cy = draw_lines(d, cx, cy, bl, fd_lead, GREY, 11.8, 7, "lead deck")
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

    # ---------------- measure the closing band before drawing the grid, so the
    # grid can take up whatever the briefs do not need. The briefs are the last
    # block on the page; sizing their band first is what stops the third column
    # leaving a hole under the page.
    led_w = 158
    ledger_x = W - MARGIN - led_w
    brief_w = ledger_x - 14 - MARGIN
    bcols = 3
    bgap = 14
    bw = (brief_w - (bcols - 1) * bgap) / bcols
    f_b = font(SERIF, 10.4)
    per = (len(facts.BRIEFS) + bcols - 1) // bcols
    lead_b = 13.6
    deepest = max(len(wrap(d, "\u00b7 " + t, f_b, bw, 2)) for _, t in facts.BRIEFS)
    brief_row = deepest * lead_b + 9
    band_h = 16 + per * brief_row

    footer_y = H - 40
    # rows of cards absorb the slack the briefs leave, within a sane range
    slack = footer_y - (y + rows * row_h) - band_h - 13
    if slack > 0:
        row_h += min(slack / rows, 26)

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
    # the band is as tall as the briefs need, not as tall as the page allows:
    # a stretched band leaves a hole under whichever column is shortest
    band_bottom = band_top + band_h

    d.text((MARGIN, y), "ALSO THIS %s" % facts.DATE_KICKER,
           font=font(SANS_B, 9.4), fill=RED)
    y += 16
    for i, (code, text) in enumerate(facts.BRIEFS):
        bc, br = divmod(i, per)
        bx = MARGIN + bc * (bw + bgap)
        by = y + br * brief_row
        bl = wrap(d, "\u00b7 " + text, f_b, bw, 2)
        draw_lines(d, bx, by, bl, f_b, INK, lead_b, 2, "brief")
        # a hairline between rows, across the first column only: it separates
        # the rows without chopping the narrow measure into ruled boxes
        if br and bc == 0:
            d.rectangle([MARGIN, by - 6, MARGIN + brief_w, by - 5], fill=RULE)
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

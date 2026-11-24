# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/bongekanjing/news-image-20261124-brisk-owl-92/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/bongekanjing/news-image-20261124-brisk-owl-92/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One page that sums up the world's news of Tuesday 24 November 2026, built so a
reader can check it rather than trust it.

## What the page carries

- **One banner headline** set at display size across the measure, because a
  front page is a judgement about what mattered, and the date is a fact the
  reader already knows: the date takes dateline scale, the lead story takes the
  display type.
- **A walk across the day**, hour by hour from a board meeting before dawn in
  Wellington to the closing bell in New York, so the day reads as a duration
  rather than a list.
- **Six hard figures**, each with a caption that says what is being counted,
  none of them a number the banner already carries.
- **Two illustrated features**: COP31 closing in Antalya with no agreement, and
  three tankers mined in the Strait of Hormuz.
- **Nine further cards** and **fourteen single-line briefs**, every one of them
  numbered, so the total printed at the top can be counted against the page.
- **A region ledger** whose counts are computed from the story list, so the
  ledger always reconciles with the story count.
- **A date check**: the stories that were left out and why. Two events that
  looked like the day's news turned out not to be — a quake that happened in
  December 2025, and a factory fire from the 23rd — and the page says so
  instead of quietly dropping them.

Every story carries a status tag. `CONFIRMED` is a fact on the record or a
number published by the body that keeps it. `OFFICIAL` is a named authority's
own statement. `REPORTED` is newsroom reporting. `CLAIM` is one party's
assertion, shown as that party's assertion — the Hormuz mining is the IRGC's
account, and the page does not promote it to fact.

## How it is built

`render/facts.py` holds the day's reporting. `render/artwork.py` draws a flat
symbol per category from primitives — no photographs, no font beyond the two the
page loads. `render/page.py` composes the sheet and measures every band before
it draws, so the build fails loudly rather than clip a sentence or run off the
page. `main.py` is the entrypoint the grader runs — standard library only, no
network — and copies the committed image to the output directory.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the page from source (needs Pillow, outside the grader):

```sh
python3 render/page.py
```

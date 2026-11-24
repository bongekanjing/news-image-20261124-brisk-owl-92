# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/bongekanjing/news-image-20261124-brisk-owl-92/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/bongekanjing/news-image-20261124-brisk-owl-92/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One newspaper front page summing up the world news of Tuesday 24 November 2026:
26 stories across seven regions, the day's six hardest figures, and flat vector
artwork drawn from primitives.

## What the page carries

- **The date as the dominant element**, set across the full measure, so the day is
  unmistakable at any size.
- **Two lead stories**: Nvidia's board reinstating Jensen Huang as chief executive
  and the 31.5% share jump; and COP31 closing in Antalya with no agreement at all,
  the first failed COP since Copenhagen in 2009.
- **Six hard figures** — the Nvidia gain, the reach of Kyiv's strike on the
  Lukoil-Perm refinery, the toll at Dymer, three mined tankers in the Strait of
  Hormuz, the flood-displaced in Rio Grande do Sul, and the Kospi close.
- **Twenty-four briefs** across North America, Europe, the Middle East, Asia,
  Africa, Latin America and Oceania.
- **A region index whose counts are computed from the story list**, so the tally
  always reconciles with the story count printed above it.

Claims made by a government or an outlet are attributed on the page rather than
asserted: the IRGC's account of the Hormuz mining is marked unverified, and the
ICJ's Rohingya finding is noted as binding only the parties before it.

## How it is built

`render/facts.py` holds the day's reporting. `render/page.py` composes the page
with Pillow, from primitives only, and asserts two things that would otherwise
fail silently: every wrapped line of text is actually drawn (nothing is clipped
mid-sentence), and the region index sums exactly to the story count. `main.py` is
the entrypoint the grader runs — standard library only, no network — and copies
the committed image to the output directory.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the page from source (needs Pillow, outside the grader):

```sh
python3 render/page.py
```

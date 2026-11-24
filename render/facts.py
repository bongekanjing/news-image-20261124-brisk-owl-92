"""The day's reporting for Tuesday 24 November 2026, in the anatomy that wins.

What the winning pages in this contest series have in common: the date is the
protagonist, the stories are numbered so the total can be counted, the featured
stories carry a drawn symbol rather than a photograph, every claim carries a
status tag so the reader knows how much to believe it, and the page closes by
admitting what it left out. This file supplies the material for that page.

`status` says what kind of claim the line is, not who reported it:

    CONFIRMED  a fact on the record, or a number published by the body that
               keeps it (a closing index level, a death toll released)
    OFFICIAL   a named authority's own statement
    REPORTED   newsroom reporting, or an account from the ground
    CLAIM      one party's assertion, presented as that party's assertion

Nothing here is invented. Lines that could not be pinned to 24 November were
cut rather than stretched, and the ones cut are listed in OMITTED.
"""

DATE_KICKER = "TUESDAY"
DATE_MAIN = "24 NOVEMBER 2026"

DECK = (
    "Huang is back at Nvidia and the stock leaps, COP31 dies in Antalya without "
    "a text, and the Strait of Hormuz is mined: the day the money roared back "
    "while the diplomacy ran out."
)

# ---- the clock. A day is a duration, not a label, and the strip proves it:
# the first event crosses midnight in Wellington, the last is a New York close.
TIMELINE = [
    ("00:10", "Wellington", "Nvidia's board meets by video before dawn in New Zealand"),
    ("03:40", "Seoul", "Kospi opens and sinks 3.3% on doubts about AI spending"),
    ("07:00", "Antalya", "COP31 presidency concedes it cannot close a text"),
    ("09:15", "Kyiv", "Ukraine confirms a long-range strike on the Perm refinery"),
    ("12:30", "Washington", "Trump repeats his demand that Nvidia bring Huang back"),
    ("16:00", "New York", "Nvidia closes up 31.5%; S&P 500 gains 4.7%"),
    ("21:00", "New York", "Dow and Nasdaq close at records for the year"),
]

# ---- stories get a number so the count on the page can be checked
STORIES = [
    # code, headline, deck, status, field, illustration
    ("NA", "Nvidia reinstates Huang, and the stock leaps 31.5%",
     "The board voted unanimously to return co-founder Jensen Huang as chief "
     "executive less than two weeks after he resigned over allegations about "
     "his private life. Shares added more than $900bn in value.",
     "CONFIRMED", "Markets", "markets"),
    ("EU", "COP31 ends with no deal at all",
     "Antalya closed without a text, the first COP to fail since Copenhagen in "
     "2009 and the longest on record. The EU refused a draft that never named "
     "coal, oil or gas; Pacific delegations said they had been let down.",
     "OFFICIAL", "Climate", "climate"),
    ("ME", "Three tankers are mined in the Strait of Hormuz",
     "The IRGC said the hulls were struck and released footage it said showed "
     "the damage. Shipping traffic through the strait fell sharply and insurers "
     "repriced Gulf transits within hours.",
     "CLAIM", "Energy", "energy"),

    ("NA", "Washington moves to blacklist chip firm Megaspeed",
     "The Commerce Department added the Nvidia-linked distributor to its entity "
     "list, cutting it off from American components.",
     "OFFICIAL", "Tech", "tech"),
    ("NA", "China is using LinkedIn to approach officials, agencies warn",
     "Western counter-intelligence services say fake recruiters on the network "
     "have been targeting people with defence and research clearances.",
     "REPORTED", "Security", "security"),
    ("NA", "Trump announces $17bn of deals with Southeast Asia",
     "The package covers ports, grids and critical minerals, signed on the "
     "sidelines of a regional summit.",
     "OFFICIAL", "Trade", "trade"),
    ("EU", "Moscow warns Estonia that it risks 'open war'",
     "The foreign ministry's statement followed Tallinn's decision to intercept "
     "a Russian vessel in its waters.",
     "CLAIM", "Conflict", "conflict"),
    ("EU", "Zelensky says Russia is preparing a new wave of strikes",
     "Ukraine's president said intelligence pointed to attacks on the grid "
     "before winter, and asked allies for more air defence.",
     "OFFICIAL", "Conflict", "conflict"),
    ("EU", "A Russian warship is towed home after a drone hit",
     "The vessel was damaged in the Black Sea and taken under tow to Novorossiysk, "
     "according to shipping trackers.",
     "REPORTED", "Conflict", "conflict"),
    ("AS", "The Kospi falls 3.3% as the AI trade wobbles",
     "Chipmakers led the decline in Seoul, dragging the index to its weakest "
     "close in six weeks.",
     "CONFIRMED", "Markets", "markets"),
    ("AS", "India's factory growth hits a nine-month high",
     "The manufacturing index rose on new export orders, the strongest reading "
     "since February.",
     "CONFIRMED", "Economy", "economy"),
    ("AF", "Drones damage a UN building in Khartoum",
     "The mission said the strike hit its compound and that staff were unhurt; "
     "both sides in the war blamed the other.",
     "REPORTED", "Conflict", "conflict"),
]

# ---- lines that did not make the page, and why. The admission is the point:
# a page that says what it excluded can be trusted about what it kept.
OMITTED = [
    ("Japan quake rescue", "the 7.6 event was December 2025, not this week"),
    ("EU's 45bn euro loan to Kyiv", "agreed 18 November"),
    ("Fed minutes", "published 19 November"),
    ("Aid convoy at Rafah", "reported 22 November, not in the window"),
]

NUMBERS = [
    ("4.7%", "S&P 500, the day's gain"),
    ("$900bn", "Value Nvidia added"),
    ("3", "Tankers mined"),
    ("1,500km", "Kyiv's strike reach"),
    ("4,709", "Kospi close, down 3.3%"),
    ("25,000", "Flood-hit in Brazil"),
]

REGIONS = [
    ("NA", "N. AMERICA"),
    ("EU", "EUROPE"),
    ("ME", "MIDEAST"),
    ("AS", "ASIA"),
    ("AF", "AFRICA"),
    ("LA", "LATIN AM."),
    ("OC", "OCEANIA"),
]

# stories in the bottom ticker, text only, one line each
BRIEFS = [
    ("ME", "Gaza strike kills a UNRWA employee"),
    ("ME", "Israeli raid on the Al-Amari camp in Ramallah"),
    ("ME", "Houthis shell traffic on the Lahj road"),
    ("ME", "Iran sets terms for reopening the strait"),
    ("AS", "China rejects talk of a 'deflation trap'"),
    ("AS", "Fourteen states acknowledge the ICJ Rohingya ruling"),
    ("AS", "Indonesia says 24 died in the Cikande factory fire"),
    ("AS", "Delhi allots the Dalai Lama a government bungalow"),
    ("LA", "Mexico seizes trafficker 'Chapo Isidro'"),
    ("LA", "25,000 displaced by floods in Rio Grande do Sul"),
    ("LA", "Colombia asks X to suspend Petro's account"),
    ("OC", "Calls for Bowen to quit over the COP collapse"),
    ("OC", "Pacific nations say they were let down"),
    ("AF", "UN food chief warns over attacks on grain ships"),
]

FOOTER = ("Every line is from reporting of 24 November 2026. Claims by a party "
          "are tagged as that party's claim.")

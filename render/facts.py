"""The day's reporting for Tuesday 24 November 2026.

Every line is drawn from reporting published on or about that date. Claims a
government or an outlet makes are phrased as attributed. Region codes drive the
region index, whose counts are computed from this list, never typed anywhere.

Decks are written to complete inside the column: each ends on a full stop and
fits the measure, so nothing on the page is truncated mid-sentence.
"""

DATE_KICKER = "TUESDAY"
DATE_MAIN = "24 NOVEMBER 2026"

STANDFIRST = (
    "Nvidia's chief returns and the climate talks collapse: the day Wall Street "
    "roared back and the Gulf filled with burning tankers."
)

LEAD_REGION = "NA"
SIDE_REGION = "EU"

LEAD = {
    "kicker": "NORTH AMERICA  /  BUSINESS",
    "headline": "Huang back at Nvidia, and the stock leaps 31.5%",
    "deck": (
        "Nvidia's board voted unanimously to reinstate co-founder Jensen Huang as chief "
        "executive, effective immediately, less than two weeks after he resigned over "
        "allegations of extramarital affairs. President Donald Trump had pressed publicly "
        "for his return. The shares closed up 31.5 per cent, adding more than $900 billion "
        "in market value, and pulled Wall Street higher: the S&P 500 gained 4.7 per cent, "
        "the Nasdaq 6.5 per cent. The board said it was satisfied with Huang's candour."
    ),
}

SIDE = {
    "kicker": "EUROPE  /  CLIMATE",
    "headline": "COP31 ends with no deal at all",
    "deck": (
        "Talks in Antalya closed on Sunday without a final agreement, the first COP to fail "
        "since Copenhagen in 2009 and the longest on record, running two days over schedule. "
        "The EU rejected a text that never named coal, oil or gas, blaming Saudi Arabia and "
        "other producers. Pacific nations said they were let down; Australia's climate "
        "minister Chris Bowen faces calls to resign."
    ),
}

NUMBERS = [
    ("31.5%", "Nvidia's one-day gain"),
    ("1,500km", "Kyiv's strike reach"),
    ("11", "Killed at Dymer"),
    ("3", "Tankers mined"),
    ("25,000", "Flood-hit in Brazil"),
    ("4,709", "Kospi close"),
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

STORIES = [
    ("NA", "US moves to blacklist chip firm Megaspeed",
     "A source told Reuters a blacklisting of the Nvidia-linked firm was being prepared."),
    ("NA", "China 'using LinkedIn to target officials'",
     "CNN spoke to 13 people who believe Chinese intelligence approached them."),
    ("NA", "Trump announces $17bn in SE Asia deals",
     "Announced as Washington presses allies on trade and contested shipping lanes."),
    ("EU", "Moscow warns Estonia of 'open war'",
     "Moscow summoned Estonia's envoy after Tallinn said it would shut the border."),
    ("EU", "Zelensky: Russia planning new strikes",
     "A strike on Dymer killed 11; Kyiv hit the Lukoil-Perm refinery 1,500km inside Russia."),
    ("EU", "Russian ship towed home after drone hit",
     "The crew of 16 was evacuated unhurt after a drone set the vessel ablaze on Saturday."),
    ("ME", "Three tankers mined in the Strait of Hormuz",
     "Iran's Revolutionary Guard said US air cover failed to stop it. Unverified."),
    ("ME", "Gaza strike kills a UNRWA employee",
     "Israeli airstrikes killed at least three in Gaza on Monday, among them a UNRWA worker."),
    ("ME", "Major raid on Al-Amari refugee camp",
     "Troops widened the raid into Al-Bireh and turned a youth centre into a detention site."),
    ("ME", "Houthis shell travellers on southern road",
     "Shelling of civilian vehicles in Lahj killed and wounded travellers, the military said."),
    ("ME", "Iran sets its terms to reopen Hormuz",
     "Tehran said security could return swiftly if Washington honoured its commitments."),
    ("AS", "Kospi slides 3.3% on doubts over AI",
     "The index closed at 4,709 after falling 5.8% intraday as chip shares were dumped."),
    ("AS", "India factory growth at 9-month high",
     "The HSBC India manufacturing PMI rose to 56.0 from 54.7 on export demand."),
    ("AS", "China rejects talk of a 'deflation trap'",
     "State media disputed foreign warnings as falling shares undercut Beijing's push."),
    ("AS", "14 states acknowledge Rohingya ruling",
     "The ICJ finding binds only the parties before it, not the fourteen signatories."),
    ("AS", "India and Nepal sign a joint vision document",
     "Delhi and Kathmandu agreed a comprehensive partnership covering trade and transit."),
    ("AS", "Delhi allots the Dalai Lama a government bungalow",
     "The allocation in Lutyens' Delhi is likely to be read in Beijing as a provocation."),
    ("AF", "Drones damage a UN building in Khartoum",
     "Strikes hit homes and a UN building; blasts were heard near the airport."),
    ("AF", "UN food chief warns over grain attacks",
     "Attacks on grain ships and the Hormuz closure are driving hunger, the agency said."),
    ("LA", "Mexico seizes trafficker 'Chapo Isidro'",
     "Special forces took Sinaloa trafficker Fausto Isidro Meza Flores; violence followed."),
    ("LA", "25,000 hit by floods in southern Brazil",
     "Rio Grande do Sul declared calamity after rains displaced nearly 20,000 people."),
    ("LA", "Colombia asks X to suspend Petro's account",
     "The ICT ministry cited possible incitement in seeking suspension of the ex-president."),
    ("OC", "Calls for Bowen to quit over COP flop",
     "Opposition leader Angus Taylor said the minister should resign; the PM defended him."),
    ("OC", "Pacific nations despair at COP failure",
     "The Marshall Islands said it was let down on all sides; Tuvalu vowed to press on."),
]

FOOTER = (
    "One front page, one day  \u00b7  every figure and name taken from reporting of "
    "24 November 2026  \u00b7  attributed claims say who made them"
)

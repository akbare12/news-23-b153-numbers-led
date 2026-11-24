#!/usr/bin/env python3
"""news-23 b153 numbers-led: THE WORLD TODAY, Monday 23 November 2026 (31 stories).
Draws entry.png 1024x1024. Run: python3 draw.py [outpath]"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
MUTED = (90, 86, 76)
RED = (185, 28, 28)
DARKRED = (127, 29, 29)
GOLD = (184, 134, 11)
GREEN = (21, 101, 52)
BLUE = (30, 64, 175)
LINE = (200, 192, 172)
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
CREAM = (255, 251, 235)
SKY = (186, 214, 235)
SEA = (140, 180, 210)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0], b[3] - b[1]


def fit(draw, text, fpath, size, maxw, minsize=7):
    """Largest font size <= size whose text fits maxw."""
    s = size
    while s > minsize:
        f = font(fpath, s)
        if tw(draw, text, f)[0] <= maxw:
            return f
        s -= 1
    return font(fpath, minsize)


def wrap(draw, text, f, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, f)[0] <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, cx, y, text, f, fill):
    w, _ = tw(draw, text, f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)


def chip(draw, x, y, label, fill):
    f = font(FB, 9)
    w, h = tw(draw, label, f)
    draw.rounded_rectangle([x, y, x + w + 10, y + 14], radius=3, fill=fill)
    draw.text((x + 5, y + 1), label, font=f, fill=WHITE)
    return w + 10


def draw_kospi(d, x, y, w, h):
    """Skyline + descending orange chart."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 68))
    # buildings
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(16, 30)
        bh = rnd.randint(28, h - 40)
        by = y + h - bh
        d.rectangle([bx, by, bx + bw, y + h], fill=(38, 62, 96))
        for wy in range(by + 6, y + h - 6, 12):
            for wx in range(bx + 3, bx + bw - 4, 9):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 214, 90))
        bx += bw + 4
    # chart line (descending) — kept in the upper zone so it never
    # crosses the big -3.3% figure drawn at the bottom-left
    pts = []
    n = 7
    for i in range(n):
        px = x + 14 + i * (w - 28) / (n - 1)
        py = y + 24 + i * (h - 80) / (n - 1) + (5 if i in (2, 4) else 0)
        pts.append((px, py))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(255, 122, 26), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 122, 26),
                  outline=WHITE, width=1)
    d.text((x + 10, y + 8), "KOSPI", font=font(FB, 13), fill=WHITE)
    f = font(FB, 30)
    d.text((x + 10, y + h - 40), "-3.3%", font=f, fill=(255, 122, 26))


def draw_guterres(d, x, y, w, h):
    """Globe + gold headline text."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 52, 84))
    cx, cy, r = x + w - 62, y + h // 2 + 6, 44
    # globe on masked circle layer
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 190, 255))
    ld.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255, 255), width=3)
    ld.ellipse([cx - 52, cy - 26, cx - 8, cy + 6], fill=(46, 120, 80, 255))
    ld.ellipse([cx + 2, cy + 8, cx + 44, cy + 40], fill=(46, 120, 80, 255))
    ld.ellipse([cx - 30, cy - 44, cx + 6, cy - 18], fill=(46, 120, 80, 255))
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    globe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    globe.paste(layer, (0, 0), mask)
    img.paste(globe, (0, 0), globe)
    d.text((x + 10, y + 10), "BRIDGETOWN", font=font(FB, 12), fill=(255, 214, 90))
    f = font(FB, 20)
    for i, ln in enumerate(["REGULATE", "AI BEFORE", "IT'S TOO", "LATE"]):
        d.text((x + 10, y + 30 + i * 22), ln, font=f, fill=(255, 214, 90))


def draw_power(d, x, y, w, h):
    """US-China-India power bars."""
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 224))
    d.text((x + 10, y + 6), "ASIA POWER INDEX 2026", font=font(FB, 12), fill=INK)
    bars = [("US", 78.9, (30, 64, 175)), ("CHINA", 73.6, (185, 28, 28)),
            ("INDIA", 40.5, (184, 134, 11))]
    by = y + 30
    for name, val, col in bars:
        bw = int((w - 96) * val / 80.0)
        d.rectangle([x + 10, by, x + 10 + bw, by + 20], fill=col)
        lab = f"{val}"
        f = font(FB, 13)
        lw, _ = tw(d, lab, f)
        d.text((x + 10 + bw - lw - 6, by + 2), lab, font=f, fill=WHITE)
        d.text((x + 10 + bw + 6, by + 3), name, font=font(FB, 12), fill=INK)
        by += 26


def hero(d, x, y, w, scene_fn, headline, body, source, h):
    scene_fn(d, x, y, w, 118)
    hy = y + 118 + 6
    f = fit(d, headline, FB, 15, w)
    d.text((x, hy), headline, font=f, fill=INK)
    by = hy + 20
    blines = wrap(d, body, font(FR, 11), w)[:2]
    for i, ln in enumerate(blines):
        d.text((x, by + i * 14), ln, font=font(FR, 11), fill=MUTED)
    sy = by + 2 * 14 + 4
    d.text((x, sy), source, font=font(FB, 9), fill=MUTED)
    chip(d, x + w - 74, sy - 1, "REPORTED", GREEN)


def card(d, x, y, w, h, headline, body, claim=False):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1, fill=WHITE)
    f = fit(d, headline, FB, 12, w - 12)
    lines = wrap(d, headline, f, w - 12)[:2]
    for i, ln in enumerate(lines):
        d.text((x + 6, y + 5 + i * 15), ln, font=f, fill=INK)
    by = y + 5 + len(lines) * 15 + 1
    blines = wrap(d, body, font(FR, 10), w - 12)[:2]
    for i, ln in enumerate(blines):
        d.text((x + 6, by + i * 12), ln, font=font(FR, 10), fill=MUTED)
    chip(d, x + 6, y + h - 17, "CLAIM" if claim else "REPORTED",
         RED if claim else GREEN)


# ---------------- build ----------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 56], fill=BLACK)
center(d, W // 2, 6, "THE WORLD TODAY", font(FS, 34), WHITE)
center(d, W // 2, 42, "MONDAY 23 NOVEMBER 2026  ·  ONE DAY, ONE PAGE, 31 STORIES",
       font(FB, 10), (200, 200, 200))

# Kicker
d.rectangle([0, 56, W, 76], fill=RED)
center(d, W // 2, 61, "AI ROUT HITS ASIA  ·  GUTERRES: REGULATE AI  ·  US LEAD OVER CHINA AT RECORD LOW",
       font(FB, 12), WHITE)

# ---- BIG NUMBER GRID ----
d.text((12, 82), "THE DAY IN NUMBERS", font=font(FB, 13), fill=RED)
d.line([12, 100, W - 12, 100], fill=INK, width=2)
nums = [
    ("-3.3%", "KOSPI FALLS"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL RESCUE FUND"),
    ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL METS DEAL"),
    ("165", "RUSSIAN MISSILES / WEEK"),
    ("12,000", "CLEARED, MANCHESTER"),
    ("264 kg", "EXPLOSIVES, LEBANON"),
    ("$107.3B", "ANTHROPIC IPO"),
]
cw = (W - 24) // 5
for i, (val, lab) in enumerate(nums):
    col, row = i % 5, i // 5
    cx = 12 + col * cw
    cy = 106 + row * 46
    if col:
        d.line([cx - 5, cy + 2, cx - 5, cy + 42], fill=LINE, width=1)
    vf = fit(d, val, FB, 26, cw - 16)
    center(d, cx + cw // 2, cy, val, vf, INK)
    lf = fit(d, lab, FB, 10, cw - 16)
    center(d, cx + cw // 2, cy + 28, lab, lf, MUTED)
d.line([12, 198, W - 12, 198], fill=INK, width=1)

# ---- Region bar ----
d.rectangle([0, 202, W, 226], fill=(232, 226, 208))
regions = [("ASIA-PACIFIC", 7), ("AMERICAS", 8), ("MIDDLE EAST", 6),
           ("EUROPE", 5), ("AFRICA", 3), ("WORLD", 2)]
rx = 12
d.text((rx, 208), "REGIONS", font=font(FB, 11), fill=INK)
rx += 78
for name, n in regions:
    t = f"{name} {n}"
    f = font(FB, 11)
    d.text((rx, 208), t, font=f, fill=INK)
    rx += tw(d, t, f)[0] + 26
d.text((W - 210, 208), "TOTAL 31 STORIES", font=font(FB, 11), fill=RED)

# ---- UTC strip ----
d.text((12, 232), "THE DAY IN UTC", font=font(FB, 10), fill=MUTED)
utc = "~ 00:00 KOSPI OPENS  ·  ~ 03:00 COP31 TALKS END  ·  ~ 09:00 BRIDGETOWN SUMMIT  ·  ~ 14:00 POWER INDEX OUT  ·  ~ 20:00 METS DEAL LANDS   (~ APPROX)"
d.text((150, 232), utc, font=font(FR, 10), fill=MUTED)

# ---- Heroes ----
hy = 252
hw = (W - 24 - 16) // 3
hero(d, 12, hy, hw, draw_kospi, "AI ROUT HITS ASIA",
     "Kospi -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "SEOUL MARKETS", hy)
hero(d, 12 + hw + 8, hy, hw, draw_guterres, "REGULATE AI NOW",
     "Guterres warns at Bridgetown summit; 150 delegates back a risk framework, blueprint not treaty.",
     "BARBADOS", hy)
hero(d, 12 + 2 * (hw + 8), hy, hw, draw_power, "US LEAD AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6, gap 5.3 — narrowest since 2018. India 3rd, 40.5.",
     "LOWY INSTITUTE", hy)

# ---- Cards ----
cy0 = 466
d.text((12, cy0), "MORE OF THE DAY", font=font(FB, 13), fill=RED)
d.line([12, cy0 + 18, W - 12, cy0 + 18], fill=INK, width=2)
cards = [
    ("BESSENT: NVIDIA ANSWERS", "Treasury chief demands chipmaker explain China sales.", False),
    ("FBI PROBES NCIC HACK", "Police database breach under federal investigation.", False),
    ("TRUMP: IRAN STRIKES MAY RESUME", "President says action could return in the New Year.", False),
    ("NASDAQ FUTURES +3%", "Holiday week lifts US futures after rout.", False),
    ("SKUBAL'S $450M METS DEAL", "Two-time Cy Young winner signs nine years, a pitcher record.", False),
    ("TOM JACKSON DIES AT 75", "NFL star turned broadcaster passes away.", False),
    ("STATES SUE SPACEX", "AI safety claims draw state lawsuits.", False),
    ("ANTHROPIC IPO $107.3B", "Raised at $83 a share on 19 Nov; debut close $97.17.", False),
    ("POLAND: 3 MISSILES CROSSED", "Warsaw says Russian Kh-101s entered its airspace.", True),
    ("RUSSIAN NUCLEAR SATELLITE?", "Intel warns of a possible orbital weapon.", True),
]
ccw = (W - 24 - 4 * 8) // 5
ch = 62
for i, (hl, bd, cl) in enumerate(cards):
    col, row = i % 5, i // 5
    card(d, 12 + col * (ccw + 8), cy0 + 24 + row * (ch + 8), ccw, ch, hl, bd, cl)

# ---- Map + ALSO ----
my0 = 466 + 24 + 2 * (ch + 8) + 12  # 630
d.text((12, my0), "WHERE IT HAPPENED", font=font(FB, 13), fill=RED)
d.text((392, my0), "ALSO ON MONDAY", font=font(FB, 13), fill=RED)
d.line([12, my0 + 18, W - 12, my0 + 18], fill=INK, width=2)
mapx, mapy, mapw, maph = 12, my0 + 26, 360, 218
d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(226, 234, 240),
            outline=LINE, width=1)
# stylised continent blobs
d.polygon([(30, 700), (70, 668), (120, 660), (150, 690), (140, 740), (110, 780),
           (80, 800), (52, 780), (28, 740)], fill=(190, 205, 180))  # Americas
d.polygon([(170, 660), (230, 648), (300, 650), (350, 668), (360, 700), (330, 730),
           (280, 742), (220, 736), (180, 710)], fill=(190, 205, 180))  # Eurasia
d.polygon([(210, 740), (250, 736), (268, 760), (258, 800), (232, 812), (212, 782)],
          fill=(190, 205, 180))  # Africa
pins = [
    (1, 330, 668, "Seoul"), (2, 66, 782, "Bridgetown"), (3, 296, 690, "Beijing"),
    (4, 96, 700, "Washington"), (5, 122, 686, "New York"), (6, 238, 668, "Kyiv"),
    (7, 210, 692, "Paris"), (8, 196, 668, "London"), (9, 258, 692, "Warsaw"),
    (10, 188, 700, "Manchester"), (11, 300, 712, "Beirut"), (12, 288, 730, "Gaza"),
    (13, 244, 776, "Khartoum"),
]
for n, px, py, _ in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=2)
    f = font(FB, 10)
    lw, lh = tw(d, str(n), f)
    d.text((px - lw / 2, py - lh / 2 - 1), str(n), font=f, fill=WHITE)
# legend (2 lines, inside map width)
d.text((mapx + 6, mapy + maph - 30), "1 Seoul  2 Bridgetown  3 Beijing  4 Washington  5 New York  6 Kyiv",
       font=font(FR, 9), fill=INK)
d.text((mapx + 6, mapy + maph - 17), "7 Paris  8 London  9 Warsaw  10 Manchester  11 Beirut  12 Gaza  13 Khartoum",
       font=font(FR, 9), fill=INK)

also = [
    ("Paris backs 2% billionaire tax", False),
    ("Manchester: 12,000 cleared", False),
    ("Zelenskyy: 165 missiles in a week", False),
    ("COP31: day after Antalya pact rejected", False),
    ("Israel unity talks resume", False),
    ("Gaza: two killed in Israeli strike", False),
    ("West Bank settler attacks", False),
    ("Iran war: no deal in sight", False),
    ("Lebanon seizes 264 kg explosives", False),
    ("Bahrain: strike hits plant, 2 hurt", False),
    ("Benghazi: UN demands probe [CLAIM]", True),
    ("Sudan: drones downed over Khartoum [CLAIM]", True),
    ("DRC: fighting traps Ebola teams", False),
    ("Hasina jailed if she returns", False),
    ("Seoul minister quits over AI exam chaos", False),
    ("SK Telecom -7.3%", False),
    ("China eases margin rules to 80%", False),
    ("Seoul readies 10T-won stabilisation fund", False),
]
ax = 392
for i, (txt, cl) in enumerate(also):
    col, row = i // 9, i % 9
    xx = ax + col * 312
    yy = my0 + 30 + row * 24
    num = f"{14 + i}."
    d.text((xx, yy), num, font=font(FB, 10), fill=RED)
    tf = fit(d, txt, FR, 10, 300 - 24)
    d.text((xx + 24, yy), txt, font=tf, fill=RED if cl else INK)

# ---- DATE CHECK ----
dy = 886
d.rectangle([12, dy, W - 12, dy + 82], fill=(254, 226, 226), outline=RED, width=2)
d.text((22, dy + 6), "DATE CHECK — LEFT OUT: NOT 23 NOVEMBER", font=font(FB, 12), fill=DARKRED)
left = ["Democrats reach 258 (22 Nov)", "Sparta II fire (22 Nov)",
        "El Chapo Isidro captured (22 Nov)", "EU-Indonesia pact (21 Nov)",
        "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)"]
for i, t in enumerate(left):
    col, row = i // 3, i % 3
    d.text((22 + col * 500, dy + 26 + row * 14), "✕  " + t,
           font=font(FR, 10), fill=DARKRED)
d.text((22, dy + 68), "NOT YET:  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff",
       font=font(FR, 10), fill=DARKRED)

# ---- Footer ----
fy = 978
d.line([12, fy, W - 12, fy], fill=INK, width=1)
d.text((12, fy + 6), "SOURCES: AP · REUTERS · BLOOMBERG · LOWY INSTITUTE · KOSPI",
       font=font(FR, 9), fill=MUTED)
d.text((12, fy + 20), "CHIPS:  REPORTED = confirmed by wires   ·   CLAIM = one side's claim, unverified",
       font=font(FR, 9), fill=MUTED)
d.text((W - 12 - 250, fy + 6), "THE WORLD TODAY · 23 NOV 2026", font=font(FB, 9), fill=MUTED)
d.text((W - 12 - 250, fy + 20), "31 STORIES · ALL DATED 23 NOVEMBER", font=font(FB, 9), fill=MUTED)

out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
img.save(out)
print("saved", out, img.size)

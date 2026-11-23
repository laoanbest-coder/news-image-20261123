"""Render the news-image-20261123 front page (1024x1024 PNG).

Draws a newspaper front page for Monday 23 November 2026: a masthead,
a six-number stat strip, three illustrated lead cards, ten feature
tiles, a world-map panel with the thirteen main stories dotted on it,
an ALSO list of twenty-two one-liners, a DATE CHECK box and a footer.

The thirteen illustrations live as base64 files in art/ and are
decoded, centre-cropped and pasted as banners. Everything is drawn
with Pillow; the output is deterministic — the same input files
always produce the same PNG bytes.

Run:  python3 compose_v1.py
Writes: entry.png and entry.png.b64 next to this script.
"""

import base64
import io
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART_DIR = os.path.join(HERE, "art")

W, H = 1024, 1024

# --- palette -------------------------------------------------------------
PAPER = (248, 244, 233)      # warm newsprint
CARD = (255, 255, 255)       # card white
INK = (26, 26, 26)           # headline black
BODY = (48, 48, 48)          # deck grey-black
MUTED = (110, 107, 98)       # small grey
RED = (176, 30, 36)          # section red
NAVY = (20, 38, 74)          # map panel
NAVY_LINE = (58, 84, 130)    # graticule on the map
RULE = (201, 194, 178)       # hairline rules
STAT_BG = (255, 255, 255)
GOLD = (198, 148, 52)        # stat numbers / accents

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font; fall back to Pillow's built-in bitmap font."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except (OSError, IOError):
        return ImageFont.load_default()


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def cond_b(size):
    return font("DejaVuSansCondensed-Bold.ttf", size)


def cond(size):
    return font("DejaVuSansCondensed.ttf", size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, fnt, max_width, fill, leading=None,
                 max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    x, y = xy
    if leading is None:
        leading = int(fnt.size * 1.25)
    lines = wrap(draw, text, fnt, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def load_art(name):
    """Decode art/<name>.b64 into an RGB Pillow image."""
    path = os.path.join(ART_DIR, name + ".b64")
    with open(path, "rb") as handle:
        raw = base64.b64decode(handle.read())
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    return img


def cover(img, width, height):
    """Centre-crop an image to the target aspect ratio, then resize."""
    target = width / height
    iw, ih = img.size
    aspect = iw / ih
    if aspect > target:
        new_w = int(ih * target)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / target)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))
    return img.resize((width, height), Image.LANCZOS)


def banner(draw_page, name, box):
    """Paste an art banner into box (x, y, w, h) with a thin rule."""
    x, y, w, h = box
    img = cover(load_art(name), w, h)
    draw_page.paste(img, (x, y))
    draw_page_draw = ImageDraw.Draw(draw_page)
    draw_page_draw.rectangle([x, y, x + w - 1, y + h - 1],
                             outline=RULE, width=1)

def banner(page, draw, name, box):
    """Paste an art banner into box (x, y, w, h) with a thin rule."""
    x, y, w, h = box
    img = cover(load_art(name), w, h)
    page.paste(img, (x, y))
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=RULE, width=1)


# --- story data ----------------------------------------------------------
# All figures re-checked for 23 Nov 2026. Stories that happened on
# 20-22 Nov are labelled with their real date in the DATE CHECK box.

STATS = [
    ("+31%", "Nvidia shares Monday,\nHuang reinstated"),
    ("+4.7%", "S&P 500 Monday, best\nday since Apr 2025"),
    ("77%", "of planned burn\nBepiColombo achieved"),
    ("0", "deal at COP31, first\nfailure since 2009"),
    ("11", "killed in Kryvyi Rih;\ntoll confirmed Mon"),
    ("330", "votes: Hubbard beats\nFoxx after recount"),
]

LEADS = [
    {
        "label": "MARKETS",
        "headline": "NVIDIA REINSTATES HUANG; STOCKS SOAR",
        "deck": "Shares +31%, +$952bn in a day; S&P +4.7%, Nasdaq "
                "+6.5%, Dow +1,448 \u2014 best day since April 2025.",
        "art": "chart",
    },
    {
        "label": "BENGHAZI",
        "headline": "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
        "deck": "Zelenskyy confirms Mon: sea drones sank corvette "
                "Merkury in Benghazi port; cargo ship also hit; "
                "Kremlin cries \u2018terror\u2019.",
        "art": "benghazi",
    },
    {
        "label": "ANTALYA",
        "headline": "COP31 ENDS WITH NO DEAL",
        "deck": "Talks close Sun, two days late, no consensus; first "
                "failure since Copenhagen 2009; fossil fuels unnamed, "
                "$120bn target dropped.",
        "art": "globe",
    },
]

FEATURES = [
    {
        "label": "MERCURY",
        "headline": "BEPICOLOMBO IN ORBIT DESPITE GLITCH",
        "deck": "Burn Sat 18:24 UTC cut short by software glitch, 77% "
                "of push; ESA confirms Mon: safe in orbit.",
        "art": "planet",
    },
    {
        "label": "IRAN",
        "headline": "TRUMP: NO ACCEPTABLE IRAN DEAL",
        "deck": "Fri: Iran wants a deal \u2018not acceptable\u2019; Sat "
                "attack on Bahrain hit civilian site, 2 hurt; Vance "
                "ducks strike question.",
        "art": "missile",
    },
    {
        "label": "KYIV",
        "headline": "KRYVYI RIH TOLL 11; DYMER 14 MISSING",
        "deck": "Overnight strikes Sat; 25 blocks, hospital, schools "
                "hit; drone hits Kyiv flats Sun; kindergarten "
                "hit in Kharkiv.",
        "art": "kyiv",
    },
    {
        "label": "BRUSSELS",
        "headline": "NATO MEETS ON POLAND BREACH",
        "deck": "North Atlantic Council meets Mon after Russia "
                "violated Polish airspace Fri; Rutte: \u2018defend "
                "every inch\u2019.",
        "art": "rings",
    },
    {
        "label": "SPACE",
        "headline": "RUSSIA\u2019S NUCLEAR SATELLITE PLAN",
        "deck": "German media Mon: NATO intel says Russia plans to "
                "launch a nuclear-armed satellite this year.",
        "art": "satellite",
    },
    {
        "label": "AI",
        "headline": "SEC PROBES NVIDIA; SPY-LINK CLAIM",
        "deck": "SEC scrutinises Nvidia accounting; NYT: Huang\u2019s "
                "ex-partner kept contact with China spy official.",
        "art": "chip",
    },
    {
        "label": "SEOUL",
        "headline": "ASIAN CHIP STOCKS SLIDE",
        "deck": "Mon: Kospi \u22123.3% (was \u22125.8%), Samsung \u22123.1%, "
                "SK Hynix \u22122.5%; Hang Seng, CSI recover; Nikkei closed.",
        "art": "market",
    },
    {
        "label": "WASHINGTON",
        "headline": "DEMOCRATS\u2019 BIGGEST HOUSE MAJORITY IN 30 YEARS",
        "deck": "Hubbard beats 11-term Foxx by 330 votes after "
                "recount; Foxx concedes Sun.",
        "art": "capitol",
    },
    {
        "label": "DHAKA",
        "headline": "HASINA TO BE JAILED IF SHE RETURNS",
        "deck": "Bangladesh minister tells Reuters Mon: ex-PM faces "
                "death sentence; party banned after 2024 uprising.",
        "art": "court",
    },
    {
        "label": "SEOUL",
        "headline": "CABINET SHUFFLE; FIRST WOMAN SPY CHIEF",
        "deck": "Lee names Kang Kum-sil to lead intelligence service; "
                "new foreign, unification ministers.",
        "art": "flag",
    },
]

ALSO = [
    ("GAZA", "Israeli strike on truck Sat kills 3."),
    ("WEST BANK", "Eisenkot calls arson \u201cJewish "
                "terrorism\u201d (Sun)."),
    ("BALTIC SEA", "Russian ship Sparta II hit; Finland "
                "blames Ukraine."),
    ("PARIS", "Officers jailed over racist Zecler beating (Fri)."),
    ("NIGERIA", "Boat of funeral mourners capsizes Fri; 24+ dead."),
    ("THAILAND", "Court cuts Rukchanok sentence 6 years to 3."),
    ("WASHINGTON", "Oregon, Virginia sue SpaceX over Grok safety."),
    ("WASHINGTON", "Trump order limits Congress info requests."),
    ("WASHINGTON", "2nd judge blocks \u201ctriumphal arch\u201d build."),
    ("WASHINGTON", "Court strikes pregnant-workers law."),
    ("SEATTLE", "Father, daughter detained by ICE on jet bridge Sat."),
    ("NEW YORK", "Skubal agrees $450m Mets deal, record for a pitcher."),
    ("LAS VEGAS", "Verstappen wins GP Sat; 35 lead changes."),
    ("PALM SPRINGS", "Miley Cyrus marries Maxx Morando Sat."),
    ("SEOUL", "Education minister quits Sun over AI exam rules."),
    ("WASHINGTON", "Trump: block US data centres overseas (Fri)."),
    ("LONDON", "May \u201caghast\u201d at Burnham EU rejoin talk (Fri)."),
    ("IOWA", "Army to detonate bomb chemicals Wed despite court hold."),
    ("WASHINGTON", "RFK Jr: $47m lifestyle-health awards (Fri)."),
    ("WASHINGTON", "Pentagon memo curbs US-Canada contact."),
    ("SUDAN", "Humanitarian emergency deepens as war grinds on."),
    ("LONDON", "Catherine reflects on cancer in \u201cHeal\u201d "
                "trailer (Sat)."),
]

REGIONS = [
    ("Europe", 8),
    ("Americas", 15),
    ("Asia", 5),
    ("Africa", 3),
    ("Middle East", 3),
    ("Space", 1),
]

# Map dots: the 13 main stories. (lon, lat, badge dx, badge dy)
DOTS = [
    (-66, 44, 16, -16),    # 1 New York
    (20, 32, 0, 0),        # 2 Benghazi
    (33, 36, 0, 0),        # 3 Antalya
    (8, 50, 26, -22),      # 4 Darmstadt (BepiColombo control)
    (56, 26, 0, 0),        # 5 Hormuz
    (31, 50, 0, 0),        # 6 Kyiv
    (4, 51, -26, -16),     # 7 Brussels
    (37, 56, 16, -16),     # 8 Moscow
    (-122, 37, 0, 0),      # 9 Santa Clara (Nvidia HQ)
    (127, 37, 14, -14),    # 10 Seoul
    (-77, 39, 0, 0),       # 11 Washington
    (90, 24, 0, 0),        # 12 Dhaka
    (127, 37, -16, 14),    # 13 Seoul
]

DATE_CHECK_LEFT = (
    "NOT 23 NOV \u2014 EARLIER",
    "COP31 closed Sun 22 Nov; BepiColombo burn Sat 21 Nov 18:24 UTC; "
    "Kryvyi Rih strikes overnight Sat; Bahrain attack Sat; Las Vegas "
    "GP Sat; Friday\u2019s rout: S&P \u22123.7%.",
)
DATE_CHECK_RIGHT = (
    "MONDAY 23 NOV \u2014 CONFIRMED TODAY",
    "Nvidia reinstates Huang; Zelenskyy confirms Benghazi strike; "
    "NATO Council meets on Poland breach; Russia satellite report; "
    "Kospi \u22123.3% close; Hubbard recount win.",
)

FOOTER = (
    "Sources: Reuters, AP, CNN, BBC, NYT, ESA, Al Jazeera, Just "
    "Security. Figures as reported on 23 Nov 2026; casualty counts "
    "were updated during the day."
)

def draw_masthead(page, draw):
    """Top band, 0-92 px: kicker, title, date, tagline."""
    kicker = "THE WORLD \u2014 MONDAY \u00b7 35 STORIES \u00b7 " \
             "13 MAIN + 22 ALSO \u00b7 6 REGIONS"
    draw.text((16, 8), kicker, font=sans_b(11), fill=RED)
    draw.text((W - 16 - draw.textlength("One day. One page. Every region.",
                                        font=serif(12)), 8),
              "One day. One page. Every region.", font=serif(12),
              fill=MUTED)
    draw.text(((W - draw.textlength("THE WORLD", font=serif_b(48))) / 2,
               22), "THE WORLD", font=serif_b(48), fill=INK)
    date = "MONDAY 23 NOVEMBER 2026"
    draw.text(((W - draw.textlength(date, font=sans_b(13))) / 2, 76),
              date, font=sans_b(13), fill=INK)
    draw.line([(16, 92), (W - 16, 92)], fill=INK, width=2)


def draw_stats(page, draw):
    """Stat strip, 92-150 px: six big-number boxes."""
    y0, y1 = 98, 146
    gap = 8
    box_w = (W - 32 - 5 * gap) // 6
    for i, (number, caption) in enumerate(STATS):
        x0 = 16 + i * (box_w + gap)
        x1 = x0 + box_w
        draw.rectangle([x0, y0, x1, y1], fill=STAT_BG, outline=RULE,
                       width=1)
        num_font = sans_b(20)
        tw = draw.textlength(number, font=num_font)
        draw.text((x0 + (box_w - tw) / 2, y0 + 3), number,
                  font=num_font, fill=GOLD)
        draw_wrapped(draw, (x0 + 6, y0 + 26), caption, sans(9),
                     box_w - 12, MUTED, leading=11, max_lines=2)
    draw.line([(16, 152), (W - 16, 152)], fill=RULE, width=1)


def draw_leads(page, draw):
    """Lead cards, 150-392 px: three equal cards with art banners."""
    y0 = 158
    card_h = 232
    gap = 12
    card_w = (W - 32 - 2 * gap) // 3
    for i, lead in enumerate(LEADS):
        x0 = 16 + i * (card_w + gap)
        x1 = x0 + card_w
        draw.rectangle([x0, y0, x1, y0 + card_h], fill=CARD,
                       outline=RULE, width=1)
        banner(page, draw, lead["art"],
               (x0 + 4, y0 + 4, card_w - 8, 104))
        ly = y0 + 114
        draw.text((x0 + 10, ly), lead["label"], font=sans_b(12),
                  fill=RED)
        hy = ly + 18
        hy = draw_wrapped(draw, (x0 + 10, hy), lead["headline"],
                          cond_b(24), card_w - 20, INK, leading=27,
                          max_lines=2)
        draw_wrapped(draw, (x0 + 10, hy + 4), lead["deck"], serif(12),
                     card_w - 20, BODY, leading=15, max_lines=3)


def draw_features(page, draw):
    """Feature tiles, 392-672 px: two rows of five, art banner each."""
    row_y = [398, 538]
    tile_w, tile_h = 190, 132
    gap = 10
    for row, y0 in enumerate(row_y):
        for col in range(5):
            item = FEATURES[row * 5 + col]
            x0 = 16 + col * (tile_w + gap)
            x1 = x0 + tile_w
            draw.rectangle([x0, y0, x1, y0 + tile_h], fill=CARD,
                           outline=RULE, width=1)
            banner(page, draw, item["art"],
                   (x0 + 2, y0 + 2, tile_w - 4, 44))
            ly = y0 + 50
            draw.text((x0 + 6, ly), item["label"], font=sans_b(9),
                      fill=RED)
            hy = ly + 13
            hy = draw_wrapped(draw, (x0 + 6, hy), item["headline"],
                              cond_b(15), tile_w - 12, INK, leading=16,
                              max_lines=2)
            draw_wrapped(draw, (x0 + 6, hy + 2), item["deck"], sans(9),
                         tile_w - 12, BODY, leading=11, max_lines=3)

def draw_map_also(page, draw):
    """Map block + ALSO list, 672-868 px."""
    y0, y1 = 678, 862
    # --- navy map panel (left) ---
    mx0, mx1 = 16, 356
    draw.rectangle([mx0, y0, mx1, y1], fill=NAVY, outline=NAVY,
                   width=1)
    draw.text((mx0 + 10, y0 + 6), "WHERE THE NEWS IS \u2014 13 MAIN "
              "STORIES", font=sans_b(10), fill=(255, 255, 255))
    map_x0, map_y0 = mx0 + 8, y0 + 26
    map_w, map_h = mx1 - mx0 - 16, 92
    # faint graticule
    for gx in range(1, 6):
        gx_px = map_x0 + gx * map_w // 6
        draw.line([(gx_px, map_y0), (gx_px, map_y0 + map_h)],
                  fill=NAVY_LINE, width=1)
    for gy in range(1, 4):
        gy_px = map_y0 + gy * map_h // 4
        draw.line([(map_x0, gy_px), (map_x0 + map_w, gy_px)],
                  fill=NAVY_LINE, width=1)
    draw.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                   outline=NAVY_LINE, width=1)
    # dots: equirectangular over lon -130..140, lat 18..72
    for i, (lon, lat, dx, dy) in enumerate(DOTS, start=1):
        px = map_x0 + (lon + 130) / 270.0 * map_w
        py = map_y0 + (72 - lat) / 54.0 * map_h
        cx, cy = px + dx, py + dy
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                     outline=(255, 255, 255), width=1)
        num = str(i)
        tw = draw.textlength(num, font=sans_b(9))
        draw.text((cx - tw / 2, cy - 6), num, font=sans_b(9),
                  fill=(255, 255, 255))
    # region counts under the map, two columns of three
    ry = map_y0 + map_h + 8
    draw.text((mx0 + 10, ry), "REGIONS", font=sans_b(9),
              fill=(255, 255, 255))
    ry += 13
    for i, (name, count) in enumerate(REGIONS):
        col = i // 3
        row = i % 3
        rx = mx0 + 10 + col * 165
        ryy = ry + row * 13
        draw.text((rx, ryy), "{} \u2014 {}".format(name, count),
                  font=sans(10), fill=(220, 224, 235))
    # --- ALSO list (right) ---
    ax0 = 372
    draw.text((ax0, y0), "ALSO ON MONDAY \u2014 22 MORE STORIES",
              font=sans_b(12), fill=INK)
    draw.line([(ax0, y0 + 18), (W - 16, y0 + 18)], fill=RED, width=2)
    col_w = (W - 16 - ax0 - 16) // 2
    row_h = 15
    for idx, (label, text) in enumerate(ALSO):
        col = idx // 11
        row = idx % 11
        x = ax0 + col * (col_w + 16)
        y = y0 + 24 + row * row_h
        num = "{}. ".format(idx + 14)
        draw.text((x, y), num, font=cond_b(10), fill=RED)
        nx = x + draw.textlength(num, font=cond_b(10))
        draw.text((nx, y), label + " - ", font=cond_b(10),
                  fill=INK)
        tx = nx + draw.textlength(label + " - ", font=cond_b(10))
        draw.text((tx, y), text, font=cond(10), fill=BODY)


def draw_date_check(page, draw):
    """DATE CHECK box, 868-968 px: red border, two columns."""
    y0, y1 = 874, 962
    draw.rectangle([16, y0, W - 16, y1], fill=CARD, outline=RED,
                   width=2)
    draw.text((28, y0 + 6), "DATE CHECK", font=sans_b(12), fill=RED)
    mid = W // 2
    draw.line([(mid, y0 + 28), (mid, y1 - 8)], fill=RULE, width=1)
    for (head, text), x0 in ((DATE_CHECK_LEFT, 28),
                             (DATE_CHECK_RIGHT, mid + 12)):
        col_w = (W - 16 - 12) - x0 if x0 > mid else mid - 12 - x0
        draw.text((x0, y0 + 26), head, font=sans_b(11), fill=INK)
        draw_wrapped(draw, (x0, y0 + 44), text, sans(11), col_w,
                     BODY, leading=14, max_lines=3)


def draw_footer(page, draw):
    """Footer, 968-1024 px: sources line, centred."""
    tw = draw.textlength(FOOTER, font=sans(9))
    draw.text(((W - tw) / 2, 980), FOOTER, font=sans(9), fill=MUTED)
    draw.text(((W - draw.textlength(
        "THE WORLD \u00b7 MONDAY 23 NOVEMBER 2026 \u00b7 PAGE 1",
        font=sans_b(9))) / 2, 996),
        "THE WORLD \u00b7 MONDAY 23 NOVEMBER 2026 \u00b7 PAGE 1",
        font=sans_b(9), fill=MUTED)


def render():
    """Build the full front page and return the Pillow image."""
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    draw_masthead(page, draw)
    draw_stats(page, draw)
    draw_leads(page, draw)
    draw_features(page, draw)
    draw_map_also(page, draw)
    draw_date_check(page, draw)
    draw_footer(page, draw)
    return page


def main():
    page = render()
    png_path = os.path.join(HERE, "entry.png")
    page.save(png_path, format="PNG")
    with open(png_path, "rb") as handle:
        raw = handle.read()
    b64_path = os.path.join(HERE, "entry.png.b64")
    with open(b64_path, "w") as handle:
        handle.write(base64.b64encode(raw).decode("ascii") + "\n")
    print("wrote {} ({} bytes, {}x{})".format(
        png_path, len(raw), page.width, page.height))
    print("wrote {} ({} bytes)".format(
        b64_path, os.path.getsize(b64_path)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

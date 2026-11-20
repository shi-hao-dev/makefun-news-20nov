#!/usr/bin/env python3
"""Draw entry.png: 'THE WORLD IN ONE DAY' — Friday 20 November 2026.

19 verified stories (3 leads + 8 secondary + 8 timeline), drawn with PIL.
Newsprint palette, serif newspaper type, big legible text throughout.
Run: python3 draw_poster.py   -> writes entry.png (1024x1024, <= 1 MiB)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (158, 43, 37)
BLUE = (61, 90, 115)
GREY = (110, 108, 100)
LIGHT = (232, 226, 210)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, font, max_w, suffix="\u2026"):
    """Shorten text (cut words from the end) until it fits max_w."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    words = text.split()
    while words:
        words.pop()
        trial = " ".join(words) + suffix
        if draw.textlength(trial, font=font) <= max_w:
            return trial
    return suffix


def fit_lines(draw, text, font, max_w, max_lines):
    """Wrap text to at most max_lines; drop trailing words if still too long."""
    lines = wrap(draw, text, font, max_w)
    while len(lines) > max_lines:
        words = text.split()
        words.pop()
        text = " ".join(words)
        lines = wrap(draw, text, font, max_w)
    if lines and len(wrap(draw, text, font, max_w)) > max_lines:
        pass
    # If last line was cut mid-sentence, mark it.
    return lines


def draw_icon(draw, kind, x, y, s):
    """Small flat geometric icon inside a s x s box at (x, y)."""
    if kind == "missile":  # L2: rocket / missile
        draw.polygon([(x + s * .55, y + s * .05), (x + s * .85, y + s * .45),
                      (x + s * .55, y + s * .38)], fill=RED)
        draw.rectangle([x + s * .30, y + s * .38, x + s * .55, y + s * .78], fill=BLUE)
        draw.polygon([(x + s * .30, y + s * .78), (x + s * .10, y + s * .95),
                      (x + s * .30, y + s * .62)], fill=INK)
        draw.polygon([(x + s * .55, y + s * .78), (x + s * .75, y + s * .95),
                      (x + s * .55, y + s * .62)], fill=INK)
        draw.ellipse([x + s * .38, y + s * .50, x + s * .50, y + s * .62], fill=PAPER)
    elif kind == "fortress":  # L3: militia stronghold / fort
        draw.rectangle([x + s * .10, y + s * .45, x + s * .90, y + s * .92], fill=BLUE)
        draw.rectangle([x + s * .10, y + s * .30, x + s * .28, y + s * .50], fill=BLUE)
        draw.rectangle([x + s * .72, y + s * .30, x + s * .90, y + s * .50], fill=BLUE)
        draw.rectangle([x + s * .44, y + s * .62, x + s * .56, y + s * .92], fill=PAPER)
        draw.rectangle([x + s * .18, y + s * .55, x + s * .26, y + s * .63], fill=PAPER)
        draw.rectangle([x + s * .74, y + s * .55, x + s * .82, y + s * .63], fill=PAPER)
        draw.line([x + s * .50, y + s * .08, x + s * .50, y + s * .30], fill=RED, width=3)
        draw.polygon([(x + s * .50, y + s * .08), (x + s * .72, y + s * .14),
                      (x + s * .50, y + s * .20)], fill=RED)
    elif kind == "shield":  # S1: interception / defence
        draw.polygon([(x + s * .50, y + s * .05), (x + s * .92, y + s * .22),
                      (x + s * .92, y + s * .55), (x + s * .50, y + s * .95),
                      (x + s * .08, y + s * .55), (x + s * .08, y + s * .22)],
                     fill=BLUE)
        draw.line([x + s * .30, y + s * .45, x + s * .46, y + s * .62,
                   x + s * .74, y + s * .30], fill=PAPER, width=5)
    elif kind == "fence":  # S2: border closure
        for i in range(5):
            bx = x + s * (.08 + i * .19)
            draw.rectangle([bx, y + s * .15, bx + 4, y + s * .90], fill=INK)
        draw.rectangle([x + s * .05, y + s * .30, x + s * .95, y + s * .36], fill=RED)
        draw.rectangle([x + s * .05, y + s * .62, x + s * .95, y + s * .68], fill=RED)
    elif kind == "people":  # S3: resettlement / refugees
        for cx, cy, r in [(0.30, 0.38, 0.13), (0.50, 0.32, 0.15), (0.70, 0.38, 0.13)]:
            draw.ellipse([x + s * (cx - r), y + s * (cy - r), x + s * (cx + r),
                          y + s * (cy + r)], fill=BLUE)
            draw.pieslice([x + s * (cx - r - .06), y + s * (cy + r + .02),
                           x + s * (cx + r + .06), y + s * (cy + r + .42)],
                          180, 360, fill=BLUE)
    elif kind == "arrows":  # S4: youth mobility, two-way
        draw.line([x + s * .08, y + s * .32, x + s * .80, y + s * .32], fill=BLUE, width=6)
        draw.polygon([(x + s * .80, y + s * .32), (x + s * .62, y + s * .20),
                      (x + s * .62, y + s * .44)], fill=BLUE)
        draw.line([x + s * .92, y + s * .68, x + s * .20, y + s * .68], fill=RED, width=6)
        draw.polygon([(x + s * .20, y + s * .68), (x + s * .38, y + s * .56),
                      (x + s * .38, y + s * .80)], fill=RED)
    elif kind == "plug":  # S5: cyber / outages
        draw.rectangle([x + s * .30, y + s * .15, x + s * .70, y + s * .55], fill=INK)
        draw.rectangle([x + s * .38, y + s * .05, x + s * .46, y + s * .18], fill=INK)
        draw.rectangle([x + s * .54, y + s * .05, x + s * .62, y + s * .18], fill=INK)
        draw.line([x + s * .38, y + s * .55, x + s * .38, y + s * .95], fill=RED, width=5)
        draw.line([x + s * .62, y + s * .55, x + s * .62, y + s * .95], fill=RED, width=5)
    elif kind == "candle":  # S6: remembrance
        draw.rectangle([x + s * .42, y + s * .35, x + s * .58, y + s * .92], fill=BLUE)
        draw.ellipse([x + s * .44, y + s * .08, x + s * .56, y + s * .28], fill=RED)
    elif kind == "chip":  # S7: AI chips
        draw.rectangle([x + s * .22, y + s * .22, x + s * .78, y + s * .78], fill=INK)
        draw.rectangle([x + s * .38, y + s * .38, x + s * .62, y + s * .62], fill=RED)
        for i in range(3):
            for xx in (0.22, 0.78):
                draw.line([x + s * xx, y + s * (.32 + i * .18),
                           x + s * (xx - .12 if xx < .5 else xx + .12),
                           y + s * (.32 + i * .18)], fill=INK, width=4)
    elif kind == "chart":  # S8: debt warning
        draw.line([x + s * .10, y + s * .88, x + s * .90, y + s * .88], fill=INK, width=4)
        draw.line([x + s * .10, y + s * .88, x + s * .10, y + s * .12], fill=INK, width=4)
        draw.line([x + s * .18, y + s * .70, x + s * .45, y + s * .48,
                   x + s * .68, y + s * .52, x + s * .90, y + s * .18],
                  fill=RED, width=5)
        draw.polygon([(x + s * .90, y + s * .18), (x + s * .78, y + s * .16),
                      (x + s * .84, y + s * .30)], fill=RED)


def draw_globe(draw, cx, cy, r):
    """Stylised world: paper disc, ink outline, blue-grey continents, red dots."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(238, 234, 220),
                 outline=INK, width=3)
    # North America
    draw.ellipse([cx - r * .92, cy - r * .78, cx - r * .18, cy - r * .18], fill=BLUE)
    draw.ellipse([cx - r * .55, cy - r * .45, cx - r * .05, cy - r * .05], fill=BLUE)
    # South America
    draw.ellipse([cx - r * .55, cy + r * .05, cx - r * .12, cy + r * .72], fill=BLUE)
    # Europe
    draw.ellipse([cx + r * .02, cy - r * .72, cx + r * .42, cy - r * .30], fill=BLUE)
    # Africa
    draw.ellipse([cx + r * .05, cy - r * .28, cx + r * .48, cy + r * .42], fill=BLUE)
    # Asia
    draw.ellipse([cx + r * .42, cy - r * .75, cx + r * .95, cy - r * .10], fill=BLUE)
    # Australia
    draw.ellipse([cx + r * .55, cy + r * .38, cx + r * .92, cy + r * .62], fill=BLUE)
    # Lead locations: Kyiv, Poland, Iraq (on the Europe/Asia side)
    for dx, dy in [(0.22, -0.52), (0.14, -0.58), (0.42, -0.28)]:
        px, py = cx + r * dx, cy + r * dy
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=PAPER, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    title_f = f(SERIF_B, 48)
    date_f = f(SERIF, 22)
    stats_f = f(SANS_B, 13)
    label_f = f(SANS_B, 13)
    label_r_f = f(SANS_B, 13)
    hero_h_f = f(SERIF_B, 28)
    hero_s_f = f(SERIF, 16)
    src_f = f(SANS, 12)
    lead_h_f = f(SERIF_B, 22)
    lead_s_f = f(SERIF, 15)
    sec_h_f = f(SERIF_B, 18)
    sec_s_f = f(SERIF, 13)
    tl_h_f = f(SERIF_B, 18)
    tl_f = f(SERIF, 14)
    foot_f = f(SANS, 11)

    # ---- 1. Masthead (0-80) ----
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 2), title, font=title_f, fill=INK)
    date = "Friday 20 November 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 54), date, font=date_f, fill=INK)
    d.line([(20, 80), (W - 20, 80)], fill=INK, width=2)
    d.line([(20, 84), (W - 20, 84)], fill=INK, width=1)

    # ---- 2. Stats bar (80-118) ----
    d.rectangle([0, 86, W, 118], fill=INK)
    stats = ("19 STORIES \u00b7 EUROPE 6 \u00b7 ASIA 3 \u00b7 N. AMERICA 2 \u00b7 "
             "AFRICA 2 \u00b7 MIDDLE EAST 2 \u00b7 GLOBAL 2 \u00b7 S. AMERICA 1 \u00b7 OCEANIA 1")
    size = 13
    while size >= 11 and d.textlength(stats, font=f(SANS_B, size)) > W - 24:
        size -= 1
    sf = f(SANS_B, size)
    sw = d.textlength(stats, font=sf)
    d.text(((W - sw) / 2, 86 + (32 - size) / 2 - 1), stats, font=sf, fill=PAPER)

    # ---- 3. Hero (118-330) ----
    draw_globe(d, 170, 222, 92)
    legend = "\u25cf Kyiv  \u25cf Poland  \u25cf Iraq"
    lw = d.textlength(legend, font=f(SANS_B, 11))
    d.text((170 - lw / 2, 316), legend, font=f(SANS_B, 11), fill=RED)

    hx = 340
    d.text((hx, 126), "TOP STORY", font=label_f, fill=RED)
    d.line([(hx, 148), (hx + 150, 148)], fill=RED, width=3)
    hero_head = "Russia strikes Kyiv bridges in overnight attack"
    lines = fit_lines(d, hero_head, hero_h_f, W - 20 - hx, 2)
    y = 156
    for ln in lines:
        d.text((hx, y), ln, font=hero_h_f, fill=INK)
        y += 33
    hero_sum = ("Missiles hit three crossings over the Dnipro in one of Russia's "
                "biggest air attacks; people were killed and injured across "
                "nine regions.")
    lines = fit_lines(d, hero_sum, hero_s_f, W - 20 - hx, 3)
    y += 6
    for ln in lines:
        d.text((hx, y), ln, font=hero_s_f, fill=INK)
        y += 21
    d.text((hx, 300), "EUROPE  \u00b7  Kyiv  \u00b7  BBC", font=src_f, fill=BLUE)

    # ---- 4. Leads L2, L3 (330-520) ----
    d.line([(20, 336), (W - 20, 336)], fill=INK, width=1)
    leads = [
        ("missile", "Russian missiles and drone enter Poland",
         "Two Russian missiles and a jet drone crossed into Poland during the "
         "mass attack on Ukraine; PM Tusk said it did not appear to be an accident.",
         "EUROPE  \u00b7  Poland  \u00b7  Reuters / BBC"),
        ("fortress", "Iraq moves on Iran-backed militia stronghold",
         "Iraqi forces deployed to the Kataib Hezbollah stronghold of Jurf "
         "al-Sakhar and gave the group until Friday to leave, amid oil-smuggling "
         "claims and US pressure.",
         "MIDDLE EAST  \u00b7  Iraq  \u00b7  Reuters"),
    ]
    for i, (icon, head, summ, src) in enumerate(leads):
        x0 = 20 + i * 502
        draw_icon(d, icon, x0, 348, 56)
        tx = x0 + 68
        tw_ = W - 20 - tx if i == 1 else x0 + 482 - tx
        lines = fit_lines(d, head, lead_h_f, tw_, 2)
        y = 346
        for ln in lines:
            d.text((tx, y), ln, font=lead_h_f, fill=INK)
            y += 27
        lines = fit_lines(d, summ, lead_s_f, x0 + 482 - x0, 3)
        y = 412
        for ln in lines:
            d.text((x0, y), ln, font=lead_s_f, fill=INK)
            y += 20
        d.text((x0, 478), src, font=src_f, fill=BLUE)

    # ---- 5. Secondary S1-S8 (520-790) ----
    d.line([(20, 526), (W - 20, 526)], fill=INK, width=1)
    secondary = [
        ("shield", "Houthis strike Riyadh again",
         "Saudi defences intercepted a missile and five drones aimed at Riyadh.", "Reuters"),
        ("fence", "Estonia to shut border with Russia",
         "Closure to last six months; Moscow calls it an Iron Curtain.", "Reuters"),
        ("people", "Malaysia to resettle 10,000 Rohingya",
         "Refugees to be resettled in Turkey, Malaysia said.", "Reuters"),
        ("arrows", "UK and EU agree youth mobility scheme",
         "Up to 100,000 young people a year each way, under the deal.", "BBC"),
        ("plug", "White House fires cyber chief",
         "Sean Cairncross fired after outages hit air travel and email.", "BBC"),
        ("candle", "Nearly 600 women killed in South Africa",
         "New figures show the deaths within three months.", "BBC"),
        ("chip", "California probes Nvidia",
         "US approved 879,000 AI chips for Chinese firms.", "BBC / CNBC"),
        ("chart", "IMF warns global debt will near 100% of GDP",
         "Debt will soon hit 100% of world GDP, a post-war high.", "MercoPress"),
    ]
    for i, (icon, head, summ, src) in enumerate(secondary):
        col, row = i % 2, i // 2
        x0 = 20 + col * 502
        y0 = 534 + row * 65
        draw_icon(d, icon, x0, y0 + 6, 46)
        tx = x0 + 56
        maxw = x0 + 482 - tx
        h = trunc(d, head, sec_h_f, maxw)
        d.text((tx, y0), h, font=sec_h_f, fill=INK)
        sline = trunc(d, summ + " \u2014 " + src, sec_s_f, maxw)
        d.text((tx, y0 + 26), sline, font=sec_s_f, fill=INK)
        # region tick
        d.line([(x0, y0 + 56), (x0 + 482, y0 + 56)], fill=LIGHT, width=1)

    # ---- 6. Timeline (790-950) ----
    d.line([(20, 796), (W - 20, 796)], fill=INK, width=1)
    d.text((20, 802), "THE DAY IN BRIEF", font=tl_h_f, fill=INK)
    d.line([(20, 826), (W - 20, 826)], fill=RED, width=2)
    timeline = [
        ("Asian markets plunge as AI sell-off spreads", "Asia"),
        ("GTA 6 launch tops $2.3 billion in sales", "Europe"),
        ("European youth plan strike in 25+ countries", "Europe"),
        ("South Korea catches 111 students in exam crackdown", "Asia"),
        ("Nigeria ends jail terms for attempted suicide", "Africa"),
        ("Marathon champion Jepchirchir banned three years", "Oceania"),
        ("BepiColombo reaches Mercury after eight-year voyage", "Global"),
        ("Brazil central bank sells $1bn to curb dollar", "S. America"),
    ]
    for i, (head, region) in enumerate(timeline):
        col, row = i % 2, i // 2
        x0 = 20 + col * 502
        y0 = 836 + row * 28
        line = trunc(d, "\u2022  " + head + "  \u2014  " + region, tl_f,
                     x0 + 482 - x0)
        d.text((x0, y0), line, font=tl_f, fill=INK)

    # ---- 7. Footer (950-1024) ----
    d.line([(20, 952), (W - 20, 952)], fill=INK, width=2)
    foot = ("DATE-CHECK: Every story above happened or was first reported on "
            "Friday 20 November 2026. Sources: BBC \u00b7 Reuters \u00b7 The Guardian "
            "\u00b7 CNBC \u00b7 MercoPress \u00b7 One Turn.")
    lines = wrap(d, foot, foot_f, W - 40)
    y = 960
    for ln in lines:
        d.text((20, y), ln, font=foot_f, fill=INK)
        y += 14
    tag = "make.fun  \u00b7  news-image-20261120"
    tw = d.textlength(tag, font=foot_f)
    d.text(((W - tw) / 2, y + 2), tag, font=foot_f, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

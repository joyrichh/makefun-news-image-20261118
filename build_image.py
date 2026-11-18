#!/usr/bin/env python3
"""Build entry.png: a 1024x1024 news-summary infographic for 18 November 2026.

Build-time tool only (uses Pillow + system DejaVu fonts, available on this VM).
The entry program itself (main.ts, Node stdlib) decodes the finished PNG from
its base64 text form (entry.png.b64, made with `base64 -w0 entry.png`) and
writes it to /output/entry.png, so grading is fully deterministic and needs
no network. The binary entry.png itself is git-ignored in the entry dir (the
connector push path is UTF-8 text only); a reference copy is kept beside the
entry dir as entry.png.reference.

All stories are real 18 Nov 2026 news, verified against Reuters/AP via
Just Security's Early Edition, One Turn, Horizon and NPR bulletins of the day.
See news.json for the same data in machine-readable form.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

NAVY = (14, 42, 71)
GOLD = (232, 184, 75)
INK = (17, 24, 39)
GREY = (71, 85, 105)
LIGHT = (241, 245, 249)
CARD_BORDER = (203, 213, 225)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

f_title = ImageFont.truetype(SERIF_B, 58)
f_kicker = ImageFont.truetype(SANS_B, 21)
f_sub = ImageFont.truetype(SANS, 23)
f_tag = ImageFont.truetype(SANS_B, 17)
f_head = ImageFont.truetype(SANS_B, 25)
f_body = ImageFont.truetype(SANS, 19)
f_also = ImageFont.truetype(SANS, 19)
f_also_b = ImageFont.truetype(SANS_B, 19)
f_foot = ImageFont.truetype(SANS, 15)

STORIES = json.loads((HERE / "news.json").read_text())["stories"]

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------- header ----------
d.rectangle([0, 0, W, 168], fill=NAVY)
d.rectangle([0, 168, W, 172], fill=GOLD)
d.text((36, 26), "WORLD NEWS  •  WEDNESDAY", font=f_kicker, fill=GOLD)
d.text((36, 56), "18 November 2026", font=f_title, fill=WHITE)
d.text((36, 126), "The day's biggest stories, in one image", font=f_sub, fill=(186, 205, 224))
# date badge on the right
d.rounded_rectangle([828, 34, 988, 132], radius=12, outline=GOLD, width=2)
d.text((908, 48), "NOV", font=f_kicker, fill=GOLD, anchor="mt")
d.text((908, 74), "18", font=ImageFont.truetype(SERIF_B, 40), fill=WHITE, anchor="mt")

# ---------- story cards: 2 cols x 3 rows ----------
mx, my, gap = 24, 192, 16
cw = (W - 2 * mx - gap) // 2          # 480
ch = 204
for i, s in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = mx + col * (cw + gap)
    y0 = my + row * (ch + gap)
    x1, y1 = x0 + cw, y0 + ch
    color = tuple(int(s["color"][j:j + 2], 16) for j in (1, 3, 5))
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=WHITE,
                        outline=CARD_BORDER, width=1)
    d.rounded_rectangle([x0, y0, x0 + 8, y1], radius=4, fill=color)
    # tag chip
    tag = s["tag"]
    tw = d.textlength(tag, font=f_tag) + 20
    d.rounded_rectangle([x0 + 22, y0 + 16, x0 + 22 + tw, y0 + 44], radius=7, fill=color)
    d.text((x0 + 32, y0 + 21), tag, font=f_tag, fill=WHITE)
    # headline (max 2 lines)
    y = y0 + 56
    for line in wrap(s["headline"], f_head, cw - 44)[:2]:
        d.text((x0 + 22, y), line, font=f_head, fill=INK)
        y += 30
    # summary (max 3 lines)
    y += 6
    for line in wrap(s["summary"], f_body, cw - 44)[:3]:
        d.text((x0 + 22, y), line, font=f_body, fill=GREY)
        y += 25

# ---------- also-today strip ----------
ay0 = my + 3 * ch + 2 * gap + 16   # 856; band 100 tall -> ends 956, footer at 978
d.rounded_rectangle([mx, ay0, W - mx, ay0 + 100], radius=14, fill=LIGHT)
d.text((mx + 22, ay0 + 10), "ALSO TODAY", font=f_also_b, fill=NAVY)
also = [
    "U.S. loses its measles-free status after 26 years — 5,400+ cases, 10 deaths.",
    "Category 5 Cyclone Xavier strikes the Northern Cook Islands.",
    "Magnitude 6.0 earthquake hits Papua New Guinea; 5.3 tremor in Romania.",
]
y = ay0 + 36
for line in also:
    d.text((mx + 22, y), "•  " + line, font=f_also, fill=INK)
    y += 21

# ---------- footer ----------
d.text((W // 2, 978), "Sources: Reuters · AP · Just Security · NPR  —  18 November 2026",
       font=f_foot, fill=GREY, anchor="mt")

img.save(HERE / "entry.png", "PNG", optimize=True)
print("saved", HERE / "entry.png", img.size)

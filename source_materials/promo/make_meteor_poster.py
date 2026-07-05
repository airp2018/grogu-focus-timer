# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math
import random


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "grogu_companion_poster.png"
OUT = ROOT / "grogu_meteor_pet_timer_poster.png"

W, H = 1080, 1560
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REGULAR = r"C:\Windows\Fonts\msyh.ttc"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def draw_center(draw, text, y, fnt, fill, stroke_width=0, stroke_fill=(0, 0, 0, 0)):
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke_width)
    w = box[2] - box[0]
    draw.text(((W - w) // 2, y), text, font=fnt, fill=fill,
              stroke_width=stroke_width, stroke_fill=stroke_fill)


def bubble(draw, x, y, w, h, text, accent):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=24,
                           fill=(8, 15, 25, 222), outline=accent, width=2)
    fnt = font(28, True)
    box = draw.textbbox((0, 0), text, font=fnt)
    tw = box[2] - box[0]
    th = box[3] - box[1]
    draw.text((x + (w - tw) // 2, y + (h - th) // 2 - 2),
              text, font=fnt, fill=(245, 252, 248, 255))


def make_background():
    img = Image.new("RGBA", (W, H), (6, 10, 18, 255))
    pix = img.load()
    for y in range(H):
        for x in range(W):
            dx = (x - W * 0.62) / W
            dy = (y - H * 0.46) / H
            glow = max(0, 1 - math.sqrt(dx * dx + dy * dy) * 2.1)
            top = max(0, 1 - y / H)
            pix[x, y] = (
                int(5 + 14 * top + 12 * glow),
                int(10 + 27 * top + 30 * glow),
                int(18 + 52 * top + 64 * glow),
                255,
            )
    return img


def add_stars_and_meteors(img):
    draw = ImageDraw.Draw(img)
    random.seed(20260705)
    for _ in range(190):
        x = random.randint(18, W - 18)
        y = random.randint(18, H - 18)
        r = random.choice([1, 1, 1, 2])
        a = random.randint(55, 185)
        color = random.choice([(235, 248, 255, a), (180, 228, 255, a), (255, 255, 240, a)])
        draw.ellipse((x, y, x + r, y + r), fill=color)

    meteors = [
        (115, 360, 390, 210, "#9ee7ff", 4),
        (760, 332, 1000, 205, "#8effc1", 3),
        (178, 1160, 500, 980, "#ffffff", 3),
        (710, 1010, 1015, 820, "#74f2ff", 4),
        (92, 735, 270, 610, "#28e890", 2),
    ]
    for x1, y1, x2, y2, color, width in meteors:
        rgb = tuple(int(color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        for extra, alpha in [(14, 26), (8, 50), (3, 145)]:
            draw.line((x1, y1, x2, y2), fill=rgb + (alpha,), width=width + extra)
        draw.ellipse((x2 - 5, y2 - 5, x2 + 5, y2 + 5), fill=(255, 255, 255, 210))


def add_grogu(img):
    base = Image.open(BASE).convert("RGBA")
    crop = base.crop((245, 475, 835, 1038))
    crop = ImageEnhance.Brightness(crop).enhance(1.08)
    crop = ImageEnhance.Contrast(crop).enhance(1.05)
    char_w = 660
    ratio = char_w / crop.width
    char = crop.resize((char_w, int(crop.height * ratio)), Image.Resampling.LANCZOS)

    mask = Image.new("L", char.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((22, 8, char.size[0] - 22, char.size[1] - 4), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.6))
    char.putalpha(mask)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((220, 695, 860, 1245), fill=(0, 0, 0, 128))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(42)))

    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse((230, 545, 850, 1215), fill=(47, 232, 144, 28))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(36)))
    img.alpha_composite(char, ((W - char.width) // 2, 590))


def add_copy(img):
    draw = ImageDraw.Draw(img)
    badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.rounded_rectangle((292, 82, 788, 136), radius=27,
                         fill=(255, 255, 255, 34), outline=(91, 255, 179, 130), width=2)
    img.alpha_composite(badge)
    draw.text((337, 92), "电子萌宠 + 时间管理", font=font(30, True), fill=(181, 255, 214, 255))

    draw_center(draw, "古古划过你的夜空", 172, font(72, True),
                (248, 255, 246, 255), stroke_width=3, stroke_fill=(0, 0, 0, 185))
    draw_center(draw, "随机表情包像流星一样出现", 294, font(34, True),
                (151, 226, 255, 245), stroke_width=1, stroke_fill=(0, 0, 0, 150))
    draw_center(draw, "陪你专注，也提醒你别再找借口", 350, font(34, True),
                (220, 238, 232, 238), stroke_width=1, stroke_fill=(0, 0, 0, 150))

    bubble(draw, 88, 1010, 292, 76, "别摸鱼，古古在看", (255, 209, 102, 230))
    bubble(draw, 712, 1038, 280, 76, "发功中，继续写", (124, 131, 255, 230))
    bubble(draw, 318, 1224, 444, 84, "再也不要找不干活的借口了", (47, 232, 144, 255))

    draw.rounded_rectangle((86, 1378, 994, 1454), radius=30,
                           fill=(8, 15, 25, 220), outline=(91, 255, 179, 120), width=1)
    footer = "浏览器里的古古电子宠物｜漂浮摇篮｜轻提醒｜随机表情"
    fnt = font(26, True)
    box = draw.textbbox((0, 0), footer, font=fnt)
    draw.text(((W - (box[2] - box[0])) // 2, 1400), footer,
              font=fnt, fill=(220, 246, 237, 250))


def main():
    img = make_background()
    add_stars_and_meteors(img)
    add_grogu(img)
    add_copy(img)
    img.convert("RGB").save(OUT, quality=96)
    print(OUT)


if __name__ == "__main__":
    main()

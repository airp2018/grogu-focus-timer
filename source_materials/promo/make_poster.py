# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import math
import random


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "extension" / "assets"
OUT = ROOT / "promo" / "grogu_companion_poster.png"

W, H = 1080, 1440

FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")


def f(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def text_size(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def draw_text_box(base, xy, text, font, pad=(22, 13), fill=(255, 255, 255, 235),
                  outline=(255, 255, 255, 120), text_fill=(22, 28, 25, 255), radius=22):
    d = ImageDraw.Draw(base)
    tw, th = text_size(d, text, font)
    x, y = xy
    box = (x, y, x + tw + pad[0] * 2, y + th + pad[1] * 2)
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((box[0], box[1] + 8, box[2], box[3] + 8), radius=radius, fill=(0, 0, 0, 78))
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(9)))
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)
    d.text((x + pad[0], y + pad[1] - 2), text, font=font, fill=text_fill)
    return box


def load_asset(name, frame=0):
    im = Image.open(ASSETS / f"{name}.webp")
    im.seek(min(frame, getattr(im, "n_frames", 1) - 1))
    return im.convert("RGBA")


def adjust(im, bright=1.2, contrast=1.07, saturation=1.04):
    r, g, b, a = im.convert("RGBA").split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    rgb = ImageEnhance.Color(rgb).enhance(saturation)
    return Image.merge("RGBA", (*rgb.split(), a))


def cover(im, size, zoom=1.0, center=(0.5, 0.5)):
    target = max(1, int(size * zoom))
    fitted = ImageOps.fit(im, (target, target), method=Image.Resampling.LANCZOS, centering=center)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(fitted, ((size - target) // 2, (size - target) // 2))
    return canvas


def avatar_with_cradle(name, size, frame=0, bright=1.2, zoom=1.08, center=(0.5, 0.45)):
    raw = adjust(load_asset(name, frame), bright=bright)
    face = cover(raw, size, zoom=zoom, center=center)

    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, size - 1, size - 1), fill=255)
    face.putalpha(mask)

    comp = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(comp)
    d.ellipse((4, 4, size - 4, size - 4), fill=(13, 18, 23, 190))
    comp.alpha_composite(face)

    s = size / 130
    # White/silver hover cradle. No red/black lower rim.
    d.pieslice((0 * s, 51 * s, 130 * s, 136 * s), 0, 180, fill=(232, 231, 225, 255))
    d.pieslice((5 * s, 70 * s, 125 * s, 131 * s), 0, 180, fill=(178, 184, 184, 118))
    d.pieslice((0 * s, 56 * s, 130 * s, 92 * s), 0, 180, fill=(251, 249, 242, 248))
    d.arc((0 * s, 55 * s, 130 * s, 92 * s), 0, 180, fill=(255, 255, 255, 240), width=max(2, int(3 * s)))

    for line in [((24, 98), (38, 94)), ((54, 91), (68, 88)), ((86, 98), (101, 94)), ((44, 111), (63, 106))]:
        d.line([(line[0][0] * s, line[0][1] * s), (line[1][0] * s, line[1][1] * s)],
               fill=(83, 88, 86, 130), width=max(1, int(2 * s)))

    d.rounded_rectangle((49 * s, 100 * s, 81 * s, 111 * s), radius=3 * s,
                        fill=(239, 236, 229, 255), outline=(88, 88, 84, 180), width=max(1, int(1 * s)))
    for i, col in enumerate([(124, 131, 255, 255), (46, 213, 115, 255), (255, 209, 102, 255)]):
        cx, cy, r = (56 + i * 9) * s, 105.5 * s, 2.35 * s
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)

    return comp


def make_background():
    img = Image.new("RGBA", (W, H), (9, 13, 18, 255))
    px = img.load()
    for y in range(H):
        for x in range(W):
            dx = (x - W * 0.62) / W
            dy = (y - H * 0.34) / H
            glow = max(0, 1 - math.sqrt(dx * dx + dy * dy) * 2.25)
            top = max(0, 1 - y / H)
            px[x, y] = (
                int(10 + 22 * glow + 10 * top),
                int(15 + 42 * glow + 9 * top),
                int(22 + 56 * glow + 15 * top),
                255,
            )

    d = ImageDraw.Draw(img)
    random.seed(12)
    for _ in range(145):
        x, y = random.randint(30, W - 30), random.randint(36, H - 40)
        s = random.choice([1, 1, 1, 2])
        a = random.randint(38, 118)
        d.ellipse((x, y, x + s, y + s), fill=(225, 241, 255, a))
    return img


def make_poster():
    img = make_background()
    d = ImageDraw.Draw(img)

    # Soft browser surface.
    panel = Image.new("RGBA", (900, 850), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle((0, 0, 900, 850), radius=34, fill=(234, 244, 245, 30),
                         outline=(255, 255, 255, 48), width=2)
    pd.rounded_rectangle((0, 0, 900, 74), radius=34, fill=(240, 246, 246, 44))
    for i, col in enumerate([(255, 95, 87, 210), (255, 190, 64, 210), (53, 211, 120, 210)]):
        pd.ellipse((34 + i * 34, 27, 52 + i * 34, 45), fill=col)
    pd.rounded_rectangle((165, 22, 820, 52), radius=15, fill=(12, 18, 25, 105))
    pd.text((190, 25), "github.com / writing / docs", font=f(16), fill=(190, 205, 210, 145))
    img.alpha_composite(panel, (90, 390))

    # Title.
    d.text((78, 88), "尤达宝宝时间管理", font=f(76, True), fill=(247, 250, 244, 255))
    d.text((82, 180), "浏览器里的陪伴电子宠物", font=f(31), fill=(190, 222, 210, 238))

    chips = ["轻提醒", "会漂浮", "不打扰", "有情绪价值"]
    x = 80
    for chip in chips:
        tw, th = text_size(d, chip, f(29, True))
        d.rounded_rectangle((x, 245, x + tw + 42, 298), radius=26,
                            fill=(255, 255, 255, 42), outline=(255, 255, 255, 78), width=1)
        d.text((x + 21, 252), chip, font=f(29, True), fill=(236, 242, 232, 242))
        x += tw + 62

    # Main character.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((250, 665, 830, 1205), fill=(0, 0, 0, 130))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(48)))

    main = avatar_with_cradle("peek", 560, frame=5, bright=1.16, zoom=1.28, center=(0.5, 0.42))
    img.alpha_composite(main, (260, 560))

    # Expression satellites.
    specs = [
        ("NO", 200, 126, 528, "NO", 8, 1.45, 1.10, (0.5, 0.44)),
        ("YES", 190, 760, 452, "YES，继续", 4, 1.20, 1.12, (0.5, 0.45)),
        ("fagong", 210, 748, 850, "发功中", 5, 1.95, 1.35, (0.5, 0.30)),
        ("cookie2", 174, 142, 910, "休息一下", 10, 1.14, 1.16, (0.5, 0.44)),
    ]

    for name, size, x0, y0, label, frame, bright, zoom, center in specs:
        glow = Image.new("RGBA", (size + 60, size + 60), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse((14, 14, size + 46, size + 46), fill=(120, 138, 255, 42))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)), (x0 - 30, y0 - 30))
        img.alpha_composite(avatar_with_cradle(name, size, frame, bright, zoom, center), (x0, y0))
        bx = x0 + size - 18 if x0 < W / 2 else x0 - 165
        by = y0 + 24
        draw_text_box(img, (bx, by), label, f(32, True), pad=(18, 10),
                      fill=(246, 250, 247, 240), outline=(255, 255, 255, 150),
                      text_fill=(20, 29, 25, 255), radius=20)

    draw_text_box(img, (585, 524), "我在。", f(34, True), pad=(24, 14),
                  fill=(247, 252, 248, 244), outline=(46, 213, 115, 145),
                  text_fill=(18, 34, 25, 255), radius=24)
    draw_text_box(img, (126, 1130), "该干什么，古古轻轻提醒你。", f(25), pad=(22, 13),
                  fill=(16, 22, 30, 216), outline=(255, 255, 255, 86),
                  text_fill=(225, 235, 229, 245), radius=22)

    footer_font = f(43, True)
    footer = "不是管教，是陪伴。"
    tw, _ = text_size(d, footer, footer_font)
    d.text(((W - tw) // 2, 1280), footer, font=footer_font, fill=(248, 250, 240, 255))
    sub = "漂过网页的小摇篮｜随机表情｜温柔提醒"
    tw, _ = text_size(d, sub, f(25))
    d.text(((W - tw) // 2, 1342), sub, font=f(25), fill=(184, 206, 198, 232))

    img.convert("RGB").save(OUT, quality=96)
    print(OUT)


if __name__ == "__main__":
    make_poster()

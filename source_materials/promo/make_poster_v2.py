# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import math
import random
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "extension" / "assets"
SRC = ROOT / "source_materials"
OUT = ROOT / "promo" / "grogu_companion_poster.png"

def load_highres_asset(name, frame_idx):
    # Mapping of target name to mp4 path, frame index and crop coordinates (w, h, x, y)
    mapping = {
        "meat": {"mp4": "烤肉.mp4", "frame": 31, "crop": [600, 600, 1000, 200]},
        "NO": {"mp4": "NO.mp4", "frame": 14, "crop": [600, 600, 480, 280]},
        "fagong": {"mp4": "发功.mp4", "frame": 10, "crop": [620, 620, 324, 19]},
        "peek": {"mp4": "peek.mp4", "frame": 8, "crop": [760, 760, 608, 139]},
        "cookie2": {"mp4": "饼干2.mp4", "frame": 26, "crop": [800, 800, 530, 100]}
    }
    
    if name in mapping:
        info = mapping[name]
        mp4_path = SRC / info["mp4"]
        if mp4_path.exists():
            cap = cv2.VideoCapture(str(mp4_path))
            cap.set(cv2.CAP_PROP_POS_FRAMES, info["frame"])
            ret, frame = cap.read()
            cap.release()
            if ret:
                w, h, x, y = info["crop"]
                cropped = frame[y:y+h, x:x+w]
                rgb_frame = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                return Image.fromarray(rgb_frame)
                
    # Fallback to load WebP if MP4 loading fails
    return load_asset(name, frame_idx)

W, H = 1080, 1560

FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")

if not FONT_BOLD.exists():
    FONT_BOLD = Path("arialbd.ttf")
if not FONT_REGULAR.exists():
    FONT_REGULAR = Path("arial.ttf")

def f(size, bold=False):
    font_path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(str(font_path), size)

def text_size(draw, text, font):
    if hasattr(draw, "textbbox"):
        box = draw.textbbox((0, 0), text, font=font)
        return box[2] - box[0], box[3] - box[1]
    else:
        return draw.textsize(text, font=font)

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
    # SSAA factor: draw at 4x resolution, then resize down for perfect anti-aliasing
    f_scale = 4
    render_size = size * f_scale
    
    raw = adjust(load_highres_asset(name, frame), bright=bright)
    face = cover(raw, render_size, zoom=zoom, center=center)
    
    mask = Image.new("L", (render_size, render_size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, render_size - 1, render_size - 1), fill=255)
    face.putalpha(mask)
    
    comp = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))
    d = ImageDraw.Draw(comp)
    
    # Circle background dark shadow to separate from nebula
    d.ellipse((8 * f_scale, 8 * f_scale, render_size - 8 * f_scale, render_size - 8 * f_scale), fill=(13, 18, 23, 200))
    comp.alpha_composite(face)
    
    s = render_size / 130.0
    
    # Helper to generate quadratic bezier points
    def get_quad_bezier(p0, p1, p2, num_pts=30):
        pts = []
        for i in range(num_pts + 1):
            t = i / num_pts
            x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
            y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
            pts.append((x * s, y * s))
        return pts

    # Helper to generate arc points
    def get_arc_pts(cx, cy, r, start_deg, end_deg, num_pts=30):
        pts = []
        for i in range(num_pts + 1):
            deg = start_deg + (end_deg - start_deg) * (i / num_pts)
            rad = math.radians(deg)
            x = cx + r * math.cos(rad)
            y = cy + r * math.sin(rad)
            pts.append((x * s, y * s))
        return pts

    # 1. cradle-inner-shadow: fill #7f827e opacity 0.22 (127, 130, 126, 56)
    pts1 = get_quad_bezier((0, 74), (65, 88), (130, 74))
    pts2 = get_arc_pts(65, 65, 65, 7.89, 175.602, 30)
    d.polygon(pts1 + pts2, fill=(127, 130, 126, 56))

    # 2. cradle-base-cup: fill #e8e3d8 (232, 227, 216, 255)
    pts1 = get_quad_bezier((0, 70), (65, 86), (130, 70))
    pts2 = get_arc_pts(65, 65, 65, 4.398, 175.602, 30)
    d.polygon(pts1 + pts2, fill=(232, 227, 216, 255))

    # 3. cradle-lower-shadow: fill #b9b7ae opacity 0.48 (185, 183, 174, 122)
    pts1 = get_quad_bezier((7, 90), (65, 119), (123, 90))
    pts2 = get_arc_pts(65, 65, 61, 23.28, 156.72, 30)
    d.polygon(pts1 + pts2, fill=(185, 183, 174, 122))

    # 4. cradle-rim-highlight: fill #f7f4ec opacity 0.95 (247, 244, 236, 242)
    pts1 = get_quad_bezier((0, 69), (65, 85), (130, 69))
    pts2 = get_quad_bezier((130, 69), (65, 80), (0, 69))
    d.polygon(pts1 + pts2, fill=(247, 244, 236, 242))

    # 5. cradle-rim-shine: fill #ffffff opacity 0.82 (255, 255, 255, 209)
    pts1 = get_quad_bezier((12, 70.5), (65, 81.5), (118, 70.5))
    pts2 = get_quad_bezier((118, 70.5), (65, 77.5), (12, 70.5))
    d.polygon(pts1 + pts2, fill=(255, 255, 255, 209))

    # 6. cradle-dashboard: fill #ece8df, stroke #5d5d58, width 1
    d.rounded_rectangle((49 * s, 100 * s, 81 * s, 111 * s), radius=3 * s,
                        fill=(236, 232, 223, 255), outline=(93, 93, 88, 255), width=max(1, int(1 * s)))

    # LED lights inside the dashboard
    for i, col in enumerate([(124, 131, 255, 255), (46, 213, 115, 255), (255, 209, 102, 255)]):
        cx, cy, r = (56 + i * 9) * s, 105.5 * s, 2.2 * s
        d.ellipse((cx - r*1.5, cy - r*1.5, cx + r*1.5, cy + r*1.5), fill=(col[0], col[1], col[2], 80))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)

    # 7. cradle-side-hinge: stroke #6e6f6a, width 2, opacity 0.85
    hinge_pts = get_quad_bezier((111, 79), (120, 82), (123, 91))
    d.line(hinge_pts, fill=(110, 111, 106, 216), width=max(1, int(2 * s)))

    # 8. cradle-scuff lines: stroke #5f625d, width 1.6, opacity 0.62
    scuffs = [
        ((54, 92), (62, 90)),
        ((58, 95), (68, 92)),
        ((87, 101), (96, 97)),
        ((11, 101), (26, 96)),
        ((41, 118), (58, 113))
    ]
    for p_start, p_end in scuffs:
        d.line([(p_start[0] * s, p_start[1] * s), (p_end[0] * s, p_end[1] * s)],
               fill=(95, 98, 93, 158), width=max(1, int(1.6 * s)))

    # 9. cradle-chip polygons: fill #666966, opacity 0.7
    chips = [
        [(22, 105), (30, 103), (28, 108), (21, 109)],
        [(93, 84), (103, 81), (102, 87), (94, 89)]
    ]
    for chip_pts in chips:
        scaled_chip = [(x * s, y * s) for x, y in chip_pts]
        d.polygon(scaled_chip, fill=(102, 105, 102, 178))

    return comp.resize((size, size), Image.Resampling.LANCZOS)

def draw_speech_bubble(img, box, text, font_size, bold=False, bg_color=(20, 30, 42, 235), border_color=(46, 213, 115, 200),
                       text_color=(240, 255, 245, 255), radius=16, pointer_direction="bottom-left"):
    scale = 2
    w_orig, h_orig = img.size
    overlay = Image.new("RGBA", (w_orig * scale, h_orig * scale), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    
    x1, y1, x2, y2 = [coord * scale for coord in box]
    od.rounded_rectangle((x1, y1, x2, y2), radius=radius * scale, fill=bg_color, outline=border_color, width=max(1, 2 * scale))
    
    # Draw pointers
    if pointer_direction == "bottom-left":
        p_width = 16 * scale
        p_height = 18 * scale
        px = x1 + 35 * scale
        py = y2
        points = [(px, py), (px + p_width, py), (px - p_width//3, py + p_height)]
        od.polygon(points, fill=bg_color)
        od.line([(px, py), (px - p_width//3, py + p_height), (px + p_width, py)], fill=border_color, width=max(1, 2 * scale))
        od.line([(px + 1, py), (px + p_width - 1, py)], fill=bg_color, width=max(1, 3 * scale))
    elif pointer_direction == "bottom-right":
        p_width = 16 * scale
        p_height = 18 * scale
        px = x2 - 50 * scale
        py = y2
        points = [(px, py), (px + p_width, py), (px + p_width + p_width//3, py + p_height)]
        od.polygon(points, fill=bg_color)
        od.line([(px, py), (px + p_width + p_width//3, py + p_height), (px + p_width, py)], fill=border_color, width=max(1, 2 * scale))
        od.line([(px + 1, py), (px + p_width - 1, py)], fill=bg_color, width=max(1, 3 * scale))
    elif pointer_direction == "bottom-center":
        p_width = 16 * scale
        p_height = 16 * scale
        px = (x1 + x2) // 2 - p_width // 2
        py = y2
        points = [(px, py), (px + p_width, py), (px + p_width // 2, py + p_height)]
        od.polygon(points, fill=bg_color)
        od.line([(px, py), (px + p_width // 2, py + p_height), (px + p_width, py)], fill=border_color, width=max(1, 2 * scale))
        od.line([(px + 1, py), (px + p_width - 1, py)], fill=bg_color, width=max(1, 3 * scale))
    elif pointer_direction == "top-center":
        p_width = 16 * scale
        p_height = 16 * scale
        px = (x1 + x2) // 2 - p_width // 2
        py = y1
        points = [(px, py), (px + p_width, py), (px + p_width // 2, py - p_height)]
        od.polygon(points, fill=bg_color)
        od.line([(px, py), (px + p_width // 2, py - p_height), (px + p_width, py)], fill=border_color, width=max(1, 2 * scale))
        od.line([(px + 1, py), (px + p_width - 1, py)], fill=bg_color, width=max(1, 3 * scale))

    # Resolve font
    font_path = FONT_BOLD if bold else FONT_REGULAR
    scaled_font = ImageFont.truetype(str(font_path), font_size * scale)
    
    lines = text.split('\n')
    line_heights = [od.textbbox((0, 0), line, font=scaled_font)[3] - od.textbbox((0, 0), line, font=scaled_font)[1] for line in lines]
    total_text_height = sum(line_heights) + 6 * scale * (len(lines) - 1)
    
    current_y = y1 + (y2 - y1 - total_text_height) // 2
    for line, lh in zip(lines, line_heights):
        lw = od.textbbox((0, 0), line, font=scaled_font)[2] - od.textbbox((0, 0), line, font=scaled_font)[0]
        tx = x1 + (x2 - x1 - lw) // 2
        od.text((tx, current_y), line, font=scaled_font, fill=text_color)
        current_y += lh + 6 * scale

    downsampled = overlay.resize((w_orig, h_orig), Image.Resampling.LANCZOS)
    img.alpha_composite(downsampled)

def make_background():
    # Build a small gradient and nebula template (270x390), then scale it up for high performance and smooth blending
    bg = Image.new("RGBA", (270, 390), (10, 13, 20, 255))
    
    # Glow layer
    glow = Image.new("RGBA", (270, 390), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    
    # 1. Violet nebula at top-right
    gd.ellipse((140, 20, 270, 150), fill=(85, 35, 120, 52))
    # 2. Teal nebula at bottom-left
    gd.ellipse((-10, 210, 150, 370), fill=(20, 80, 105, 68))
    # 3. Emerald green nebula at bottom-right
    gd.ellipse((100, 240, 240, 380), fill=(15, 75, 45, 40))
    # 4. Soft central light
    gd.ellipse((50, 110, 220, 280), fill=(30, 60, 90, 30))
    
    glow = glow.filter(ImageFilter.GaussianBlur(38))
    bg.alpha_composite(glow)
    
    # Resize to poster size
    img = bg.resize((W, H), Image.Resampling.BICUBIC)
    
    # Add random stars
    d = ImageDraw.Draw(img)
    random.seed(42)
    for _ in range(160):
        x = random.randint(10, W - 10)
        y = random.randint(10, H - 10)
        size = random.choice([1, 1, 1, 2, 3])
        opacity = random.randint(55, 220)
        if size == 3:
            d.ellipse((x - 2, y - 2, x + 4, y + 4), fill=(150, 210, 255, int(opacity * 0.35)))
            d.ellipse((x, y, x + 2, y + 2), fill=(255, 255, 255, opacity))
        else:
            d.ellipse((x, y, x + size, y + size), fill=(255, 255, 255, opacity))
            
    return img

def make_poster():
    img = make_background()
    d = ImageDraw.Draw(img)
    
    # 1. Poster Title Header
    d.text((W // 2, 130), "古古原力专注助理", font=f(72, True), fill=(255, 255, 255, 255), anchor="mm")
    d.text((W // 2, 215), "GROGU FOCUS TIMER", font=f(28, True), fill=(46, 213, 115, 255), anchor="mm")
    
    pitch = "“不是管教，是陪伴。” —— 浏览器里的电子宠物时间管理伴侣"
    d.text((W // 2, 275), pitch, font=f(24), fill=(185, 205, 220, 230), anchor="mm")
    
    # Thin divider line
    d.line([(140, 330), (940, 330)], fill=(50, 65, 80, 255), width=2)
    
    # 2. Main Character (Center)
    # Draw soft glow under main character
    glow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_overlay)
    gd.ellipse((320, 890, 760, 935), fill=(46, 213, 115, 48))
    img.alpha_composite(glow_overlay.filter(ImageFilter.GaussianBlur(28)))
    
    # Draw big Grogu (using high-res meat close-up smile asset for optimal visual clarity)
    main_grogu = avatar_with_cradle("meat", 440, frame=12, bright=1.12, zoom=1.15, center=(0.5, 0.45))
    img.alpha_composite(main_grogu, (320, 500))
    
    # 3. Main character speech bubble (repositioned to center to prevent overlapping satellite faces)
    draw_speech_bubble(img, (300, 365, 780, 485), "原力与我们同在，\n专注时间开始咯！", 25, True,
                       bg_color=(15, 25, 38, 230), border_color=(46, 213, 115, 210),
                       text_color=(235, 255, 240, 255), radius=16, pointer_direction="bottom-center")
                       
    # 4. Satellites and their speech bubbles
    satellites = [
        # Top Left
        ("NO", 170, 95, 435, "哼，不准分心！", 8, 1.35, 1.10, (0.5, 0.44), (60, 340, 300, 405), "bottom-center"),
        # Top Right
        ("fagong", 170, 815, 435, "原力爆发中！", 5, 1.85, 1.35, (0.5, 0.30), (780, 340, 1020, 405), "bottom-center"),
        # Bottom Left
        ("peek", 170, 95, 745, "偷偷看你一眼", 4, 1.16, 1.18, (0.5, 0.42), (60, 950, 300, 1015), "top-center"),
        # Bottom Right
        ("cookie2", 170, 815, 745, "吃个小饼干吧", 10, 1.14, 1.16, (0.5, 0.44), (780, 950, 1020, 1015), "top-center")
    ]
    
    for name, size, x0, y0, label, frame, bright, zoom, center, bubble_box, bubble_dir in satellites:
        # Draw soft satellite glow
        sat_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sgd = ImageDraw.Draw(sat_glow)
        sgd.ellipse((x0 - 15, y0 - 15, x0 + size + 15, y0 + size + 15), fill=(80, 120, 255, 30))
        img.alpha_composite(sat_glow.filter(ImageFilter.GaussianBlur(12)))
        
        # Draw satellite avatar
        sat_img = avatar_with_cradle(name, size, frame, bright, zoom, center)
        img.alpha_composite(sat_img, (x0, y0))
        
        # Draw speech bubble
        draw_speech_bubble(img, bubble_box, label, 18, True,
                           bg_color=(15, 23, 33, 220), border_color=(255, 255, 255, 60),
                           text_color=(235, 245, 250, 255), radius=12, pointer_direction=bubble_dir)

    # 5. Highlights Cards Section
    cards = [
        ("智能防分心", "悬浮窗常驻提醒", "网页悬浮，轻量提醒\n自定义工作与休息节奏", (60, 1080, 360, 1290)),
        ("原力一键唤", "快捷键全局响应", "召唤/关闭快捷操作\n沉浸工作不被打扰", (390, 1080, 690, 1290)),
        ("趣致萌宠伴", "丰富表情与音效", "点击播放萌趣配音\n给您满满的情绪价值", (720, 1080, 1020, 1290))
    ]
    
    for title, subtitle, desc, box in cards:
        x1, y1, x2, y2 = box
        # Translucent glassmorphic card
        card_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        csd = ImageDraw.Draw(card_shadow)
        csd.rounded_rectangle((x1, y1 + 5, x2, y2 + 5), radius=16, fill=(0, 0, 0, 80))
        img.alpha_composite(card_shadow.filter(ImageFilter.GaussianBlur(10)))
        
        # Card body overlay
        card_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cod = ImageDraw.Draw(card_overlay)
        cod.rounded_rectangle(box, radius=16, fill=(255, 255, 255, 15), outline=(255, 255, 255, 45), width=1)
        img.alpha_composite(card_overlay)
        
        # Text layout (drawn directly on opaque image context)
        cx = (x1 + x2) // 2
        d.text((cx, y1 + 35), title, font=f(26, True), fill=(255, 255, 255, 255), anchor="mm")
        d.text((cx, y1 + 80), subtitle, font=f(18), fill=(46, 213, 115, 255), anchor="mm")
        
        # Body description
        lines = desc.split('\n')
        curr_y = y1 + 135
        for line in lines:
            d.text((cx, curr_y), line, font=f(18), fill=(185, 200, 215, 220), anchor="mm")
            curr_y += 30

    # 6. Poster Footer
    d.line([(100, 1340), (980, 1340)], fill=(50, 65, 80, 255), width=1)
    
    d.text((W // 2, 1380), "古古原力专注助理 · 陪伴你专注的每一分钟", font=f(22, True), fill=(160, 180, 195, 255), anchor="mm")
    d.text((W // 2, 1430), "安装方式：下载源码 -> Chrome 扩展程序 -> 开启开发者模式 -> 加载已解压的扩展程序", font=f(18), fill=(120, 140, 155, 230), anchor="mm")
    d.text((W // 2, 1475), "MAY THE FORCE BE WITH YOU", font=f(18, True), fill=(46, 213, 115, 200), anchor="mm")

    # Save output image
    img.convert("RGB").save(OUT, quality=96)
    print(f"Poster successfully saved to: {OUT}")

if __name__ == "__main__":
    make_poster()

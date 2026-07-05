import os
import math
from PIL import Image, ImageDraw

def generate_cradle_animation():
    webp_in = r"extension/assets/zhaoshou.webp"
    webp_out = r"extension/assets/zhaoshou_cradle.webp"
    
    if not os.path.exists(webp_in):
        print(f"Error: {webp_in} does not exist.")
        return
        
    print(f"Loading {webp_in}...")
    im = Image.open(webp_in)
    
    frames = []
    try:
        while True:
            frames.append(im.copy())
            im.seek(im.tell() + 1)
    except EOFError:
        pass
        
    print(f"Found {len(frames)} frames. Rendering cradle overlay...")
    
    render_size = 200  # Let's make the preview 200x200 for high resolution in README
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
        
    out_frames = []
    for frame_idx, f in enumerate(frames):
        # 1. Convert frame to RGBA
        f_rgba = f.convert("RGBA")
        
        # 2. Resize and crop the frame to fill render_size x render_size
        # The frame is 240x160.
        # Scale it so that height becomes render_size (200), width becomes 300.
        f_scaled = f_rgba.resize((300, 200), Image.Resampling.LANCZOS)
        
        # We want to crop a 200x200 square.
        # Horizontal translation (translateX = 6px in 160px size -> 6/160 * 200 = 7.5px in 200px size)
        # Shift crop window left by 7.5px -> Center X shifts from 150 to 142.5 -> Crop X starts at 42.5.
        # Vertical translation (translateY = 2px in 160px size -> 2/160 * 200 = 2.5px in 200px size)
        # Shift crop window up by 2.5px -> Center Y shifts from 100 to 97.5 -> Crop Y starts at -2.5 (we pad at top).
        
        # Let's crop X from 42 to 242.
        # Y from 0 to 200, but we translate the image down by 3px and fill the top with black/transparent.
        canvas = Image.new("RGBA", (200, 200), (17, 18, 20, 255)) # Dark background matching video
        cropped_video = f_scaled.crop((42, 0, 242, 200))
        canvas.paste(cropped_video, (0, 3), cropped_video) # translateY of 3px
        
        # 3. Apply circular mask to the video
        mask = Image.new("L", (200, 200), 0)
        md = ImageDraw.Draw(mask)
        md.ellipse((0, 0, 199, 199), fill=255)
        
        masked_canvas = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        masked_canvas.paste(canvas, (0, 0), mask)
        
        # 4. Create final frame canvas
        comp = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        d = ImageDraw.Draw(comp)
        
        # Draw background shadow inside circle
        d.ellipse((0, 0, 199, 199), fill=(17, 18, 20, 255))
        comp.alpha_composite(masked_canvas)
        
        # 5. Draw the cradle paths on top
        # A. Inner shadow: fill (127, 130, 126, 56)
        pts1 = get_quad_bezier((0, 70), (65, 106), (130, 70))
        pts2 = get_arc_pts(65, 65, 65, 4.398, 175.602, 30)
        d.polygon(pts1 + pts2, fill=(127, 130, 126, 56))
        
        # B. Base cup: fill (232, 227, 216, 255)
        pts1 = get_quad_bezier((0, 70), (65, 102), (130, 70))
        pts2 = get_arc_pts(65, 65, 65, 4.398, 175.602, 30)
        d.polygon(pts1 + pts2, fill=(232, 227, 216, 255))
        
        # C. Lower shadow: fill (185, 183, 174, 122)
        pts1 = get_quad_bezier((7, 90), (65, 119), (123, 90))
        pts2 = get_arc_pts(65, 65, 61, 23.28, 156.72, 30)
        d.polygon(pts1 + pts2, fill=(185, 183, 174, 122))
        
        # D. Rim highlight: fill (247, 244, 236, 242)
        pts1 = get_quad_bezier((0, 69), (65, 101), (130, 69))
        pts2 = get_quad_bezier((130, 69), (65, 95), (0, 69))
        d.polygon(pts1 + pts2, fill=(247, 244, 236, 242))
        
        # E. Rim shine: fill (255, 255, 255, 209)
        pts1 = get_quad_bezier((12, 70.5), (65, 96.5), (118, 70.5))
        pts2 = get_quad_bezier((118, 70.5), (65, 91.5), (12, 70.5))
        d.polygon(pts1 + pts2, fill=(255, 255, 255, 209))
        
        # F. Dashboard: fill (236, 232, 223, 255), outline (93, 93, 88, 255)
        d.rounded_rectangle((49 * s, 102 * s, 81 * s, 113 * s), radius=3 * s,
                            fill=(236, 232, 223, 255), outline=(93, 93, 88, 255), width=max(1, int(1 * s)))
        
        # G. Cyan LEDs (friendship theme!)
        led_color = (0, 210, 211, 255)
        for i in range(3):
            cx, cy, r = (56 + i * 9) * s, 107.5 * s, 2.2 * s
            # Outer glow
            d.ellipse((cx - r*1.5, cy - r*1.5, cx + r*1.5, cy + r*1.5), fill=(led_color[0], led_color[1], led_color[2], 80))
            # Inner led
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=led_color)
            
        # H. Side hinge
        hinge_pts = get_quad_bezier((111, 79), (120, 82), (123, 91))
        d.line(hinge_pts, fill=(110, 111, 106, 216), width=max(1, int(2 * s)))
        
        # I. Scuff marks
        scuffs = [
            ((54, 97), (62, 95)),
            ((58, 100), (68, 97)),
            ((87, 106), (96, 102)),
            ((11, 106), (26, 101)),
            ((41, 123), (58, 118))
        ]
        for p_start, p_end in scuffs:
            d.line([(p_start[0] * s, p_start[1] * s), (p_end[0] * s, p_end[1] * s)],
                   fill=(95, 98, 93, 158), width=max(1, int(1.6 * s)))
                   
        # J. Chips
        chips = [
            [(22, 108), (30, 106), (28, 111), (21, 112)],
            [(93, 87), (103, 84), (102, 90), (94, 92)]
        ]
        for chip_pts in chips:
            scaled_chip = [(x * s, y * s) for x, y in chip_pts]
            d.polygon(scaled_chip, fill=(102, 105, 102, 178))
            
        # K. Add thin subtle outer ring border to circle matching our CSS
        d.ellipse((0.5 * s, 0.5 * s, render_size - 0.5 * s, render_size - 0.5 * s),
                  outline=(255, 255, 255, 51), width=max(1, int(1.5 * s)))
                  
        out_frames.append(comp)
        
    print(f"Saving combined WebP animation to {webp_out}...")
    out_frames[0].save(
        webp_out,
        save_all=True,
        append_images=out_frames[1:],
        duration=83,  # 12fps -> ~83ms
        loop=0,
        optimize=True
    )
    print("Done!")

if __name__ == "__main__":
    generate_cradle_animation()

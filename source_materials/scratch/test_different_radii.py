from PIL import Image, ImageDraw

def render_css_radius_correctly(w, h, rx, ry, filename):
    # This renders the exact mathematical shape of a box with CSS border-radius rx / ry
    # rx is a list of 4 horizontal radii in pixels, ry is vertical radii in pixels
    # e.g., rx = [w/2, w/2, w/2, w/2], ry = [h*0.3, h*0.3, h*0.7, h*0.7]
    
    # We will create a high-resolution canvas, draw the mask, and resize
    scale = 8
    ws, hs = w * scale, h * scale
    mask = Image.new("L", (ws, hs), 0)
    draw = ImageDraw.Draw(mask)
    
    r_x = [r * scale for r in rx]
    r_y = [r * scale for r in ry]
    
    # Draw corners
    # Top-Left: arc from 180 to 270 deg
    draw.pieslice([0, 0, 2*r_x[0], 2*r_y[0]], 180, 270, fill=255)
    # Top-Right: arc from 270 to 360 deg
    draw.pieslice([ws - 2*r_x[1], 0, ws, 2*r_y[1]], 270, 360, fill=255)
    # Bottom-Right: arc from 0 to 90 deg
    draw.pieslice([ws - 2*r_x[2], hs - 2*r_y[2], ws, hs], 0, 90, fill=255)
    # Bottom-Left: arc from 90 to 180 deg
    draw.pieslice([0, hs - 2*r_y[3], 2*r_x[3], hs], 90, 180, fill=255)
    
    # Now fill the core bounding box structure:
    # We fill the middle horizontal box: from X=0 to ws, Y=max(tl_y, tr_y) to hs - max(bl_y, br_y)
    top_y = max(r_y[0], r_y[1])
    bot_y = hs - max(r_y[2], r_y[3])
    if bot_y > top_y:
        draw.rectangle([0, top_y, ws, bot_y], fill=255)
    
    # We fill the top middle vertical box: from X=tl_x to ws - tr_x, Y=0 to top_y
    draw.rectangle([r_x[0], 0, ws - r_x[1], top_y], fill=255)
    
    # We fill the bottom middle vertical box: from X=bl_x to ws - br_x, Y=bot_y to hs
    draw.rectangle([r_x[3], bot_y, ws - r_x[2], hs], fill=255)
    
    mask = mask.resize((w, h), Image.Resampling.LANCZOS)
    
    # Make preview image
    preview = Image.new("RGBA", (w + 20, h + 20), (30, 40, 45, 255))
    green_bg = Image.new("RGBA", (w, h), (143, 188, 143, 255))
    preview.paste(green_bg, (10, 10), mask)
    preview.save(filename)

# Option 1: Egg shape, narrower top, wider bottom (classic pram capsule shape!)
# border-radius: 50% 50% 50% 50% / 60% 60% 40% 40% -> wait!
# If ry is [0.4 * h, 0.4 * h, 0.6 * h, 0.6 * h], the top vertical radius is 0.4 (flatter dome)
# and the bottom is 0.6 (deeper cup).
# Let's test different combinations:
w, h = 120, 150

# A: top 35%, bottom 65% (tapered top dome, rounder bottom cup)
# border-radius: 50% 50% 50% 50% / 35% 35% 65% 65%
render_css_radius_correctly(w, h, [w/2]*4, [h*0.35, h*0.35, h*0.65, h*0.65], "pram_option_A.png")

# B: top 65%, bottom 35% (longer top canopy dome, flatter bottom)
# border-radius: 50% 50% 50% 50% / 65% 65% 35% 35%
render_css_radius_correctly(w, h, [w/2]*4, [h*0.65, h*0.65, h*0.35, h*0.35], "pram_option_B.png")

# C: border-radius: 50% 50% 50% 50% / 40% 40% 60% 60%
render_css_radius_correctly(w, h, [w/2]*4, [h*0.4, h*0.4, h*0.6, h*0.6], "pram_option_C.png")

# D: border-radius: 50% 50% 50% 50% / 50% 50% 50% 50% (regular ellipse)
render_css_radius_correctly(w, h, [w/2]*4, [h*0.5, h*0.5, h*0.5, h*0.5], "pram_option_D.png")

print("All correctly calculated options rendered.")

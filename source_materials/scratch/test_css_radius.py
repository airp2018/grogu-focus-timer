from PIL import Image, ImageDraw

def draw_css_border_radius(w, h, rx, ry):
    # Simulates rendering a CSS border-radius box in PIL
    # We will draw a filled mask with the specified border-radius
    # and then draw a border.
    # For rx and ry, they represent the horizontal and vertical radii of the 4 corners:
    # Top-Left, Top-Right, Bottom-Right, Bottom-Left.
    
    # We create a larger image and scale down for antialiasing
    scale = 4
    ws, hs = w * scale, h * scale
    mask = Image.new("L", (ws, hs), 0)
    draw = ImageDraw.Draw(mask)
    
    # Radii in pixels
    # rx = [tl, tr, br, bl]
    # ry = [tl, tr, br, bl]
    r_x = [int(r * ws) for r in rx]
    r_y = [int(r * hs) for r in ry]
    
    # Draw corners
    # Top-Left corner ellipse bbox: (0, 0, 2*rx[0], 2*ry[0])
    draw.pieslice([0, 0, 2 * r_x[0], 2 * r_y[0]], 180, 270, fill=255)
    # Top-Right corner ellipse bbox: (ws - 2*rx[1], 0, ws, 2*ry[1])
    draw.pieslice([ws - 2 * r_x[1], 0, ws, 2 * r_y[1]], 270, 360, fill=255)
    # Bottom-Right corner ellipse bbox: (ws - 2*rx[2], hs - 2*ry[2], ws, hs)
    draw.pieslice([ws - 2 * r_x[2], hs - 2 * r_y[2], ws, hs], 0, 90, fill=255)
    # Bottom-Left corner ellipse bbox: (0, hs - 2*rx[3], 2*rx[3], hs)
    draw.pieslice([0, hs - 2 * r_y[3], 2 * r_x[3], hs], 90, 180, fill=255)
    
    # Draw inner rects to fill the body
    draw.rectangle([r_x[0], 0, ws - r_x[1], hs], fill=255)
    draw.rectangle([0, max(r_y[0], r_y[1]), ws, hs - max(r_y[2], r_y[3])], fill=255)
    
    # Resize back with high quality antialiasing
    mask = mask.resize((w, h), Image.Resampling.LANCZOS)
    
    # Create final preview image
    preview = Image.new("RGBA", (w + 40, h + 40), (15, 23, 25, 0))
    # Place mask in center
    img_content = Image.new("RGBA", (w, h), (143, 188, 143, 255)) # Green background
    preview.paste(img_content, (20, 20), mask)
    
    # Let's draw a nice glowing border
    draw_prev = ImageDraw.Draw(preview)
    # Draw simple outline for the shape
    # We can trace the mask's contour
    return preview

# Try an egg/pram shape:
# In CSS: border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%
# Here, rx is [0.5, 0.5, 0.5, 0.5], ry is [0.6, 0.6, 0.4, 0.4]
preview1 = draw_css_border_radius(120, 150, [0.5, 0.5, 0.5, 0.5], [0.6, 0.6, 0.4, 0.4])
preview1.save("preview_pram_1.png")

# Try a capsule/dome shape:
# rx is [0.5, 0.5, 0.5, 0.5], ry is [0.4, 0.4, 0.4, 0.4]
# Or a flatter top and bottom, or custom shapes
# Let's try: border-radius: 50% 50% 40% 40% / 40% 40% 60% 60%
preview2 = draw_css_border_radius(120, 150, [0.5, 0.5, 0.45, 0.45], [0.4, 0.4, 0.6, 0.6])
preview2.save("preview_pram_2.png")

print("Previews generated.")

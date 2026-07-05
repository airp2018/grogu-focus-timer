from PIL import Image, ImageDraw

# Create a test image to preview the custom border-radius shape
# We will simulate a 120x145 container with a border-radius of 50% 50% 50% 50% / 60% 60% 40% 40%
# In PIL, we can draw a custom path or an ellipse that fits this shape, 
# but let's draw an egg/pram shape using curves to see how it looks.
# An egg-shaped outline can be drawn using two ellipses or a custom polygon.
# Let's write a quick visual preview.

im = Image.new("RGBA", (300, 300), (15, 23, 25, 255))
draw = ImageDraw.Draw(im)

# Drawing a capsule/egg shape that resembles the hover-pram
# Top is a round dome: semi-ellipse from Y=50 to Y=150, X=90 to X=210
# Bottom is a rounded cup: semi-ellipse from Y=120 to Y=230, X=90 to X=210
# Let's draw an outline of the pram shape:
# Top curve:
draw.chord([90, 50, 210, 170], 180, 360, outline=(143, 188, 143, 255), width=4)
# Bottom curve (flatter):
draw.chord([90, 110, 210, 230], 0, 180, outline=(143, 188, 143, 255), width=4)
# Side connecting lines
draw.line([90, 110, 90, 170], fill=(143, 188, 143, 255), width=4)
draw.line([210, 110, 210, 170], fill=(143, 188, 143, 255), width=4)

im.save("test_pram_shape.png")
print("Pram shape test image generated.")

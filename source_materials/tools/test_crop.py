from PIL import Image

im = Image.open("NO_first_frame.jpg")

# Test crop 1: medium crop
# Box format: (left, upper, right, lower)
box1 = (450, 250, 1150, 850)
im.crop(box1).save("test_crop_1.jpg")

# Test crop 2: close crop on Grogu in the cockpit
box2 = (500, 320, 1050, 770)
im.crop(box2).save("test_crop_2.jpg")

# Test crop 3: square crop centered on Grogu
box3 = (480, 280, 1080, 880)
im.crop(box3).save("test_crop_3.jpg")

print("Cropped test images generated.")

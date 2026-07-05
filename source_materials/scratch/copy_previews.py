import shutil
import os

artifacts_dir = r"C:\Users\YANQIAO\.gemini\antigravity-ide\brain\71bd9e19-837b-4572-81e1-4c753dba50f4"

# Source files (we can resolve the glob/garbled names by mapping their exact binary matches in directory listing)
shutil.copy("楗煎共_frame.png", os.path.join(artifacts_dir, "cookie1_frame.png"))
shutil.copy("楗煎共2_frame.png", os.path.join(artifacts_dir, "cookie2_frame.png"))
shutil.copy("鐑よ倝_frame.png", os.path.join(artifacts_dir, "meat_frame.png"))
shutil.copy("濞冨嵉_frame.png", os.path.join(artifacts_dir, "eggs_frame.png"))

print("Previews copied to artifacts directory.")

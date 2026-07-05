import os
import subprocess
from PIL import Image

def process_peek_clip():
    mp4_path = "grogu-focus-timer/表情包（视频）.mp4"
    output_name = "peek"
    crop_coords = "800:800:560:130"
    output_dir = "grogu-focus-timer/extension/assets"
    
    os.makedirs(output_dir, exist_ok=True)
    
    gif_path = os.path.join(output_dir, f"{output_name}_temp.gif")
    webp_path = os.path.join(output_dir, f"{output_name}.webp")
    m4a_path = os.path.join(output_dir, f"{output_name}.m4a")
    
    print(f"[+] Processing {mp4_path} -> {output_name}")
    
    # 1. Generate temp GIF with crop and palette use
    vf_filter = f"crop={crop_coords},fps=12,scale=240:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    gif_cmd = [
        "ffmpeg", "-y",
        "-i", mp4_path,
        "-vf", vf_filter,
        "-loop", "0",
        gif_path
    ]
    subprocess.run(gif_cmd, check=True)
    
    # 2. Convert GIF to WebP using Pillow
    print(f"[+] Converting GIF to WebP...")
    with Image.open(gif_path) as im:
        frames = []
        try:
            while True:
                frames.append(im.copy())
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        
        frames[0].save(
            webp_path,
            save_all=True,
            append_images=frames[1:],
            duration=83,
            loop=0,
            optimize=True
        )
    
    if os.path.exists(gif_path):
        os.remove(gif_path)
    print(f"[+] WebP saved to {webp_path}")
    
    # 3. Extract Audio
    print(f"[+] Extracting audio to {m4a_path}...")
    m4a_cmd = [
        "ffmpeg", "-y",
        "-i", mp4_path,
        "-vn",
        "-c:a", "aac",
        "-b:a", "128k",
        m4a_path
    ]
    subprocess.run(m4a_cmd, check=True)
    print("[+] Audio saved successfully!")

if __name__ == "__main__":
    process_peek_clip()

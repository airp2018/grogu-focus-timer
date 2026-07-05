import os
import subprocess
from PIL import Image

def process_random_clip(mp4_path, output_name, crop_coords, output_dir="extension/assets"):
    os.makedirs(output_dir, exist_ok=True)
    
    gif_path = os.path.join(output_dir, f"{output_name}_temp.gif")
    webp_path = os.path.join(output_dir, f"{output_name}.webp")
    m4a_path = os.path.join(output_dir, f"{output_name}.m4a")
    
    print(f"\n[+] Processing clip file: {mp4_path} -> {output_name}")
    
    # ffmpeg visual filter with spatial crop, 12fps and color palette optimization
    vf_filter = f"crop={crop_coords},fps=12,scale=240:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    
    # 1. Export High-Quality GIF using ffmpeg palettegen
    print(f"  -> 1. Generating temporary high-quality GIF...")
    gif_cmd = [
        "ffmpeg", "-y",
        "-i", mp4_path,
        "-vf", vf_filter,
        "-loop", "0",
        gif_path
    ]
    result_gif = subprocess.run(gif_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result_gif.returncode != 0:
        print("  [Error] Temporary GIF generation failed:")
        print(result_gif.stderr.decode('utf-8', errors='ignore'))
        return False
        
    # 2. Convert GIF to WebP using Pillow
    print(f"  -> 2. Converting GIF to WebP: {webp_path}")
    try:
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
                duration=83,  # 12fps -> ~83ms
                loop=0,
                optimize=True
            )
        
        if os.path.exists(gif_path):
            os.remove(gif_path)
        print(f"  -> Successfully generated WebP! (Size: {os.path.getsize(webp_path)} bytes)")
    except Exception as e:
        print(f"  [Warning] WebP conversion failed: {e}. Keeping GIF instead.")
        
    # 3. Extract audio as M4A (AAC format)
    print(f"  -> 3. Extracting audio to M4A: {m4a_path}")
    m4a_cmd = [
        "ffmpeg", "-y",
        "-i", mp4_path,
        "-vn",
        "-c:a", "aac",
        "-b:a", "128k",
        m4a_path
    ]
    result_audio = subprocess.run(m4a_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result_audio.returncode != 0:
        print("  [Error] Audio extraction failed:")
        print(result_audio.stderr.decode('utf-8', errors='ignore'))
        return False
        
    print(f"  -> Clip [{output_name}] complete!")
    return True

def main():
    clips_config = [
        {"file": "饼干.mp4",  "out": "cookie1", "crop": "800:800:820:140"},
        {"file": "饼干2.mp4", "out": "cookie2", "crop": "800:800:530:100"},
        {"file": "烤肉.mp4",  "out": "meat",    "crop": "600:600:1000:200"},
        {"file": "娃卵.mp4",  "out": "eggs",    "crop": "600:600:700:250"}
    ]
    
    for config in clips_config:
        if os.path.exists(config["file"]):
            process_random_clip(config["file"], config["out"], config["crop"])
        else:
            print(f"Error: file {config['file']} does not exist in root directory.")

if __name__ == "__main__":
    main()

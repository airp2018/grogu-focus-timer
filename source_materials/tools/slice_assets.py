import os
import subprocess
from PIL import Image

def slice_asset(video_path, start_time, end_time, name, output_dir="extension/assets"):
    os.makedirs(output_dir, exist_ok=True)
    
    gif_path = os.path.join(output_dir, f"{name}.gif")
    webp_path = os.path.join(output_dir, f"{name}.webp")
    m4a_path = os.path.join(output_dir, f"{name}.m4a")
    
    print(f"\n[+] Processing [{name}] ({start_time} to {end_time})...")
    
    # 1. Export High-Quality GIF using ffmpeg palettegen
    print(f"  -> Generating high-quality GIF: {gif_path}")
    gif_cmd = [
        "ffmpeg", "-y",
        "-ss", start_time,
        "-to", end_time,
        "-i", video_path,
        "-vf", "fps=12,scale=240:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        "-loop", "0",
        gif_path
    ]
    result_gif = subprocess.run(gif_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result_gif.returncode != 0:
        print("  [Error] GIF generation failed:")
        print(result_gif.stderr.decode('utf-8', errors='ignore'))
        return False
        
    # 2. Convert GIF to WebP using Pillow (for smaller file size and native webp loading)
    print(f"  -> Converting GIF to WebP: {webp_path}")
    try:
        with Image.open(gif_path) as im:
            frames = []
            try:
                while True:
                    frames.append(im.copy())
                    im.seek(im.tell() + 1)
            except EOFError:
                pass
            
            # Save as animated webp
            # Duration per frame is roughly 1000ms / fps (1000 / 12 = 83ms)
            frames[0].save(
                webp_path,
                save_all=True,
                append_images=frames[1:],
                duration=83,
                loop=0,
                optimize=True
            )
            print(f"  -> Successfully created WebP! (Size: {os.path.getsize(webp_path)} bytes)")
            
            # Clean up the intermediate GIF to save space
            os.remove(gif_path)
    except Exception as e:
        print(f"  [Warning] WebP conversion failed: {e}. Keeping GIF instead.")
        
    # 3. Export M4A audio (using standard AAC encoder)
    print(f"  -> Extracting audio to M4A: {m4a_path}")
    m4a_cmd = [
        "ffmpeg", "-y",
        "-ss", start_time,
        "-to", end_time,
        "-i", video_path,
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
        
    print(f"  -> Success processing [{name}]!")
    return True

if __name__ == "__main__":
    v1 = "raw_assets/【曼达洛人】古古奶音音合集（第一季）.mp4"
    
    # Define our targeted assets
    assets_to_slice = [
        # 1. 喝汤 (用于休息时间/休息提醒)
        {"start": "00:00:29", "end": "00:00:34", "name": "soup"},
        # 2. 玩飞船金属球 (用于工作状态)
        {"start": "00:00:39", "end": "00:00:44", "name": "knob"},
        # 3. 使用原力 (用于计时结束/强力提醒)
        {"start": "00:01:12", "end": "00:01:17", "name": "force"},
        # 4. 吃青蛙 (额外备选趣味表情)
        {"start": "00:00:50", "end": "00:00:55", "name": "frog"}
    ]
    
    success_count = 0
    for asset in assets_to_slice:
        if slice_asset(v1, asset["start"], asset["end"], asset["name"]):
            success_count += 1
            
    print(f"\nProcessing complete. Successfully generated {success_count} assets.")

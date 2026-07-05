import os
import subprocess
import glob
from PIL import Image

def process_single_clip(mp4_path, output_dir="extension/assets"):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(mp4_path)
    name, _ = os.path.splitext(filename)
    
    gif_path = os.path.join(output_dir, f"{name}_temp.gif")
    webp_path = os.path.join(output_dir, f"{name}.webp")
    m4a_path = os.path.join(output_dir, f"{name}.m4a")
    
    print(f"\n[+] Processing clip file: {filename}")
    
    # Check if we should apply spatial crop to zoom in on Grogu (1904x1080 fullscreen recording)
    # Target crop: 600x600 box centered at X=480, Y=280
    vf_filter = "fps=12,scale=240:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    
    if name in ["NO", "NO2", "YES"]:
        print("  -> Applying custom spatial crop to center on Grogu (600x600 square)...")
        vf_filter = "crop=600:600:480:280," + vf_filter
    
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
        
        # File is now closed. Safe to delete.
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
        
    print(f"  -> Clip [{name}] processing complete!")
    return True

def main():
    # Process files in root directory first if they exist
    for name in ["NO", "NO2", "YES"]:
        mp4_file = f"{name}.mp4"
        if os.path.exists(mp4_file):
            process_single_clip(mp4_file)
            
    input_dir = "raw_assets/my_clips"
    os.makedirs(input_dir, exist_ok=True)
    
    # Scan for MP4s in my_clips
    mp4_files = glob.glob(os.path.join(input_dir, "*.mp4"))
    
    if not mp4_files:
        return
        
    print(f"\n[+] Found {len(mp4_files)} custom clips in '{input_dir}'. Processing...")
    success_count = 0
    for mp4_file in mp4_files:
        if process_single_clip(mp4_file):
            success_count += 1
            
    print(f"\nConversion finished.")

if __name__ == "__main__":
    main()

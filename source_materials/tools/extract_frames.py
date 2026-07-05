import os
import subprocess
import glob

def extract_and_rename_frames(video_path, output_dir, interval=5):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Extracting frames from {video_path} to {output_dir}...")
    
    # 1. Use ffmpeg to extract frames every 'interval' seconds
    # Named temp_frame_001.jpg, temp_frame_002.jpg, ...
    temp_pattern = os.path.join(output_dir, "temp_frame_%03d.jpg")
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"fps=1/{interval},scale=480:-1",
        "-vsync", "vfr",
        temp_pattern
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running ffmpeg: {result.stderr.decode('utf-8', errors='ignore')}")
        return False
        
    # 2. Rename files to represent exact timestamps
    temp_files = sorted(glob.glob(os.path.join(output_dir, "temp_frame_*.jpg")))
    print(f"Extracted {len(temp_files)} frames. Renaming with timestamps...")
    
    for i, filepath in enumerate(temp_files):
        # Calculate time in seconds
        seconds = i * interval
        minutes = seconds // 60
        secs = seconds % 60
        
        new_filename = f"{minutes:02d}m{secs:02d}s.jpg"
        new_filepath = os.path.join(output_dir, new_filename)
        
        if os.path.exists(new_filepath):
            os.remove(new_filepath)
        os.rename(filepath, new_filepath)
        
    print(f"Done renaming! Keyframes saved in: {output_dir}")
    return True

if __name__ == "__main__":
    v1 = "raw_assets/【曼达洛人】古古奶音音合集（第一季）.mp4"
    v2 = "raw_assets/【曼达洛人】古古奶音音合集（第二季第一部分）.mp4"
    
    extract_and_rename_frames(v1, "raw_assets/keyframes/video1")
    extract_and_rename_frames(v2, "raw_assets/keyframes/video2")
    
    v3 = "raw_assets/grogu_memes_compile.mp4"
    extract_and_rename_frames(v3, "raw_assets/keyframes/video3", interval=3)


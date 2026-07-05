import subprocess

def extract_first_frame(video_path, output_image):
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vframes", "1",
        output_image
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Extracted first frame of {video_path} to {output_image}")

if __name__ == "__main__":
    extract_first_frame("NO.mp4", "NO_first_frame.jpg")
    extract_first_frame("NO2.mp4", "NO2_first_frame.jpg")

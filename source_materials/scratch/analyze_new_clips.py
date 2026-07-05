import cv2
import os
import glob

clips = ["饼干.mp4", "饼干2.mp4", "烤肉.mp4", "娃卵.mp4"]

print("Analyzing clip resolutions and generating frame previews...")

for clip in clips:
    if not os.path.exists(clip):
        print(f"Error: {clip} not found in workspace root.")
        continue
        
    cap = cv2.VideoCapture(clip)
    if not cap.isOpened():
        print(f"Error opening {clip}")
        continue
        
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"\nClip: {clip}")
    print(f"  Resolution: {width}x{height}")
    print(f"  Total Frames: {total_frames}")
    print(f"  FPS: {fps:.2f}")
    
    # Read frame from the middle of the video
    middle_frame_idx = total_frames // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_idx)
    ret, frame = cap.read()
    
    if ret:
        name, _ = os.path.splitext(clip)
        preview_path = f"{name}_frame.png"
        cv2.imwrite(preview_path, frame)
        print(f"  Saved preview to {preview_path}")
    else:
        print(f"  Failed to read frame at index {middle_frame_idx}")
        
    cap.release()

import os
import glob

def generate_gallery(keyframes_root, output_html_path):
    print("Generating gallery HTML...")
    
    # CSS & HTML Template
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>古古表情包选片室 - Grogu Focus Timer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #121214;
            color: #e2e8f0;
            margin: 0;
            padding: 20px;
        }
        header {
            text-align: center;
            padding: 30px 0;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            border: 1px solid #334155;
        }
        h1 {
            margin: 0;
            color: #8fbc8f;
            font-size: 2.5rem;
            text-shadow: 0 0 10px rgba(143,188,143,0.3);
        }
        p.subtitle {
            color: #94a3b8;
            margin-top: 10px;
        }
        .section-title {
            font-size: 1.8rem;
            margin: 40px 0 20px;
            border-bottom: 2px solid #8fbc8f;
            padding-bottom: 10px;
            color: #cbd5e1;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }
        .card {
            background-color: #1e293b;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #334155;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
            border-color: #8fbc8f;
        }
        .card img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            background-color: #0f172a;
            display: block;
        }
        .card-info {
            padding: 10px;
            text-align: center;
            background-color: #0f172a;
            font-weight: bold;
            font-size: 0.9rem;
            color: #8fbc8f;
        }
    </style>
</head>
<body>
    <header>
        <h1>🟢 古古表情包选片室 🟢</h1>
        <p class="subtitle">每 5 秒自动截取一帧。请预览并挑选出您想剪辑成表情包或音效的画面对应的时间戳！</p>
    </header>
"""

    for video_id in ["video1", "video2", "video3"]:
        if video_id == "video1":
            dir_name = "第一季 (第一部)"
        elif video_id == "video2":
            dir_name = "第二季 (第二部)"
        else:
            dir_name = "本地表情包集合 (第三部 - 每3秒一帧)"
        html_content += f'<h2 class="section-title">{dir_name}</h2>'
        html_content += '<div class="grid">'
        
        img_dir = os.path.join(keyframes_root, video_id)
        # Find all jpg files
        jpg_files = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))
        
        for filepath in jpg_files:
            filename = os.path.basename(filepath)
            # Make path relative to HTML location (assuming HTML is in tools/ or project root)
            # If HTML is in the project root: raw_assets/keyframes/{video_id}/{filename}
            rel_path = f"raw_assets/keyframes/{video_id}/{filename}"
            timestamp = filename.replace(".jpg", "")
            
            html_content += f"""
            <div class="card">
                <img src="{rel_path}" alt="{timestamp}">
                <div class="card-info">{timestamp}</div>
            </div>"""
            
        html_content += '</div>'
        
    html_content += """
</body>
</html>
"""
    
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Gallery HTML generated at: {output_html_path}")

if __name__ == "__main__":
    generate_gallery("raw_assets/keyframes", "gallery.html")

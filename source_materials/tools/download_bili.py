import urllib.request
import json
import ssl
import re
import os
import subprocess

def download_bili_video(bvid, output_dir="raw_assets"):
    os.makedirs(output_dir, exist_ok=True)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    context = ssl._create_unverified_context()
    
    print(f"\n[1/4] 获取视频 {bvid} 信息...")
    view_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    req = urllib.request.Request(view_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, context=context, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data['code'] != 0:
                print(f"Error: API 返回错误代码 {data['code']}: {data['message']}")
                return False
            
            aid = data['data']['aid']
            cid = data['data']['pages'][0]['cid']
            title = data['data']['title']
            # Clean title for filename
            clean_title = re.sub(r'[\\/*?:"<>|]', "", title).strip()
            print(f"成功! 视频标题: {clean_title} (AID: {aid}, CID: {cid})")
    except Exception as e:
        print(f"获取视频基本信息失败: {e}")
        return False
        
    print(f"\n[2/4] 获取流媒体播放地址...")
    play_url = f"https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=32&fnval=16"
    req_play = urllib.request.Request(play_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req_play, context=context, timeout=15) as resp:
            play_data = json.loads(resp.read().decode('utf-8'))
            if play_data['code'] != 0:
                print(f"Error: 无法获取播放地址 {play_data['message']}")
                return False
            
            dash = play_data['data']['dash']
            video_url = dash['video'][0]['baseUrl']
            audio_url = dash['audio'][0]['baseUrl']
            print("播放地址获取成功！")
    except Exception as e:
        print(f"获取播放地址失败: {e}")
        return False

    temp_video = os.path.join(output_dir, f"temp_{bvid}_video.m4s")
    temp_audio = os.path.join(output_dir, f"temp_{bvid}_audio.m4s")
    final_output = os.path.join(output_dir, f"{clean_title}.mp4")

    # Helper function to download stream in chunks
    def download_stream(url, filepath, stream_name):
        print(f"下载 {stream_name}...")
        req_stream = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req_stream, context=context, timeout=30) as resp:
            total_size = int(resp.headers.get('content-length', 0))
            downloaded = 0
            block_size = 1024 * 64
            with open(filepath, 'wb') as f:
                while True:
                    buffer = resp.read(block_size)
                    if not buffer:
                        break
                    f.write(buffer)
                    downloaded += len(buffer)
                    if total_size > 0:
                        percent = downloaded * 100 / total_size
                        print(f"\r进度: {percent:.1f}% ({downloaded}/{total_size} 字节)", end='')
            print()

    print(f"\n[3/4] 开始下载音视频分流数据...")
    try:
        download_stream(video_url, temp_video, "视频轨道")
        download_stream(audio_url, temp_audio, "音频轨道")
    except Exception as e:
        print(f"\n下载流媒体失败: {e}")
        # Clean up
        if os.path.exists(temp_video): os.remove(temp_video)
        if os.path.exists(temp_audio): os.remove(temp_audio)
        return False

    print(f"\n[4/4] 使用 ffmpeg 合并音视频...")
    try:
        # ffmpeg -y -i video.m4s -i audio.m4s -c:v copy -c:a aac -strict experimental output.mp4
        cmd = [
            "ffmpeg", "-y",
            "-i", temp_video,
            "-i", temp_audio,
            "-c:v", "copy",
            "-c:a", "aac",
            final_output
        ]
        # Run command silently
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"🎉 视频下载合并成功！保存为: {final_output}")
            success = True
        else:
            print(f"合并视频失败，ffmpeg 错误代码: {result.returncode}")
            print(result.stderr.decode('utf-8', errors='ignore'))
            success = False
    except Exception as e:
        print(f"调用 ffmpeg 合并失败: {e}")
        success = False
    finally:
        # Cleanup temp files
        if os.path.exists(temp_video): os.remove(temp_video)
        if os.path.exists(temp_audio): os.remove(temp_audio)
        
    return success

if __name__ == "__main__":
    import sys
    bvids = ["BV1TDEH6WEJZ", "BV1oHEb6xE4B"]
    for bvid in bvids:
        print("="*50)
        print(f"正在处理: {bvid}")
        download_bili_video(bvid)

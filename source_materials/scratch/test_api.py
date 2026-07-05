import urllib.request
import json
import ssl
import sys

bvid = "BV1TDEH6WEJZ"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}
context = ssl._create_unverified_context()

try:
    print("Fetching view info for:", bvid)
    view_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    req = urllib.request.Request(view_url, headers=headers)
    with urllib.request.urlopen(req, context=context, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        if data['code'] == 0:
            aid = data['data']['aid']
            cid = data['data']['pages'][0]['cid']
            title = data['data']['title']
            print(f"Success! Title: {title}, AID: {aid}, CID: {cid}")
            
            # Fetch play url
            play_url = f"https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=32&fnval=16"
            print("Fetching playurl from:", play_url)
            req2 = urllib.request.Request(play_url, headers=headers)
            with urllib.request.urlopen(req2, context=context, timeout=10) as resp2:
                play_data = json.loads(resp2.read().decode('utf-8'))
                if play_data['code'] == 0:
                    print("Success fetching play url data!")
                    dash = play_data['data']['dash']
                    print("Dash videos:", len(dash['video']))
                    print("Dash audios:", len(dash['audio']))
                    print("Video URL 1:", dash['video'][0]['baseUrl'])
                    print("Audio URL 1:", dash['audio'][0]['baseUrl'])
                else:
                    print("Playurl API error:", play_data)
        else:
            print("View API error:", data)
except Exception as e:
    print("Error:", e)

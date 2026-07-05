import urllib.request
import re
import json
import ssl
import sys

print("Python version:", sys.version)
url = "https://www.bilibili.com/video/BV1TDEH6WEJZ/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}

context = ssl._create_unverified_context()
req = urllib.request.Request(url, headers=headers)
try:
    print("Sending request to:", url)
    with urllib.request.urlopen(req, context=context, timeout=10) as response:
        print("Response code:", response.getcode())
        html = response.read().decode('utf-8')
        print("Successfully fetched HTML. Length:", len(html))
        
        # Try to find window.__playinfo__
        playinfo_match = re.search(r'window\.__playinfo__\s*=\s*({.*?})\s*</script>', html)
        if playinfo_match:
            print("Found __playinfo__!")
            playinfo = json.loads(playinfo_match.group(1))
            print("Keys in playinfo:", playinfo.keys())
        else:
            print("window.__playinfo__ not found in page source.")
except Exception as e:
    print("Error during fetch:", e)

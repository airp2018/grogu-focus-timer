import urllib.request
import ssl
import socket

print("Testing network...")
context = ssl._create_unverified_context()
try:
    print("Fetching httpbin.org...")
    with urllib.request.urlopen("https://httpbin.org/ip", context=context, timeout=3) as resp:
        print("Success httpbin:", resp.read().decode())
except Exception as e:
    print("Error httpbin:", e)

try:
    print("Fetching baidu.com...")
    with urllib.request.urlopen("https://www.baidu.com", context=context, timeout=3) as resp:
        print("Success baidu: length", len(resp.read()))
except Exception as e:
    print("Error baidu:", e)

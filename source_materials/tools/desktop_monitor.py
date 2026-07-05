import ctypes
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys

# Windows API calls to get the foreground window title
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def get_active_window_title():
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return ""
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value

# Lightweight HTTP request handler with CORS enabled
class MonitorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/active':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow browser extension calls
            self.end_headers()
            
            title = get_active_window_title()
            
            # Simple app detection based on window title suffix
            app_name = ""
            if " - " in title:
                app_name = title.split(" - ")[-1]
                
            response = {
                "title": title,
                "app": app_name
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    # Disable logging requests to console to keep it clean
    def log_message(self, format, *args):
        return

def run(port=8001):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, MonitorHandler)
    print(f"==================================================")
    print(f"🟢 古古桌面应用监控服务已开启 🟢")
    print(f"运行在: http://127.0.0.1:{port}/active")
    print(f"这个脚本会默默监测你当前活跃的系统窗口标题，并报告给插件。")
    print(f"按 Ctrl+C 可以退出服务。")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n正在关闭监控服务...")
        httpd.server_close()

if __name__ == "__main__":
    port_arg = 8001
    if len(sys.argv) > 1:
        try:
            port_arg = int(sys.argv[1])
        except ValueError:
            pass
    run(port=port_arg)

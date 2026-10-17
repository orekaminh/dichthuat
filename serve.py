import http.server
import socketserver


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    # Không cho trình duyệt lưu bản cũ của trang
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8765), NoCacheHandler) as httpd:
    httpd.serve_forever()

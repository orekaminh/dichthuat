"""
Phiên dịch trực tiếp — chương trình khởi chạy để đóng gói thành .exe chia sẻ.

Chạy một máy chủ web nhỏ ngay trên máy (chỉ phục vụ nội bộ 127.0.0.1, không ai
từ bên ngoài truy cập được), rồi mở trang index.html bằng Google Chrome ở chế
độ "--app" (cửa sổ gọn, không có thanh địa chỉ, giống một ứng dụng riêng).

Máy nhận vẫn cần cài sẵn Google Chrome: phần nhận dạng giọng nói dùng dịch vụ
nhận dạng có sẵn trong Chrome, trình duyệt khác hoặc Chrome đóng gói riêng
(Chromium/Electron) sẽ không có tính năng này.
"""
import http.server
import os
import shutil
import socket
import socketserver
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from tkinter import messagebox


def resource_path(name):
    # Khi đóng gói bằng PyInstaller (--onefile), file đi kèm được giải nén
    # vào một thư mục tạm, đường dẫn đó nằm trong sys._MEIPASS.
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=resource_path("."), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # không có cửa sổ console để in ra, nên im lặng luôn


def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def find_chrome():
    candidates = [
        os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"),
                     "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                     "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("LocalAppData", ""),
                     "Google", "Chrome", "Application", "chrome.exe"),
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return shutil.which("chrome")


def main():
    port = free_port()
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), QuietHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/index.html"
    chrome = find_chrome()

    root = tk.Tk()
    root.title("Phiên dịch trực tiếp")
    root.geometry("440x230")
    root.resizable(False, False)
    try:
        root.iconbitmap(resource_path("app.ico"))
    except Exception:
        pass

    tk.Label(root, text="🎧 Phiên dịch trực tiếp", font=("Segoe UI", 17, "bold")).pack(pady=(20, 6))
    tk.Label(root, text="Đang chạy…", font=("Segoe UI", 11), fg="#15803d").pack()
    tk.Label(
        root,
        text="Giữ cửa sổ nhỏ này mở trong suốt buổi họp.\nĐóng cửa sổ này sẽ tắt luôn chương trình.",
        font=("Segoe UI", 10), fg="#555", justify="center",
    ).pack(pady=12)

    def open_browser():
        if chrome:
            subprocess.Popen([chrome, f"--app={url}"])
        else:
            webbrowser.open(url)

    tk.Button(root, text="Mở lại cửa sổ phiên dịch", font=("Segoe UI", 10),
              command=open_browser).pack(pady=4)

    def on_close():
        httpd.shutdown()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    if not chrome:
        messagebox.showwarning(
            "Thiếu Google Chrome",
            "Không tìm thấy Google Chrome trên máy này.\n\n"
            "Chương trình cần Google Chrome để nghe và nhận dạng giọng nói, "
            "trình duyệt khác (Edge, Cốc Cốc, Firefox…) sẽ không dùng được.\n\n"
            "Hãy cài Chrome tại https://www.google.com/chrome/ rồi mở lại chương trình.",
        )

    open_browser()
    root.mainloop()


if __name__ == "__main__":
    main()

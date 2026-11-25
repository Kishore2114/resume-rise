"""Serve ResumeRise locally. Run: python serve.py"""
import functools
import http.server
import socket
import socketserver
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
START_PORT = 8000


def free_port(host, start):
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
            except OSError:
                continue
            return port
    raise SystemExit("No free port between %s and %s." % (start, start + 19))


def main():
    port = free_port(HOST, START_PORT)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    url = "http://%s:%s/index.html" % (HOST, port)

    with socketserver.TCPServer((HOST, port), handler) as httpd:
        print("ResumeRise is running.", flush=True)
        print("Open this address in your browser:", flush=True)
        print("  " + url, flush=True)
        print("Leave this window open. Press Ctrl+C to stop.", flush=True)
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()

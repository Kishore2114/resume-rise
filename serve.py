"""Serve ResumeRise locally. Run: python serve.py"""
import functools
import http.server
import json
import os
import socket
import socketserver
import threading
import urllib.error
import urllib.request
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


class ResumeRiseHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/chat/completions":
            self.send_error(404)
            return

        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))

            ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
            try:
                ollama_request = urllib.request.Request(
                    "http://127.0.0.1:11434/api/chat",
                    data=json.dumps({
                        "model": ollama_model,
                        "messages": body.get("messages", []),
                        "stream": False,
                        "options": {"temperature": body.get("temperature", 0.2)},
                    }).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(ollama_request, timeout=120) as response:
                    local = json.loads(response.read().decode("utf-8"))
                    text = local.get("message", {}).get("content", "")
                    self.send_json(response.status, {"choices": [{"message": {"role": "assistant", "content": text}}]})
                return
            except (urllib.error.URLError, TimeoutError):
                pass

            if not api_key:
                self.send_json(503, {"error": {"message": "No local model is available. Install Ollama, then run: ollama pull llama3.2:3b"}})
                return

            model = body.get("model") or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
            payload = json.dumps({
                "model": model,
                "temperature": body.get("temperature", 0.2),
                "messages": body.get("messages", []),
            }).encode("utf-8")

            request = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=payload,
                headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=120) as response:
                response_body = json.loads(response.read().decode("utf-8"))
                self.send_json(response.status, response_body)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            try:
                detail = json.loads(detail)
            except json.JSONDecodeError:
                pass
            self.send_json(exc.code, detail)
        except (json.JSONDecodeError, urllib.error.URLError, TimeoutError) as exc:
            self.send_json(502, {"error": {"message": str(exc)}})

    def send_json(self, status, body):
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    port = free_port(HOST, START_PORT)
    handler = functools.partial(ResumeRiseHandler, directory=str(ROOT))
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

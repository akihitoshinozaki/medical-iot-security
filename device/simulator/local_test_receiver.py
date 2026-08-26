#!/usr/bin/env python3
"""Throwaway local receiver for testing the simulator + capture pipeline.

This is NOT Aki's receiving server - it's a stand-in so the traffic
contract, simulator, and capture/export pipeline can be exercised
end-to-end before Aki's real endpoint exists. Swap --url in
simulate_device.py to point at the real one once it's up.

Usage:
    python3 local_test_receiver.py
    python3 local_test_receiver.py --port 8765
"""

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class IngestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            reading = json.loads(body)
            print(f"received {reading}")
        except json.JSONDecodeError:
            print(f"received non-JSON body ({length} bytes)")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

    def log_message(self, format, *args):
        pass  # quiet the default per-request access log; we print above instead


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = HTTPServer(("0.0.0.0", args.port), IngestHandler)
    print(f"Listening on http://0.0.0.0:{args.port}/ingest (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")


if __name__ == "__main__":
    main()

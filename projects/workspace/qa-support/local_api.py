"""Bounded loopback API for the ArchVerity API Client fixture."""

import argparse
import json
import re
import time
from urllib.parse import parse_qsl, urlsplit
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def log_message(self, _format, *_args):
        pass

    def respond(self, status, payload):
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == "/health" and not parsed.query:
            self.respond(200, {"status": "ok", "fixture": "archverity-validation"})
        elif parsed.path == "/qa-openapi" and not parsed.query:
            self.respond(200, {"source": "openapi", "status": "ok"})
        elif parsed.path == "/qa-slow":
            try:
                values = parse_qsl(parsed.query, keep_blank_values=True, strict_parsing=True)
            except ValueError:
                values = []
            if len(values) != 1 or values[0][0] != "delay_ms" or re.fullmatch(r"[0-9]{1,4}", values[0][1]) is None:
                self.respond(400, {"error": "delay_ms must be an integer from 0 to 5000"})
                return
            delay_ms = int(values[0][1])
            if delay_ms > 5000:
                self.respond(400, {"error": "delay_ms must be an integer from 0 to 5000"})
                return
            time.sleep(delay_ms / 1000)
            try:
                self.respond(200, {"source": "slow", "delay_ms": delay_ms})
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                # A client-side Cancel is the expected result for this fixture route.
                pass
        else:
            self.respond(404, {"error": "unknown fixture path"})

    def do_POST(self):
        if self.path not in ("/qa-roundtrip", "/qa-postman"):
            self.respond(404, {"error": "unknown fixture path"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 32768:
                self.respond(413, {"error": "request body must be 1..32768 bytes"})
                return
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise ValueError("JSON object required")
        except (ValueError, json.JSONDecodeError):
            self.respond(400, {"error": "valid JSON object required"})
            return
        self.respond(200, {"source": self.path.removeprefix("/"), "received": payload})


def make_server(port=18427):
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=18427)
    args = parser.parse_args()
    with make_server(args.port) as server:
        print(f"ArchVerity QA API: http://127.0.0.1:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

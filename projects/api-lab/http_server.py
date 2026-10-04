"""HTTP imports share the workspace's API; add deterministic scenario routes."""

import json
import sys
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "workspace/qa-support"))
from local_api import Handler as WorkspaceHandler


class Handler(WorkspaceHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == "/items/42":
            self.respond(200, {"id": 42, "name": "demo", "enabled": True, "optional": None})
        elif parsed.path == "/cookies/set":
            body = b'{"cookieSet":true}'
            self.send_response(200)
            self.send_header("Set-Cookie", "demo_cookie=archverity; Path=/; HttpOnly; SameSite=Lax")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif parsed.path == "/cookies/show":
            cookie = self.headers.get("Cookie", "")
            self.respond(200, {"hasDemoCookie": "demo_cookie=archverity" in cookie.split("; ")})
        elif parsed.path == "/headers":
            self.respond(200, {"hasAuthorization": bool(self.headers.get("Authorization")),
                               "demoHeader": self.headers.get("X-Demo", "")[:128]})
        elif parsed.path == "/error":
            self.respond(500, {"error": "intentional demo failure"})
        elif parsed.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/health")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif parsed.path == "/large":
            try:
                size = int(parse_qs(parsed.query).get("bytes", ["4096"])[0])
            except ValueError:
                self.respond(400, {"error": "bytes must be 1..1000000"})
                return
            if not 1 <= size <= 1_000_000:
                self.respond(400, {"error": "bytes must be 1..1000000"})
                return
            self.respond(200, {"data": "x" * size})
        else:
            super().do_GET()


def make_server(port=18427):
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)

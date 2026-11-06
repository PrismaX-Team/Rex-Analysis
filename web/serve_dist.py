#!/usr/bin/env python3
"""Serve dist/ as a single-page app.

Extensionless paths get index.html so a deep route like /rcb/1.0/tasks/Physics_001 survives a refresh.
"""

from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


# Not in every Python's mimetypes table.
SimpleHTTPRequestHandler.extensions_map.update({".webp": "image/webp", ".woff2": "font/woff2"})


def make_handler(directory: Path):
    root = directory.resolve()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root), **kwargs)

        def do_GET(self) -> None:
            path = self.path.split("?", 1)[0]
            target = (root / path.lstrip("/")).resolve()
            inside = target == root or root in target.parents
            if inside and path not in ("/", "") and not path.endswith("/") and not Path(path).suffix:
                index = target / "index.html" if target.is_dir() else root / "index.html"
                if index.is_file():
                    body = index.read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
            super().do_GET()

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8090)
    parser.add_argument("--directory", default="dist")
    args = parser.parse_args()
    directory = Path(args.directory).resolve()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(directory))
    print(f"serving {directory} on {args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

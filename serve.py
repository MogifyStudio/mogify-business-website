#!/usr/bin/env python3
"""Local preview server for the static site in ./site.

Supports the clean URLs the live site uses (/about -> about.html, /services/logo-design -> services/logo-design.html)
and serves 404.html for missing pages.

    python3 serve.py            # http://localhost:8000
    python3 serve.py 8080       # custom port
"""
import http.server, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "site")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split("?", 1)[0].split("#", 1)[0]
        fs = os.path.join(ROOT, p.lstrip("/"))
        if os.path.isdir(fs) and os.path.isfile(os.path.join(fs, "index.html")):
            return os.path.join(fs, "index.html")
        if os.path.isfile(fs):
            return fs
        if os.path.isfile(fs.rstrip("/") + ".html"):
            return fs.rstrip("/") + ".html"
        return os.path.join(ROOT, "404.html")


if __name__ == "__main__":
    print(f"Serving {ROOT} at http://localhost:{PORT}  (Ctrl+C to stop)")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()

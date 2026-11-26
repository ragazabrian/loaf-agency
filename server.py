#!/usr/bin/env python3
"""
Loaf Agency Local Development & Preview Server
Handles SPA routing, static assets, and mocks the ACF WordPress API endpoint.

Usage:
    python3 server.py [port]
"""

import http.server
import socketserver
import os
import sys
import mimetypes

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Ensure additional mimetypes
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("font/woff", ".woff")
mimetypes.add_type("font/otf", ".otf")
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("image/svg+xml", ".svg")

class LoafRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS for local testing
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        clean_path = self.path.split("?")[0].rstrip("/")

        # Handle WP Global ACF API endpoint
        if clean_path in ("/wp-json/acf/v3/global", "/wp-json/acf/v3/global.json", "/api/global.json"):
            json_file = os.path.join(DIRECTORY, "wp-json", "acf", "v3", "global.json")
            if not os.path.exists(json_file):
                json_file = os.path.join(DIRECTORY, "wp-json", "acf", "v3", "global")
            if os.path.exists(json_file):
                with open(json_file, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(content)
                return

        # Check if requested path exists directly
        requested_file = os.path.join(DIRECTORY, self.path.lstrip("/").split("?")[0])
        if os.path.isfile(requested_file):
            return super().do_GET()

        # Check for pre-rendered route/index.html
        route_index = os.path.join(DIRECTORY, self.path.lstrip("/").split("?")[0], "index.html")
        if os.path.isfile(route_index):
            self.path = "/" + os.path.relpath(route_index, DIRECTORY)
            return super().do_GET()

        # SPA fallback to root index.html for unknown routes
        self.path = "/index.html"
        return super().do_GET()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), LoafRequestHandler) as httpd:
        print("==================================================")
        print(f" Loaf Agency Local Server running at:")
        print(f" http://localhost:{PORT}")
        print(f" Serving directory: {DIRECTORY}")
        print(" Press Ctrl+C to stop.")
        print("==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run()

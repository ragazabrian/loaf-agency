#!/usr/bin/env python3
"""
Loaf Agency Site Cloner
Downloads all HTML routes, static assets, fonts, media, and CMS data from https://loaf.agency/
"""

import os
import sys
import re
import urllib.request
import urllib.error
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://loaf.agency"
WP_URL = "https://wp.loaf.agency"
TARGET_DIR = os.path.dirname(os.path.abspath(__file__))
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

def fetch_url(url, as_bytes=False):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            if as_bytes:
                return content
            return content.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def save_file(rel_path, content, is_bytes=False):
    abs_path = os.path.join(TARGET_DIR, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    mode = "wb" if is_bytes else "w"
    encoding = None if is_bytes else "utf-8"
    with open(abs_path, mode, encoding=encoding) as f:
        f.write(content)
    print(f"Saved: {rel_path} ({len(content)} bytes)")

def download_asset(url, rel_path):
    data = fetch_url(url, as_bytes=True)
    if data:
        save_file(rel_path, data, is_bytes=True)
        return True
    return False

def main():
    print("=== 1. Fetching Sitemap and Pages ===")
    sitemap_xml = fetch_url(f"{BASE_URL}/sitemap.xml")
    if sitemap_xml:
        save_file("sitemap.xml", sitemap_xml)
        urls = re.findall(r"<loc>(https?://[^<]+)</loc>", sitemap_xml)
    else:
        urls = [BASE_URL]
    
    print(f"Found {len(urls)} pages in sitemap.")
    
    # Robots.txt
    robots = fetch_url(f"{BASE_URL}/robots.txt")
    if robots:
        save_file("robots.txt", robots)

    # 2. Download Static Bundles and Media
    static_files = [
        # CSS & JS
        "/static/css/app.74dcd457e3fdb84dafd6f3cbab7bda41.css",
        "/static/css/app.74dcd457e3fdb84dafd6f3cbab7bda41.css.map",
        "/static/js/manifest.2ae2e69a05c33dfc65f8.js",
        "/static/js/manifest.2ae2e69a05c33dfc65f8.js.map",
        "/static/js/vendor.cb614c02cbf9e1d98346.js",
        "/static/js/vendor.cb614c02cbf9e1d98346.js.map",
        "/static/js/app.f48c5d85b67754881d31.js",
        "/static/js/app.f48c5d85b67754881d31.js.map",
        # Fonts
        "/static/fonts/Apercu-Mono.1bd0efe.woff",
        "/static/fonts/Apercu-Mono.66402a7.otf",
        "/static/fonts/Apercu-Mono.f807d15.woff2",
        "/static/fonts/CircularStd-Book.981f110.woff",
        "/static/fonts/CircularStd-Book.9da2e9e.woff2",
        "/static/fonts/CircularStd-Medium.6ba84e1.woff2",
        "/static/fonts/CircularStd-Medium.930d01b.woff",
        "/static/fonts/union-regular-webfont.599d21a.woff2",
        "/static/fonts/union-regular-webfont.c1a9e8c.woff",
        # Media
        "/static/media/Bubble-compressed.e87e12d.mp4",
        "/static/media/flower.42d3952.mp4",
        # Images
        "/img/news/preview.png",
        "/favicon.ico"
    ]

    print("\n=== 2. Downloading Core Static Assets ===")
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(download_asset, f"{BASE_URL}{path}", path): path for path in static_files}
        for future in as_completed(futures):
            path = futures[future]
            try:
                res = future.result()
            except Exception as e:
                print(f"Failed {path}: {e}")

    # 3. Download WP Global ACF Data
    print("\n=== 3. Fetching WP Global CMS Data ===")
    global_json = fetch_url(f"{WP_URL}/wp-json/acf/v3/global")
    if global_json:
        save_file("wp-json/acf/v3/global", global_json)
        save_file("wp-json/acf/v3/global.json", global_json)
        save_file("api/global.json", global_json)

    # 4. Download All Pages
    print("\n=== 4. Downloading All HTML Pages ===")
    def download_page(page_url):
        html = fetch_url(page_url)
        if not html:
            return
        parsed_path = page_url.replace(BASE_URL, "").strip("/")
        if not parsed_path:
            rel = "index.html"
        else:
            rel = f"{parsed_path}/index.html"
        save_file(rel, html)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(download_page, u) for u in urls]
        for f in as_completed(futures):
            f.result()

    print("\nDone downloading site assets!")

if __name__ == "__main__":
    main()

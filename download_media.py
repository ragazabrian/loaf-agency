#!/usr/bin/env python3
"""
Loaf Agency Remote Media Downloader
Parses wp-json/acf/v3/global.json and downloads uploaded WordPress images and media files.

Usage:
    python3 download_media.py [--max-files 100] [--include-videos]
"""

import os
import sys
import json
import re
import argparse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
GLOBAL_JSON = os.path.join(DIRECTORY, "wp-json", "acf", "v3", "global.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def extract_media_urls(obj, include_videos=False):
    urls = set()
    valid_exts = r'\.(?:jpg|jpeg|png|webp|gif|svg' + (r'|mp4|webm|mp3' if include_videos else r'') + r')'
    
    def walk(val):
        if isinstance(val, str):
            matches = re.findall(r'https?://[^\s\"\'\<\>]+\.(?:jpg|jpeg|png|webp|gif|svg|mp4|webm|mp3)', val, re.IGNORECASE)
            for m in matches:
                if re.search(valid_exts, m, re.IGNORECASE):
                    urls.add(m)
        elif isinstance(val, dict):
            for v in val.values():
                walk(v)
        elif isinstance(val, list):
            for item in val:
                walk(item)

    walk(obj)
    return sorted(urls)

def download_file(url, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return True, url, "Cached"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
        with open(target_path, "wb") as f:
            f.write(content)
        return True, url, f"Downloaded ({len(content)} bytes)"
    except Exception as e:
        return False, url, str(e)

def main():
    parser = argparse.ArgumentParser(description="Download media assets from Loaf Agency ACF global data")
    parser.add_argument("--max-files", type=int, default=50, help="Maximum number of files to download (0 for all)")
    parser.add_argument("--include-videos", action="store_true", help="Include video files (.mp4)")
    parser.add_argument("--workers", type=int, default=6, help="Parallel download threads")
    args = parser.parse_args()

    if not os.path.exists(GLOBAL_JSON):
        print(f"Error: {GLOBAL_JSON} not found. Run clone.py first.")
        sys.exit(1)

    with open(GLOBAL_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    urls = extract_media_urls(data, include_videos=args.include_videos)
    print(f"Found {len(urls)} media URLs in dataset.")

    if args.max_files > 0:
        urls = urls[:args.max_files]
        print(f"Downloading first {len(urls)} assets...")

    out_base = os.path.join(DIRECTORY, "wp-content", "uploads")
    
    tasks = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for u in urls:
            # Map wp.loaf.agency/wp-content/uploads/2026/... to local path
            if "uploads/" in u:
                rel = u.split("uploads/")[-1].split("?")[0]
            else:
                rel = os.path.basename(u.split("?")[0])
            dest = os.path.join(out_base, rel)
            tasks.append(executor.submit(download_file, u, dest))

        success = 0
        for f in as_completed(tasks):
            ok, url, msg = f.result()
            if ok:
                success += 1
                print(f"[OK] {os.path.basename(url)}: {msg}")
            else:
                print(f"[FAIL] {os.path.basename(url)}: {msg}")

    print(f"\nFinished: {success}/{len(urls)} media files ready in {out_base}")

if __name__ == "__main__":
    main()

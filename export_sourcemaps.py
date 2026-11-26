#!/usr/bin/env python3
"""
Unpack Webpack Source Maps into clean human-readable source code in src/
"""

import os
import json

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MAPS = [
    os.path.join(DIRECTORY, "static", "js", "app.f48c5d85b67754881d31.js.map"),
    os.path.join(DIRECTORY, "static", "css", "app.74dcd457e3fdb84dafd6f3cbab7bda41.css.map")
]
OUT_DIR = os.path.join(DIRECTORY, "src")

def extract():
    total_unpacked = 0
    for map_file in MAPS:
        if not os.path.exists(map_file):
            continue
        with open(map_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        sources = data.get("sources", [])
        contents = data.get("sourcesContent", [])
        if not contents:
            continue

        for s, c in zip(sources, contents):
            if not c:
                continue
            clean = s.replace("webpack:///", "").replace("./", "")
            if clean.startswith("src/"):
                clean = clean[4:]
            if "?" in clean:
                clean = clean.split("?")[0]
            target = os.path.join(OUT_DIR, clean)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8") as out:
                out.write(c)
            total_unpacked += 1

    print(f"Extracted {total_unpacked} source files into {OUT_DIR}")

if __name__ == "__main__":
    extract()

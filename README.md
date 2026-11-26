# Loaf Agency Website Clone & Source Code

> Complete clone, static mirror, and extracted Vue.js source code for [loaf.agency](https://loaf.agency/).

This repository contains the complete production website, all 59 pre-rendered routes, static assets (JS, CSS, Web Fonts, SVG, MP4 media), the full 1.1MB ACF CMS JSON dataset, and the original unminified Vue.js components unpacked from Webpack sourcemaps.

---

## 🚀 Quick Start

### 1. Run with Python (Zero Dependencies)

The included `server.py` handles SPA routing, static asset serving, and serves the local `/wp-json/acf/v3/global` mock API.

```bash
# Start local server on port 8000
python3 server.py 8000
```

Open your browser to:
👉 **[http://localhost:8000](http://localhost:8000)**

---

### 2. Run with Node.js / NPM

```bash
# Install dependencies
npm install

# Start local server
npm start
```

---

## 📂 Project Structure

```
loaf-agency/
├── index.html                   # Main SPA entry point
├── server.py                    # Python development & SPA preview server
├── clone.py                     # Automated scraping & mirroring script
├── download_media.py            # WordPress uploads media downloader
├── export_sourcemaps.py         # Sourcemap unpacker tool
├── package.json                 # Project dependencies & npm scripts
├── sitemap.xml                  # Full site XML sitemap (59 URLs)
├── robots.txt                   # Robots directives
│
├── src/                         # Extracted unminified Vue source code (116 files)
│   ├── App.vue                  # Root Vue application component
│   ├── main.js                  # App bootstrap, routing & API initialization
│   ├── seo.js                   # Dynamic meta tags & SEO updater
│   ├── utils.js                 # Helper functions
│   ├── router/                  # Vue Router configuration
│   ├── components/              # Vue pages & views (Home, Work, About, etc.)
│   │   └── modules/             # UI modules (Projects, AudioPlayer, Sliders, etc.)
│   ├── plugins/                 # GSAP animations, DrawSVGPlugin, ScrollMagic
│   └── assets/                  # SVG icons, animations, and videos
│
├── static/                      # Production compiled assets
│   ├── css/                     # Compiled styles (app.*.css + source maps)
│   ├── js/                      # Webpack bundles (manifest, vendor, app + maps)
│   ├── fonts/                   # Apercu Mono, Circular Std, Union webfonts
│   └── media/                   # Video assets (Bubble-compressed.mp4, flower.mp4)
│
├── wp-json/acf/v3/              # Full WordPress ACF REST API dataset (1.1 MB)
│   └── global.json              # Complete database of pages, case studies, and showcases
│
├── about/                       # Pre-rendered SSR route
├── work/                        # Pre-rendered Work routes (35+ case studies)
├── emotion-lab/                 # Pre-rendered Emotion Lab research articles
└── showcase/                    # Pre-rendered Industry showcase pages
```

---

## 🛠️ Python Utilities

| Script | Description |
|---|---|
| `server.py` | Built-in HTTP server supporting HTML5 history mode and local ACF API endpoints. |
| `clone.py` | Multi-threaded crawler that fetches routes, CSS, JS, fonts, media, and CMS data. |
| `download_media.py` | Scans `global.json` and optionally downloads high-res WordPress image/video uploads. |
| `export_sourcemaps.py` | Extracts Webpack source maps into human-readable Vue and JavaScript source files. |

### Optional: Download Remote WordPress Media

By default, image tags load from the live CDN at `wp.loaf.agency`. To download the media locally:

```bash
# Download first 50 images
python3 download_media.py --max-files 50

# Download all images & videos
python3 download_media.py --max-files 0 --include-videos
```

---

## 🌐 Tech Stack

- **Frontend Framework**: Vue.js 2.x + Vue Router
- **Animation**: GSAP (GreenSock) + TweenMax + DrawSVGPlugin + SplitText + ScrollMagic
- **Styling**: Tailwind CSS + Custom SCSS + Custom Web Fonts (Circular Std, Apercu Mono, Union)
- **CMS / Data Source**: WordPress REST API + Advanced Custom Fields (ACF Pro)
- **Architecture**: Hybrid SPA + Pre-rendered Static HTML for SEO

---

## 📄 License & Attribution

All content, design, and branding are the property of [Loaf Creative](https://loaf.agency/) (Colony, Jactin House, 24 Hood Street, Manchester). This clone is provided for educational, research, and backup purposes.

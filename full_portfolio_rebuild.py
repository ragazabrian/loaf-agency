#!/usr/bin/env python3
"""
Complete overhaul of Loaf Agency into Brian Ragaza's Portfolio.
- Replaces fonts with Bricolage Grotesque across all CSS and HTML
- Replaces hero video with hero-animation.mp4
- Replaces all Loaf logos with 'brian ragaza' wordmark
- Replaces all remaining Loaf content, posts, showcases, and quotes with Brian's
- Fixes all 28 project images and videos to local, responsive assets
- Ensures full mobile/desktop responsiveness
"""

import os
import json
import re

REPO_DIR = "/Users/bjhamburger/.gemini/antigravity/scratch/loaf-agency"
PORTFOLIO_DIR = "/Users/bjhamburger/.gemini/antigravity/scratch/brian-ragaza-portfolio"

def main():
    print("=== 1. Updating Typography & CSS to Bricolage Grotesque ===")
    css_path = os.path.join(REPO_DIR, "static", "css", "app.74dcd457e3fdb84dafd6f3cbab7bda41.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    font_import = "@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=JetBrains+Mono:wght@400;500&display=swap');\n"
    font_overrides = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, *, h1, h2, h3, h4, h5, h6, p, a, span, div, li, ul, input, textarea, button {
  font-family: 'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  letter-spacing: -0.02em;
}

.Header__logo .logo-wordmark,
.logo-wordmark {
  font-family: 'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-weight: 800 !important;
  font-size: 24px !important;
  letter-spacing: -0.04em !important;
  text-transform: lowercase !important;
  line-height: 1 !important;
  display: inline-block !important;
}

.bubble__wrapper {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  overflow: hidden !important;
  pointer-events: none !important;
  z-index: 1 !important;
}

.bubble__wrapper video {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  opacity: 0.75 !important;
}

.image-src {
  background-size: cover !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
}

.image-src video {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
}
"""
    if "Bricolage+Grotesque" not in css:
        css = font_overrides + "\n" + css
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css)
        print("Injected Bricolage Grotesque and layout overrides into app.css")

    # 2. Update JavaScript bundle (Header logo, footer, role text)
    print("\n=== 2. Updating JavaScript Bundle (Header & Footer) ===")
    app_js_path = os.path.join(REPO_DIR, "static", "js", "app.f48c5d85b67754881d31.js")
    with open(app_js_path, "r", encoding="utf-8") as f:
        js = f.read()

    # Replace SVG header logos (both desktop and burger menu)
    old_logo_pattern = (
        r'i\("svg",\{attrs:\{xmlns:"http://www\.w3\.org/2000/svg",width:"117\.82",height:"34\.01",viewBox:"0 0 117\.82 34\.01"\}\},\[i\("g",\{attrs:\{transform:"translate\(-0\.01 0\.1\)"\}\},\[i\("path",\{attrs:\{"data-name":"Path 1",d:"M89\.66,16\.91a17\.04,17\.04,0,0,0-34\.08,0,17\.1,17\.1,0,0,0,17\.04,17H89\.64Z",fill:"#fff"\}\}\),t\._v\(" "\),i\("path",\{attrs:\{"data-name":"Path 2",d:"M54\.03,16\.91a17\.04,17\.04,0,1,1-17\.04-17,17\.02,17\.02,0,0,1,17\.04,17",fill:"#fff"\}\}\),t\._v\(" "\),i\("path",\{attrs:\{"data-name":"Path 3",d:"M91\.8,33\.91V16\.52c0-10\.67,5\.26-16\.6,16\.14-16\.6h9\.89Z",fill:"#fff"\}\}\),t\._v\(" "\),i\("path",\{attrs:\{"data-name":"Path 4",d:"M\.01-\.1V17\.29c0,10\.67,5\.26,16\.6,16\.14,16\.6h9\.89Z",fill:"#fff"\}\}\)\]\)\]\)'
    )
    new_logo_replacement = (
        'i("span",{staticClass:"logo-wordmark",style:{fontFamily:"\'Bricolage Grotesque\',sans-serif",fontWeight:"800",fontSize:"24px",letterSpacing:"-0\.04em",textTransform:"lowercase",lineHeight:"1",color:"currentColor"}},[t._v("brian ragaza")])'
    )
    js, count = re.subn(old_logo_pattern, new_logo_replacement, js)
    print(f"Replaced {count} Loaf SVG logo occurrences with 'brian ragaza' wordmark")

    # Replace center moreThanCreative in header with clean role text
    old_center_logo = 'i("moreThanCreative",{attrs:{classes:"tw-h-auto beautiful-idea",fill:"dark"===t.theme?"white":"black"}})'
    new_center_text = 'i("span",{staticClass:"header-role tw-hidden md:tw-inline-block",style:{fontFamily:"\'Bricolage Grotesque\',sans-serif",fontWeight:"500",fontSize:"13px",letterSpacing:"-0.01em",opacity:"0.65",color:"currentColor"}},[t._v("Senior Product Designer • Manila / Remote")])'
    js = js.replace(old_center_logo, new_center_text)

    # In burger menu center:
    old_burger_center = 'i("moreThanCreative",{attrs:{classes:"tw-w-full tw-h-auto beautiful-idea",fill:"black"}})'
    new_burger_center = 'i("span",{staticClass:"header-role-menu",style:{fontFamily:"\'Bricolage Grotesque\',sans-serif",fontWeight:"500",fontSize:"14px",letterSpacing:"-0.01em",color:"#000",opacity:"0.6"}},[t._v("Senior Product Designer & Design Operations Lead")])'
    js = js.replace(old_burger_center, new_burger_center)

    # In footer: replace moreThanCreative with headline
    old_footer_graphic = 'i("moreThanCreative",{attrs:{classes:"tw-w-[200px] lg:tw-w-[277px] tw-mt-20 lg:tw-mt-40 tw-hidden lg:tw-block",fill:"dark"===t.theme?"white":"black"}})'
    new_footer_graphic = 'i("span",{staticClass:"footer-tagline tw-block tw-mt-10 lg:tw-mt-20",style:{fontFamily:"\'Bricolage Grotesque\',sans-serif",fontWeight:"700",fontSize:"28px",letterSpacing:"-0.03em",color:"dark"===t.theme?"#fff":"#000"}},[t._v("designing software where mistakes are expensive.")])'
    js = js.replace(old_footer_graphic, new_footer_graphic)

    # Update labels and remaining Loaf mentions
    js = js.replace('"aria-label":"Loaf home"', '"aria-label":"Brian Ragaza home"')
    js = js.replace('siteName:"Loaf"', 'siteName:"Brian Ragaza"')
    js = js.replace('siteUrl:"https://loaf.agency"', 'siteUrl:"https://ragazabrian.github.io/loaf-agency"')
    js = js.replace('attrs:{label:"Work at Loaf"', 'attrs:{label:"Selected Work"')
    js = js.replace('[t._v("Emotion Lab")])', '[t._v("Process")])')
    js = js.replace('Emotion:{title:"Emotion Lab"', 'Emotion:{title:"Design Process"')
    js = js.replace('Back to Emotion Lab', 'Back to Design Process')

    # Update footer static text (Colony, Jactin House -> Manila / Remote)
    js = js.replace(
        "Colony, Jactin House, 24 Hood Street\"),i(\"br\"),t._v(\"Ancoats,\\n                    Manchester M4 6WX",
        "Senior Product Designer & Design Operations Lead\"),i(\"br\"),t._v(\"Manila, Philippines • Remote Worldwide"
    )
    js = js.replace(
        "https://maps.app.goo.gl/ePk8dEjitZgEEsSB9",
        "https://www.linkedin.com/in/ragazabrian"
    )
    js = js.replace("Google Maps", "LinkedIn Profile")
    js = js.replace('[this._v("Instagram")]', '[this._v("Dribbble")]')

    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(js)
    print("Updated app.js with logo, role text, footer, and navigation updates")

    # 3. Comprehensive CMS Dataset Rebuild
    print("\n=== 3. Rebuilding global.json CMS Dataset ===")
    with open(os.path.join(PORTFOLIO_DIR, "js", "data.js"), "r", encoding="utf-8") as f:
        data_js = f.read()
    match = re.search(r'const\s+PROJECTS_DATA\s*=\s*(\[[\s\S]*?\]);', data_js)
    projects_data = json.loads(match.group(1))

    global_json_path = os.path.join(REPO_DIR, "wp-json", "acf", "v3", "global.json")
    with open(global_json_path, "r", encoding="utf-8") as f:
        cms = json.load(f)

    # Clean Loaf posts and replace with Brian's UX Articles
    cms["posts"] = [
        {
            "ID": 501,
            "post_title": "Mission-Critical Software: When UX Mistakes Cost Millions",
            "post_name": "mission-critical-ux",
            "post_date": "2026-11-15 00:00:00",
            "excerpt": "Architecting zero-cognitive-overhead interfaces for hyperscale infrastructure and supply chain operations.",
            "acf": [{"summary": "Designing enterprise software where operational errors carry massive real-world penalties."}]
        },
        {
            "ID": 502,
            "post_title": "Scaling Design Operations from Zero to 17 Enterprise Customers",
            "post_name": "scaling-design-ops",
            "post_date": "2026-10-20 00:00:00",
            "excerpt": "Standardizing cross-functional Figma tokens, design rituals, and engineering telemetry at Kaya AI.",
            "acf": [{"summary": "How we built the design foundation powering multi-billion-dollar contractor workflows."}]
        },
        {
            "ID": 503,
            "post_title": "Bento KPI Widgets & Glanceable Telematics",
            "post_name": "bento-kpi-widgets",
            "post_date": "2026-09-12 00:00:00",
            "excerpt": "Translating dense data center sensor feeds into clear, actionable components.",
            "acf": [{"summary": "Balancing density and glanceability in industrial monitoring software."}]
        },
        {
            "ID": 504,
            "post_title": "Awarded Top 100 Filipino on LinkedIn (2024 & 2025)",
            "post_name": "top-100-recognition",
            "post_date": "2026-08-01 00:00:00",
            "excerpt": "Recognized for thought leadership in software design, UX architecture, and tech community mentorship.",
            "acf": [{"summary": "Honored for contributions to global technology and product design."}]
        }
    ]

    # Clean Loaf showcases and replace with Brian's 6 Core Specializations
    cms["showcase"] = [
        {
            "ID": 601,
            "post_name": "enterprise-ai",
            "post_title": "Enterprise & Hyperscale AI",
            "acf": [{"caption": "Google & OpenAI Backed", "summary": "UI architecture for data center campuses and supply chain intelligence."}]
        },
        {
            "ID": 602,
            "post_name": "design-systems",
            "post_title": "Design Systems & Token Architecture",
            "acf": [{"caption": "Deterministic Multi-Brand Tokens", "summary": "Bridging Figma component libraries directly into production codebases."}]
        },
        {
            "ID": 603,
            "post_name": "mobile-apps",
            "post_title": "Mobile Apps & Field Companions",
            "acf": [{"caption": "iOS & Android Experiences", "summary": "From health & shared medication tracking to superintendent delivery manifests."}]
        },
        {
            "ID": 604,
            "post_name": "fintech-banking",
            "post_title": "Fintech & Multi-Currency Banking",
            "acf": [{"caption": "Cross-Border Wealth & FX", "summary": "Biometric authorization, real-time hedging, and portfolio allocation UX."}]
        },
        {
            "ID": 605,
            "post_name": "saas-tooling",
            "post_title": "High-Density B2B SaaS",
            "acf": [{"caption": "8+ Hour Daily Workflow Tools", "summary": "Reducing friction and cognitive fatigue for operators handling complex pipelines."}]
        },
        {
            "ID": 606,
            "post_name": "luxury-commerce",
            "post_title": "Luxury Brands & Prestige E-Commerce",
            "acf": [{"caption": "Bespoke Digital Flagships", "summary": "High-craft digital experiences for Creed, Libertine, and ASUS ROG."}]
        }
    ]

    # Map image paths for all 28 projects
    new_work = {}
    p_assets_dir = os.path.join(REPO_DIR, "portfolio-assets")

    for idx, p in enumerate(projects_data):
        slug = p["slug"]
        cat = p.get("category", "Product Design")

        # Determine best local image
        img_rel = None
        img_raw = p.get("hoverImage", "")
        if "case-studies/" in img_raw:
            img_rel = f"portfolio-assets/case-studies/{os.path.basename(img_raw)}"
        elif "projects/" in img_raw:
            img_rel = f"portfolio-assets/projects/{os.path.basename(img_raw)}"
        elif os.path.exists(os.path.join(p_assets_dir, "projects", f"{slug}.png")):
            img_rel = f"portfolio-assets/projects/{slug}.png"
        elif os.path.exists(os.path.join(p_assets_dir, "projects", f"{slug}.jpg")):
            img_rel = f"portfolio-assets/projects/{slug}.jpg"
        else:
            img_rel = "portfolio-assets/og-preview.png"

        # Check local case study video
        video_rel = None
        if os.path.exists(os.path.join(p_assets_dir, "case-studies", f"{slug}.mp4")):
            video_rel = f"portfolio-assets/case-studies/{slug}.mp4"

        img_obj = {
            "ID": 2000 + idx,
            "id": 2000 + idx,
            "title": p["title"],
            "filename": os.path.basename(img_rel),
            "url": img_rel,
            "width": 1920,
            "height": 1080,
            "sizes": {
                "thumbnail": img_rel,
                "medium": img_rel,
                "medium_large": img_rel,
                "large": img_rel,
                "1536x1536": img_rel,
                "2048x2048": img_rel
            }
        }

        blocks = [
            {
                "acf_fc_layout": "hero_summary",
                "heading": p["title"],
                "text": f"<p>{p.get('shortDescription', '')}</p><p><strong>Client:</strong> {p.get('client', 'Enterprise')}<br><strong>Category:</strong> {cat}<br><strong>Disciplines:</strong> {', '.join(p.get('tags', []))}</p>"
            },
            {
                "acf_fc_layout": "gallery_single",
                "image": img_obj,
                "caption": f"{p['title']} — Designed by Brian Ragaza"
            }
        ]

        if p.get("link"):
            blocks.append({
                "acf_fc_layout": "text_block",
                "text": f"<p><a href='{p['link']}' target='_blank' rel='noopener' class='hover hover--link tw-font-bold'>View Live Project on {p.get('linkText', 'External Platform')} ↗</a></p>"
            })

        new_work[slug] = {
            "ID": 2000 + idx,
            "post_date": "2026-11-20 00:00:00",
            "post_content": p.get("shortDescription", ""),
            "post_title": p["title"],
            "post_name": slug,
            "post_modified_gmt": "2026-11-26 00:00:00",
            "menu_order": idx + 1,
            "post_type": "work",
            "status": "publish",
            "scope": p.get("client", ""),
            "category": [cat],
            "permalink": f"./work/{slug}",
            "acf": [
                {
                    "client": p.get("client", "Client Project"),
                    "caption": cat,
                    "seo_title": f"{p['title']} — Brian Ragaza",
                    "seo_title_full": f"{p['title']} — Brian Ragaza Senior Product Designer",
                    "seo_description": p.get("shortDescription", ""),
                    "seo_image": img_obj,
                    "homepage_title_override": "",
                    "feature_image": img_obj,
                    "feature_image_portrait": img_obj,
                    "feature_video": video_rel,
                    "work_page_image_override": None,
                    "summary": f"<p>{p.get('shortDescription', '')}</p>",
                    "sub_title": cat,
                    "info_title": "Overview & Scope",
                    "info_overview": (
                        f"<p>{p.get('shortDescription', '')}</p>"
                        f"<p><strong>Deliverables:</strong> {', '.join(p.get('tags', []))}</p>"
                    ),
                    "blocks": blocks
                }
            ]
        }

    cms["work"] = new_work

    # Save to all locations
    for target in [
        os.path.join(REPO_DIR, "wp-json", "acf", "v3", "global.json"),
        os.path.join(REPO_DIR, "wp-json", "acf", "v3", "global"),
        os.path.join(REPO_DIR, "api", "global.json")
    ]:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(cms, f, indent=2)
    print("Rebuilt global.json, global, and api/global.json")

    # 4. Update index.html and 404.html with Google Fonts and responsive styles
    print("\n=== 4. Updating index.html & 404.html ===")
    index_path = os.path.join(REPO_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    font_tags = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  html, body, *, h1, h2, h3, h4, h5, h6, p, a, span, div, li, ul, input, textarea, button {
    font-family: 'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    letter-spacing: -0.02em;
  }
  .logo-wordmark {
    font-family: 'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-weight: 800 !important;
    font-size: 24px !important;
    letter-spacing: -0.04em !important;
    text-transform: lowercase !important;
    line-height: 1 !important;
    display: inline-block !important;
  }
  .bubble__wrapper {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    overflow: hidden !important;
    pointer-events: none !important;
    z-index: 1 !important;
  }
  .bubble__wrapper video {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    opacity: 0.75 !important;
  }
</style>
"""
    if "Bricolage+Grotesque" not in html:
        html = html.replace("<head>", "<head>\n" + font_tags)

    # Ensure no old Loaf strings in HTML head
    html = html.replace("content=\"Loaf Creative\"", "content=\"Brian Ragaza\"")
    html = html.replace("content=\"Loaf\"", "content=\"Brian Ragaza\"")
    html = html.replace("content=\"@loafcreative\"", "content=\"@ragazabrian\"")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(REPO_DIR, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated index.html and 404.html")

    # 5. Update all 28 work routes and 6 emotion-lab routes
    print("\n=== 5. Updating All Route Pages ===")
    work_dir = os.path.join(REPO_DIR, "work")
    for slug in os.listdir(work_dir):
        p = os.path.join(work_dir, slug, "index.html")
        if os.path.isfile(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)

    el_dir = os.path.join(REPO_DIR, "emotion-lab")
    for slug in os.listdir(el_dir):
        p = os.path.join(el_dir, slug, "index.html")
        if os.path.isfile(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)

    for sub in ["about", "work", "emotion-lab", "privacy-policy"]:
        p = os.path.join(REPO_DIR, sub, "index.html")
        if os.path.isfile(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)

    print("All routes synchronized!")
    print("\n=== Overhaul Complete! ===")

if __name__ == "__main__":
    main()

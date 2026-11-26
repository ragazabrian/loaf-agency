#!/usr/bin/env python3
"""
Iterates and replaces Loaf Agency content with Brian Ragaza's Portfolio content,
preserving the exact design, animation, and layout system.
"""

import os
import json
import re

PORTFOLIO_DIR = "/Users/bjhamburger/.gemini/antigravity/scratch/brian-ragaza-portfolio"
LOAF_DIR = "/Users/bjhamburger/.gemini/antigravity/scratch/loaf-agency"

def load_portfolio_projects():
    data_js_path = os.path.join(PORTFOLIO_DIR, "js", "data.js")
    with open(data_js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract JSON array from "const PROJECTS_DATA = [ ... ];"
    match = re.search(r'const\s+PROJECTS_DATA\s*=\s*(\[[\s\S]*?\]);', content)
    if not match:
        raise ValueError("Could not find PROJECTS_DATA in data.js")
    return json.loads(match.group(1))

def main():
    print("Loading Brian Ragaza's portfolio projects...")
    projects = load_portfolio_projects()
    print(f"Loaded {len(projects)} projects.")

    global_json_path = os.path.join(LOAF_DIR, "wp-json", "acf", "v3", "global.json")
    with open(global_json_path, "r", encoding="utf-8") as f:
        cms = json.load(f)

    # 1. Update Global SEO
    cms["seo"] = {
        "title": "Brian Ragaza — Senior Product Designer (UX/UI)",
        "description": "Senior Product Designer & Design Operations Lead specializing in mission-critical software where accuracy, speed, and cognitive clarity are non-negotiable. Backed by Google, Accenture & OpenAI.",
        "image": "./portfolio-assets/og-preview.png"
    }

    # 2. Update Home Page ACF
    home_page = cms["pages"]["home"]
    home_page["post_title"] = "Home"
    home_page["acf"][0]["strapline"] = "Senior Product Designer & Design Ops Lead"
    home_page["acf"][0]["heading"] = "Designing software where mistakes are expensive."
    home_page["acf"][0]["intro"] = "<p>Mission-Critical Workflow Architecture & Design Systems for Enterprise Software.</p>\n"
    home_page["acf"][0]["home_hero"] = [
        {"line": "Senior Product Designer & Design Ops Lead. "},
        {"line": "Designing software where mistakes are "},
        {"line": "expensive — backed by Google, Accenture "},
        {"line": "& OpenAI across 50+ enterprise platforms."},
        {"line": ""}
    ]
    home_page["acf"][0]["home_hero_mobile"] = (
        "Senior Product Designer & Design Ops Lead. Designing software where mistakes are expensive "
        "— backed by Google, Accenture & OpenAI across 50+ enterprise platforms."
    )
    home_page["acf"][0]["description"] = (
        "Specializing in mission-critical software where accuracy, speed, and cognitive clarity are non-negotiable. "
        "From hyperscale data center infrastructure and AI supply chain tools to multi-currency banking and luxury brand experiences, "
        "I build scalable systems for users who cannot afford errors."
    )
    home_page["acf"][0]["description_2"] = "Ready to build something mission-critical?\nLet's connect: ragazabrian@gmail.com"

    # Featured home projects (first 8)
    featured_slugs = [
        "ai-construction", "ai-workspace", "caregiving-app", "mobile-banking",
        "emma-axa", "rog-batman", "creed-perfume", "logistics-ai"
    ]
    home_projects = []
    for idx, slug in enumerate(featured_slugs):
        proj = next((p for p in projects if p["slug"] == slug), None)
        if proj:
            home_projects.append({
                "ID": 1000 + idx,
                "post_author": "1",
                "post_date": "2026-11-20 00:00:00",
                "post_date_gmt": "2026-11-20 00:00:00",
                "post_content": "",
                "post_title": proj["title"],
                "post_excerpt": proj["shortDescription"],
                "post_status": "publish",
                "comment_status": "closed",
                "ping_status": "closed",
                "post_password": "",
                "post_name": proj["slug"],
                "to_ping": "",
                "pinged": "",
                "post_modified": "2026-11-26 00:00:00",
                "post_modified_gmt": "2026-11-26 00:00:00",
                "post_content_filtered": "",
                "post_parent": 0,
                "guid": f"./work/{proj['slug']}",
                "menu_order": idx + 1,
                "post_type": "work",
                "post_mime_type": "",
                "comment_count": "0",
                "filter": "raw"
            })
    home_page["acf"][0]["projects"] = home_projects

    # 3. Update About Page ACF
    about_page = cms["pages"]["about"]
    about_page["post_title"] = "About Brian"
    about_acf = about_page["acf"][0]
    about_acf["intro_1"] = {
        "title": "Brian Ragaza",
        "description": "Senior Product Designer & Design Operations Lead specializing in mission-critical software where accuracy, speed, and cognitive clarity are non-negotiable."
    }
    about_acf["intro_2"] = {
        "title": "Experience & Impact",
        "description": "Designing enterprise platforms backed by Google, Accenture & OpenAI across hyperscale data centers, AI supply chain, and global luxury brands."
    }
    about_acf["intro"] = (
        "<p>Senior Product Designer & Design Operations Lead with over a decade of experience designing enterprise software, design systems, and mission-critical workflows.</p>\n"
        "<p>Currently Design Operations Lead & Product Design Lead at Kaya AI (Columbus, Ohio / Remote), building the entire design function from zero across product, marketing, and brand for an AI-native procurement and supply chain platform, scaling to 17 enterprise customers including Suffolk and Turner Construction.</p>\n"
        "<p>Recognized as a LinkedIn Top Voice in UX Research (2024 & 2025) and Awarded Top 100 Filipino on LinkedIn for contributions to software design and technology.</p>"
    )

    # About clients / partners logos
    client_logos = [
        {"id": 1, "title": "Google", "url": "./portfolio-assets/google-white.png", "width": 180, "height": 60},
        {"id": 2, "title": "OpenAI", "url": "./portfolio-assets/openai-white.png", "width": 180, "height": 60},
        {"id": 3, "title": "Accenture", "url": "./portfolio-assets/accenture-white.png", "width": 180, "height": 60},
        {"id": 4, "title": "AXA", "url": "./portfolio-assets/companies/axa.png", "width": 140, "height": 60},
        {"id": 5, "title": "Kaya AI", "url": "./portfolio-assets/companies/kaya-ai.svg", "width": 160, "height": 60},
        {"id": 6, "title": "Top 100 Filipinos", "url": "./portfolio-assets/top-100-filipinos-white.png", "width": 160, "height": 60}
    ]
    about_acf["clients"] = {
        "title": "Partners & Backing",
        "logos": client_logos
    }

    # About Results / Stats slider
    about_acf["results"] = {
        "title": "Key Metrics & Recognition",
        "slides": [
            {"title": "50+ Enterprise Platforms", "stat": "50+", "description": "High-density SaaS & B2B platforms designed and shipped globally."},
            {"title": "$100B+ Build Value", "stat": "$100B+", "description": "Hyperscale data center infrastructure telematics and workflow tooling."},
            {"title": "Top Voice in UX Research", "stat": "Top Voice", "description": "Recognized on LinkedIn for writing on mission-critical workflow architecture."},
            {"title": "Top 100 Filipino on LinkedIn", "stat": "Top 100", "description": "Awarded in 2024 & 2025 for contributions to software design & tech."},
            {"title": "25+ Global Brand Launches", "stat": "25+", "description": "Market-leading digital experiences and bespoke ecommerce architectures."}
        ]
    }

    # 4. Build Work Items Dictionary
    new_work = {}
    categories_set = set()

    for idx, p in enumerate(projects):
        slug = p["slug"]
        cat = p.get("category", "Product Design")
        categories_set.add(cat)

        # Image resolution
        img_url = p.get("hoverImage", "")
        if img_url.startswith("assets/"):
            img_url = "./portfolio-assets/" + img_url.replace("assets/", "")
        elif not img_url:
            img_url = "./portfolio-assets/og-preview.png"

        # Feature video if available
        feature_video = p.get("videoDesktop") or (p.get("caseStudyVideo") if "caseStudyVideo" in p else None)

        # Build responsive image dict
        sizes_dict = {
            "thumbnail": img_url,
            "medium": img_url,
            "medium_large": img_url,
            "large": img_url,
            "1536x1536": img_url,
            "2048x2048": img_url
        }
        image_obj = {
            "ID": 2000 + idx,
            "id": 2000 + idx,
            "title": p["title"],
            "filename": os.path.basename(img_url.split("?")[0]),
            "url": img_url,
            "width": 1920,
            "height": 1080,
            "sizes": sizes_dict
        }

        # Build blocks for rich case study view
        blocks = [
            {
                "acf_fc_layout": "hero_summary",
                "heading": p["title"],
                "text": f"<p>{p.get('shortDescription', '')}</p><p><strong>Client / Scope:</strong> {p.get('client', 'Enterprise')}<br><strong>Category:</strong> {cat}<br><strong>Deliverables:</strong> {', '.join(p.get('tags', []))}</p>"
            },
            {
                "acf_fc_layout": "gallery_single",
                "image": image_obj,
                "caption": f"{p['title']} — UI Architecture & Interface Design"
            }
        ]

        if p.get("link"):
            blocks.append({
                "acf_fc_layout": "text_block",
                "text": f"<p><a href='{p['link']}' target='_blank' rel='noopener' class='btn'>View on {p.get('linkText', 'Dribbble')} ↗</a></p>"
            })

        work_item = {
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
                    "seo_image": image_obj,
                    "homepage_title_override": "",
                    "feature_image": image_obj,
                    "feature_image_portrait": image_obj,
                    "feature_video": feature_video,
                    "work_page_image_override": None,
                    "summary": f"<p>{p.get('shortDescription', '')}</p>",
                    "sub_title": cat,
                    "info_title": "Project Overview",
                    "info_overview": (
                        f"<p>{p.get('shortDescription', '')}</p>"
                        f"<p><strong>Tags:</strong> {', '.join(p.get('tags', []))}</p>"
                    ),
                    "blocks": blocks
                }
            ]
        }
        new_work[slug] = work_item

    cms["work"] = new_work

    # 5. Work Categories
    cms["work_categories"] = [
        {"term_id": i + 1, "name": cat_name, "slug": cat_name.lower().replace(" & ", "-").replace(" ", "-")}
        for i, cat_name in enumerate(sorted(categories_set))
    ]

    # 6. Update EmotionLab to Design Process & Methodology
    cms["pages"]["emotionlab"]["post_title"] = "Design Process"
    cms["pages"]["emotionlab"]["acf"][0] = {
        "intro": "<p>Design Process & Methodology — Workflow architecture, cognitive modeling, and tokenized design systems built for zero-error execution.</p>\n",
        "randd": "Map the workflow before drawing screens. I deeply map user journeys, edge cases, and operational constraints so that complex systems feel effortlessly natural to the people who rely on them daily."
    }

    methodologies = [
        {
            "slug": "workflow-architecture",
            "title": "Workflow Architecture & UX Research",
            "sub_title": "Map the workflow before drawing screens",
            "summary": "Deep mapping of user journeys, edge cases, and operational constraints so that complex enterprise systems feel effortlessly natural to the people who rely on them daily."
        },
        {
            "slug": "dense-dashboards",
            "title": "Dashboards, Onboarding & Multi-Step Tools",
            "sub_title": "Designing dense, high-frequency software",
            "summary": "Balancing cognitive load, telemetry visibility, and frictionless interactions for operators who spend 8+ hours a day inside mission-critical dashboards."
        },
        {
            "slug": "design-tokens-systems",
            "title": "Design Tokens & Scalable Systems",
            "sub_title": "Multi-brand, dark-mode-first token architecture",
            "summary": "Building composable, deterministic UI token architectures and components that bridge design directly into production codebases with zero drift."
        },
        {
            "slug": "usability-audits",
            "title": "Enterprise Usability Audits & Friction Reduction",
            "sub_title": "Eliminating friction where mistakes are expensive",
            "summary": "Systematic heuristic evaluations, workflow streamlining, and error-prevention patterns for high-stakes operational environments."
        },
        {
            "slug": "state-modeling",
            "title": "Edge-Case & State Modeling",
            "sub_title": "Designing for failure states and asynchronous sync",
            "summary": "Designing every permutation of latency, partial sync, conflict resolution, and offline resilience in distributed enterprise software."
        },
        {
            "slug": "design-operations",
            "title": "Design Operations & Team Scaling",
            "sub_title": "From zero to enterprise readiness",
            "summary": "Standardizing Figma libraries, QA handoff rituals, design-to-engineering telemetry, and cross-functional design sprints."
        }
    ]

    cms_emotionlab = []
    for idx, m in enumerate(methodologies):
        sample_img = {
            "ID": 3000 + idx,
            "url": "./portfolio-assets/og-preview.png",
            "width": 1200,
            "height": 630,
            "sizes": {"thumbnail": "./portfolio-assets/og-preview.png"}
        }
        cms_emotionlab.append({
            "ID": 3000 + idx,
            "post_date": "2026-11-20 00:00:00",
            "post_title": m["title"],
            "post_name": m["slug"],
            "post_modified_gmt": "2026-11-26 00:00:00",
            "menu_order": idx + 1,
            "post_type": "emotionlab",
            "type": "Methodology",
            "author": "Brian Ragaza",
            "permalink": f"./emotion-lab/{m['slug']}",
            "acf": [
                {
                    "sub_title": m["sub_title"],
                    "intro": f"<p>{m['summary']}</p>",
                    "body": f"<p>{m['summary']}</p><p>Written by Brian Ragaza • Senior Product Designer & Design Operations Lead.</p>",
                    "poster_image": sample_img,
                    "poster_video": None
                }
            ]
        })
    cms["emotionlab"] = cms_emotionlab

    # Save to all global.json locations
    save_targets = [
        os.path.join(LOAF_DIR, "wp-json", "acf", "v3", "global.json"),
        os.path.join(LOAF_DIR, "wp-json", "acf", "v3", "global"),
        os.path.join(LOAF_DIR, "api", "global.json")
    ]
    for target in save_targets:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(cms, f, indent=2)
        print(f"Updated: {target}")

    # 7. Update index.html, 404.html, and pre-rendered pages with Brian Ragaza's content
    index_path = os.path.join(LOAF_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Replace Loaf branding with Brian Ragaza in HTML head & title
    html = re.sub(r'<title>.*?</title>', '<title>Brian Ragaza — Senior Product Designer (UX/UI)</title>', html)
    html = re.sub(
        r'<meta name="description" content=".*?"',
        '<meta name="description" content="Brian Ragaza — Senior Product Designer & Design Operations Lead specializing in mission-critical software backed by Google, Accenture & OpenAI."',
        html
    )
    html = re.sub(
        r'<meta property="og:title" content=".*?"',
        '<meta property="og:title" content="Brian Ragaza — Senior Product Designer (UX/UI)"',
        html
    )
    html = re.sub(
        r'<meta property="og:description" content=".*?"',
        '<meta property="og:description" content="Senior Product Designer & Design Operations Lead specializing in mission-critical software backed by Google, Accenture & OpenAI."',
        html
    )
    html = re.sub(
        r'<meta name="twitter:title" content=".*?"',
        '<meta name="twitter:title" content="Brian Ragaza — Senior Product Designer (UX/UI)"',
        html
    )
    html = re.sub(
        r'<meta name="twitter:description" content=".*?"',
        '<meta name="twitter:description" content="Senior Product Designer & Design Operations Lead specializing in mission-critical software backed by Google, Accenture & OpenAI."',
        html
    )

    # Replace SSR fallback copy inside .ssr-page
    ssr_replacement = (
        '<h1>Brian Ragaza — Senior Product Designer &amp; Design Operations Lead</h1>'
        '<p>Designing software where mistakes are expensive. Backed by Google, Accenture &amp; OpenAI across 50+ enterprise platforms.</p>'
        '<h2>Selected Work</h2>'
        '<ul>'
        '<li><a href="/work/ai-construction">AI Construction UI Architecture &amp; Design System</a> — US Construction Software</li>'
        '<li><a href="/work/ai-workspace">AI Learning Workspace for Students &amp; Instructors</a> — EdTech SaaS Platform</li>'
        '<li><a href="/work/caregiving-app">Family Caregiving Mobile App</a> — Shared Health &amp; Medication App</li>'
        '<li><a href="/work/mobile-banking">Multi-Currency Mobile Banking App</a> — Digital Banking Platform</li>'
        '<li><a href="/work/emma-axa">Emma by AXA Philippines</a> — Insurance &amp; Wealth</li>'
        '<li><a href="/work/rog-batman">ROG Phone 6 BATMAN Edition</a> — ASUS Republic of Gamers</li>'
        '<li><a href="/work/creed-perfume">Creed Perfume Australia Official</a> — Luxury Fragrance</li>'
        '</ul>'
        '<h2>Design Process &amp; Methodology</h2>'
        '<ul>'
        '<li><a href="/emotion-lab/workflow-architecture">Workflow Architecture &amp; UX Research</a></li>'
        '<li><a href="/emotion-lab/dense-dashboards">Dashboards, Onboarding &amp; Multi-Step Tools</a></li>'
        '<li><a href="/emotion-lab/design-tokens-systems">Design Tokens &amp; Scalable Systems</a></li>'
        '<li><a href="/emotion-lab/usability-audits">Enterprise Usability Audits &amp; Friction Reduction</a></li>'
        '<li><a href="/emotion-lab/state-modeling">Edge-Case &amp; State Modeling</a></li>'
        '<li><a href="/emotion-lab/design-operations">Design Operations &amp; Team Scaling</a></li>'
        '</ul>'
        '<address>Brian Ragaza<br>Manila, Philippines • Remote Worldwide<br>'
        '<a href="mailto:ragazabrian@gmail.com">ragazabrian@gmail.com</a><br>'
        '<a href="https://www.linkedin.com/in/ragazabrian" target="_blank" rel="noopener">LinkedIn Profile</a></address>'
    )
    html = re.sub(r'<h1>Over 20 years helping brands bloom.*?<p><a href="/privacy-policy">Privacy policy</a></p>', ssr_replacement, html, flags=re.DOTALL)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated index.html")

    # Also update 404.html
    with open(os.path.join(LOAF_DIR, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated 404.html")

    # 8. Update static/js/app.*.js for hardcoded footer strings
    app_js_path = os.path.join(LOAF_DIR, "static", "js", "app.f48c5d85b67754881d31.js")
    with open(app_js_path, "r", encoding="utf-8") as f:
        app_js = f.read()

    # Clean replacements in app.js
    app_js = app_js.replace("hello@loaf.agency", "ragazabrian@gmail.com")
    app_js = app_js.replace("+441616729844", "mailto:ragazabrian@gmail.com")
    app_js = app_js.replace("+44 (0)161 672 9844", "ragazabrian@gmail.com")
    app_js = app_js.replace("Colony, Jactin House, 24 Hood Street\\nAncoats, Manchester M4 6WX", "Senior Product Designer & Design Ops Lead\\nManila, Philippines • Remote Worldwide")
    app_js = app_js.replace("Colony, Jactin House, 24 Hood Street<br />Ancoats,\\n                      Manchester M4 6WX", "Senior Product Designer & Design Ops Lead<br />Manila, Philippines • Remote Worldwide")
    app_js = app_js.replace("https://www.linkedin.com/company/loaf-creative/", "https://www.linkedin.com/in/ragazabrian")
    app_js = app_js.replace("https://instagram.com/loafcreative", "https://www.linkedin.com/in/ragazabrian")

    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(app_js)
    print("Updated hardcoded contact/footer strings in app.js")

    print("\nContent iteration completed successfully!")

if __name__ == "__main__":
    main()

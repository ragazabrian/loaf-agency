// Per-page <title>, description, canonical, Open Graph and Twitter tags,
// worked out from the route and the WordPress data, and robots (noindex for
// drafts, pages marked "Hide from search engines", and pages that don't
// exist).
//
// The settings (title formats, separator, site name, defaults) come from
// WordPress: Theme Options > SEO & Structured Data, delivered in the global
// API as content.seo. Each item can override its title, description, image
// and indexing in its "SEO" box (seo_* ACF fields). The same rules are
// implemented in PHP (loaf_seo_format_title in functions.php) for the future
// server-rendered head, so keep the two in step.
//
// updateMeta() runs after every navigation (router.afterEach) and once the
// WordPress data has loaded (main.js); components don't set titles
// themselves.

import { setRobotsMeta } from "@/utils";

// The shell's own tags (index.html) are the fallback when WordPress has no
// value, captured once before anything is changed
let shellDefaults = null;
function captureShellDefaults() {
  if (shellDefaults) return shellDefaults;
  // On the live site the head was rendered for the landing page
  // (public/index.php), so its tags are that page's, not the site's: use
  // the site defaults the server put alongside them
  const fromServer = document.getElementById("loaf-seo-defaults");
  if (fromServer) {
    try {
      shellDefaults = JSON.parse(fromServer.textContent);
      return shellDefaults;
    } catch (e) {
      // fall through to the shell's own tags
    }
  }
  const read = (selector) => {
    const el = document.head.querySelector(selector);
    return el ? el.getAttribute("content") : null;
  };
  shellDefaults = {
    title: document.title,
    description: read('meta[name="description"]'),
    image: read('meta[property="og:image"]'),
  };
  return shellDefaults;
}

// Only used if WordPress sends no settings at all
const FALLBACK = {
  format: "{title} {sep} {site}",
  separator: "-",
  siteName: "Loaf",
  siteUrl: "https://loaf.agency",
};

// Static routes: their {title}, and the WordPress page (content.pages key)
// that can supply a description / SEO overrides
const ROUTE_PAGES = {
  Home: { page: "home" },
  About: { title: "About", page: "about" },
  Work: { title: "Work" },
  Emotion: { title: "Emotion Lab", page: "emotionlab" },
  Privacy: { title: "Privacy Policy", page: "privacypolicy" },
  Signup: { title: "Sign up" },
  EmotionRnd: { title: "Exploration", noindex: true },
  Type: { title: "Type", noindex: true },
  // The info overlay repeats the case study's own content, so it
  // canonicalises to the case study (see canonical below) rather than
  // being noindexed: Google treats noindex + canonical as conflicting
  ProjectInfo: {},
  NotFound: { title: "Page not found", notFound: true },
};

const first = (...values) => values.find((v) => typeof v === "string" && v.trim() !== "");

function acfOf(item) {
  if (!item || !item.acf) return {};
  return Array.isArray(item.acf) ? item.acf[0] || {} : item.acf;
}

function imageUrl(image) {
  if (!image) return null;
  if (typeof image === "string") return image;
  return image.url || null;
}

function plainText(html) {
  if (!html) return "";
  const div = document.createElement("div");
  div.innerHTML = html;
  return (div.textContent || "").replace(/\s+/g, " ").trim();
}

// Trim to ~155 characters at a word boundary. Text too short to describe a
// page (e.g. a placeholder "test") returns "" so the next source or the site
// default is used. Only for auto-derived text: an editor's seo_description
// is always used as-is.
function summarise(text, max = 155) {
  text = plainText(text);
  if (text.length < 40) return "";
  if (text.length <= max) return text;
  const cut = text.slice(0, max);
  return cut.slice(0, cut.lastIndexOf(" ") > 80 ? cut.lastIndexOf(" ") : max).replace(/[\s,.;:–—-]+$/, "") + "…";
}

// Apply a title format, e.g. "{client} — {title} {sep} {site}". Tokens with
// no value are removed along with any doubled-up spaces or separators.
// Mirrors loaf_seo_format_title() in functions.php.
export function formatTitle(format, tokens) {
  let title = format;
  Object.keys(tokens).forEach((token) => {
    title = title.split("{" + token + "}").join(tokens[token] || "");
  });
  return title
    .replace(/\{[a-z_]+\}/g, "")
    .replace(/\s{2,}/g, " ")
    .replace(/^[\s\-–—|:·]+|[\s\-–—|:·]+$/g, "");
}

// Everything known about the current route: kind, the WordPress item, and
// whether it exists. Also used by App.vue to show the 404 view.
export function resolveRoute(route, content) {
  const loaded = !!(content && content.work);
  const id = route.params && route.params.id;
  let kind = null;
  let item = null;

  if (route.name === "Project" || route.name === "ProjectInfo") {
    kind = "work";
    item = loaded ? content.work[id] : null;
  } else if (route.name === "EmotionPost") {
    kind = "emotionlab";
    item = loaded ? (content.emotionlab || []).find((p) => p.post_name === id) : null;
  } else if (route.name === "Showcase") {
    kind = "showcase";
    item = loaded ? (content.showcase || {})[id] : null;
  }

  // Only a route with an item can be missing, and only once data is in
  const missing = !!(kind && loaded && !item);
  return { kind, item, loaded, missing };
}

export function metaFor(route, content) {
  const shell = captureShellDefaults();
  const seo = (content && content.seo) || {};
  const site = seo.site || {};
  const formats = seo.title_formats || {};
  const siteName = site.name || FALLBACK.siteName;
  const separator = site.separator || FALLBACK.separator;
  const siteUrl = (site.url || FALLBACK.siteUrl).replace(/\/+$/, "");
  const defaultDescription = first(site.default_description, shell.description) || "";
  const defaultImage = first(site.default_image, shell.image);

  const { kind, item, loaded, missing } = resolveRoute(route, content);
  const routeInfo = ROUTE_PAGES[route.name] || {};
  const page = routeInfo.page && content && content.pages ? content.pages[routeInfo.page] : null;
  const source = item || page; // whichever carries seo_* overrides
  const acf = acfOf(source);

  let title;
  let description;
  let image;
  let type = "website";
  let noindex = !!routeInfo.noindex;
  const tokens = { sep: separator, site: siteName };

  if (missing || routeInfo.notFound) {
    title = formatTitle(formats.page || FALLBACK.format, Object.assign({ title: "Page not found" }, tokens));
    return {
      title,
      description: defaultDescription,
      image: defaultImage,
      canonical: null, // a page that doesn't exist has no canonical
      type,
      noindex: true,
      siteName,
      locale: site.locale,
      twitterCard: site.twitter_card,
      twitterHandle: site.twitter_handle,
    };
  }

  if (kind && item) {
    const itemTitle = plainText(item.post_title);
    tokens.title = first(acf.seo_title, itemTitle);
    if (kind === "work") {
      tokens.client = plainText(acf.client);
      tokens.subtitle = plainText(acf.sub_title);
      description = first(acf.seo_description, summarise(acf.summary), summarise(acf.info_overview));
      image = first(acf.seo_image, imageUrl(acf.feature_image));
      type = "article";
      if (item.status === "draft") noindex = true; // private preview links
    } else if (kind === "emotionlab") {
      tokens.subtitle = plainText(acf.sub_title);
      description = first(acf.seo_description, summarise(item.post_content));
      image = first(acf.seo_image, imageUrl(acf.poster_image));
      type = "article";
    } else if (kind === "showcase") {
      description = first(acf.seo_description, summarise(acf.introduction));
      image = first(acf.seo_image, imageUrl(acf.highlight && acf.highlight.image));
    }
    title = acf.seo_title && acf.seo_title_full
      ? acf.seo_title
      : formatTitle(formats[kind] || FALLBACK.format, tokens);
  } else if (route.name === "Home") {
    title = first(acf.seo_title, site.home_title, shell.title);
    description = first(acf.seo_description);
  } else {
    tokens.title = first(acf.seo_title, routeInfo.title, plainText(page && page.post_title));
    title = acf.seo_title && acf.seo_title_full
      ? acf.seo_title
      : formatTitle(formats.page || FALLBACK.format, tokens);
    description = first(acf.seo_description);
    image = first(acf.seo_image);
  }

  if (acf.seo_noindex) noindex = true;

  // Canonical: the clean path, without query string or trailing slash; the
  // case study info overlay points at its case study
  let path = route.path === "/" ? "/" : route.path.replace(/\/+$/, "");
  if (route.name === "ProjectInfo") path = path.replace(/\/info$/, "");

  return {
    title: title || shell.title,
    description: description || defaultDescription,
    image: image || defaultImage,
    canonical: loaded || !kind ? siteUrl + path : null,
    type,
    noindex,
    siteName,
    locale: site.locale,
    twitterCard: site.twitter_card,
    twitterHandle: site.twitter_handle,
  };
}

function setTag(selector, create, value) {
  let el = document.head.querySelector(selector);
  if (value === null || value === undefined || value === "") {
    if (el && el.hasAttribute("data-seo")) el.parentNode.removeChild(el);
    return;
  }
  if (!el) {
    el = document.createElement(create.tag);
    Object.keys(create.attrs).forEach((a) => el.setAttribute(a, create.attrs[a]));
    el.setAttribute("data-seo", "");
    document.head.appendChild(el);
  }
  el.setAttribute(create.tag === "link" ? "href" : "content", value);
}

const meta = (attr, key) => ({
  selector: `meta[${attr}="${key}"]`,
  create: { tag: "meta", attrs: { [attr]: key } },
});

export function applyMeta(m) {
  document.title = m.title;
  const tags = [
    [meta("name", "description"), m.description],
    [{ selector: 'link[rel="canonical"]', create: { tag: "link", attrs: { rel: "canonical" } } }, m.canonical],
    [meta("property", "og:title"), m.title],
    [meta("property", "og:description"), m.description],
    [meta("property", "og:url"), m.canonical],
    [meta("property", "og:image"), m.image],
    [meta("property", "og:type"), m.type],
    [meta("property", "og:site_name"), m.siteName],
    [meta("property", "og:locale"), m.locale],
    [meta("name", "twitter:card"), m.twitterCard],
    [meta("name", "twitter:site"), m.twitterHandle],
    [meta("name", "twitter:title"), m.title],
    [meta("name", "twitter:description"), m.description],
    [meta("name", "twitter:image"), m.image],
  ];
  tags.forEach(([t, value]) => setTag(t.selector, t.create, value));
  setRobotsMeta(m.noindex ? "noindex" : null);
}

export function updateMeta(route, content) {
  captureShellDefaults();
  // The first navigation runs before the WordPress data has arrived. Leave
  // the head alone until it has: the server already rendered it for this
  // URL (public/index.php), and filling in defaults now would briefly swap
  // the right title for the generic one. main.js calls this again once the
  // data is in, which sets the same values.
  if (!content || !content.work) return;
  applyMeta(metaFor(route, content));
}



// WEBPACK FOOTER //
// ./src/seo.js
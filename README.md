# grofolio.tech

Ready to Grow Your Business? Discover Smarter Marketing Strategies. Explore practical digital marketing insights, expert strategies, and actionable guides to grow your online presence, reach more customers, and generate leads.

Zero-build static site: HTML, CSS, a little vanilla JS, Tailwind from CDN. No Node, no npm, no generator. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. You can also double-click `index.html` — links are relative, so the site works from a file path, from a subfolder, or from a domain root (`https://www.grofolio.tech/`).

## Layout

```
index.html                  homepage + marketing strategy post feed
about/index.html            about page (/about/)
privacy/index.html          privacy policy for analytics & ad compliance
ads.txt                     Google AdSense publisher ID verification
sitemap.xml                 XML sitemap for Google Search Console & search engines
llms.txt                    plain markdown index for AI models (Gemini, ChatGPT, Claude)
llms-full.txt               expanded full-text markdown index for deep LLM context
robots.txt                  crawler directives (disallows /prompt/ and /404/)
feed.xml                    RSS 2.0 feed for readers and aggregators
404.html                    custom not-found fallback
404/index.html              not-found page folder (/404/)
assets/css/style.css        custom CSS; brand colors, print styles, fallback layout
assets/js/main.js           theme toggle + consent bar, feed filter, code copy buttons
assets/grofolio-logo.png    high-resolution brand logo
assets/grofolio-logo-web.png web-optimized retina brand logo
assets/favicon-32x32.png    site favicon
assets/images/<year>/       post diagrams and featured images
blogs/<post-slug>/index.html one folder per post; the URL is /blogs/<post-slug>/
vercel.json                 clean URLs and redirects
```

## Brand Colors

- **Deep Espresso (`#27221B`):** Primary logo & authoritative typography colour.
- **Coral (`#FE7264`):** Signature accent colour representing creativity, energy, attention, and growth.
- **Rich Brown (`#423117`):** Secondary brand colour for warmth, experience, and grounded business thinking.
- **White (`#FFFFFF`):** Background colour representing clarity and simplicity.

## Theme

Light is the default. One inline line in each page's `<head>` applies a saved dark choice before paint with zero flash:

```html
<script>
  if (localStorage.theme === 'dark') document.documentElement.classList.add('dark');
</script>
```

## Publish a Post

1. Copy `prompt/template.html` into a new slug folder: `mkdir -p blogs/new-strategy && cp prompt/template.html blogs/new-strategy/index.html`.
2. Update `<title>`, `meta[name=description]`, `link[rel=canonical]`, Open Graph, and Twitter metadata.
3. Put featured images in `assets/images/2026/`.
4. Add the entry to `<ol id="post-feed">` in `index.html`.
5. Update `sitemap.xml` and `feed.xml`.

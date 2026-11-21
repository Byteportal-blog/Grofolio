#!/usr/bin/env python3
"""
Grofolio Blogger Exporter
Converts any Grofolio blog post into an official Blogger Atom XML import file.

Features:
- Converts local relative image URLs to live absolute grofolio.tech CDN URLs.
- Sanitizes raw SVGs to clean symbols (prevents oversized SVG expansion on Blogger).
- Adds inline styles to tables and callout boxes for clean rendering on Blogger.
- Adds canonical SEO attribution linking back to the original article on grofolio.tech.

Usage:
    python scripts/export_blogger.py <slug>
    python scripts/export_blogger.py --all
    Example: python scripts/export_blogger.py coca-cola-marketing-strategy
"""

import os
import sys
import re
import html as html_lib
import argparse
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOGGER_BLOG_ID = "8940675546180095"

def parse_and_convert(slug):
    post_dir = os.path.join(BASE_DIR, 'blogs', slug)
    if not os.path.exists(post_dir):
        post_dir = os.path.join(BASE_DIR, slug)
    index_file = os.path.join(post_dir, 'index.html')
    if not os.path.exists(index_file):
        raise FileNotFoundError(f"Article not found at: {index_file}")

    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Title
    title_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = html_lib.unescape(title_m.group(1).strip()) if title_m else slug

    # 2. Tags
    tags = re.findall(r'<meta property="article:tag" content="(.*?)">', html, re.I)
    if not tags:
        tags = ["Marketing Strategy", "Digital Marketing", "Business Growth"]

    canonical_url = f"https://www.grofolio.tech/blogs/{slug}/"

    # 3. Extract prose body
    prose_m = re.search(r'<div class="prose[^"]*">(.*?)</div>\s*</article>', html, re.S | re.I)
    if not prose_m:
        prose_m = re.search(r'<div class="prose[^"]*">(.*?)</div>\s*<footer', html, re.S | re.I)
    if not prose_m:
        raise ValueError(f"Could not extract prose content from {index_file}")
    
    raw_body = prose_m.group(1)

    # Check for featured hero figure above prose and include at top of Blogger post
    hero_m = re.search(r'(<!-- Featured Image[^>]*-->\s*<figure[^>]*>.*?</figure>)', html, re.S | re.I)
    if not hero_m:
        hero_m = re.search(r'(<figure[^>]*class="mt-6[^"]*"[^>]*>.*?</figure>)', html, re.S | re.I)
    if hero_m:
        raw_body = hero_m.group(1) + "\n\n" + raw_body

    # 4. Convert relative image paths to live Grofolio CDN URLs
    def replace_img_src(match):
        prefix = match.group(1)
        src = match.group(2)
        if src.startswith('http'):
            return f'{prefix}src="{src}"'
        clean_src = re.sub(r'^(?:\.\./|\./|/)+', '', src)
        absolute_src = f"https://www.grofolio.tech/{clean_src}"
        return f'{prefix}src="{absolute_src}"'

    clean_body = re.sub(r'(<img\s+[^>]*?)src="([^"]+)"', replace_img_src, raw_body)

    # 5. Convert relative anchor links to absolute
    def replace_a_href(match):
        prefix = match.group(1)
        href = match.group(2)
        if href.startswith('http') or href.startswith('#') or href.startswith('mailto:'):
            return f'{prefix}href="{href}"'
        clean_href = re.sub(r'^(?:\.\./|\./|/)+', '', href)
        if not clean_href.startswith('blogs/') and not clean_href.startswith('about') and not clean_href.startswith('privacy'):
            clean_href = f"blogs/{clean_href}"
        return f'{prefix}href="https://www.grofolio.tech/{clean_href}"'

    clean_body = re.sub(r'(<a\s+[^>]*?)href="([^"]+)"', replace_a_href, clean_body)

    # 6. Replace raw SVGs with universal inline checkmark
    clean_body = re.sub(
        r'<svg[^>]*>.*?</svg>',
        '<span style="display:inline-block; font-size:18px; color:#fe7264; margin-right:6px; vertical-align:middle;">✔</span>',
        clean_body,
        flags=re.S
    )

    # 7. Add inline fallback styles for #quick-answer box
    clean_body = re.sub(
        r'<div id="quick-answer"[^>]*>',
        '<div id="quick-answer" style="background:#fafaf9; border-left:4px solid #fe7264; border-radius:8px; padding:18px; margin:24px 0; font-family:sans-serif;">',
        clean_body
    )

    # 8. Add inline borders and padding to table elements for clean rendering
    clean_body = re.sub(r'<table[^>]*>', '<table style="width:100%; border-collapse:collapse; margin:24px 0; font-family:sans-serif; font-size:14px; border:1px solid #e7e5e4;">', clean_body)
    clean_body = re.sub(r'<th\s+class="([^"]*)"', r'<th style="border:1px solid #e7e5e4; padding:12px 14px; background:#f5f5f4; text-align:left;" class="\1"', clean_body)
    clean_body = re.sub(r'<td\s+class="([^"]*)"', r'<td style="border:1px solid #e7e5e4; padding:12px 14px; text-align:left;" class="\1"', clean_body)

    # 9. Style figures and captions for Blogger
    clean_body = re.sub(r'<figure[^>]*>', '<figure style="margin:28px 0; text-align:center;">', clean_body)
    clean_body = re.sub(r'<figcaption[^>]*>', '<figcaption style="margin-top:8px; font-size:13px; color:#78716c; text-align:center; font-family:sans-serif;">', clean_body)
    clean_body = re.sub(r'(<img\s+[^>]*class="[^"]*)"', r'\1" style="max-width:100%; height:auto; border-radius:8px; border:1px solid #e7e5e4;"', clean_body)

    # 9. Canonical attribution callout
    attribution = f"""
<div style="margin-top: 40px; padding: 18px 22px; background: #fafaf9; border-left: 4px solid #fe7264; border-radius: 6px; font-family: sans-serif; font-size: 15px; color: #44403c;">
    <strong>Original Article:</strong> This guide was originally published on 
    <a href="{canonical_url}" target="_blank" rel="noopener" style="color: #fe7264; font-weight: 600; text-decoration: underline;">
        grofolio.tech — {title}
    </a>.
</div>
"""
    clean_body = clean_body.strip() + "\n" + attribution

    # 10. Extract published date or fallback
    date_m = re.search(r'<meta property="article:published_time" content="(.*?)">', html)
    if date_m:
        pub_date_str = date_m.group(1).strip()
        pub_dt = datetime.fromisoformat(pub_date_str).replace(tzinfo=timezone.utc)
    else:
        pub_dt = datetime.now(timezone.utc)

    iso_published = pub_dt.strftime("%Y-%m-%dT08:00:00.000+00:00")
    iso_updated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000+00:00")

    # 11. Escape content for Blogger Atom XML
    def escape_xml(text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

    escaped_body = escape_xml(clean_body)
    escaped_title = escape_xml(title)

    categories_xml = "\n".join([
        f'  <category scheme="http://www.blogger.com/atom/ns#" term="{escape_xml(tag)}" />'
        for tag in tags
    ])

    post_id = f"tag:blogger.com,1999:blog-{BLOGGER_BLOG_ID}.post-{int(pub_dt.timestamp())}"

    atom_xml = f"""<entry xmlns='http://www.w3.org/2005/Atom'>
  <id>{post_id}</id>
  <published>{iso_published}</published>
  <updated>{iso_updated}</updated>
  <title type='text'>{escaped_title}</title>
  <content type='html'>{escaped_body}</content>
  <link rel='replies' type='application/atom+xml' href='https://www.blogger.com/feeds/{BLOGGER_BLOG_ID}/posts/default' title='Post Comments'/>
{categories_xml}
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/blogger/2008/kind#post"/>
  <author>
    <name>Grofolio Editorial Team</name>
    <uri>https://www.grofolio.tech/about/</uri>
    <email>noreply@blogger.com</email>
  </author>
</entry>
"""

    # Wrap in Blogger Atom feed container
    full_feed_xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' xmlns:georss='http://www.georss.org/georss' xmlns:gd='http://schemas.google.com/g/2005' xmlns:thr='http://purl.org/syndication/thread/1.0'>
  <id>tag:blogger.com,1999:blog-{BLOGGER_BLOG_ID}</id>
  <updated>{iso_updated}</updated>
  <title type='text'>grofolio.tech Blogger Export</title>
  <link rel='self' type='application/atom+xml' href='https://www.blogger.com/feeds/{BLOGGER_BLOG_ID}/archive'/>
  <author>
    <name>Grofolio</name>
    <uri>https://www.grofolio.tech/</uri>
  </author>
  <generator version='7.00' uri='https://www.blogger.com'>Blogger</generator>
{atom_xml}
</feed>
"""

    exports_dir = os.path.join(BASE_DIR, 'blogger-exports')
    os.makedirs(exports_dir, exist_ok=True)
    out_file = os.path.join(exports_dir, f"{slug}.xml")

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(full_feed_xml)

    print(f"  ✓ Exported: {os.path.relpath(out_file, BASE_DIR)}")
    return out_file

def main():
    parser = argparse.ArgumentParser(description="Export Grofolio blog posts to Blogger Atom XML.")
    parser.add_argument("slug", nargs="?", help="Slug of the post (e.g. b2b-digital-marketing-strategy)")
    parser.add_argument("--all", action="store_true", help="Export all posts in blogs/")

    args = parser.parse_args()

    blogs_dir = os.path.join(BASE_DIR, 'blogs')
    if args.all or not args.slug:
        if os.path.exists(blogs_dir):
            posts = [d for d in os.listdir(blogs_dir) if os.path.isdir(os.path.join(blogs_dir, d)) and os.path.exists(os.path.join(blogs_dir, d, 'index.html'))]
            print(f"Exporting all {len(posts)} posts from {blogs_dir}...")
            for slug in sorted(posts):
                parse_and_convert(slug)
        else:
            print("No blogs directory found.")
    else:
        parse_and_convert(args.slug)

if __name__ == '__main__':
    main()

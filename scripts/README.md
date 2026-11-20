# Cross-Posting Guide (Medium & Blogger)

Grofolio articles can easily be cross-posted to **Medium** and **Blogger** with full canonical SEO attribution to drive authority back to `grofolio.tech`.

---

## 1. Medium (10 Seconds)
1. Open 👉 **[medium.com/p/import](https://medium.com/p/import)**.
2. Paste the live post URL:
   ```text
   https://www.grofolio.tech/blogs/<slug>/
   ```
3. Click **Import**. Medium automatically copies the text, diagrams, and sets the canonical URL.
4. Click **Publish**.

---

## 2. Blogger (30 Seconds)
1. Run the exporter script for your post:
   ```bash
   python scripts/export_blogger.py <slug>
   ```
   *To export all posts at once:*
   ```bash
   python scripts/export_blogger.py --all
   ```
   *Example:*
   ```bash
   python scripts/export_blogger.py b2b-digital-marketing-strategy
   ```
   *This outputs `blogger-exports/<slug>.xml` with live CDN images, styled tables, and canonical attribution.*

2. Go to **blogger.com** &rarr; **Settings** &rarr; scroll to **Manage Blog**.
3. Click **Import content** &rarr; select `blogger-exports/<slug>.xml`.
4. Done!

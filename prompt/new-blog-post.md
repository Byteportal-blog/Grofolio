# Prompt: write a new post for grofolio.tech

Copy the block below into your agent, fill in the **TOPIC** section, send. It already knows the stack (zero-build static site, `prompt/template.html`, `index.html` feed) and the house style.

---

## Prompt

You are writing one new post for **grofolio.tech**, a practical digital marketing knowledge hub built as a zero-build static blog (plain HTML, Tailwind from CDN, a little vanilla JS). No npm, no build step, no generator.

### Topic

- Subject: `<topic, link, case study, or a few bullets>`
- Primary Search Query: `<what a marketer or business owner types into Google, e.g. "b2b lead generation strategy", "organic customer acquisition cost">`
- Angle I care about: `<why this matters to a growing business, or leave blank>`
- Anything to leave out: `<or leave blank>`

If the subject is a link or a case study, fetch it and read it first. Do not guess facts, metrics, dates, or tools. Anything you cannot verify goes in the post as an open question, or is cut.

### Voice — the part that matters most

Write like you are explaining this to a smart business partner or marketing director over coffee.

- Short sentences. One idea each. If a sentence needs a comma to breathe, split it.
- Simple words. Say "use" not "utilise", "make" not "facilitate", "so" not "consequently".
- Second person. "You launch an ad set… you wait for conversions." Put the reader in the scene.
- Concrete before abstract. A real example, a real metric, a real dollar figure — then the idea behind it.
- Define a term the first time you use it, in the same sentence. Never let jargon stand alone.
- Analogies are welcome if they are one line and accurate.
- No filler openers ("In today's fast-paced digital world…"), no hype adjectives, no exclamation marks.
- Take a position. Say whether a tactic is worth your time and budget, and say why.
- Explain the downside too. Honest, grounded posts are the ones that earn trust.

### Shape

1. **Hook** — the friction the reader already feels (e.g. rising ad spend, low conversion rates). Two or three sentences, no throat-clearing.
2. **The short version** — 3 bullets: what it is, what it does for you, where it stops or what it costs.
3. **Body** — 3–5 `h2` sections, each answering one question a reader would actually ask ("Why do typical campaigns fail?", "How do you capture commercial intent?", "How should you allocate budget?").
4. **Show, don't tell** — one practical table, framework, or workflow diagram.
5. **What it is not** — a bullet list of limits and trade-offs. This builds trust.
6. **Takeaway** — one sentence plus one small action the reader can do this week.
7. **Links** — authoritative reference sources.

Length: 800–1200 words.

---

### Complete SEO Process (Search Intent Focused)

Every post must be engineered for Google search intent, high organic click-through rates (CTR), and rich social snippets. Do **not** waste title space on brand prefixes or generic naming.

#### 1. Search-Intent Focused Title (`<title>`)
- **Formula:** `[Primary Search Query / Problem Solved] + [Specific Value or Constraint] + [Action Hook]`
- **Length:** 50–60 characters max.
- **Rule:** Target what marketers actually type in Google ("b2b lead generation strategy", "organic customer acquisition", "google ads vs seo").

#### 2. Search-Intent Meta Description (`<meta name="description">`)
- **Formula:** `[Target problem solved] + [Exact methods / funnels / actions] + [Outcome or CAC/speed benefit].`
- **Length:** 140–160 characters.

#### 3. Featured Image & Social Cards
- **Specs:** 1200×630 diagram or high-res visual in `assets/images/<year>/`.
- **Open Graph & Twitter Cards:** Complete tags with canonical URL ending in `https://www.grofolio.tech/<slug>/`.

#### 4. Schema.org JSON-LD Structured Data
Include valid `BlogPosting` schema in `<head>` for rich snippets.

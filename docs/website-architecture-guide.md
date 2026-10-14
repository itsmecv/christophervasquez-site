# Website Architecture & Publishing Guide

## How it all fits together

Your site runs on a simple pipeline with no manual deploy step:

```
GitHub repo (itsmecv/christophervasquez-site)
        │  push to "main"
        ▼
Cloudflare Pages project (christophervasquez-site)
  - pulls the repo
  - runs: python3 build.py
  - publishes the output
        │
        ▼
  4 live domains (all serve the same site)
```

## The pieces

**GitHub repository** — `github.com/itsmecv/christophervasquez-site` (public)
- `content/posts/` — blog posts as Markdown files
- `content/home.md`, `content/services.md` — the main pages
- `assets/` — images used by posts and pages
- `build.py` — the build script Cloudflare runs on every push

**Cloudflare Pages** — project `christophervasquez-site`
- Connected directly to the GitHub repo (production branch: `main`)
- Build command: `python3 build.py`, output directory: `public`
- Every push to `main` triggers a fresh build and deploy automatically (~1–2 minutes)
- Preview URL: `https://christophervasquez-site.pages.dev`

**Domains** — all four point at the Pages project via CNAME records:
- `christophervasquez.net`
- `www.christophervasquez.net`
- `threefoldeight.com`
- `www.threefoldeight.com`

All four are CNAME records → `christophervasquez-site.pages.dev`, proxied through Cloudflare. Both domains are registered at Porkbun.

## Publishing a blog post (from your phone)

You only need the GitHub app (or github.com in a browser). No computer, no Muse.

**Step 1 — Upload your images**

1. Open the repo `itsmecv/christophervasquez-site` in the GitHub app
2. Go into the `assets` folder
3. Tap Add file → Upload files, and pick your images
4. Name them clearly, e.g. `my-post-0.jpg`, `my-post-1.jpg`
5. Commit directly to `main`

**Step 2 — Create the post**

1. Go into `content/posts/`
2. Tap Add file → Create new file
3. Name it with a slug, e.g. `my-post-title.md`
4. Paste this template and fill it in:

```markdown
---
title: My Post Title
date: 2026-10-14
---

Your opening paragraph here...

![describe the image](../assets/my-post-0.jpg)

More text...

![describe the second image](../assets/my-post-1.jpg)

Final paragraph...
```

5. Commit directly to `main`

**Step 3 — Done.** Cloudflare picks up the push, rebuilds, and deploys. Your post is live on all four domains in about a minute or two.

## Image rules

- Put image files in the `assets/` folder (repo root, next to `content/`)
- Reference them from posts as `../assets/filename.jpg`
- JPG, PNG, and GIF all work
- Keep filenames lowercase with dashes, no spaces (e.g. `kitchen-cabinets-0.jpg`)

## Editing an existing post or page

1. Open the file in the GitHub app (`content/posts/...` or `content/home.md`)
2. Tap the pencil icon, make your edits
3. Commit to `main` — redeploys automatically

## Rollback

Wix is still published as a fallback until you confirm the new sites look right on your phone. The old Cloudflare Pages project (`christophervasquez`) also still exists but serves nothing.

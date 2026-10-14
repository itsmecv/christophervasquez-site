# christophervasquez.net — static site

A plain static rebuild of christophervasquez.net and threefoldeight.com.
No frameworks, no build tools beyond Python 3 (standard library only).

## How publishing works

This repo is connected directly to Cloudflare Pages. The entire deploy
pipeline is:

1. Commit changes to the `main` branch (from the GitHub app, the web UI,
   or any git client).
2. Cloudflare Pages detects the push, runs `python3 build.py`, and
   publishes the generated `public/` directory.
3. The new version is live on all four domains in about 1–2 minutes.

There is no manual deploy step and no other automation. If you can commit,
you can publish.

## Repository layout

| Path | Purpose |
|---|---|
| `content/home.md` | Home page source |
| `content/services.md` | Services page source |
| `content/posts/<slug>.md` | One Markdown file per blog post (see format below) |
| `assets/` | Images referenced by posts; copied through to `public/assets/` |
| `build.py` | The site generator (Python 3, stdlib only) |
| `public/` | Generated output — **what gets deployed**. Never edit by hand; it is overwritten on every build |
| `docs/` | Reference documents (architecture guide, etc.). Not published to the site |

## Adding a blog post

1. Create `content/posts/<slug>.md`, e.g. `content/posts/my-trip.md`,
   with `title:` and `date:` front matter:

   ```markdown
   ---
   title: My New Post
   date: 2026-10-14
   ---

   Post body in Markdown...
   ```

2. If the post needs images, upload them to `assets/` (lowercase names,
   dashes instead of spaces, e.g. `my-trip-0.jpg`) and reference them as:

   ```markdown
   ![alt text](../assets/my-trip-0.jpg)
   ```

3. Commit to `main`. Cloudflare rebuilds and deploys automatically.

The post page appears at `/blog/<slug>.html` and is added to the blog
index automatically, newest first by date.

A complete worked example (lorem ipsum text with two embedded images) is in
[`docs/website-architecture-guide.md`](docs/website-architecture-guide.md).

## Editing existing content

Edit the Markdown in `content/`, commit to `main`, and the site
regenerates. To preview locally before committing:

```bash
python3 build.py
# open public/index.html in a browser
```

## Full architecture

See [`docs/website-architecture-guide.md`](docs/website-architecture-guide.md)
(also as [PDF](docs/website-architecture-guide.pdf)) for the complete
picture: the GitHub → Cloudflare Pages pipeline, the DNS setup for all
four domains, the publish sequence, and phone-friendly upload directions.

## Domains and DNS

Four hostnames serve this site, all CNAME records (proxied) pointing at
the Pages project — no A records:

- `christophervasquez.net` → `christophervasquez-site.pages.dev`
- `www.christophervasquez.net` → `christophervasquez-site.pages.dev`
- `threefoldeight.com` → `christophervasquez-site.pages.dev`
- `www.threefoldeight.com` → `christophervasquez-site.pages.dev`

Both domains are registered at Porkbun. `social.threefoldeight.com` is
separate and points at the Mastodon host — do not touch it.

> **Lesson learned:** when moving custom domains between Cloudflare Pages
> projects, point the DNS CNAMEs at the *new* project's `pages.dev`
> address **first**, then attach the domains. Attaching first leaves them
> stuck in "pending" validation.

## Cloudflare Pages settings

- Project: `christophervasquez-site`
- Production branch: `main`
- Build command: `python3 build.py`
- Output directory: `public`

## Troubleshooting

- **Push didn't deploy:** check the Cloudflare Pages dashboard for the
  project — failed builds show their logs there. The most common cause is
  a Python error in `build.py`.
- **Post missing from the blog index:** check the `date:` front matter —
  posts sort newest-first, and a missing or malformed date can misplace it.
- **Image not showing:** confirm the file is in `assets/` and the post
  references it as `../assets/<filename>` with the exact filename
  (case-sensitive).
- **Domain not loading:** verify the CNAME still points at
  `christophervasquez-site.pages.dev` in the Cloudflare DNS dashboard.

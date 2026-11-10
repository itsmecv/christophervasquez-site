#!/usr/bin/env python3
"""
Static site builder for christophervasquez.net.

Editable sources live in content/ :
  content/home.md, content/services.md        -> home and services pages
  content/posts/<slug>.md                     -> one blog post each, with front matter:
      ---
      title: My Post Title
      date: 2026-04-28
      ---
  content/notes/<slug>.md                     -> one short microblog note each,
                                                 front matter has date only:
      ---
      date: 2026-04-28 14:30
      ---

Images referenced by posts live in assets/ and are copied through to public/assets/.

The build also generates:
  public/feed.xml     Atom feed of all posts and notes. Bridgy Fed polls it to
                      bridge the site into the fediverse (and Bluesky), so
                      people can follow @christophervasquez.net@christophervasquez.net
                      from Mastodon. IMPORTANT: never send a webmention to
                      fed.brid.gy for this site -- once any webmention arrives,
                      Bridgy Fed stops reading the feed and expects webmentions
                      for everything.
  public/_redirects   Cloudflare Pages redirects for /.well-known/webfinger
                      and host-meta, pointing at fed.brid.gy so the domain
                      handle above resolves.

Usage:
    python3 build.py          # regenerates public/ from content/

Adding a new post:
    1. Drop a new file content/posts/my-new-post.md (with title/date front matter).
    2. Put any images it needs in assets/.
    3. Run: python3 build.py

Adding a new note (microblog):
    1. Drop a new file content/notes/my-note.md with a date front matter only
       (no title -- notes are bridged to the fediverse as full-text posts,
       while titled posts are bridged as title + link).
    2. Run: python3 build.py
"""
import os
import re
import shutil
from datetime import date, datetime
from xml.sax.saxutils import escape as xml_escape

try:
    from zoneinfo import ZoneInfo
    LOCAL_TZ = ZoneInfo("America/Los_Angeles")
except Exception:  # no tzdata available; fall back to a fixed PST offset
    from datetime import timezone, timedelta
    LOCAL_TZ = timezone(timedelta(hours=-8))

SITE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(SITE, "content")
POSTS_DIR = os.path.join(CONTENT, "posts")
NOTES_DIR = os.path.join(CONTENT, "notes")
ASSETS = os.path.join(SITE, "assets")
PUBLIC = os.path.join(SITE, "public")

SITE_URL = "https://christophervasquez.net"
AUTHOR_NAME = "Christopher Vasquez"
FEDIVERSE_HANDLE = "@christophervasquez.net@christophervasquez.net"

# ---------------------------------------------------------------------------
# Markdown -> HTML (minimal built-in converter; no dependencies required)
# ---------------------------------------------------------------------------

def _inline(text):
    """Inline markdown: images, links, bold, italic, code."""
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',
                 r'<img src="\2" alt="\1" loading="lazy">', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

def markdown_to_html(md):
    """Convert a markdown string to an HTML fragment."""
    lines = md.split("\n")
    out, para, in_list = [], [], False
    def flush_para():
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para.clear()
    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False
    for line in lines:
        s = line.strip()
        if not s:
            flush_para(); close_list(); continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            flush_para(); close_list()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>" + _inline(m.group(2)) + f"</h{lvl}>")
            continue
        if re.match(r"^[-*]\s+", s):
            flush_para()
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append("<li>" + _inline(re.sub(r"^[-*]\s+", "", s)) + "</li>")
            continue
        if s.startswith(">"):
            flush_para(); close_list()
            out.append("<blockquote>" + _inline(s.lstrip("> ").strip()) + "</blockquote>")
            continue
        close_list()
        para.append(s)
    flush_para(); close_list()
    return "\n".join(out)

# ---------------------------------------------------------------------------
# Front matter
# ---------------------------------------------------------------------------

def read_markdown(path):
    """Return (front_matter dict, body markdown)."""
    text = open(path, encoding="utf-8").read()
    meta = {}
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    else:
        body = text
    return meta, body.strip()

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------

def parse_date(raw):
    """Parse 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM' (local time) to a datetime."""
    raw = raw.strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=LOCAL_TZ)
        except ValueError:
            continue
    return datetime(1970, 1, 1, tzinfo=LOCAL_TZ)

def iso(dt):
    return dt.isoformat()

def human_date(dt):
    return dt.strftime("%B %-d, %Y")

def human_datetime(dt):
    return dt.strftime("%B %-d, %Y, %-I:%M %p")

def absolutize(html, page_dir):
    """Rewrite relative asset/link URLs in a fragment to absolute site URLs.

    page_dir is the fragment's directory relative to the site root
    ('blog' or 'notes'); fragments there reference assets as ../assets/...
    """
    html = html.replace('src="../assets/', f'src="{SITE_URL}/assets/')
    html = html.replace('href="../assets/', f' href="{SITE_URL}/assets/')
    html = html.replace('src="assets/', f'src="{SITE_URL}/assets/')
    html = html.replace('href="assets/', f' href="{SITE_URL}/assets/')
    return html

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

BASE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title} | Christopher Vasquez</title>
<link rel="stylesheet" href="{root}styles.css">
<link rel="alternate" type="application/atom+xml" title="Christopher Vasquez — posts and notes" href="{root}feed.xml">
</head>
<body>
<header class="site-header">
  <a class="brand" href="{root}index.html">Christopher Vasquez</a>
  <nav>
    <a href="{root}index.html">Home</a>
    <a href="{root}blog/index.html">Blog</a>
    <a href="{root}notes/index.html">Notes</a>
    <a href="{root}services.html">Services</a>
    <a href="https://social.threefoldeight.com/@itsmecv" rel="me">Mastodon</a>
  </nav>
</header>
<main>
{content}
</main>
<footer class="site-footer">
  <p>&copy; Christopher Vasquez &middot; Seattle, WA</p>
  <p class="social">
    <a href="https://social.threefoldeight.com/@itsmecv" rel="me">Mastodon</a>
    &middot;
    <a href="https://www.linkedin.com/in/christopheravasquez/">LinkedIn</a>
  </p>
  <p class="social">Follow this site on the fediverse: {fediverse_handle}</p>
</footer>
</body>
</html>
"""

# Representative h-card for the home page: Bridgy Fed reads the bridged
# profile (name, photo, bio) from this block.
HCARD = """
<div class="h-card profile-card">
  <img class="u-photo" src="assets/home-portrait.jpg" alt="Christopher Vasquez">
  <div>
    <p class="profile-name"><a class="p-name u-url" rel="me" href="https://christophervasquez.net/">Christopher Vasquez</a></p>
    <p class="p-note">Technology leader in Seattle, WA. Product and engineering
    leadership, coffee, and nailing the fundamentals. This site is on the
    fediverse: follow {fediverse_handle} from Mastodon or any fediverse app.</p>
  </div>
</div>
"""

CSS = """/* christophervasquez.net */
:root { --maxw: 760px; --ink: #222; --muted: #666; --accent: #1a5fb4; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
       color: var(--ink); line-height: 1.65; margin: 0; background: #fff; }
.site-header { display: flex; justify-content: space-between; align-items: center;
  padding: 1rem 1.5rem; border-bottom: 1px solid #eee; }
.brand { font-weight: 700; font-size: 1.15rem; color: var(--ink); text-decoration: none; }
nav a { margin-left: 1.25rem; color: var(--accent); text-decoration: none; }
nav a:hover { text-decoration: underline; }
main { max-width: var(--maxw); margin: 0 auto; padding: 2rem 1.5rem 3rem; }
h1 { font-size: 2rem; line-height: 1.25; }
h2 { font-size: 1.45rem; margin-top: 2rem; }
h3 { font-size: 1.15rem; }
img { max-width: 100%; height: auto; display: block; margin: 1.5rem auto; }
a { color: var(--accent); }
.post-date { color: var(--muted); font-size: 0.95rem; margin-top: -0.75rem; }
.post-meta { color: var(--muted); font-size: 0.9rem; margin-top: 2rem; }
.post-list { list-style: none; padding: 0; }
.post-list li { margin: 0 0 1.1rem; }
.post-list .d { color: var(--muted); font-size: 0.9rem; margin-left: 0.6rem; }
.note { border-bottom: 1px solid #eee; padding: 1.25rem 0; }
.note .post-meta { margin-top: 0.75rem; }
.profile-card { display: flex; gap: 1rem; align-items: center;
  border: 1px solid #eee; border-radius: 8px; padding: 1rem; margin-top: 2.5rem; }
.profile-card img { width: 72px; height: 72px; object-fit: cover;
  border-radius: 50%; margin: 0; flex: none; }
.profile-card p { margin: 0.25rem 0; }
.profile-name { font-weight: 700; }
blockquote { border-left: 3px solid #ddd; margin: 1.5rem 0; padding: 0.25rem 1rem; color: #444; }
code { background: #f4f4f4; padding: 0.1em 0.35em; border-radius: 3px; }
.site-footer { text-align: center; color: var(--muted); font-size: 0.9rem;
  padding: 2rem 1rem; border-top: 1px solid #eee; }
.back { display: inline-block; margin-top: 2rem; }
"""

# Cloudflare Pages redirects: let fed.brid.gy answer WebFinger / host-meta
# for this domain so @christophervasquez.net@christophervasquez.net resolves.
REDIRECTS = """/.well-known/host-meta https://fed.brid.gy/.well-known/host-meta 302
/.well-known/host-meta.xrd https://fed.brid.gy/.well-known/host-meta.xrd 302
/.well-known/webfinger https://fed.brid.gy/.well-known/webfinger 302
"""

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    print("wrote", os.path.relpath(path, SITE))

def render_page(page_title, root, content):
    return BASE.format(page_title=page_title, root=root, content=content,
                       fediverse_handle=FEDIVERSE_HANDLE)

def main():
    # fresh output dir
    if os.path.isdir(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(os.path.join(PUBLIC, "blog"))
    os.makedirs(os.path.join(PUBLIC, "notes"))

    # assets + stylesheet + redirects
    if os.path.isdir(ASSETS):
        shutil.copytree(ASSETS, os.path.join(PUBLIC, "assets"))
    open(os.path.join(PUBLIC, "styles.css"), "w").write(CSS)
    open(os.path.join(PUBLIC, "_redirects"), "w").write(REDIRECTS)

    # home + services
    for name in ("home", "services"):
        meta, body = read_markdown(os.path.join(CONTENT, name + ".md"))
        html = markdown_to_html(body)
        if name == "home":
            html += HCARD.format(fediverse_handle=FEDIVERSE_HANDLE)
        out = "index.html" if name == "home" else "services.html"
        write(os.path.join(PUBLIC, out),
              render_page(meta.get("title", name.title()), "", html))

    # posts
    posts = []
    if os.path.isdir(POSTS_DIR):
        for fn in sorted(os.listdir(POSTS_DIR)):
            if not fn.endswith(".md"):
                continue
            slug = fn[:-3]
            meta, body = read_markdown(os.path.join(POSTS_DIR, fn))
            dt = parse_date(meta.get("date", "1970-01-01"))
            posts.append({
                "slug": slug,
                "title": meta.get("title", slug),
                "dt": dt,
                "html": markdown_to_html(body),
                "url": f"{SITE_URL}/blog/{slug}.html",
            })
    posts.sort(key=lambda p: p["dt"], reverse=True)

    for p in posts:
        content = (
            f"<article class=\"h-entry\">\n"
            f"<h1 class=\"p-name\">{p['title']}</h1>\n"
            f"<p class=\"post-date\"><time class=\"dt-published\" "
            f"datetime=\"{iso(p['dt'])}\">{human_date(p['dt'])}</time></p>\n"
            f"<div class=\"e-content\">\n{p['html']}\n</div>\n"
            f"<p class=\"post-meta\">by <a class=\"p-author h-card\" "
            f"href=\"{SITE_URL}/\">{AUTHOR_NAME}</a> &middot; "
            f"<a class=\"u-url\" href=\"{p['url']}\">permalink</a></p>\n"
            f'<a class="back" href="index.html">&larr; All posts</a>\n</article>')
        write(os.path.join(PUBLIC, "blog", p["slug"] + ".html"),
              render_page(p["title"], "../", content))

    # blog index
    items = "\n".join(
        f'<li><a href="{p["slug"]}.html">{p["title"]}</a>'
        f'<span class="d">{human_date(p["dt"])}</span></li>' for p in posts)
    index_content = f"<h1>Blog</h1>\n<ul class=\"post-list\">\n{items}\n</ul>"
    write(os.path.join(PUBLIC, "blog", "index.html"),
          render_page("Blog", "../", index_content))

    # notes (microblog: no titles; bridged to the fediverse as full-text notes)
    notes = []
    if os.path.isdir(NOTES_DIR):
        for fn in sorted(os.listdir(NOTES_DIR)):
            if not fn.endswith(".md"):
                continue
            slug = fn[:-3]
            meta, body = read_markdown(os.path.join(NOTES_DIR, fn))
            dt = parse_date(meta.get("date", "1970-01-01"))
            notes.append({
                "slug": slug,
                "dt": dt,
                "html": markdown_to_html(body),
                "url": f"{SITE_URL}/notes/{slug}.html",
            })
    notes.sort(key=lambda n: n["dt"], reverse=True)

    def note_html(n, standalone):
        return (
            f"<article class=\"h-entry note\">\n"
            f"<div class=\"e-content\">\n{n['html']}\n</div>\n"
            f"<p class=\"post-meta\"><time class=\"dt-published\" "
            f"datetime=\"{iso(n['dt'])}\">{human_datetime(n['dt'])}</time>"
            f" &middot; by <a class=\"p-author h-card\" "
            f"href=\"{SITE_URL}/\">{AUTHOR_NAME}</a> &middot; "
            f"<a class=\"u-url\" href=\"{n['url']}\">permalink</a></p>\n"
            f"</article>")

    for n in notes:
        content = note_html(n, True) + \
            '\n<a class="back" href="index.html">&larr; All notes</a>'
        write(os.path.join(PUBLIC, "notes", n["slug"] + ".html"),
              render_page("Note", "../", content))

    # notes index (an h-feed of full notes)
    feed_items = "\n".join(note_html(n, False) for n in notes)
    notes_index = (
        f"<h1>Notes</h1>\n"
        f"<p>Short posts and updates. Follow along on the fediverse: "
        f"{FEDIVERSE_HANDLE}, or subscribe to the "
        f"<a href=\"../feed.xml\">feed</a>.</p>\n"
        f"<div class=\"h-feed\">\n{feed_items}\n</div>")
    write(os.path.join(PUBLIC, "notes", "index.html"),
          render_page("Notes", "../", notes_index))

    # Atom feed (posts + notes) -- Bridgy Fed polls this to bridge the site
    entries = []
    for p in posts:
        entries.append({"title": p["title"], "dt": p["dt"], "url": p["url"],
                        "html": absolutize(p["html"], "blog")})
    for n in notes:
        entries.append({"title": "", "dt": n["dt"], "url": n["url"],
                        "html": absolutize(n["html"], "notes")})
    entries.sort(key=lambda e: e["dt"], reverse=True)
    latest = entries[0]["dt"] if entries else parse_date("1970-01-01")

    parts = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f"<title>{AUTHOR_NAME}</title>",
        "<subtitle>Posts and notes from christophervasquez.net</subtitle>",
        f'<link href="{SITE_URL}/feed.xml" rel="self"/>',
        f'<link href="{SITE_URL}/"/>',
        f"<id>{SITE_URL}/</id>",
        f"<updated>{iso(latest)}</updated>",
        f"<author><name>{AUTHOR_NAME}</name><uri>{SITE_URL}/</uri></author>",
    ]
    for e in entries:
        parts += [
            "<entry>",
            f"<title>{xml_escape(e['title'])}</title>",
            f'<link href="{e["url"]}"/>',
            f"<id>{e['url']}</id>",
            f"<published>{iso(e['dt'])}</published>",
            f"<updated>{iso(e['dt'])}</updated>",
            f'<content type="html">{xml_escape(e["html"])}</content>',
            "</entry>",
        ]
    parts.append("</feed>")
    write(os.path.join(PUBLIC, "feed.xml"), "\n".join(parts) + "\n")

    print(f"done: {len(posts)} posts, {len(notes)} notes -> {PUBLIC}")

if __name__ == "__main__":
    main()

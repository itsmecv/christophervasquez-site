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

Images referenced by posts live in assets/ and are copied through to public/assets/.

Usage:
    python3 build.py          # regenerates public/ from content/

Adding a new post:
    1. Drop a new file content/posts/my-new-post.md (with title/date front matter).
    2. Put any images it needs in assets/.
    3. Run: python3 build.py
"""
import os
import re
import shutil
from datetime import date

SITE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(SITE, "content")
POSTS_DIR = os.path.join(CONTENT, "posts")
ASSETS = os.path.join(SITE, "assets")
PUBLIC = os.path.join(SITE, "public")

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
# Templates
# ---------------------------------------------------------------------------

BASE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title} | Christopher Vasquez</title>
<link rel="stylesheet" href="{root}styles.css">
</head>
<body>
<header class="site-header">
  <a class="brand" href="{root}index.html">Christopher Vasquez</a>
  <nav>
    <a href="{root}index.html">Home</a>
    <a href="{root}blog/index.html">Blog</a>
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
</footer>
</body>
</html>
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
.post-list { list-style: none; padding: 0; }
.post-list li { margin: 0 0 1.1rem; }
.post-list .d { color: var(--muted); font-size: 0.9rem; margin-left: 0.6rem; }
blockquote { border-left: 3px solid #ddd; margin: 1.5rem 0; padding: 0.25rem 1rem; color: #444; }
code { background: #f4f4f4; padding: 0.1em 0.35em; border-radius: 3px; }
.site-footer { text-align: center; color: var(--muted); font-size: 0.9rem;
  padding: 2rem 1rem; border-top: 1px solid #eee; }
.back { display: inline-block; margin-top: 2rem; }
"""

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    print("wrote", os.path.relpath(path, SITE))

def main():
    # fresh output dir
    if os.path.isdir(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(os.path.join(PUBLIC, "blog"))

    # assets + stylesheet
    if os.path.isdir(ASSETS):
        shutil.copytree(ASSETS, os.path.join(PUBLIC, "assets"))
    open(os.path.join(PUBLIC, "styles.css"), "w").write(CSS)

    # home + services
    for name in ("home", "services"):
        meta, body = read_markdown(os.path.join(CONTENT, name + ".md"))
        html = markdown_to_html(body)
        out = "index.html" if name == "home" else "services.html"
        write(os.path.join(PUBLIC, out),
              BASE.format(page_title=meta.get("title", name.title()),
                          root="", content=html))

    # posts
    posts = []
    for fn in sorted(os.listdir(POSTS_DIR)):
        if not fn.endswith(".md"):
            continue
        slug = fn[:-3]
        meta, body = read_markdown(os.path.join(POSTS_DIR, fn))
        posts.append({
            "slug": slug,
            "title": meta.get("title", slug),
            "date": meta.get("date", "1970-01-01"),
            "html": markdown_to_html(body),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)

    for p in posts:
        content = (f"<article>\n<h1>{p['title']}</h1>\n"
                   f"<p class=\"post-date\">{p['date']}</p>\n"
                   f"{p['html']}\n"
                   f'<a class="back" href="index.html">&larr; All posts</a>\n</article>')
        write(os.path.join(PUBLIC, "blog", p["slug"] + ".html"),
              BASE.format(page_title=p["title"], root="../", content=content))

    # blog index
    items = "\n".join(
        f'<li><a href="{p["slug"]}.html">{p["title"]}</a>'
        f'<span class="d">{p["date"]}</span></li>' for p in posts)
    index_content = f"<h1>Blog</h1>\n<ul class=\"post-list\">\n{items}\n</ul>"
    write(os.path.join(PUBLIC, "blog", "index.html"),
          BASE.format(page_title="Blog", root="../", content=index_content))

    print(f"done: {len(posts)} posts -> {PUBLIC}")

if __name__ == "__main__":
    main()

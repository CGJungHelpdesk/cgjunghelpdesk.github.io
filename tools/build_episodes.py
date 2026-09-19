#!/usr/bin/env python3
"""Regenerates /e/NNN.html from the podcast feed — one page per numbered episode.

Run from the repo root whenever a new episode is out:
    python3 tools/build_episodes.py
Each page keeps the episode as the headline (so shared links preview with the
episode's own title and artwork) and pitches the app underneath.
"""
import html, re, sys, urllib.request
from pathlib import Path

FEED = "https://feeds.redcircle.com/c1a3de7b-1b92-4c7f-8e36-8484721d29f4"
ROOT = Path(__file__).resolve().parent.parent
SITE = "https://cgjunghelpdesk.github.io"

def fetch():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
    request = urllib.request.Request(FEED, headers={"User-Agent": "JungHelpdesk-site/1.0"})
    return urllib.request.urlopen(request, timeout=40).read().decode("utf-8", "ignore")

def tag(item, name):
    match = re.search(rf"<{name}[^>]*>(.*?)</{name}>", item, re.S)
    if not match: return ""
    text = match.group(1).strip()
    cdata = re.match(r"<!\[CDATA\[(.*)\]\]>$", text, re.S)
    return (cdata.group(1) if cdata else html.unescape(text)).strip()

def plain(text, limit=420):
    text = re.sub(r"<br\s*/?>|</p>", " ", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit: return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"

def minutes(raw):
    parts = [int(float(p)) for p in raw.split(":")] if raw else []
    seconds = sum(p * 60 ** i for i, p in enumerate(reversed(parts)))
    return f"{round(seconds / 60)} min" if seconds else ""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — C.G. Jung Helpdesk</title>
<meta name="description" content="{summary_attr}">
<meta property="og:title" content="{title} — C.G. Jung Helpdesk">
<meta property="og:description" content="{summary_attr}">
<meta property="og:image" content="{image}">
<meta property="og:type" content="music.song">
<meta property="og:url" content="{site}/e/{number}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#131110">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600&display=swap">
<link rel="stylesheet" href="/site.css">
</head>
<body>
<header class="top">
  <a class="brand" href="/"><img src="/img/icon.png" alt="" width="34" height="34"><span>Jung Helpdesk</span></a>
  <nav><a class="nav-cta" href="/">About the app</a></nav>
</header>
<main class="ep">
  <div class="ep-card">
    <img src="{image}" alt="" width="132" height="132">
    <div>
      <p class="eyebrow">Episode {number}</p>
      <h1>{title}</h1>
      <p class="meta">{meta}<span id="moment"></span></p>
    </div>
  </div>
  <p class="ep-sum">{summary}</p>
  <div class="cta-row">
    <a class="btn ghost" href="{listen}">Listen on RedCircle</a>
  </div>

  <section class="ep-pitch">
    <div>
      <p class="eyebrow">Shared from the Jung Helpdesk app</p>
      <h2>This episode is one star on a map of sixty.</h2>
      <p>The app turns the C.G. Jung Helpdesk podcast into curated journeys, a star map of every episode, and transcripts you can search. With the app installed, this link opens right at the shared moment.</p>
      <div class="cta-row">
        <a class="btn" href="#" data-store>Coming soon to the App Store</a>
        <a class="btn ghost" href="/">See the app</a>
      </div>
    </div>
    <div class="phone"><img src="/img/08-map-selected.jpg" alt="The app's star map with one episode selected" width="660" height="1434" loading="lazy"></div>
  </section>
</main>
<footer class="foot">
  <span>© 2026 C.G. Jung Helpdesk</span>
  <a href="/support.html">Support</a>
  <a href="/privacy.html">Privacy</a>
</footer>
<script src="/site.js"></script>
<script>
  const t = parseInt(new URLSearchParams(location.search).get("t"), 10);
  if (t > 0) {{
    const h = Math.floor(t / 3600), m = Math.floor(t % 3600 / 60), s = t % 60;
    const clock = (h ? h + ":" + String(m).padStart(2, "0") : m) + ":" + String(s).padStart(2, "0");
    document.getElementById("moment").textContent = " · shared at " + clock;
  }}
</script>
</body>
</html>
"""

def main():
    feed = fetch()
    show_image = re.search(r'<itunes:image href="([^"]+)"', feed)
    count = 0
    for item in re.findall(r"<item>(.*?)</item>", feed, re.S):
        raw_title = tag(item, "title")
        match = re.match(r"\s*(\d{1,3})\s*-\s*(.+)", raw_title)
        if not match: continue
        number = f"{int(match.group(1)):03d}"
        title = re.sub(r"\s*\(remastered\)\s*$", "", match.group(2), flags=re.I)
        image = re.search(r'<itunes:image href="([^"]+)"', item) or show_image
        summary = plain(tag(item, "description") or tag(item, "itunes:summary"))
        date = re.search(r"\d{1,2} \w{3} \d{4}", tag(item, "pubDate"))
        meta = " · ".join(p for p in [date.group(0) if date else "", minutes(tag(item, "itunes:duration"))] if p)
        page = PAGE.format(
            title=html.escape(title), number=number, site=SITE,
            summary=html.escape(summary), summary_attr=html.escape(summary[:200], quote=True),
            image=html.escape(image.group(1) if image else f"{SITE}/img/og.jpg", quote=True),
            meta=html.escape(meta),
            listen="https://redcircle.com/shows/c-g-jung-helpdesk",
        )
        (ROOT / "e" / f"{number}.html").write_text(page, encoding="utf-8")
        count += 1
    print(f"wrote {count} episode pages")

if __name__ == "__main__":
    main()

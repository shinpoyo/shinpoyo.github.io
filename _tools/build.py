#!/usr/bin/env python3
"""_src/*.html（ページ本文）に共通のヘッダー・フッターを付けて、公開用の HTML を書き出す。

使い方：python3 _tools/build.py
- _src の各ファイルは、先頭に「キー: 値」の行、`---` の行、その下に本文を書く
  - path: 出力先（例：works/mashimashida/ → works/mashimashida/index.html。トップは空）
  - title: ページ名（<title> は「ページ名 | shinpoyo」になる。トップはサイト名のみ）
  - description: 検索結果・共有カードの説明
  - nav: ヘッダーで強調するメニュー（top / works / about / contact）
  - image: 共有カード画像（省略時は assets/img/ogp.jpg）
  - date: 記事の公開日（YYYY-MM-DD）。date があるページは「記事」として一覧に載る
  - summary: 記事一覧に出す1〜2文の紹介
  - crumb: パンくず（構造化データ）での短い名前（省略時は title の「 — 」より前）
  - game_url / genre / lang: 作品ページ用。遊ぶ URL（例：mashimashida/）・ジャンル・対応言語（例：ja,en）
  - catch: 作品ページ用。「ほかの作品」に出す一言の紹介
  - updated: 作品ページ用。ゲーム本体の最終更新日（YYYY-MM-DD）
- 本文に `<!-- ARTICLES -->` と書くと記事一覧（新しい順）、`<!-- ARTICLES:3 -->` で最新3件に置き換わる
- 記事ページは本文の先頭に公開日、末尾にシェアのリンクと「ほかの記事」を自動で付ける
- 作品ページ（game_url があるページ）は、見出しの下に作った人と最終更新日、本文の途中と末尾に広告枠、末尾にシェアのリンクと「ほかの作品」を自動で付ける
- 記事は feed.xml（Atom）にも書き出す
- 各ページに構造化データ（JSON-LD）を付け、sitemap.xml には git の最終コミット日を lastmod として入れる
- `_` で始まるフォルダは GitHub Pages（Jekyll）で公開されない
"""
from pathlib import Path
from datetime import date
from urllib.parse import quote
import html
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://shinpoyo.com/"
AUTHOR = {"@type": "Person", "name": "shinpoyo", "url": SITE + "about/"}

NAV = [
    ("top", "/", "トップ"),
    ("works", "/works/", "作品"),
    ("articles", "/articles/", "記事"),
    ("about", "/about/", "このサイトについて"),
    ("contact", "/contact/", "お問い合わせ"),
]

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="google-adsense-account" content="ca-pub-3053925393924248">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="shinpoyo">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<meta name="theme-color" content="#0b0b0c" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#fafaf7" media="(prefers-color-scheme: light)">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=M+PLUS+1p:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="alternate" type="application/atom+xml" title="shinpoyo の記事" href="/feed.xml">
{jsonld}</head>
<body>
<header class="site-header"><div class="inner">
  <a class="brand" href="/">shin<span>poyo</span></a>
  <nav class="site-nav" aria-label="サイト内メニュー">
{nav}
  </nav>
</div></header>
"""

FOOT = """<footer class="site-footer"><div class="inner">
  <span>© 2026 shinpoyo. All rights reserved.</span>
  <nav aria-label="フッターメニュー">
    <a href="/about/">このサイトについて</a>
    <a href="/privacy/">プライバシーポリシー</a>
    <a href="/contact/">お問い合わせ</a>
    <a href="https://github.com/shinpoyo">GitHub</a>
  </nav>
</div></footer>
<script src="/ads.js"></script>
</body>
</html>
"""


def parse(src: Path):
    meta, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
    data = {}
    for line in meta.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data, body


def article_list(articles, limit=None):
    items = []
    for a in articles[:limit]:
        d = a["date"]
        items.append(
            f'  <li><time datetime="{d}">{d.replace("-", ".")}</time>'
            f'<span><a href="/{a["path"]}">{html.escape(a["title"])}</a>'
            f'<br><span class="small muted">{html.escape(a.get("summary", ""))}</span></span></li>'
        )
    return '<ul class="news">\n' + "\n".join(items) + "\n</ul>"


def git_date(src: Path):
    """src の最終コミット日（YYYY-MM-DD）。未コミットの変更があれば今日"""
    def git(*args):
        try:
            return subprocess.run(["git", *args, "--", str(src)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        except OSError:
            return ""
    if git("status", "--porcelain"):
        return date.today().isoformat()
    return git("log", "-1", "--format=%cs") or date.today().isoformat()


def crumb_name(meta):
    return meta.get("crumb") or meta["title"].split(" — ")[0]


def jsonld(meta, titles):
    path = meta.get("path", "")
    url = SITE + path
    image = SITE + meta.get("image", "assets/img/ogp.jpg")
    data = []
    if not path:
        data.append({"@context": "https://schema.org", "@type": "WebSite", "name": "shinpoyo", "url": SITE,
                     "inLanguage": "ja", "description": meta["description"], "author": AUTHOR})
    else:
        items, parts = [("トップ", SITE)], path.strip("/").split("/")
        for i in range(len(parts)):
            p = "/".join(parts[: i + 1]) + "/"
            if p in titles:
                items.append((titles[p], SITE + p))
        data.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": n, "name": name, "item": u} for n, (name, u) in enumerate(items, 1)]})
    if meta.get("date"):
        article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": meta["title"],
                   "description": meta["description"], "image": image, "datePublished": meta["date"],
                   "author": AUTHOR, "publisher": AUTHOR, "mainEntityOfPage": url, "inLanguage": "ja"}
        if meta["modified"] > meta["date"]:
            article["dateModified"] = meta["modified"]
        data.append(article)
    if meta.get("game_url"):
        langs = meta.get("lang", "ja").split(",")
        data.append({"@context": "https://schema.org", "@type": "VideoGame", "name": crumb_name(meta),
                     "description": meta["description"], "url": SITE + meta["game_url"], "image": image,
                     "genre": meta.get("genre", ""), "gamePlatform": "Web browser",
                     "applicationCategory": "GameApplication", "operatingSystem": "Web browser",
                     "inLanguage": langs[0] if len(langs) == 1 else langs, "isAccessibleForFree": True,
                     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"}, "author": AUTHOR})
    return "".join(
        '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"
        for d in data)


def share_links(meta, label="この記事をシェア"):
    url = quote(SITE + meta["path"], safe="")
    text = quote(meta["title"], safe="")
    return (f'<p class="share small">{label}：'
            f'<a href="https://x.com/intent/post?text={text}&amp;url={url}" target="_blank" rel="noopener">X（Twitter）</a>'
            f'<a href="https://b.hatena.ne.jp/entry/s/{"shinpoyo.com/" + meta["path"]}" target="_blank" rel="noopener">はてなブックマーク</a></p>')


AD_SLOT = '<aside class="ad" data-ad hidden aria-label="広告"><p>広告</p></aside>'


def insert_before_nth_h2(body, n, html_block):
    """本文の n 番目の <h2 の直前に差し込む（なければ何もしない）"""
    idx = -1
    for _ in range(n):
        idx = body.find("<h2", idx + 1)
        if idx < 0:
            return body
    return body[:idx] + html_block + "\n\n  " + body[idx:]


def other_works(meta, works):
    items = []
    for w in works:
        if w["path"] == meta["path"]:
            continue
        items.append(
            f'  <li class="work"><a href="/{w["path"]}"><img src="/{w.get("image", "assets/img/ogp.jpg")}" alt="" width="1280" height="720" loading="lazy"></a>'
            f'<div class="body"><h3><a href="/{w["path"]}">{html.escape(crumb_name(w))}</a></h3>'
            f'<p>{html.escape(w.get("catch", ""))}</p></div></li>'
        )
    return '<h2>ほかの作品</h2>\n<ul class="works works-mini">\n' + "\n".join(items) + "\n</ul>"


def expand(body, meta, articles, works=()):
    body = re.sub(r"<!-- ARTICLES(?::(\d+))? -->", lambda m: article_list(articles, int(m.group(1)) if m.group(1) else None), body)
    if meta.get("date"):
        d = meta["date"]
        stamp = f'<p class="muted small">公開日：<time datetime="{d}">{d.replace("-", ".")}</time>　／　書いた人：shinpoyo</p>'
        body = body.replace("<!-- DATE -->", stamp)
        others = [a for a in articles if a["path"] != meta["path"]][:3]
        more = share_links(meta) + "\n"
        if others:
            more += "<h2>ほかの記事</h2>\n" + article_list(others)
        body = body.replace("<!-- MORE -->", more)
        body = insert_before_nth_h2(body, 3, AD_SLOT)
    if meta.get("game_url"):
        line = '<p class="muted small byline">作った人：<a href="/about/">shinpoyo</a>'
        if meta.get("updated"):
            u = meta["updated"]
            line += f'　／　ゲームの最終更新：<time datetime="{u}">{u.replace("-", ".")}</time>'
        line += "</p>"
        body = body.replace("</h1>", "</h1>\n  " + line, 1)
        body = insert_before_nth_h2(body, 2, AD_SLOT)
        tail = share_links(meta, "この作品をシェア") + "\n" + other_works(meta, works) + "\n"
        last_ad = body.rfind('<aside class="ad"')
        at = last_ad if last_ad >= 0 else body.rfind("</main>")
        body = body[:at] + tail + "  " + body[at:]
    return body


def render(meta, body, titles):
    path = meta.get("path", "")
    title = meta["title"] if not path else f"{meta['title']} | shinpoyo"
    nav = "\n".join(
        f'    <a href="{href}"' + (' aria-current="page"' if key == meta.get("nav") else "") + f">{label}</a>"
        for key, href, label in NAV
    )
    head = HEAD.format(
        title=html.escape(title),
        description=html.escape(meta["description"], quote=True),
        url=SITE + path,
        image=SITE + meta.get("image", "assets/img/ogp.jpg"),
        og_type="website" if not path else "article",
        nav=nav,
        jsonld=jsonld(meta, titles),
    )
    return head + body.strip() + "\n" + FOOT


def main():
    lastmod = {}
    pages = [(src, *parse(src)) for src in sorted((ROOT / "_src").glob("*.html"))]
    for src, meta, _ in pages:
        meta["modified"] = git_date(src)
    titles = {m.get("path", ""): crumb_name(m) for _, m, _ in pages}
    articles = sorted((m for _, m, _ in pages if m.get("date")), key=lambda m: (m["date"], m["path"]), reverse=True)
    works = [m for _, m, _ in pages if m.get("game_url")]
    for src, meta, body in pages:
        body = expand(body, meta, articles, works)
        out = ROOT / meta.get("path", "") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(meta, body, titles), encoding="utf-8")
        lastmod[SITE + meta.get("path", "")] = max(meta["modified"], meta.get("date", ""))
        print("wrote", out.relative_to(ROOT))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(lastmod):
        sitemap.append(f"  <url><loc>{u}</loc><lastmod>{lastmod[u]}</lastmod></url>")
    for g in sorted({SITE + m["game_url"] for _, m, _ in pages if m.get("game_url")}):
        sitemap.append(f"  <url><loc>{g}</loc></url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    print("wrote sitemap.xml")
    write_feed(articles)


def write_feed(articles):
    """記事の Atom フィード（新しい順に 20 件）"""
    def esc(t):
        return html.escape(t, quote=True)
    updated = max(max(a["date"], a["modified"]) for a in articles)
    entries = []
    for a in articles[:20]:
        url = SITE + a["path"]
        entries.append(
            "  <entry>\n"
            f"    <title>{esc(a['title'])}</title>\n"
            f'    <link href="{url}"/>\n'
            f"    <id>{url}</id>\n"
            f"    <published>{a['date']}T00:00:00+09:00</published>\n"
            f"    <updated>{max(a['date'], a['modified'])}T00:00:00+09:00</updated>\n"
            f"    <summary>{esc(a.get('summary', a['description']))}</summary>\n"
            "  </entry>"
        )
    feed = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        "  <title>shinpoyo の記事</title>\n"
        f'  <link href="{SITE}articles/"/>\n'
        f'  <link rel="self" href="{SITE}feed.xml"/>\n'
        f"  <id>{SITE}</id>\n"
        f"  <updated>{updated}T00:00:00+09:00</updated>\n"
        "  <author><name>shinpoyo</name></author>\n"
        + "\n".join(entries) + "\n</feed>\n"
    )
    (ROOT / "feed.xml").write_text(feed, encoding="utf-8")
    print("wrote feed.xml")


if __name__ == "__main__":
    main()

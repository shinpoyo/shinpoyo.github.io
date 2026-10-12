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
- 本文に `<!-- ARTICLES -->` と書くと記事一覧（新しい順）、`<!-- ARTICLES:3 -->` で最新3件に置き換わる
- 記事ページは本文の先頭に公開日、末尾に「ほかの記事」を自動で付ける
- `_` で始まるフォルダは GitHub Pages（Jekyll）で公開されない
"""
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://shinpoyo.com/"

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
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><circle cx='32' cy='32' r='30' fill='%23facc15'/><text x='32' y='44' font-size='34' text-anchor='middle' font-family='sans-serif' font-weight='900' fill='%23111'>s</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=M+PLUS+1p:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
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


def expand(body, meta, articles):
    import re
    body = re.sub(r"<!-- ARTICLES(?::(\d+))? -->", lambda m: article_list(articles, int(m.group(1)) if m.group(1) else None), body)
    if meta.get("date"):
        d = meta["date"]
        stamp = f'<p class="muted small">公開日：<time datetime="{d}">{d.replace("-", ".")}</time>　／　書いた人：shinpoyo</p>'
        body = body.replace("<!-- DATE -->", stamp)
        others = [a for a in articles if a["path"] != meta["path"]][:3]
        if others:
            body = body.replace("<!-- MORE -->", "<h2>ほかの記事</h2>\n" + article_list(others))
    return body


def render(meta, body):
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
    )
    return head + body.strip() + "\n" + FOOT


def main():
    urls = []
    pages = [(src, *parse(src)) for src in sorted((ROOT / "_src").glob("*.html"))]
    articles = sorted((m for _, m, _ in pages if m.get("date")), key=lambda m: (m["date"], m["path"]), reverse=True)
    for src, meta, body in pages:
        body = expand(body, meta, articles)
        out = ROOT / meta.get("path", "") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(meta, body), encoding="utf-8")
        urls.append(SITE + meta.get("path", ""))
        print("wrote", out.relative_to(ROOT))
    urls.append(SITE + "privacy/")
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(set(urls)) + [SITE + "mashimashida/", SITE + "keshikasu/", SITE + "mogumogu-camera/"]:
        sitemap.append(f"  <url><loc>{u}</loc></url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()

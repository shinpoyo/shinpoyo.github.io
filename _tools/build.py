#!/usr/bin/env python3
"""_src/*.html（ページ本文）に共通のヘッダー・フッターを付けて、公開用の HTML を書き出す。

使い方：python3 _tools/build.py
- _src の各ファイルは、先頭に「キー: 値」の行、`---` の行、その下に本文を書く
  - path: 出力先（例：works/mashimashida/ → works/mashimashida/index.html。トップは空）
  - title: ページ名（<title> は「ページ名 | shinpoyo」になる。トップはサイト名のみ）
  - description: 検索結果・共有カードの説明
  - nav: ヘッダーで強調するメニュー（top / works / about / contact）
  - image: 共有カード画像（省略時は assets/img/ogp.jpg）
- `_` で始まるフォルダは GitHub Pages（Jekyll）で公開されない
"""
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://shinpoyo.com/"

NAV = [
    ("top", "/", "トップ"),
    ("works", "/works/", "作品"),
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
    for src in sorted((ROOT / "_src").glob("*.html")):
        meta, body = parse(src)
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

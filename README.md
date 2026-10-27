# shinpoyo.github.io

shinpoyo の個人サイト **https://shinpoyo.com/** 。各プロジェクトの GitHub Pages は `https://shinpoyo.com/<リポジトリ名>/` で配信される。

## 構成

| パス | 内容 |
|---|---|
| `/` | トップ（作品一覧・お知らせ） |
| `/works/` | 作品一覧と、作品ごとの紹介ページ（遊び方・FAQ など） |
| `/articles/` | 記事（`_src` で `date:` を付けたページが自動で一覧に載る） |
| `/about/` `/contact/` `/privacy/` | このサイトについて・お問い合わせ・プライバシーポリシー |
| `assets/` | 共通 CSS（`site.css`）と画像 |
| `ads.js` | 広告（AdSense）の設定。ID が空なら何も出さない |
| `ads.txt` `robots.txt` `sitemap.xml` `feed.xml` | 広告・検索エンジン・フィード向け（`sitemap.xml` と `feed.xml` は自動で書き出す） |

## ページの編集

ページ本文は `_src/*.html` にあり、共通のヘッダー・フッターは `_tools/build.py` が付ける。

```bash
python3 _tools/build.py        # _src から各 index.html と sitemap.xml を書き出す
python3 _tools/make_icons.py   # アイコン（favicon.ico など）を作り直すときだけ
```

- `_src` を直したら必ず実行して、書き出された HTML も一緒にコミットする（GitHub Pages はビルドせずにそのまま公開）
- `_` で始まるフォルダは公開されない
- 構造化データ（JSON-LD）・パンくず・sitemap の lastmod・記事のシェアリンクは自動で付く。作品ページは `game_url:` `genre:` を書くと作品（VideoGame）として扱われる

## ドキュメント

- 独自ドメインの設定：[docs/custom-domain.md](docs/custom-domain.md)
- 広告（AdSense）の導入手順：[docs/adsense.md](docs/adsense.md)
- アクセス解析の導入手順：[docs/analytics.md](docs/analytics.md)
- サイトの品質チェックと改善の順番：[docs/quality-audit.md](docs/quality-audit.md)
- AdSense で収益を上げているサイトの特徴 20 と反映状況：[docs/adsense-success-features.md](docs/adsense-success-features.md)
- Search Console の確認手順：[docs/search-console.md](docs/search-console.md)
- 作業履歴：[docs/worklog.md](docs/worklog.md)

© 2026 shinpoyo. All rights reserved.

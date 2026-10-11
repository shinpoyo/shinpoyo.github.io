# shinpoyo.github.io

shinpoyo の個人サイト **https://shinpoyo.com/** 。各プロジェクトの GitHub Pages は `https://shinpoyo.com/<リポジトリ名>/` で配信される。

## 構成

| パス | 内容 |
|---|---|
| `/` | トップ（作品一覧・お知らせ） |
| `/works/` | 作品一覧と、作品ごとの紹介ページ（遊び方・FAQ など） |
| `/about/` `/contact/` `/privacy/` | このサイトについて・お問い合わせ・プライバシーポリシー |
| `assets/` | 共通 CSS（`site.css`）と画像 |
| `ads.js` | 広告（AdSense）の設定。ID が空なら何も出さない |
| `ads.txt` `robots.txt` `sitemap.xml` | 広告・検索エンジン向け |

## ページの編集

ページ本文は `_src/*.html` にあり、共通のヘッダー・フッターは `_tools/build.py` が付ける。

```bash
python3 _tools/build.py   # _src から各 index.html と sitemap.xml を書き出す
```

- `_src` を直したら必ず実行して、書き出された HTML も一緒にコミットする（GitHub Pages はビルドせずにそのまま公開）
- `_` で始まるフォルダは公開されない

## ドキュメント

- 独自ドメインの設定：[docs/custom-domain.md](docs/custom-domain.md)
- 広告（AdSense）の導入手順：[docs/adsense.md](docs/adsense.md)
- 作業履歴：[docs/worklog.md](docs/worklog.md)

© 2026 shinpoyo. All rights reserved.

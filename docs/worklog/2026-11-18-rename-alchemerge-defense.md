# 2026-11-18 紹介サイトのゲーム名を「アルケマージ・ディフェンス」に変更

## 依頼
ゲーム名を「アルケマージ・ディフェンス」（Alchemerge Defense）に決めたので、紹介サイト側も直す（shinji「直そうか」）。ゲーム本体は shinpoyo/alchemerge_defense#11。

## やったこと
- `_src/00-top.html`・`_src/10-works.html`・`_src/35-alchemerge-defense.html` の「アルケマージ」を「アルケマージ・ディフェンス」に、「（Alchemerge）」を「（Alchemerge Defense）」に置き換え（タイトル、説明、パンくず、見出し、作品カード、一覧表、画像の alt、iframe の title、お知らせの作品名）
- `README.md` の作品一覧の名前
- `python3 _tools/build.py` で各 `index.html` と `sitemap.xml` を書き出し直した（sitemap は更新日だけ変わる）

## 変えていないもの
- URL（`/works/alchemerge-defense/`・`/alchemerge_defense/`）と画像ファイル名
- `docs/worklog.md` の過去の記録

## 確認
- 置き換え後、「アルケマージ」単独で残っている箇所がない（`docs/` を除く）
- Playwright で作品一覧と紹介ページを開き、ページエラーなし

# 作業履歴

## 2026-10-11 個人サイトの作成（独自ドメイン案 A）

- 方針：`shinpoyo.com` を個人サイトにし、全プロジェクトの GitHub Pages を `shinpoyo.com/<リポジトリ名>/` で配信する
- `shinpoyo/shinpoyo.github.io` リポジトリを作成（ユーザーサイト用。`main` のルートをそのまま公開）
- トップページ `index.html`：作品一覧（マシマシ打・けしカス・もぐもぐカメラ）、フッターに SMUDGE プライバシーポリシーへのリンク
  - 旧版の mashimashityping は「ラーメン二郎」表記が残るため一覧から外した（URL は引き続き有効）
- `404.html`：存在しないパス用
- `CNAME` ファイルは**まだ置かない**：DNS 設定前に独自ドメインを有効にすると、`shinpoyo.github.io/*` が未設定の `shinpoyo.com` に転送されて全プロジェクトが見られなくなるため。DNS 設定後に Settings → Pages から設定する

## 2026-10-11 Cloudflare の入力方法を追記

- Add record の各欄（Name / Content・IPv4 address・IPv6 address・Target / Proxy status）に何を入れるかを [custom-domain.md](custom-domain.md) に表で追記

## 2026-10-11 GitHub に push・公開確認

- ユーザーが `shinpoyo/shinpoyo.github.io`（public・空）を作成 → `main` に push
- 約 1 分で GitHub Pages が自動で有効になり、`https://shinpoyo.github.io/` が 200（トップページ表示）
- 既存プロジェクト（mashimashida・keshikasu・mogumogu-camera・smudge-privacy）も引き続き 200、存在しないパスは自作の 404 ページ
- DNS 確認：所有確認の TXT（`_github-pages-challenge-shinpoyo.shinpoyo.com`）は登録済み。A / AAAA / CNAME はまだ

## 2026-10-11 広告（Google AdSense）の準備

- 方針：AdSense を shinpoyo.com 単位で申し込む。場所はトップ・マシマシ打の食券購入下部・完飲番付・常連カード（結果画面はポップアップ内のため置かない）
- `privacy/index.html`：プライバシーポリシーを新設（端末内保存のみ・広告 Cookie とオプトアウト・外部送信の一覧・免責・著作権・お問い合わせ）
- `ads.js`：AdSense の ID を入れると作品一覧の下に広告枠を出す。空なら何もしない
- トップのフッターにプライバシーポリシーへのリンク
- 確認：ID 空 → 広告枠なし・外部読み込みなし／ダミー ID → 枠表示・読み込み 1 回、エラーなし。プライバシーポリシーはスマホ幅で横スクロールなし
- 手順書 [adsense.md](adsense.md) を作成

## 2026-10-11 AdSense のサイト確認用設定

- ユーザーの AdSense アカウント（サイト運営者 ID `pub-3053925393924248`）を確認
- トップ `index.html` に確認用メタタグ `google-adsense-account` を追加（外部読み込みは発生しない）
- `ads.txt` を追加：`google.com, pub-3053925393924248, DIRECT, f08c47fec0942fa0`
- 広告そのものは、審査通過・広告ユニット作成後に `ads.js` へ ID を入れてから表示する

## 2026-10-11 サイトの作り込み（AdSense 審査に向けて）

- ユーザーが AdSense（AdSense for YouTube からのアップグレード）で shinpoyo.com の審査をリクエスト
- 中身を充実させるため、複数ページ構成に作り直した
  - トップ：紹介文・作品カード（スクリーンショット付き）・お知らせ
  - `/works/`：作品一覧（比較表）
  - `/works/mashimashida/`：遊び方・食券・退店ペナルティ・称号・コールの用語集・上達のコツ・FAQ
  - `/works/keshikasu/`：遊び方・つぶを増やす方法・消しゴムにもどる（てんせい）・コツ・安心して遊べる工夫・FAQ
  - `/works/mogumogu-camera/`：使い方・4つのえんしゅつ・設定・反応の調整・プライバシーと安全（広告は置かない）
  - `/about/`（運営者・方針・広告・AI の利用・技術・権利）、`/contact/`（連絡方法・不具合報告の書き方）
  - プライバシーポリシーを共通レイアウトへ移し、問い合わせ先を `/contact/` に
- 内容は各作品の公開中のコード・画面から確認した事実だけを書いた（けしカスの文言データ、もぐもぐカメラの設定・判定方法など）
- 共通 CSS `assets/site.css`、ページ生成スクリプト `_tools/build.py`（`_src/*.html` → 各 `index.html` と `sitemap.xml`）
- 共有カード画像 `assets/img/ogp.jpg`（1200×630）、各ページに canonical・OGP、`robots.txt`、`sitemap.xml`、404 ページを新デザインに
- 確認：全 8 ページを PC・スマホ幅で表示し、横スクロールなし・内部リンク切れなし・読み込みエラーなし

## 2026-10-12 記事コーナーの開設

- ユーザー作業の確認（DNS）：Search Console の所有確認 TXT、SPF（`v=spf1 -all`）、DNSSEC（AD フラグ）が有効
- `_tools/build.py` に記事の仕組みを追加：`date:` 付きのページを記事として扱い、`<!-- ARTICLES -->` で一覧、記事ページに公開日と「ほかの記事」を自動で付ける。ヘッダーに「記事」
- 記事 4 本を公開（`/articles/`）
  - 「ニンニク」が「にんいく」になる理由 — ローマ字入力の「ん」の打ち方（例はマシマシ打の判定エンジンで実際に確認。最初に書いた例 2 つの誤りをここで修正）
  - タイピングを速くする練習のしかた — 正確さが先、速さはあと
  - マシマシ打ができるまで — 2つの試作を1つにまとめた話（このプロジェクトの実際の経緯）
  - 個人開発のゲームを独自ドメインで公開する — GitHub Pages と Cloudflare（今回の実際の手順とつまずき）
- トップに「新しい記事」（最新 3 件）、お知らせに記事コーナー開設を追加
- 確認：全 13 ページを PC・スマホ幅で表示し、横スクロールなし・内部リンク切れなし

## 2026-10-12 プライバシーポリシーに全国完飲番付を追記

- マシマシ打の全国完飲番付（Cloudflare Workers + D1）で送る情報を追記：公開される情報（名前・絵文字アイコン・成績）、公開されない情報（プレイヤー ID・打鍵の記録・IP アドレスはハッシュ化または保存しない）、非表示の運用
- 外部送信の表に Cloudflare（全国完飲番付）を追加。改定日を記載
- マシマシ打の紹介ページへの追記は、番付の公開（API のデプロイ）後に行う

## 2026-10-12 お問い合わせフォーム・もぐもぐカメラの非掲載

- お問い合わせページに Google フォーム（https://forms.gle/49ejNbzBm9jkLjZMA）を埋め込み。表示されないとき用のリンク、GitHub Issues の案内も残す
- プライバシーポリシー：外部送信の表に Google フォームを追加、お問い合わせ内容の利用目的を追記
- ユーザーの指示で「もぐもぐカメラ」をサイトから外した：紹介ページ・画像を削除し、トップ・作品一覧・サイトマップ・プライバシーポリシーから記述を削除（アプリ本体 `/mogumogu-camera/` の非公開はリポジトリ側の設定で行う）
- マシマシ打の紹介ページに全国完飲番付の説明（FAQ）を追加、お知らせを更新
- 確認：全ページを PC・スマホ幅で表示、横スクロール・内部リンク切れなし、フォームの埋め込み表示 OK

## 2026-10-12 CAA・サイトマップの確認

- ユーザーが CAA（`0 issue "letsencrypt.org"`）を追加。DNS 上では Cloudflare が自社の発行会社（pki.goog・ssl.com・comodoca.com・digicert.com）を自動で追加済み。追加後もサイトと api.shinpoyo.com は正常に応答
- Search Console でサイトマップが「読み込めませんでした」：`sitemap.xml` は 200・`application/xml`・XML として正しく、robots.txt からも参照、Googlebot の UA でも取得できる → 登録直後によく出る表示のため、数日待って再確認

## 2026-10-13 サイトの改善（検索対策・アイコン・記事追加）

- 改善案を相談 → 「出来ることやって」の指示で、次を実施
- **構造化データ（JSON-LD）**：`_tools/build.py` で全ページに自動付与
  - トップ：`WebSite`／トップ以外：`BreadcrumbList`（パンくず）
  - 記事：`BlogPosting`（公開日・著者・画像。更新があれば `dateModified`）
  - 作品ページ：`VideoGame`（`_src` に `game_url:` `genre:` `lang:` を追加。無料・ブラウザで遊べる）
- **sitemap.xml に `<lastmod>`**：`_src` ファイルの git 最終コミット日（未コミットの変更があれば当日）
- **アイコン**：`favicon.ico`（16/32/48）・`assets/img/icon.svg`・`assets/img/apple-touch-icon.png`（180）を `_tools/make_icons.py` で生成。`theme-color`（ダーク／ライト）も追加。404 ページにも反映
- **記事のシェアリンク**：記事の末尾に X・はてなブックマークへのリンク（外部スクリプトは読み込まないので、プライバシーポリシーの変更は不要）
- **新しい記事**：「小さい「っ」「ゃ」やカタカナ語はどう打つ？ — ローマ字入力で迷いやすい文字」（`/articles/romaji-tricky/`）。主要な日本語入力に共通の打ち方だけを書き、マシマシ打が受け付ける入力については書いていない。トップのお知らせにも追加
- 目次・記事末の作品への導線は、すでに全記事にあったため対応不要
- **アクセス解析**は Cloudflare 側の操作とトークンが必要なため、手順書 [analytics.md](analytics.md) を作成
- 確認：全 14 ページを PC・スマホ幅（375px）で表示し、横スクロールなし・内部リンク切れなし・JS エラーなし・JSON-LD はすべて正しく読める。アイコン 3 種は 200

## 2026-10-14 SMUDGE 体験版の掲載

- ユーザーの指示で、SMUDGE のブラウザ体験版（最初の27面）をこのサイトで公開する準備
- `/smudge/`：ゲーム本体。SMUDGE リポジトリ（private）の `npm run build:web` の出力 `dist-web/` をそのままコピー。更新手順は SMUDGE の `docs/web-trial.md`
- `/works/smudge/`：紹介ページ（`_src/40-smudge.html`）。遊び方、Android 版（Google Play のクローズドテスト）への参加方法、FAQ。ゲーム内の「Android版について」はここを開く
- 作品一覧・トップの作品とお知らせに追加。画像 `assets/img/smudge.jpg`（スマホ幅の画面を 1280x720 に配置）
- ゲームは外部へ何も送信しない（フォントも同梱）ため、プライバシーポリシーの変更は不要

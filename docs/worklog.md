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

## 2026-10-14 作品を2つ追加（開発中）

- ユーザーの依頼で、未完成の2作品をサイトに掲載（どちらも GitHub Pages で公開済み。ゲーム本体は別リポジトリで、サイト側は紹介ページとリンクだけ）
  - コミック接待オセロ（`shinpoyo/Reversi-with-Sis`）→ 遊ぶ：`/Reversi-with-Sis/`、紹介：`/works/reversi-with-sis/`
  - ALCHEMERGE: RAGNAROK（`shinpoyo/alchemerge_defense`）→ 遊ぶ：`/alchemerge_defense/`、紹介：`/works/alchemerge-defense/`
  - ゲームの URL は大文字・小文字を区別する（`/reversi-with-sis/` は 404）
- 紹介ページの内容は、2つの `index.html` のコードを読んで確かめた事実だけを書いた（イライラ度の増減値・コマンドの回数・エンディングの条件・ステージ倍率／召喚コスト・合体・各属性の効果・WAVE の敵の数・強化の選択肢・奥義ゲージなど）
- 確認できたこと：どちらも外部への通信はなし。コミック接待オセロは何も保存しない。ALCHEMERGE はベストスコアと図鑑を localStorage に保存。ALCHEMERGE の「戦績ポスト」は、押したときだけ X の投稿画面を開く
- 画像：ゲームを Playwright で実際に動かして撮影し、作品カード用（横長1280×720）と紹介ページ用（スマホ縦）を作成。コミック接待オセロの「イライラ度95%」「ちゃぶ台返し」の画面は、撮影のために画面の関数を呼んで状態を作った
- 「開発中」のタグ（`.tag.wip`）を追加。トップ・作品一覧に2作品を追加し、お知らせを更新
- `_tools/build.py`：sitemap の「遊ぶ」URL を各ページの `game_url:` から作るように変更（これまで固定の2件だけで、SMUDGE や今回の2作品が入っていなかった）
- About の「AI の利用について」に、2作品のイラストが AI 生成であることを追記（※ユーザーに確認依頼）
- 前回の PR #1 は取り込み済みで、main には SMUDGE（PR #2）も入っていたため、作業ブランチを最新の main から作り直した
- 確認：全 11 ページを PC・スマホ幅で表示し、横スクロールなし・内部リンク切れなし・JS エラーなし・JSON-LD（作品ページは `VideoGame`）が正しく読める
- ゲーム側で気づいた点（別リポジトリのため未修正）
  - ALCHEMERGE：幅 430px のスマホで、上の「進化図鑑」ボタンが縦書きのように折り返して、ヘッダーからはみ出す
  - ALCHEMERGE：「再出撃」で飛び級進化の確率（強化で上げた分）が元に戻らない

## 2026-10-15 作品名の変更（コミック接待オセロ → ねーちゃんとオセロ）

- ユーザーの指示で、サイト上の作品名を「ねーちゃんとオセロ」に変更（`_src` 内のタイトル・見出し・説明文・alt・パンくず・お知らせ・About の例）
- URL は変えていない（`/works/reversi-with-sis/`・`/Reversi-with-Sis/`）。ゲーム本体のタイトル（別リポジトリの `index.html`）は未変更

## 2026-10-16 作品を2つ追加（はるしねーちゃん・Bullet Reflector）

- ユーザーの依頼で、すでに公開されている2作品を紹介ページ付きで掲載（ゲーム本体は別リポジトリで、そのまま `/<リポジトリ名>/` で配信）
  - はるしねーちゃん（`shinpoyo/haru_nechan_quiz_app`）→ 遊ぶ：`/haru_nechan_quiz_app/`、紹介：`/works/haru-nechan-quiz/`
  - Bullet Reflector（`shinpoyo/Bullet-Reflector`）→ 遊ぶ：`/Bullet-Reflector/`、紹介：`/works/bullet-reflector/`
- 紹介ページの内容は、各リポジトリのコードを読んで確かめた事実だけを書いた（パリィの判定・倍率・スキル・敵・ボス／クイズの流れ・ランクの基準・モード・保存される記録）
- 画像は本番の URL を Playwright で操作して撮影。作品カード用（横長）と紹介ページ用（スマホ縦）を作成
- はるしねーちゃんの外部送信を確認
  - AI 出題と Gemini の声：利用者が入れた Gemini API キーで Google に送信（キーは localStorage に保存）
  - 既定の声：同梱の音声ファイルで再生（外部送信なし）
  - 設定画面から選べるのは「Gemini の声」と「七海（甘め）」の2種。コードに VOICEVOX（api.tts.quest）への送信があるが、画面からは選べないため、ポリシーには書いていない
- プライバシーポリシー：外部送信の表に Gemini API を追加、端末内の保存に Gemini API キーを追記、改定日を 2026年10月16日 に
- Bullet Reflector は外部送信なし（フォントのみ Google Fonts）。広告・課金なし
- トップ（カード・お知らせ）、作品一覧に2作品を追加
- 確認：全ページを PC・スマホ幅で表示し、横スクロールなし・内部リンク切れなし・JS エラーなし
- 確認してほしいこと：はるしねーちゃんのイラスト（`haru_*.jpg`）が AI 生成かどうかは、コードからは判断できないため、About への記載は未対応

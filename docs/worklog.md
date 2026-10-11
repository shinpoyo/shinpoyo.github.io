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

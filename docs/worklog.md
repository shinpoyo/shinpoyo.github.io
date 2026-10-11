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

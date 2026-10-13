# アクセス解析（Cloudflare Web Analytics）の導入手順

どのページが読まれているかを知るための設定。Cookie を使わず、個人を特定する情報も集めない。

## ユーザー作業

1. Cloudflare ダッシュボード → **Analytics & Logs → Web Analytics** → **Add a site**
2. ホスト名に `shinpoyo.com` を入力
   - DNS が「Proxied（オレンジの雲）」なら自動で有効にできる（その場合は下の作業は不要）
   - 「DNS only（グレーの雲）」なら JS スニペットが表示される
3. スニペット内の `"token": "…"` の値を Claude に伝える

## Claude 側の作業（トークンを受け取ったら）

- `_tools/build.py` の共通フッターにビーコン（`https://static.cloudflareinsights.com/beacon.min.js`）を追加して再ビルド
- プライバシーポリシーの「外部送信」の表に Cloudflare Web Analytics を追加（送る情報：閲覧したページの URL・リファラー・ブラウザの種類・表示速度。Cookie は使わない）
- 改定日を更新

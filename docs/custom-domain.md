# 独自ドメイン shinpoyo.com の設定手順

ユーザーサイト（このリポジトリ）に `shinpoyo.com` を設定すると、同じアカウントのプロジェクトサイトも自動で
`https://shinpoyo.com/<リポジトリ名>/` に変わります（旧 URL `shinpoyo.github.io/...` からは自動転送）。

> ⚠️ 手順 2（DNS）が終わる前に手順 3（Custom domain）をしないこと。先にすると全プロジェクトが一時的に見られなくなります。

## 1. ドメインの所有確認（GitHub アカウント単位・乗っ取り防止）

1. GitHub 右上アイコン → **Settings** → 左メニュー **Pages** → **Add a domain** → `shinpoyo.com` → Add domain
2. 表示された TXT レコード（名前 `_github-pages-challenge-shinpoyo`、値はランダム文字列）を Cloudflare に追加
   - Cloudflare → shinpoyo.com → **DNS** → **Records** → **Add record** → Type `TXT`
3. 数分待って GitHub に戻り **Verify**

### Cloudflare の入力欄の対応（Add record の画面）

| Type | Name 欄 | 値の欄（欄の名前） | Proxy status | TTL |
|---|---|---|---|---|
| TXT（所有確認） | `_github-pages-challenge-shinpoyo` | GitHub に表示された文字列（Content） | なし | Auto |
| A | `@` | `185.199.108.153` など（IPv4 address） | DNS only | Auto |
| AAAA | `@` | `2606:50c0:8000::153` など（IPv6 address） | DNS only | Auto |
| CNAME | `www` | `shinpoyo.github.io`（Target） | DNS only | Auto |

- Name の `@` はドメインそのもの（`shinpoyo.com`）の意味。保存後は一覧に `shinpoyo.com` と表示される
- Name に `.shinpoyo.com` は付けない（自動で付く）
- 1 回の Add record で入れられる値は 1 つ。A は 4 回、AAAA も 4 回繰り返す
- A / AAAA / CNAME は最初オレンジの雲（Proxied）になっているので、クリックして灰色（DNS only）にしてから Save

## 2. Cloudflare の DNS レコード

Cloudflare → shinpoyo.com → DNS → Records → Add record。**Proxy status はすべて「DNS only」（灰色の雲）**にする。

| Type | Name | Content |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `shinpoyo.github.io` |

## 3. このリポジトリに独自ドメインを設定

1. `shinpoyo/shinpoyo.github.io` → **Settings** → **Pages**
   - Build and deployment → Source が **Deploy from a branch**、Branch が **main / (root)** になっていることを確認
2. **Custom domain** に `shinpoyo.com` → Save（DNS チェックが緑になるまで数分〜）
3. 証明書の発行後（最大 1 日程度）、**Enforce HTTPS** にチェック

## 4. 各プロジェクト側

- **mashimashida**：Actions → 「Deploy to GitHub Pages」→ **Run workflow**（main）。共有カード（OGP）の URL が `https://shinpoyo.com/mashimashida/` になる
- **smudge-privacy**：アプリストアにプライバシーポリシーの URL を登録している場合、旧 URL からは転送されるが、新 URL `https://shinpoyo.com/smudge-privacy/` に更新しておくと安全
- その他のプロジェクトはそのままで OK（相対パスで作られていれば自動で新 URL で動く）

## 5. 確認

- `https://shinpoyo.com/` にトップページが出る
- `https://shinpoyo.com/mashimashida/` でゲームが動く
- `https://shinpoyo.github.io/mashimashida/` が新 URL に転送される

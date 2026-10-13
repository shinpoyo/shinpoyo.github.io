#!/usr/bin/env python3
"""サイトのアイコン（黄色い丸に「s」）を書き出す。使い方：python3 _tools/make_icons.py

- favicon.ico（48×48 ほか）… 検索結果・ブラウザのタブ用
- assets/img/apple-touch-icon.png（180×180）… iPhone のホーム画面用
- assets/img/icon.svg … 対応ブラウザのタブ用
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
YELLOW, INK, BG = "#facc15", "#111111", "#0b0b0c"


def draw(size, full_bleed=False):
    s = size * 4  # 大きく描いて縮小（ふちをなめらかに）
    img = Image.new("RGBA", (s, s), BG if full_bleed else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = s * 0.1 if full_bleed else s * 0.03
    d.ellipse([pad, pad, s - pad, s - pad], fill=YELLOW)
    font = ImageFont.truetype(FONT, int(s * 0.62))
    d.text((s / 2, s / 2 - s * 0.03), "s", font=font, fill=INK, anchor="mm")
    return img.resize((size, size), Image.LANCZOS)


draw(48).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
draw(180, full_bleed=True).convert("RGB").save(ROOT / "assets/img/apple-touch-icon.png", optimize=True)
(ROOT / "assets/img/icon.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<circle cx="32" cy="32" r="30" fill="#facc15"/>'
    '<text x="32" y="44" font-size="38" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-weight="800" fill="#111">s</text>'
    "</svg>\n", encoding="utf-8")
print("wrote favicon.ico, assets/img/apple-touch-icon.png, assets/img/icon.svg")

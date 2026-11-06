#!/usr/bin/env python3
"""『蒼穹斬』主人公の四面図（正面・右側面・背面・左側面）を SVG で書き出す。

使い方：python3 _design/soukyu/make_turnaround.py
出力：_design/soukyu/character-turnaround.svg
参考：ユーザーから受け取った動画（AI 生成）の主人公。見えない部分は推定で描いている。
"""
import math
from pathlib import Path

OUT = Path(__file__).with_name('character-turnaround.svg')

# ---------------- 色 ----------------
LINE = '#3a3040'
C = dict(
    hair='#c8ccd8', hair_s='#9ba1b4', hair_h='#eef0f6', hair_l='#646a80',
    skin='#fde6db', skin_s='#f1bfae', blush='#ff9aa6',
    iris_t='#12528a', iris_b='#4fd4f2', pupil='#0b2c4c',
    blue='#2f64b9', blue_s='#21488c', blue_h='#4b80d2',
    white='#f4f4f1', white_s='#d2d6df',
    gold='#d9b04c', gold_s='#a27625', gold_h='#f7e08c',
    silver='#d6dbe3', silver_s='#99a2b2', silver_h='#ffffff',
    leather='#6b4428', leather_s='#47291a',
    glove='#4a3020', glove_s='#2f1d13',
    stock='#22202a', stock_s='#121118',
    ribbon='#1c1b22', ribbon_in='#c4303d',
    blade='#7fe6ff', blade_s='#2cb6e8', grip='#2c3a78', sheath='#1f2650', sheath_s='#141936',
)

_id = [0]


def nid():
    _id[0] += 1
    return _id[0]


def f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


# ---------------- 形の部品 ----------------
def cr_segments(pts, closed=False):
    """Catmull-Rom で点を通るなめらかな曲線（3次ベジェ）にする。"""
    n = len(pts)
    s = ''
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += f' C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}'
    return s


def blob(pts):
    return f'M{f(pts[0][0])},{f(pts[0][1])}' + cr_segments(pts, True) + ' Z'


def curve(pts):
    return f'M{f(pts[0][0])},{f(pts[0][1])}' + cr_segments(pts, False)


def poly(pts):
    return 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts) + ' Z'


def strands(pts, bend=.18):
    """髪の房のように、点と点を少し膨らんだ曲線でつなぐ（閉じない）。"""
    s = f'M{f(pts[0][0])},{f(pts[0][1])}'
    for a, b in zip(pts, pts[1:]):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        cx, cy = mx + (b[1] - a[1]) * bend, my - (b[0] - a[0]) * bend
        s += f' Q{f(cx)},{f(cy)} {f(b[0])},{f(b[1])}'
    return s


def limb(pts, ws):
    """中心線と太さから、腕・脚の輪郭を作る。"""
    n = len(pts)
    L, R = [], []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            tx, ty = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            tx, ty = x - pts[i - 1][0], y - pts[i - 1][1]
        else:
            tx, ty = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        l = math.hypot(tx, ty)
        nx, ny = -ty / l, tx / l
        w = ws[i] / 2
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
    s = f'M{f(L[0][0])},{f(L[0][1])}' + cr_segments(L)
    s += f' A{f(ws[-1] / 2)},{f(ws[-1] / 2)} 0 0 1 {f(R[-1][0])},{f(R[-1][1])}'
    Rr = R[::-1]
    s += cr_segments(Rr)
    s += f' A{f(ws[0] / 2)},{f(ws[0] / 2)} 0 0 1 {f(L[0][0])},{f(L[0][1])} Z'
    return s


def mir(pts):
    return [(-x, y) for x, y in reversed(pts)]


def path(d, fill='none', sw=2.0, stroke=LINE, extra=''):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke and sw else ''
    return f'<path d="{d}" fill="{fill}"{st} stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def cel(d, fill, shade, dx=-6, dy=-4, sw=2.0, hi=None, hdx=5, hdy=4):
    """アニメ塗り：本体の色を少しずらして重ね、右下に影の帯を残す。"""
    i = nid()
    s = f'<clipPath id="k{i}"><path d="{d}"/></clipPath><g clip-path="url(#k{i})">'
    s += f'<path d="{d}" fill="{shade}"/><path d="{d}" fill="{fill}" transform="translate({dx},{dy})"/>'
    if hi:
        s += f'<path d="{d}" fill="{hi}" opacity=".55" transform="translate({dx},{dy})" clip-path="url(#k{i}h)"/>'
    s += '</g>'
    if hi:
        s = s.replace('</g>', '', 1)
        s += f'<clipPath id="k{i}h"><path d="{d}" transform="translate({hdx},{hdy})"/></clipPath>'
        s += f'<g clip-path="url(#k{i})"><path d="{d}" fill="{hi}" opacity=".0"/></g></g>'
    s += path(d, 'none', sw)
    return s


def clipped(d_clip, inner):
    i = nid()
    return f'<clipPath id="k{i}"><path d="{d_clip}"/></clipPath><g clip-path="url(#k{i})">{inner}</g>'


def ell(cx, cy, rx, ry, fill, sw=2.0, stroke=LINE, extra=''):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke and sw else ''
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}"{st} {extra}/>'


def line(pts, col, w=1.6, extra=''):
    return path(curve(pts), 'none', w, col, extra)


def g(inner, tr=''):
    return f'<g transform="{tr}">{inner}</g>' if tr else f'<g>{inner}</g>'


# ---------------- 共通の小物 ----------------
def diamond(x, y, s=5, col=None):
    col = col or C['gold']
    return path(poly([(x, y - s * 1.6), (x + s, y), (x, y + s * 1.6), (x - s, y)]), col, 1.2)


def fleur(x, y, s=1.0, flip=False):
    """金の飾り（ユリの紋章風）。"""
    k = -1 if flip else 1
    pts = [(0, -16), (4, -6), (12, -10), (8, 0), (14, 6), (4, 4), (2, 12), (-2, 12), (-4, 4), (-14, 6), (-8, 0), (-12, -10), (-4, -6)]
    pts = [(x + px * s, y + py * s * k) for px, py in pts]
    return path(poly(pts), C['gold'], 1.2)


def buckle(x, y, w=16, h=14):
    return (path(poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)]), 'none', 3.2, C['gold_s']) +
            path(poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)]), 'none', 2.0, C['gold']) +
            line([(x + w / 2, y + 1), (x + w / 2, y + h - 1)], C['gold'], 2))


def ruffle(cx, cy, rx, ry, n=7, rot=0):
    """白いフリル。"""
    pts = []
    for i in range(n * 2):
        a = i / (n * 2) * math.tau
        r = 1 if i % 2 == 0 else .78
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    d = blob(pts)
    return f'<g transform="rotate({rot} {cx} {cy})">' + cel(d, C['white'], C['white_s'], -3, -2, 1.6) + '</g>'


def glove_hand(x, y, mirror=False):
    k = -1 if mirror else 1
    pts = [(-8, -24), (10, -24), (14, -2), (12, 22), (6, 38), (-2, 40), (-8, 34), (-12, 14), (-12, -6)]
    pts = [(x + px * k, y + py) for px, py in pts]
    s = cel(blob(pts), C['glove'], C['glove_s'], -3 * k, -3, 1.8)
    for i in range(3):
        fx = x + (-5 + i * 5) * k
        s += line([(fx, y + 18), (fx + 1 * k, y + 34)], C['glove_s'], 1.2)
    s += line([(x - 10 * k, y - 14), (x + 12 * k, y - 14)], C['glove_s'], 1.4)
    return s


def pauldron(cx, cy, k=1, scale=1.0):
    """左肩の銀の重ね肩当て（3枚）。k=1 で右向きに広がる。"""
    s = ''
    plates = [
        [(-26, 6), (-6, -4), (20, -2), (38, 12), (40, 30), (22, 26), (-4, 24), (-22, 22)],
        [(-24, 22), (-4, 14), (22, 16), (40, 28), (40, 44), (20, 40), (-4, 38), (-20, 36)],
        [(-20, 36), (-2, 28), (22, 30), (38, 42), (36, 56), (18, 52), (-2, 50), (-16, 48)],
    ]
    for pl in reversed(plates):
        pts = [(cx + px * k * scale, cy + py * scale) for px, py in pl]
        d = blob(pts)
        s += cel(d, C['silver'], C['silver_s'], -4 * k, -3, 1.8)
        # 金の縁
        s += line([pts[2], pts[3], pts[4]], C['gold'], 2.4)
        s += line([(pts[1][0], pts[1][1] + 3), (pts[2][0], pts[2][1] + 3)], C['silver_h'], 2)
    # 丸い紋章
    ox, oy = cx + 10 * k * scale, cy + 8 * scale
    s += ell(ox, oy, 8 * scale, 7 * scale, C['gold'], 1.4)
    s += ell(ox, oy, 3.5 * scale, 3 * scale, C['gold_s'], 0)
    s += path(curve([(ox - 8 * k * scale, oy), (ox - 16 * k * scale, oy - 6 * scale), (ox - 20 * k * scale, oy + 2 * scale)]), 'none', 2.2, C['gold'])
    for r in (0, 1):
        s += ell(cx + (24 + r * 6) * k * scale, cy + (42 + r * 3) * scale, 2, 2, C['gold_s'], 0)
    return s


def ribbon_ornament(x, y, k=1, rot=0):
    """髪留め：黒い角飾り（内側が赤）と黒いリボン。"""
    s = f'<g transform="rotate({rot} {x} {y})">'
    s += path(curve([(x + 2 * k, y + 4), (x + 8 * k, y + 30), (x + 6 * k, y + 40)]), 'none', 4, C['ribbon'])
    s += path(curve([(x + 8 * k, y + 4), (x + 18 * k, y + 26), (x + 20 * k, y + 36)]), 'none', 3.5, C['ribbon'])
    s += path(poly([(x - 8 * k, y + 2), (x + 2 * k, y - 34), (x + 16 * k, y)]), C['ribbon'], 1.8)
    s += path(poly([(x - 2 * k, y - 2), (x + 3 * k, y - 22), (x + 10 * k, y - 2)]), C['ribbon_in'], 0)
    s += ell(x + 3 * k, y + 3, 9, 6, C['ribbon'], 1.6)
    s += '</g>'
    return s


def sword_sheathed(hx, hy, ex, ey, front_grip=True):
    """鞘に入った剣。(hx,hy)=鞘の口、(ex,ey)=鞘の先。"""
    ang = math.atan2(ey - hy, ex - hx)
    L = math.hypot(ex - hx, ey - hy)
    deg = math.degrees(ang)
    s = f'<g transform="translate({f(hx)},{f(hy)}) rotate({f(deg)})">'
    sh = poly([(0, -9), (L - 16, -8), (L, 0), (L - 16, 8), (0, 9)])
    s += cel(sh, C['sheath'], C['sheath_s'], 0, -3, 1.8)
    s += line([(10, -3), (L - 20, -3)], '#3a4686', 1.6)
    s += path(poly([(-4, -11), (22, -11), (22, 11), (-4, 11)]), C['gold'], 1.6)       # 鞘口
    s += path(poly([(L - 46, -9), (L - 22, -9), (L, 0), (L - 22, 9), (L - 46, 9)]), C['gold'], 1.6)  # こじり
    s += fleur(L - 60, 0, .7)
    if front_grip:
        s += path(poly([(-8, -22), (-2, -22), (-2, 22), (-8, 22)]), C['gold'], 1.6)   # 鍔
        s += ell(-5, 0, 4, 4, '#49c8ff', 1)
        grip = poly([(-8, -6), (-60, -6), (-60, 6), (-8, 6)])
        s += path(grip, C['grip'], 1.6)
        for i in range(5):
            s += line([(-12 - i * 10, -6), (-18 - i * 10, 6)], '#6476c8', 1.4)
        s += path(poly([(-60, -8), (-72, -6), (-74, 0), (-72, 6), (-60, 8)]), C['gold'], 1.6)  # 柄頭
    s += '</g>'
    return s


# ================= 正面 =================
def front_view():
    o = []
    # --- ツインテール（後ろ）
    tail_r = [(52, 22), (78, 12), (106, 28), (124, 62), (132, 106), (128, 150), (136, 196), (130, 242), (118, 284), (104, 320), (90, 352),
              (98, 304), (100, 262), (94, 222), (90, 180), (84, 140), (74, 100), (62, 70), (52, 46)]
    for tp in (tail_r, mir(tail_r)):
        o.append(cel(blob(tp), C['hair'], C['hair_s'], -6, -3, 2))
    for k in (1, -1):
        for i in range(4):
            o.append(line([(k * (70 + i * 8), 30 + i * 6), (k * (104 + i * 6), 90 + i * 10), (k * (108 + i * 2), 200 + i * 12), (k * (98 + i * 2), 300 - i * 20)], C['hair_s'], 1.3))
    # --- 後ろ髪
    bh = [(0, -2), (38, 3), (60, 24), (70, 58), (72, 100), (70, 140), (66, 178), (56, 196), (40, 184), (20, 160)]
    bh = bh + [(-x, y) for x, y in reversed(bh[1:])]
    o.append(cel(blob(bh), C['hair_s'], '#868ca0', -4, -3, 2))
    # --- 鞘（体の後ろ寄り）
    o.append(sword_sheathed(58, 342, 122, 640, front_grip=False))
    # --- 脚
    for k in (-1, 1):
        cl = [(k * 29, 410), (k * 31, 500), (k * 33, 598), (k * 34, 665), (k * 34, 735), (k * 34, 786)]
        ws = [60, 50, 36, 40, 30, 24]
        d = limb(cl, ws)
        o.append(cel(d, C['stock'], C['stock_s'], -4 * k, -2, 2))
        o.append(clipped(d, f'<rect x="-80" y="380" width="160" height="96" fill="{C["skin"]}"/>'
                            f'<rect x="{-80 if k < 0 else 0}" y="380" width="80" height="96" fill="{C["skin_s"]}" opacity=".0"/>'))
        o.append(clipped(d, f'<rect x="{k * 31 - (14 if k < 0 else -6)}" y="380" width="10" height="96" fill="{C["skin_s"]}"/>'))
        o.append(path(d, 'none', 2))
        # ニーハイの上端（V字の装甲つき）
        o.append(clipped(d, path(poly([(k * 31 - 40, 476), (k * 31 + 40, 476), (k * 31 + 40, 492), (k * 31 - 40, 492)]), '#2e2b38', 0)))
        o.append(line([(k * 31 - 30, 476), (k * 31 + 30, 476)], LINE, 2))
        vpl = [(k * 31 - 18, 490), (k * 31, 512), (k * 31 + 18, 490), (k * 31 + 16, 540), (k * 31, 556), (k * 31 - 16, 540)]
        o.append(cel(poly(vpl), C['silver'], C['silver_s'], -3 * k, -2, 1.8))
        # ひざ当て
        o.append(cel(blob([(k * 33 - 22, 572), (k * 33, 560), (k * 33 + 22, 572), (k * 33 + 20, 598), (k * 33, 610), (k * 33 - 20, 598)]), C['silver'], C['silver_s'], -3 * k, -3, 2))
        o.append(ell(k * 33, 585, 7, 6, C['gold'], 1.4))
        # すね当て（ブーツ）
        bd = limb([(k * 33, 606), (k * 34, 665), (k * 34, 735), (k * 34, 786)], [40, 44, 34, 28])
        o.append(cel(bd, C['silver'], C['silver_s'], -5 * k, -2, 2))
        o.append(line([(k * 33, 614), (k * 34, 700), (k * 34, 780)], C['gold'], 2.2))
        o.append(line([(k * 33 - 17, 612), (k * 33 + 17, 612)], C['gold'], 2.6))
        o.append(line([(k * 34 - 12, 700), (k * 34 - 13, 760)], C['silver_h'], 2.2))
        # 足先
        ft = [(k * 34 - 18, 786), (k * 34 + 18, 786), (k * 34 + 22, 822), (k * 34 + 16, 842), (k * 34 - 16, 842), (k * 34 - 22, 822)]
        o.append(cel(poly(ft), C['silver'], C['silver_s'], -3 * k, -2, 2))
        o.append(line([(k * 34 - 18, 818), (k * 34, 812), (k * 34 + 18, 818)], C['gold'], 2.2))
    # --- ペチコート（白いプリーツ）
    pet = 'M-90,400 L90,400 L102,448'
    xs = list(range(102, -103, -12))
    for i, x in enumerate(xs):
        pet += f' L{x},{452 if i % 2 else 446}'
    pet += ' Z'
    o.append(cel(pet, C['white'], C['white_s'], 0, -3, 1.8))
    for x in range(-96, 97, 12):
        o.append(line([(x * .92, 424), (x, 446)], C['white_s'], 1.2))
    # --- 白い前垂れ（2段）
    ap2 = poly([(-34, 380), (34, 380), (46, 436), (0, 442), (-46, 436)])
    o.append(cel(ap2, C['white'], C['white_s'], -3, -3, 1.8))
    o.append(line([(-40, 428), (0, 434), (40, 428)], C['gold'], 2.4))
    for x in (-24, 0, 24):
        o.append(fleur(x, 418, .75))
    ap1 = poly([(-24, 336), (24, 336), (30, 392), (12, 400), (0, 396), (-12, 400), (-30, 392)])
    o.append(cel(ap1, C['white'], C['white_s'], -3, -3, 1.8))
    o.append(line([(-26, 386), (-12, 393), (0, 389), (12, 393), (26, 386)], C['white_s'], 1.4))
    # --- 青い外スカート（前開き）
    for k in (-1, 1):
        sp = (f'M{k * 54},336 C{k * 70},370 {k * 90},405 {k * 106},442 Q{k * 80},452 {k * 50},442 '
              f'C{k * 42},405 {k * 32},370 {k * 23},336 Z')
        o.append(cel(sp, C['blue'], C['blue_s'], -5 * k if k > 0 else 5, -3, 2))
        o.append(path(f'M{k * 102},436 Q{k * 78},445 {k * 52},437', 'none', 3, C['gold']))
        o.append(path(f'M{k * 28},345 C{k * 36},375 {k * 44},405 {k * 52},437', 'none', 2.6, C['gold']))
        o.append(fleur(k * 66, 424, .8))
        o.append(fleur(k * 90, 426, .6))
    # --- 胴（青）
    torso = ('M-16,148 C-30,160 -50,164 -68,174 C-76,186 -66,214 -56,224 C-52,245 -48,268 -41,296 '
             'C-45,312 -50,326 -53,340 L53,340 C50,326 45,312 41,296 C48,268 52,245 56,224 '
             'C66,214 76,186 68,174 C50,164 30,160 16,148 Z')
    o.append(cel(torso, C['blue'], C['blue_s'], -5, -3, 2))
    bod = ('M-15,160 C-28,172 -38,186 -40,210 C-42,236 -38,252 -33,262 L-21,340 L21,340 L33,262 '
           'C38,252 42,236 40,210 C38,186 28,172 15,160 Z')
    o.append(cel(bod, C['white'], C['white_s'], -4, -4, 1.8))
    o.append(path('M-15,160 C-28,172 -38,186 -40,210 C-42,236 -38,252 -33,262 L-21,340', 'none', 2.6, C['gold']))
    o.append(path('M15,160 C28,172 38,186 40,210 C42,236 38,252 33,262 L21,340', 'none', 2.6, C['gold']))
    o.append(line([(-36, 238), (-20, 252), (-4, 242)], C['white_s'], 2))
    o.append(line([(4, 242), (20, 252), (36, 238)], C['white_s'], 2))
    o.append(line([(0, 214), (0, 258)], C['white_s'], 1.3))
    for k in (-1, 1):
        for y in (292, 322):
            o.append(diamond(k * 24, y, 3.6))
    o.append(line([(0, 278), (0, 336)], C['white_s'], 1.3))
    # 胸元のカットと金の飾り
    o.append(path('M0,182 C-8,190 -8,202 0,212 C8,202 8,190 0,182 Z', C['skin'], 1.6))
    o.append(line([(0, 196), (0, 210)], C['skin_s'], 1.2))
    o.append(path(poly([(-22, 164), (22, 164), (14, 172), (6, 184), (0, 190), (-6, 184), (-14, 172)]), C['gold'], 1.6))
    o.append(path(poly([(-8, 168), (8, 168), (0, 180)]), C['gold_s'], 0))
    # 立ち襟
    col = 'M-17,134 L17,134 L19,162 C8,168 -8,168 -19,162 Z'
    o.append(cel(col, C['blue'], C['blue_s'], -3, -2, 1.8))
    o.append(line([(-17, 136), (17, 136)], C['gold'], 2.4))
    o.append(line([(0, 136), (0, 160)], C['gold'], 2))
    o.append(path('M-19,160 C-8,166 8,166 19,160', 'none', 2.4, C['gold']))
    # 胸下のベルト
    o.append(cel(poly([(-49, 260), (49, 260), (48, 273), (-48, 273)]), C['leather'], C['leather_s'], 0, -3, 1.8))
    o.append(path(poly([(-10, 256), (10, 256), (14, 266), (0, 278), (-14, 266)]), C['gold'], 1.4))
    # 腰のベルト（2本）
    b1 = 'M-55,324 C-20,330 20,332 56,328 L57,341 C20,345 -20,343 -55,337 Z'
    o.append(cel(b1, C['leather'], C['leather_s'], 0, -3, 1.8))
    o.append(buckle(-16, 324, 18, 15))
    b2 = 'M-50,344 C-10,352 30,360 64,374 L61,387 C28,374 -10,366 -52,357 Z'
    o.append(cel(b2, C['leather'], C['leather_s'], 0, -3, 1.8))
    o.append(buckle(8, 353, 17, 14))
    # --- 右腕（見て左）：袖・フリル・革の籠手
    o.append(cel(limb([(-66, 184), (-75, 232), (-85, 284)], [44, 38, 34]), C['blue'], C['blue_s'], 4, -3, 2))
    o.append(line([(-72, 200), (-80, 270)], C['blue_h'], 2))
    o.append(ruffle(-87, 292, 22, 11, 7, 18))
    ba = limb([(-89, 300), (-96, 350), (-102, 396)], [30, 28, 24])
    o.append(cel(ba, C['leather'], C['leather_s'], 3, -3, 2))
    for y, xx in ((318, -92), (348, -96), (378, -100)):
        o.append(clipped(ba, path(poly([(xx - 24, y - 4), (xx + 24, y), (xx + 24, y + 6), (xx - 24, y + 2)]), C['leather_s'], 0)))
        o.append(ell(xx + 2, y + 1, 2.4, 2.4, C['gold'], 0))
    o.append(path(ba, 'none', 2))
    o.append(glove_hand(-106, 420, mirror=False))
    # --- 左腕（見て右）：袖・肩当て・銀の籠手
    o.append(cel(limb([(66, 184), (75, 232), (85, 284)], [44, 38, 34]), C['blue'], C['blue_s'], -4, -3, 2))
    o.append(ell(87, 298, 16, 14, C['silver'], 2))
    o.append(path('M73,298 A14,12 0 0 0 101,298', 'none', 2.4, C['gold']))
    va = limb([(89, 310), (96, 354), (102, 396)], [32, 30, 26])
    o.append(cel(va, C['silver'], C['silver_s'], -4, -3, 2))
    o.append(line([(76, 312), (102, 316)], C['gold'], 2.6))
    o.append(diamond(95, 350, 4))
    o.append(line([(88, 330), (94, 386)], C['silver_h'], 2))
    o.append(ruffle(103, 398, 14, 6, 6, 10))
    o.append(glove_hand(106, 420, mirror=True))
    o.append(pauldron(62, 168, 1, 1.0))
    # --- 首
    o.append(path('M-11,122 L-12,140 L12,140 L11,122 Z', C['skin'], 1.6))
    o.append(path('M-11,128 C-4,136 4,136 11,128 L11,140 L-11,140 Z', C['skin_s'], 0))
    # --- 顔
    face = 'M-50,56 C-52,92 -42,118 -14,132 Q0,138 14,132 C42,118 52,92 50,56 Z'
    o.append(cel(face, C['skin'], C['skin_s'], -4, -3, 2))
    for k in (-1, 1):
        o.append(ell(k * 52, 92, 6, 10, C['skin'], 1.6))
    o.extend(eyes_front())
    o.append(line([(-1, 106), (1, 110)], C['skin_s'], 1.6))
    o.append(path('M-8,119 Q0,126 8,119', 'none', 1.8, '#8a4a50'))
    for k in (-1, 1):
        o.append(ell(k * 31, 108, 10, 4.5, C['blush'], 0, extra='opacity=".45"'))
        for i in range(3):
            o.append(line([(k * (25 + i * 5), 110), (k * (28 + i * 5), 105)], '#ff7f90', 1, 'opacity=".5"'))
    # --- 前髪・横髪
    for k in (-1, 1):
        sl = [(-48, 48), (-58, 80), (-63, 122), (-61, 162), (-55, 194), (-46, 210), (-46, 182), (-44, 142), (-42, 102), (-40, 70)]
        if k > 0:
            sl = [(-x, y) for x, y in sl]
        o.append(cel(blob(sl), C['hair'], C['hair_s'], -3, -3, 2))
    top = 'M-62,46 C-60,10 -30,-4 0,-3 C30,-4 60,10 62,46'
    tips = [(62, 46), (57, 88), (47, 60), (39, 80), (30, 58), (19, 86), (12, 60), (5, 102), (-2, 62), (-12, 84), (-20, 58), (-30, 80), (-38, 58), (-48, 86), (-53, 56), (-62, 46)]
    bangs = top + strands(tips, .1)[len(f'M{f(tips[0][0])},{f(tips[0][1])}'):] + ' Z'
    o.append(cel(bangs, C['hair'], C['hair_s'], -4, -4, 2))
    for a, b in ((-40, -48), (-18, -12), (2, 5), (20, 19), (40, 39)):
        o.append(line([(a * .4, 8), (a * .9, 40), (b, 76)], C['hair_s'], 1.3))
    for x in (-40, -26, -12, 8, 22, 36):
        o.append(line([(x, 22), (x + 8, 20)], C['hair_h'], 3))
    o.append(path('M-2,-1 C-8,-26 12,-38 17,-20 C12,-28 2,-22 5,-1 Z', C['hair'], 1.8))
    o.append(ribbon_ornament(56, 26, 1, 12))
    o.append(ribbon_ornament(-56, 26, -1, -12))
    return ''.join(o)


def eyes_front():
    o = []
    for k in (-1, 1):
        def X(x):
            return x * k
        cx = X(22)
        o.append(path(f'M{X(38)},86 Q{X(24)},77 {X(8)},84 L{X(9)},100 Q{X(22)},106 {X(36)},98 Z', '#ffffff', 1.2))
        gid = f'ir{nid()}'
        o.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["iris_t"]}"/><stop offset="1" stop-color="{C["iris_b"]}"/></linearGradient></defs>')
        o.append(ell(cx, 93, 9.5, 12, f'url(#{gid})', 1.2))
        o.append(ell(cx, 91, 4.2, 6.4, C['pupil'], 0))
        o.append(ell(cx, 99, 5.5, 3, '#9ff0ff', 0, extra='opacity=".7"'))
        o.append(ell(cx - 4 * k, 87, 3.2, 3.2, '#ffffff', 0))
        o.append(ell(cx + 3 * k, 98, 1.6, 1.6, '#ffffff', 0))
        o.append(path(f'M{X(41)},89 Q{X(26)},73 {X(6)},82 L{X(6)},86 Q{X(24)},79 {X(38)},92 Z', '#2a2030', 1))
        o.append(line([(X(40), 89), (X(45), 84)], '#2a2030', 2))
        o.append(line([(X(33), 101), (X(22), 105), (X(12), 101)], '#7a5060', 1.2))
        o.append(line([(X(38), 68), (X(26), 63), (X(12), 67)], '#6a6070', 2))
    return o


# ================= 背面 =================
def back_view():
    """背面：見て左がキャラの左（肩当て・鞘）、見て右がキャラの右（革の籠手）。"""
    o = []
    o.append(sword_sheathed(-58, 342, -122, 640, front_grip=False))
    # 脚（後ろ）
    for k in (-1, 1):
        cl = [(k * 29, 410), (k * 31, 500), (k * 33, 598), (k * 34, 665), (k * 34, 735), (k * 34, 786)]
        d = limb(cl, [60, 50, 36, 42, 30, 24])
        o.append(cel(d, C['stock'], C['stock_s'], -4 * k, -2, 2))
        o.append(clipped(d, f'<rect x="-80" y="380" width="160" height="96" fill="{C["skin"]}"/>'))
        o.append(path(d, 'none', 2))
        o.append(clipped(d, path(poly([(k * 31 - 40, 476), (k * 31 + 40, 476), (k * 31 + 40, 492), (k * 31 - 40, 492)]), '#2e2b38', 0)))
        o.append(line([(k * 31 - 30, 476), (k * 31 + 30, 476)], LINE, 2))
        o.append(line([(k * 33 - 10, 598), (k * 33 + 10, 598)], C['stock_s'], 2))
        bd = limb([(k * 33, 640), (k * 34, 700), (k * 34, 786)], [38, 34, 28])
        o.append(cel(bd, C['silver'], C['silver_s'], -4 * k, -2, 2))
        o.append(line([(k * 33 - 16, 644), (k * 33 + 16, 644)], C['gold'], 2.6))
        o.append(line([(k * 34, 650), (k * 34, 780)], C['silver_s'], 2))
        ft = [(k * 34 - 18, 786), (k * 34 + 18, 786), (k * 34 + 20, 826), (k * 34 + 14, 842), (k * 34 - 14, 842), (k * 34 - 20, 826)]
        o.append(cel(poly(ft), C['silver'], C['silver_s'], -3 * k, -2, 2))
        o.append(path(poly([(k * 34 - 10, 828), (k * 34 + 10, 828), (k * 34 + 8, 842), (k * 34 - 8, 842)]), C['leather_s'], 1.4))
    # ペチコート
    pet = 'M-92,400 L92,400 L104,448'
    for i, x in enumerate(range(104, -105, -12)):
        pet += f' L{x},{452 if i % 2 else 446}'
    pet += ' Z'
    o.append(cel(pet, C['white'], C['white_s'], 0, -3, 1.8))
    for x in range(-96, 97, 12):
        o.append(line([(x * .92, 424), (x, 446)], C['white_s'], 1.2))
    # スカート（後ろは閉じている）
    sk = 'M-54,336 L54,336 C70,370 90,405 106,442 Q0,458 -106,442 C-90,405 -70,370 -54,336 Z'
    o.append(cel(sk, C['blue'], C['blue_s'], -5, -3, 2))
    o.append(path('M102,436 Q0,452 -102,436', 'none', 3, C['gold']))
    for x in (-60, -20, 20, 60):
        o.append(line([(x * .55, 350), (x, 440)], C['blue_s'], 1.6))
    o.append(fleur(0, 428, .8))
    # 胴（後ろ）
    torso = ('M-16,148 C-30,160 -50,164 -68,174 C-76,186 -66,214 -56,224 C-52,245 -48,268 -41,296 '
             'C-45,312 -50,326 -53,340 L53,340 C50,326 45,312 41,296 C48,268 52,245 56,224 '
             'C66,214 76,186 68,174 C50,164 30,160 16,148 Z')
    o.append(cel(torso, C['blue'], C['blue_s'], -5, -3, 2))
    o.append(line([(0, 162), (0, 338)], C['blue_s'], 1.6))
    for k in (-1, 1):
        o.append(line([(k * 20, 170), (k * 30, 230), (k * 24, 300), (k * 26, 338)], C['blue_s'], 1.4))
        o.append(line([(k * 34, 182), (k * 46, 210)], C['blue_h'], 2))
    o.append(cel(poly([(-49, 260), (49, 260), (48, 273), (-48, 273)]), C['leather'], C['leather_s'], 0, -3, 1.8))
    b1 = 'M-55,328 C-20,332 20,330 56,324 L56,337 C20,343 -20,345 -57,341 Z'
    o.append(cel(b1, C['leather'], C['leather_s'], 0, -3, 1.8))
    b2 = 'M-64,374 C-30,360 10,352 50,344 L52,357 C10,366 -28,374 -61,387 Z'
    o.append(cel(b2, C['leather'], C['leather_s'], 0, -3, 1.8))
    col = 'M-17,134 L17,134 L19,162 C8,168 -8,168 -19,162 Z'
    o.append(cel(col, C['blue'], C['blue_s'], -3, -2, 1.8))
    o.append(line([(-17, 136), (17, 136)], C['gold'], 2.4))
    # 腕：見て左＝キャラの左（銀の籠手・肩当て）、見て右＝キャラの右（革の籠手）
    o.append(cel(limb([(-66, 184), (-75, 232), (-85, 284)], [44, 38, 34]), C['blue'], C['blue_s'], 4, -3, 2))
    o.append(ell(-87, 298, 15, 13, C['silver'], 2))
    va = limb([(-89, 310), (-96, 354), (-102, 396)], [32, 30, 26])
    o.append(cel(va, C['silver'], C['silver_s'], 4, -3, 2))
    o.append(line([(-76, 312), (-102, 316)], C['gold'], 2.6))
    o.append(line([(-98, 330), (-104, 386)], C['silver_s'], 2))
    o.append(glove_hand(-106, 420, mirror=False))
    o.append(pauldron(-62, 168, -1, 1.0))
    o.append(cel(limb([(66, 184), (75, 232), (85, 284)], [44, 38, 34]), C['blue'], C['blue_s'], -4, -3, 2))
    o.append(ruffle(87, 292, 22, 11, 7, -18))
    ba = limb([(89, 300), (96, 350), (102, 396)], [30, 28, 24])
    o.append(cel(ba, C['leather'], C['leather_s'], -3, -3, 2))
    for y, xx in ((318, 92), (348, 96), (378, 100)):
        o.append(clipped(ba, path(poly([(xx - 24, y), (xx + 24, y - 4), (xx + 24, y + 2), (xx - 24, y + 6)]), C['leather_s'], 0)))
    o.append(path(ba, 'none', 2))
    o.append(glove_hand(106, 420, mirror=True))
    # 首・後頭部
    o.append(path('M-12,122 L-12,146 L12,146 L12,122 Z', C['skin_s'], 1.6))
    bh = [(0, -3), (40, 2), (62, 26), (70, 62), (70, 104), (66, 146), (58, 182), (44, 200), (30, 178), (14, 196), (0, 176)]
    bh = bh + [(-x, y) for x, y in reversed(bh[1:])]
    o.append(cel(blob(bh), C['hair'], C['hair_s'], -5, -4, 2))
    for x in (-50, -32, -14, 4, 22, 40, 56):
        o.append(line([(x * .3, 6), (x * .9, 60), (x, 150)], C['hair_s'], 1.3))
    for x in (-34, -18, 0, 18, 34):
        o.append(line([(x, 26), (x + 8, 25)], C['hair_h'], 3))
    o.append(path('M-2,-1 C-8,-26 12,-38 17,-20 C12,-28 2,-22 5,-1 Z', C['hair'], 1.8))
    # ツインテール（背面では体の手前）
    tail_r = [(50, 20), (78, 12), (104, 30), (118, 66), (120, 110), (114, 150), (120, 196), (114, 240), (104, 280), (92, 318), (80, 350),
              (84, 302), (84, 262), (80, 222), (78, 182), (76, 142), (70, 100), (58, 64), (48, 42)]
    for tp in (tail_r, mir(tail_r)):
        o.append(cel(blob(tp), C['hair'], C['hair_s'], -5, -3, 2))
    for k in (1, -1):
        for i in range(3):
            o.append(line([(k * (64 + i * 10), 34 + i * 6), (k * (96 + i * 6), 100 + i * 10), (k * (98 + i * 3), 210 + i * 12), (k * (88 + i * 2), 300 - i * 20)], C['hair_s'], 1.3))
    o.append(ribbon_ornament(-54, 26, -1, -10))
    o.append(ribbon_ornament(54, 26, 1, 10))
    return ''.join(o)


# ================= 側面（右向き） =================
def side_view(near='bracer'):
    """右向き（+x が顔の向き）。near='bracer' で右側面、'pauldron' で左側面（呼ぶ側で左右反転）。"""
    o = []
    left = near == 'pauldron'
    # 奥のツインテール
    far_t = [(-10, 18), (-36, 6), (-64, 22), (-84, 60), (-92, 110), (-94, 160), (-98, 210), (-92, 260), (-82, 300), (-72, 336), (-70, 292), (-72, 244), (-68, 196), (-62, 150), (-52, 100), (-34, 56), (-16, 36)]
    o.append(cel(blob(far_t), C['hair_s'], '#878da1', -4, -3, 2))
    # 奥（反対側）の肩当て or 鞘
    if not left:
        o.append(sword_sheathed(28, 346, -128, 610, front_grip=True))
        o.append(pauldron(-6, 170, -1, .9))
    # 奥の脚
    fl = limb([(-10, 405), (-6, 500), (-2, 598), (-6, 665), (-10, 735), (-12, 782)], [64, 52, 38, 42, 30, 22])
    o.append(cel(fl, C['stock_s'], '#0a0a10', -3, -2, 2))
    o.append(cel(limb([(-2, 606), (-6, 665), (-10, 735), (-12, 782)], [40, 44, 32, 26]), C['silver_s'], '#7a8394', -3, -2, 2))
    o.append(cel('M-26,782 L4,782 C18,798 34,818 42,838 L42,842 L-28,842 L-30,814 Z', C['silver_s'], '#7a8394', -3, -2, 2))
    # 手前の脚
    nl_c = [(-2, 405), (2, 500), (8, 598), (4, 665), (0, 735), (-2, 782)]
    nl = limb(nl_c, [70, 56, 40, 44, 32, 24])
    o.append(cel(nl, C['stock'], C['stock_s'], -4, -2, 2))
    o.append(clipped(nl, f'<rect x="-80" y="380" width="160" height="96" fill="{C["skin"]}"/><rect x="18" y="380" width="30" height="96" fill="{C["skin_s"]}" opacity=".0"/>'))
    o.append(path(nl, 'none', 2))
    o.append(clipped(nl, path(poly([(-50, 476), (50, 470), (50, 486), (-50, 492)]), '#2e2b38', 0)))
    o.append(line([(-34, 478), (36, 472)], LINE, 2))
    o.append(cel(poly([(14, 486), (34, 492), (38, 540), (28, 556), (16, 540)]), C['silver'], C['silver_s'], -2, -2, 1.8))
    o.append(cel(blob([(10, 566), (28, 570), (34, 588), (28, 606), (12, 610), (14, 588)]), C['silver'], C['silver_s'], -2, -3, 2))
    o.append(ell(26, 588, 4, 6, C['gold'], 1.2))
    bd = limb([(8, 606), (4, 665), (0, 735), (-2, 782)], [40, 46, 34, 28])
    o.append(cel(bd, C['silver'], C['silver_s'], -5, -2, 2))
    o.append(line([(8 - 18, 610), (8 + 18, 612)], C['gold'], 2.6))
    o.append(line([(24, 620), (20, 700), (14, 776)], C['gold'], 2.2))
    o.append(line([(10, 650), (4, 760)], C['silver_h'], 2.2))
    ft = 'M-16,782 L14,782 C28,798 46,818 54,836 L54,842 L-18,842 L-20,814 Z'
    o.append(cel(ft, C['silver'], C['silver_s'], -3, -2, 2))
    o.append(line([(16, 800), (30, 828), (34, 842)], C['gold'], 2.2))
    o.append(path(poly([(-20, 826), (-6, 826), (-6, 842), (-20, 842)]), C['leather_s'], 1.4))
    # ペチコート
    pet = 'M-80,400 L70,400 L82,446'
    for i, x in enumerate(range(82, -95, -12)):
        pet += f' L{x},{452 if i % 2 else 446}'
    pet += ' Z'
    o.append(cel(pet, C['white'], C['white_s'], 0, -3, 1.8))
    # スカート
    sk = 'M-40,336 L34,336 C46,370 60,405 76,440 Q0,456 -86,440 C-70,405 -54,370 -40,336 Z'
    o.append(cel(sk, C['blue'], C['blue_s'], -4, -3, 2))
    ap = 'M22,336 L34,336 C46,370 60,405 76,440 L58,444 C48,405 36,370 22,336 Z'
    o.append(cel(ap, C['white'], C['white_s'], -2, -2, 1.6))
    o.append(path('M74,438 Q0,452 -84,438', 'none', 3, C['gold']))
    o.append(path('M24,342 C36,375 46,405 58,442', 'none', 2.4, C['gold']))
    o.append(fleur(-30, 430, .7))
    o.append(fleur(10, 434, .6))
    # 胴
    torso = ('M-4,150 C-22,165 -32,190 -34,220 C-34,250 -26,280 -24,300 C-28,320 -36,335 -40,345 L36,345 '
             'C34,320 30,305 30,296 C34,282 44,270 52,250 C60,236 58,214 46,196 C40,184 36,170 32,152 Z')
    o.append(cel(torso, C['blue'], C['blue_s'], -4, -3, 2))
    bod = ('M32,156 C36,170 40,184 46,196 C58,214 60,236 52,250 C44,270 34,282 30,296 L32,345 L18,345 '
           'L18,296 C22,280 30,262 32,240 C32,220 26,200 20,180 Z')
    o.append(cel(bod, C['white'], C['white_s'], -3, -3, 1.8))
    o.append(path('M20,180 C26,200 32,220 32,240 C30,262 22,280 18,296 L18,345', 'none', 2.6, C['gold']))
    o.append(diamond(20, 312, 3.4))
    o.append(line([(44, 238), (52, 250)], C['white_s'], 2))
    belts = (cel(poly([(-36, 258), (52, 256), (48, 270), (-34, 272)]), C['leather'], C['leather_s'], 0, -3, 1.8) +
             cel(poly([(-44, 326), (40, 326), (40, 339), (-44, 341)]), C['leather'], C['leather_s'], 0, -3, 1.8) +
             cel(poly([(-50, 352), (42, 344), (42, 357), (-48, 366)]), C['leather'], C['leather_s'], 0, -3, 1.8))
    o.append(belts)
    o.append(path(poly([(44, 252), (54, 254), (52, 270), (44, 272)]), C['gold'], 1.2))
    o.append(buckle(26, 326, 12, 13))
    # 襟・首
    o.append(path('M6,120 L26,128 L30,146 L2,146 Z', C['skin'], 1.6))
    o.append(path('M6,124 L24,130 L28,140 L4,140 Z', C['skin_s'], 0))
    col = 'M-2,138 L32,140 L34,164 L-4,164 Z'
    o.append(cel(col, C['blue'], C['blue_s'], -2, -2, 1.8))
    o.append(line([(-2, 140), (32, 142)], C['gold'], 2.4))
    o.append(line([(32, 142), (34, 162)], C['gold'], 2))
    # 手前の腕
    o.append(cel(limb([(2, 182), (3, 236), (5, 286)], [46, 40, 34]), C['blue'], C['blue_s'], -4, -3, 2))
    o.append(line([(-8, 200), (-8, 270)], C['blue_h'], 2))
    if not left:
        o.append(ruffle(5, 294, 22, 10, 7, 0))
        ba = limb([(6, 300), (9, 350), (12, 394)], [30, 28, 24])
        o.append(cel(ba, C['leather'], C['leather_s'], -3, -3, 2))
        for y in (318, 348, 378):
            o.append(clipped(ba, path(poly([(-20, y - 2), (40, y + 2), (40, y + 8), (-20, y + 4)]), C['leather_s'], 0)))
            o.append(ell(-2 + y * .02, y + 3, 2.2, 2.2, C['gold'], 0))
        o.append(path(ba, 'none', 2))
    else:
        o.append(ell(6, 298, 16, 14, C['silver'], 2))
        o.append(path('M-8,300 A15,12 0 0 0 20,300', 'none', 2.4, C['gold']))
        va = limb([(7, 310), (10, 354), (12, 394)], [32, 30, 26])
        o.append(cel(va, C['silver'], C['silver_s'], -4, -3, 2))
        o.append(line([(-8, 314), (24, 312)], C['gold'], 2.6))
        o.append(diamond(10, 352, 4))
        o.append(ruffle(13, 398, 14, 6, 6, 0))
    o.append(glove_hand(14, 422, mirror=False))
    if left:
        o.append(pauldron(-4, 166, 1, 1.0))
        o.append(sword_sheathed(28, 346, -128, 610, front_grip=True))
    # 頭
    bh = [(-6, -2), (30, 2), (54, 26), (60, 56), (40, 70), (10, 92), (-10, 140), (-20, 176), (-38, 194), (-56, 166), (-66, 120), (-68, 76), (-58, 32), (-36, 6)]
    o.append(cel(blob(bh), C['hair'], C['hair_s'], -4, -4, 2))
    face = ('M10,58 L52,56 C56,70 56,82 58,92 L64,103 L58,108 C58,112 60,116 57,119 C59,122 57,126 53,128 '
            'C52,133 46,138 36,138 C26,138 14,132 8,124 L4,100 Z')
    o.append(cel(face, C['skin'], C['skin_s'], 3, -3, 2))
    o.append(ell(-2, 98, 7, 11, C['skin'], 1.6))
    o.append(line([(-3, 92), (0, 100), (-3, 106)], C['skin_s'], 1.2))
    o.append(path('M38,84 Q46,81 53,86 L51,100 Q45,102 40,98 Z', '#ffffff', 1.1))
    gid = f'ir{nid()}'
    o.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["iris_t"]}"/><stop offset="1" stop-color="{C["iris_b"]}"/></linearGradient></defs>')
    o.append(ell(47, 92, 4.5, 10.5, f'url(#{gid})', 1))
    o.append(ell(47, 88, 1.8, 2.2, '#ffffff', 0))
    o.append(path('M35,87 Q46,77 55,86 L53,88 Q45,82 37,90 Z', '#2a2030', 1))
    o.append(line([(36, 87), (30, 83)], '#2a2030', 2))
    o.append(line([(40, 69), (48, 67), (55, 70)], '#6a6070', 1.8))
    o.append(line([(52, 121), (57, 121)], '#8a4a50', 1.6))
    o.append(ell(40, 110, 8, 4, C['blush'], 0, extra='opacity=".45"'))
    sl = [(6, 56), (20, 66), (23, 108), (21, 150), (17, 186), (12, 204), (8, 172), (4, 130), (1, 90)]
    o.append(cel(blob(sl), C['hair'], C['hair_s'], -3, -3, 2))
    bangs = 'M-6,-2 C14,-4 40,4 54,22 C62,32 66,40 64,46' + strands([(64, 46), (62, 74), (56, 58), (56, 84), (48, 62), (42, 78), (36, 58), (22, 56), (12, 46)], .12)[len('M64,46'):] + ' C0,30 -10,14 -6,-2 Z'
    o.append(cel(bangs, C['hair'], C['hair_s'], -3, -4, 2))
    for i in range(5):
        o.append(line([(-50 + i * 8, 30 + i * 4), (-56 + i * 10, 100), (-46 + i * 12, 170 - i * 8)], C['hair_s'], 1.3))
    for x in (-30, -14, 4, 20):
        o.append(line([(x, 16 - (x > 0) * 2), (x + 9, 16)], C['hair_h'], 3))
    o.append(path('M8,-2 C2,-30 22,-38 26,-22 C20,-30 12,-24 14,-2 Z', C['hair'], 1.8))
    # 手前のツインテール
    near_t = [(-14, 16), (-40, 10), (-70, 30), (-90, 70), (-98, 120), (-100, 170), (-104, 220), (-98, 270), (-88, 310), (-80, 348), (-78, 300), (-80, 250), (-76, 200), (-70, 150), (-58, 100), (-40, 60), (-22, 40)]
    o.append(cel(blob(near_t), C['hair'], C['hair_s'], -4, -3, 2))
    for i in range(3):
        o.append(line([(-30 - i * 8, 26 + i * 4), (-78 - i * 4, 80 + i * 8), (-88 - i * 2, 200 + i * 10), (-84 - i * 2, 310 - i * 20)], C['hair_s'], 1.3))
    o.append(ribbon_ornament(-18, 22, -1, -20))
    return ''.join(o)


# ================= 剣の詳細 =================
def sword_detail():
    o = []
    o.append('<defs><filter id="glow" x="-50%" y="-10%" width="200%" height="120%"><feGaussianBlur stdDeviation="7"/></filter>'
             f'<linearGradient id="bl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["blade_s"]}"/><stop offset=".45" stop-color="#d9fbff"/><stop offset="1" stop-color="{C["blade"]}"/></linearGradient></defs>')
    blade = poly([(-13, 100), (13, 100), (11, 420), (0, 470), (-11, 420)])
    o.append(path(blade, '#4fd6ff', 0, extra='filter="url(#glow)" opacity=".8"'))
    o.append(path(blade, 'url(#bl)', 1.8, '#1b6f9a'))
    o.append(line([(0, 106), (0, 440)], '#ffffff', 2.2))
    for y in (180, 260, 340):
        o.append(line([(-8, y), (-2, y + 20)], '#ffffff', 1.2, 'opacity=".7"'))
    # 鍔
    guard = 'M-50,82 C-40,76 -20,82 -10,88 L10,88 C20,82 40,76 50,82 C46,92 34,96 24,100 L-24,100 C-34,96 -46,92 -50,82 Z'
    o.append(cel(guard, C['gold'], C['gold_s'], 0, -3, 1.8))
    o.append(path(poly([(-10, 84), (10, 84), (14, 100), (0, 116), (-14, 100)]), C['gold'], 1.6))
    o.append(path(poly([(-5, 92), (5, 92), (6, 100), (0, 108), (-6, 100)]), '#49c8ff', 1.2))
    o.append(path('M-50,82 C-58,74 -60,66 -54,60', 'none', 3, C['gold']))
    o.append(path('M50,82 C58,74 60,66 54,60', 'none', 3, C['gold']))
    # 柄
    o.append(path(poly([(-7, 8), (7, 8), (7, 80), (-7, 80)]), C['grip'], 1.6))
    for i in range(7):
        y = 12 + i * 10
        o.append(line([(-7, y), (7, y + 8)], '#6476c8', 1.6))
        o.append(line([(7, y), (-7, y + 8)], '#1c2656', 1.2))
    o.append(path(poly([(-9, -12), (9, -12), (12, 0), (8, 10), (-8, 10), (-12, 0)]), C['gold'], 1.6))
    o.append(ell(0, -2, 3.5, 3.5, '#49c8ff', 1))
    return ''.join(o)


# ================= 組み立て =================
def build():
    Wd, Hd = 2200, 1180
    top = 160
    cols = [240, 660, 1080, 1500]
    labels = [('正面', 'FRONT'), ('右側面', 'RIGHT'), ('背面', 'BACK'), ('左側面', 'LEFT')]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" font-family="Hiragino Kaku Gothic ProN, Hiragino Sans, Yu Gothic, Noto Sans CJK JP, Noto Sans JP, sans-serif">']
    s.append(f'<rect width="{Wd}" height="{Hd}" fill="#f3f1ec"/>')
    s.append(f'<rect x="0" y="0" width="{Wd}" height="92" fill="#1d2240"/>')
    s.append('<text x="40" y="58" font-size="34" font-weight="700" fill="#f3e3b8">蒼穹斬　主人公（白銀の騎士・仮）　キャラクター四面図</text>')
    s.append('<text x="40" y="82" font-size="15" fill="#b9c3e0">参考：受け取った動画（AI 生成）。動画で見えない部分（背面・側面の細部）は推定。等倍・同じ高さで並べています</text>')
    # 目安線
    guides = [(0, '頭頂'), (136, 'あご'), (272, '胸下'), (400, '股下'), (590, 'ひざ'), (842, '足元')]
    for y, name in guides:
        yy = top + y
        s.append(f'<line x1="70" y1="{yy}" x2="1700" y2="{yy}" stroke="#c9c3b6" stroke-width="1" stroke-dasharray="6 6"/>')
        s.append(f'<text x="18" y="{yy + 5}" font-size="14" fill="#8a8272">{name}</text>')
    s.append(f'<text x="18" y="{top + 470}" font-size="13" fill="#8a8272">約6.2頭身</text>')
    views = [front_view(), side_view('bracer'), back_view(), side_view('pauldron')]
    for i, (cx, v) in enumerate(zip(cols, views)):
        tr = f'translate({cx},{top})' + (' scale(-1,1)' if i == 3 else '')
        s.append(f'<ellipse cx="{cx}" cy="{top + 842}" rx="110" ry="14" fill="#000" opacity=".08"/>')
        s.append(g(v, tr))
        jp, en = labels[i]
        s.append(f'<text x="{cx}" y="{top + 900}" font-size="26" font-weight="700" fill="#2a2f4a" text-anchor="middle">{jp}</text>')
        s.append(f'<text x="{cx}" y="{top + 924}" font-size="14" fill="#8a8272" text-anchor="middle" letter-spacing="3">{en}</text>')
    # 右の欄：剣・色・メモ
    px = 1730
    s.append(f'<rect x="{px}" y="112" width="450" height="1046" rx="14" fill="#ffffff" stroke="#ddd6c8"/>')
    s.append(f'<text x="{px + 24}" y="146" font-size="20" font-weight="700" fill="#2a2f4a">武器：結晶の長剣</text>')
    s.append(g(sword_detail(), f'translate({px + 90},180) scale(.92)'))
    s.append(g(sword_sheathed(0, 0, 330, 0, front_grip=False), f'translate({px + 150},200) rotate(90)'))
    s.append(f'<text x="{px + 190}" y="560" font-size="13" fill="#6a6458">刀身は水色に光る結晶</text>')
    s.append(f'<text x="{px + 190}" y="580" font-size="13" fill="#6a6458">鍔は金・中央に青い宝石</text>')
    s.append(f'<text x="{px + 190}" y="600" font-size="13" fill="#6a6458">柄は紺の菱巻き／鞘は紺＋金</text>')
    s.append(f'<text x="{px + 24}" y="650" font-size="20" font-weight="700" fill="#2a2f4a">配色</text>')
    pal = [('髪', C['hair'], C['hair_s']), ('瞳', C['iris_b'], C['iris_t']), ('肌', C['skin'], C['skin_s']), ('上着・スカート', C['blue'], C['blue_s']),
           ('胴衣・前垂れ', C['white'], C['white_s']), ('金の縁・飾り', C['gold'], C['gold_s']), ('鎧（銀）', C['silver'], C['silver_s']),
           ('ベルト・革の籠手', C['leather'], C['leather_s']), ('手袋', C['glove'], C['glove_s']), ('ニーハイ', C['stock'], C['stock_s']),
           ('リボン・角飾り', C['ribbon'], C['ribbon_in']), ('刀身', C['blade'], C['blade_s'])]
    for i, (nm, c1, c2) in enumerate(pal):
        x = px + 24 + (i % 2) * 212
        y = 670 + (i // 2) * 40
        s.append(f'<rect x="{x}" y="{y}" width="26" height="26" rx="4" fill="{c1}" stroke="#555" stroke-width=".8"/>')
        s.append(f'<rect x="{x + 28}" y="{y}" width="14" height="26" rx="3" fill="{c2}" stroke="#555" stroke-width=".8"/>')
        s.append(f'<text x="{x + 50}" y="{y + 12}" font-size="13" fill="#3a3a3a">{nm}</text>')
        s.append(f'<text x="{x + 50}" y="{y + 25}" font-size="10.5" fill="#8a8272">{c1}</text>')
    s.append(f'<text x="{px + 24}" y="944" font-size="20" font-weight="700" fill="#2a2f4a">左右で違うところ</text>')
    notes = ['・左肩だけ銀の重ね肩当て（3枚・金の紋章）', '・左前腕は銀の籠手、右前腕は茶の革の籠手（ベルト3本）',
             '・右ひじに白いフリル', '・剣は左腰に佩く（腰ベルトは左へ斜めに下がる）', '・髪留めは左右とも黒リボン＋黒い角飾り（内側が赤）',
             '・アホ毛1本、前髪の1房が目の間に落ちる']
    for i, n in enumerate(notes):
        s.append(f'<text x="{px + 24}" y="{976 + i * 26}" font-size="14" fill="#3a3a3a">{n}</text>')
    s.append('</svg>')
    OUT.write_text('\n'.join(s), encoding='utf-8')
    print('wrote', OUT)


if __name__ == '__main__':
    build()

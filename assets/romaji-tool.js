// ローマ字入力の確認ツール（記事「ローマ字入力で迷いやすい文字の打ち方」用）
// かな→ローマ字の判定は、マシマシ打の判定エンジン（mashimashida の src/engine/romaji.ts）と同じ表と規則を使う。
(() => {
  const BASE = {
    'あ': ['a'], 'い': ['i', 'yi'], 'う': ['u', 'wu', 'whu'], 'え': ['e'], 'お': ['o'],
    'か': ['ka', 'ca'], 'き': ['ki'], 'く': ['ku', 'cu', 'qu'], 'け': ['ke'], 'こ': ['ko', 'co'],
    'さ': ['sa'], 'し': ['shi', 'si', 'ci'], 'す': ['su'], 'せ': ['se', 'ce'], 'そ': ['so'],
    'た': ['ta'], 'ち': ['chi', 'ti'], 'つ': ['tsu', 'tu'], 'て': ['te'], 'と': ['to'],
    'な': ['na'], 'に': ['ni'], 'ぬ': ['nu'], 'ね': ['ne'], 'の': ['no'],
    'は': ['ha'], 'ひ': ['hi'], 'ふ': ['fu', 'hu'], 'へ': ['he'], 'ほ': ['ho'],
    'ま': ['ma'], 'み': ['mi'], 'む': ['mu'], 'め': ['me'], 'も': ['mo'],
    'や': ['ya'], 'ゆ': ['yu'], 'よ': ['yo'],
    'ら': ['ra'], 'り': ['ri'], 'る': ['ru'], 'れ': ['re'], 'ろ': ['ro'],
    'わ': ['wa'], 'を': ['wo'],
    'が': ['ga'], 'ぎ': ['gi'], 'ぐ': ['gu'], 'げ': ['ge'], 'ご': ['go'],
    'ざ': ['za'], 'じ': ['ji', 'zi'], 'ず': ['zu'], 'ぜ': ['ze'], 'ぞ': ['zo'],
    'だ': ['da'], 'ぢ': ['di'], 'づ': ['du'], 'で': ['de'], 'ど': ['do'],
    'ば': ['ba'], 'び': ['bi'], 'ぶ': ['bu'], 'べ': ['be'], 'ぼ': ['bo'],
    'ぱ': ['pa'], 'ぴ': ['pi'], 'ぷ': ['pu'], 'ぺ': ['pe'], 'ぽ': ['po'],
    'ゔ': ['vu'],
    'ぁ': ['xa', 'la'], 'ぃ': ['xi', 'li'], 'ぅ': ['xu', 'lu'], 'ぇ': ['xe', 'le'], 'ぉ': ['xo', 'lo'],
    'ゃ': ['xya', 'lya'], 'ゅ': ['xyu', 'lyu'], 'ょ': ['xyo', 'lyo'], 'ゎ': ['xwa', 'lwa'],
    'っ': ['xtu', 'ltu', 'xtsu', 'ltsu'],
    'ー': ['-'], '、': [','], '。': ['.'], '！': ['!'], '？': ['?'], '～': ['~'],
  };
  const COMBO = {};
  const Y_ROW = {
    'き': ['ky'], 'ぎ': ['gy'], 'し': ['sh', 'sy'], 'じ': ['j', 'jy', 'zy'],
    'ち': ['ch', 'ty', 'cy'], 'ぢ': ['dy'], 'に': ['ny'], 'ひ': ['hy'],
    'び': ['by'], 'ぴ': ['py'], 'み': ['my'], 'り': ['ry'],
  };
  for (const [k, heads] of Object.entries(Y_ROW)) {
    for (const [s, v] of Object.entries({ 'ゃ': 'a', 'ゅ': 'u', 'ょ': 'o' })) COMBO[k + s] = heads.map((h) => h + v);
  }
  Object.assign(COMBO, {
    'しぇ': ['she', 'sye'], 'ちぇ': ['che', 'tye', 'cye'], 'じぇ': ['je', 'jye', 'zye'],
    'ふぁ': ['fa'], 'ふぃ': ['fi'], 'ふぇ': ['fe'], 'ふぉ': ['fo'],
    'てぃ': ['thi'], 'でぃ': ['dhi'], 'でゅ': ['dhu'], 'とぅ': ['twu'],
    'うぃ': ['wi'], 'うぇ': ['we'], 'うぉ': ['who'],
    'ゔぁ': ['va'], 'ゔぃ': ['vi'], 'ゔぇ': ['ve'], 'ゔぉ': ['vo'], 'つぁ': ['tsa'],
  });

  const toHira = (s) => s.replace(/[ァ-ヶ]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) - 0x60));

  // 位置 i から始まる入力候補 { r: ローマ字, n: 消費するかなの数 }
  function cands(s, i) {
    const out = [];
    const c = s[i];
    if (c === 'ん') {
      const next = i + 1 < s.length ? cands(s, i + 1) : null;
      if (next && next.length && next.every((x) => !/^[aiueony]/.test(x.r))) out.push({ r: 'n', n: 1 });
      out.push({ r: 'nn', n: 1 }, { r: 'xn', n: 1 });
      return out;
    }
    if (c === 'っ') {
      const next = i + 1 < s.length ? cands(s, i + 1) : [];
      next.forEach((x) => { if (/^[bcdfghjkmpqrstvwyz]/.test(x.r)) out.push({ r: x.r[0] + x.r, n: x.n + 1 }); });
      BASE['っ'].forEach((r) => out.push({ r, n: 1 }));
      return out;
    }
    const two = s.substr(i, 2);
    if (COMBO[two]) COMBO[two].forEach((r) => out.push({ r, n: 2 }));
    if (BASE[c]) BASE[c].forEach((r) => out.push({ r, n: 1 }));
    else out.push({ r: c.toLowerCase(), n: 1 });
    return out;
  }

  // 打鍵数がいちばん少ない区切り方（区切りごとに、同じ範囲を打てるほかの打ち方も返す）
  function plan(s) {
    const best = new Array(s.length + 1).fill(null);
    best[s.length] = { len: 0 };
    for (let i = s.length - 1; i >= 0; i--) {
      for (const c of cands(s, i)) {
        const rest = best[i + c.n];
        if (!rest) continue;
        const len = c.r.length + rest.len;
        if (!best[i] || len < best[i].len) best[i] = { len, c };
      }
    }
    const segs = [];
    for (let i = 0; i < s.length; i += best[i].c.n) {
      const c = best[i].c;
      const alts = [...new Set(cands(s, i).filter((x) => x.n === c.n).map((x) => x.r))];
      segs.push({ kana: s.substr(i, c.n), r: c.r, alts });
    }
    return segs;
  }

  // マシマシ打と同じ1キーずつの判定。受け付けた文字数を返す
  function judge(s, typed) {
    let pos = 0, buf = '';
    const input = (k) => {
      if (pos >= s.length) return false;
      const cs = cands(s, pos);
      const nb = buf + k;
      const m = cs.filter((c) => c.r.startsWith(nb));
      if (m.length) {
        buf = nb;
        const exact = m.find((c) => c.r === nb);
        if (exact && m.every((c) => c.r === nb)) { pos += exact.n; buf = ''; }
        return true;
      }
      const ex = buf && cs.find((c) => c.r === buf);
      if (ex) { pos += ex.n; buf = ''; return input(k); }
      return false;
    };
    let ok = 0;
    for (const k of typed) { if (!input(k)) break; ok++; }
    // 最後の n のように、まだ確定していないが打ち終わりとして認められる入力
    if (buf && pos < s.length && cands(s, pos).some((c) => c.r === buf && pos + c.n >= s.length)) pos = s.length;
    return { ok, done: pos >= s.length, kanaDone: pos };
  }

  // ローマ字 → かな（日本語入力と同じ区切り方）
  const R2K = {};
  for (const [k, rs] of Object.entries(BASE)) rs.forEach((r) => { if (!R2K[r]) R2K[r] = k; });
  for (const [k, rs] of Object.entries(COMBO)) rs.forEach((r) => { R2K[r] = k; });
  Object.assign(R2K, { xn: 'ん', nn: 'ん', "n'": 'ん' });
  const KEYS = Object.keys(R2K);
  const VOWEL_Y = /[aiueoy]/;

  function toKana(src) {
    const s = src.toLowerCase();
    const segs = [];
    let i = 0;
    while (i < s.length) {
      const c = s[i], d = s[i + 1];
      if (c === 'n' && d !== undefined && d !== 'n' && d !== "'" && !VOWEL_Y.test(d)) {
        segs.push({ r: 'n', kana: 'ん', note: 'single-n' }); i += 1; continue;
      }
      if (c === 'n' && d === undefined) { segs.push({ r: 'n', kana: 'n', pending: true }); i += 1; continue; }
      if (/[bcdfghjkmpqrstvwyz]/.test(c) && c === d) { segs.push({ r: c, kana: 'っ' }); i += 1; continue; }
      let hit = '';
      for (let len = 4; len >= 1; len--) {
        const part = s.substr(i, len);
        if (part.length === len && R2K[part]) { hit = part; break; }
      }
      if (hit) { segs.push({ r: hit, kana: R2K[hit] }); i += hit.length; continue; }
      const rest = s.slice(i);
      if (KEYS.some((k) => k.startsWith(rest))) { segs.push({ r: rest, kana: rest, pending: true }); break; }
      segs.push({ r: c, kana: c, bad: true }); i += 1;
    }
    // 「nn」のあとに母音・y が来ると、その文字は な行 にならない
    segs.forEach((g, k) => {
      const next = segs[k + 1];
      if (g.r === 'nn' && next && /^[aiueoy]/.test(next.r)) g.warn = true;
    });
    return segs;
  }

  const esc = (t) => t.replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));

  // --- ローマ字 → かな
  const rIn = document.getElementById('rk-in');
  const rOut = document.getElementById('rk-out');
  const rSegs = document.getElementById('rk-segs');
  const rNote = document.getElementById('rk-note');
  function updateR() {
    const v = rIn.value.replace(/\s/g, '');
    if (!v) { rOut.textContent = '—'; rSegs.innerHTML = ''; rNote.textContent = ''; return; }
    const segs = toKana(v);
    rOut.textContent = segs.map((g) => g.kana).join('');
    rSegs.innerHTML = segs.map((g) => {
      const cls = g.bad ? ' bad' : g.warn ? ' warn' : g.pending ? ' pending' : '';
      return `<li class="seg${cls}"><code>${esc(g.r)}</code><span>${esc(g.kana)}</span></li>`;
    }).join('');
    const notes = [];
    if (segs.some((g) => g.warn)) notes.push('「nn」で「ん」が確定したので、すぐ後ろの文字は な行・にゃ行 になりません。「ん」のあとを な行 にしたいときは、n をもう1つ足します（例：ninnniku）。');
    if (segs.some((g) => g.note === 'single-n')) notes.push('次が子音（n・y 以外）なので、n 1回で「ん」になりました。');
    if (segs.length && segs[segs.length - 1].r === 'n' && segs[segs.length - 1].pending) notes.push('最後の n は、まだ「ん」か な行 か決まっていません。続けて打つなら nn にしておくと確実です。');
    if (segs.some((g) => g.bad)) notes.push('赤い文字は、かなになりません。');
    rNote.textContent = notes.join(' ');
  }
  rIn.addEventListener('input', updateR);

  // --- かな → 打ち方
  const kIn = document.getElementById('kr-in');
  const kOut = document.getElementById('kr-out');
  const kTable = document.getElementById('kr-table');
  const pIn = document.getElementById('kr-try');
  const pOut = document.getElementById('kr-judge');
  const KANA_ONLY = /^[ぁ-ゖァ-ヶー、。！？～]+$/;
  let target = '';
  function updateK() {
    const v = kIn.value.replace(/\s/g, '');
    target = '';
    if (!v) { kOut.textContent = '—'; kTable.innerHTML = ''; updateP(); return; }
    if (!KANA_ONLY.test(v)) {
      kOut.textContent = 'ひらがな・カタカナで入れてください（漢字や英字は判定できません）';
      kTable.innerHTML = ''; updateP(); return;
    }
    target = toHira(v);
    const segs = plan(target);
    const keys = segs.map((g) => g.r).join('');
    kOut.innerHTML = `<code>${esc(keys)}</code> <span class="muted small">（${keys.length} 打）</span>`;
    kTable.innerHTML = '<thead><tr><th>かな</th><th>いちばん短い打ち方</th><th>ほかに通る打ち方</th></tr></thead><tbody>' +
      segs.map((g) => `<tr><td>${esc(g.kana)}</td><td><code>${esc(g.r)}</code></td><td>${g.alts.filter((a) => a !== g.r).map((a) => `<code>${esc(a)}</code>`).join(' ') || '<span class="muted">—</span>'}</td></tr>`).join('') +
      '</tbody>';
    updateP();
  }
  function updateP() {
    const typed = pIn.value.toLowerCase().replace(/\s/g, '');
    if (!target) { pOut.textContent = 'まず上の欄に言葉を入れてください。'; return; }
    if (!typed) { pOut.textContent = '上の打ち方のどれで打っても判定します。'; return; }
    const j = judge(target, typed);
    const good = esc(typed.slice(0, j.ok)), bad = esc(typed.slice(j.ok));
    let msg;
    if (bad) msg = `<span class="ng">${bad.charAt(0)}</span> で止まります（${j.ok + 1} 打目）`;
    else if (j.done) msg = '<span class="ok">打てました</span>';
    else msg = `ここまで OK（${target.slice(0, j.kanaDone) || '…'}）`;
    pOut.innerHTML = `<code><span class="ok">${good}</span><span class="ng">${bad}</span></code>　${msg}`;
  }
  kIn.addEventListener('input', updateK);
  pIn.addEventListener('input', updateP);

  // 例のボタン
  document.querySelectorAll('[data-rk]').forEach((b) => b.addEventListener('click', () => { rIn.value = b.dataset.rk; updateR(); }));
  document.querySelectorAll('[data-kr]').forEach((b) => b.addEventListener('click', () => { kIn.value = b.dataset.kr; pIn.value = ''; updateK(); }));

  updateR();
  updateK();
})();

// 作品が遊ばれた回数を数える（作品一覧を、遊ばれた回数の多い順に並べるため）。
// 数えるのは「遊ぶ」のリンクを押したときと、作品ページに埋め込んだゲームを触ったとき。
// 送るのは作品の ID だけ（例：{"game":"keshikasu"}）。Cookie は使わない。
// サーバー（api.shinpoyo.com、mashimashida リポジトリの worker/）は 1日・1作品・1人につき1回だけ数える。
(() => {
  const API = 'https://api.shinpoyo.com/v1/plays';
  const me = document.currentScript;
  let games = {};
  try { games = JSON.parse(me.dataset.games || '{}'); } catch (e) { return; }

  const today = () => new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);

  function send(game) {
    // 同じブラウザで同じ日に2回目は送らない（サーバーでも数えないが、通信を省く）
    const key = 'plays:' + game;
    try { if (localStorage.getItem(key) === today()) return; localStorage.setItem(key, today()); } catch (e) { /* 保存できなくても送る */ }
    const body = JSON.stringify({ game });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon(API, body)) return;
    } catch (e) { /* 下で fetch */ }
    fetch(API, { method: 'POST', body, keepalive: true, mode: 'cors' }).catch(() => {});
  }

  /** /keshikasu/ や /keshikasu/index.html → 作品 ID（遊ぶ URL でなければ null） */
  function gameOf(href) {
    let url;
    try { url = new URL(href, location.href); } catch (e) { return null; }
    if (url.origin !== location.origin) return null;
    for (const [path, id] of Object.entries(games)) {
      if (url.pathname === path || url.pathname.startsWith(path)) return id;
    }
    return null;
  }

  // 「遊ぶ」のリンク（中ボタン・Ctrl+クリックで新しいタブに開いたときも数える）
  const onLink = (ev) => {
    const a = ev.target.closest && ev.target.closest('a[href]');
    if (!a) return;
    const id = gameOf(a.getAttribute('href'));
    if (id) send(id);
  };
  document.addEventListener('click', onLink, true);
  document.addEventListener('auxclick', onLink, true);

  // 作品ページに埋め込んだゲーム：中を触るとページのフォーカスが iframe に移るので、それで数える
  window.addEventListener('blur', () => {
    setTimeout(() => {
      const f = document.activeElement;
      if (f && f.tagName === 'IFRAME') {
        const id = gameOf(f.getAttribute('src') || '');
        if (id) send(id);
      }
    }, 0);
  });
})();

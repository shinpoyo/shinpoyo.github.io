// PC でしか遊べない作品（例：キーボードが必要なマシマシ打）を、スマホ・タブレットで開こうとしたときに確認を出す。
// 対象は紹介ページに pc_only: と書いた作品（_tools/build.py が data-games に入れる）。
// 指で触る端末（マウスがなく、ホバーできない）のときだけ働く。PC では何もしない。
(() => {
  const me = document.currentScript;
  let games = {};
  try { games = JSON.parse(me.dataset.games || '{}'); } catch (e) { return; }
  const touch = matchMedia('(hover: none) and (pointer: coarse)').matches;
  if (!touch) return;

  function gameOf(href) {
    let url;
    try { url = new URL(href, location.href); } catch (e) { return null; }
    if (url.origin !== location.origin) return null;
    for (const [path, g] of Object.entries(games)) if (url.pathname.startsWith(path)) return g;
    return null;
  }

  let dlg;
  function ask(game, href) {
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.className = 'pc-only-dialog';
      dlg.innerHTML = '<p class="pc-only-title"></p><p class="pc-only-text"></p>' +
        '<div class="pc-only-actions"><a class="btn" href="/works/">スマホで遊べる作品を見る</a>' +
        '<a class="btn ghost pc-only-open">それでも開く</a>' +
        '<button type="button" class="pc-only-close">閉じる</button></div>';
      document.body.appendChild(dlg);
      dlg.querySelector('.pc-only-close').addEventListener('click', () => dlg.close());
      dlg.addEventListener('click', (ev) => { if (ev.target === dlg) dlg.close(); });
    }
    dlg.querySelector('.pc-only-title').textContent = `${game.name}は、パソコン向けのゲームです`;
    dlg.querySelector('.pc-only-text').textContent = `${game.need}で遊ぶので、スマホやタブレットでは遊べません。パソコンで shinpoyo.com を開いてください。`;
    dlg.querySelector('.pc-only-open').setAttribute('href', href);
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
  }

  document.addEventListener('click', (ev) => {
    const a = ev.target.closest && ev.target.closest('a[href]');
    if (!a || a.classList.contains('pc-only-open')) return;
    const g = gameOf(a.getAttribute('href'));
    if (!g) return;
    ev.preventDefault();
    ask(g, a.getAttribute('href'));
  }, true);
})();

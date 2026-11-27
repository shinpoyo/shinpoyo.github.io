// 作品ページの一番上のゲーム。はじめは表紙（作品の画像＋「ここを押して遊ぶ」）だけを出し、
// 押されたら iframe を読み込む。ページを開いただけではゲームを読み込まないので、表示が軽く、
// スマホでページを下に読み進めるときに、指がゲームに吸い込まれることもない。
// JavaScript が動かないときは、表紙がゲームへの普通のリンクとして働く。
(() => {
  const head = document.querySelector('.site-header');
  const setHead = () => { if (head) document.documentElement.style.setProperty('--head', head.offsetHeight + 'px'); };
  setHead();
  addEventListener('resize', setHead);

  document.querySelectorAll('.game-first').forEach((box) => {
    const cover = box.querySelector('.game-cover');
    const frame = box.querySelector('iframe[data-src]');
    if (!cover || !frame) return;
    cover.addEventListener('click', (ev) => {
      if (ev.button !== 0 || ev.ctrlKey || ev.metaKey || ev.shiftKey) return; // 新しいタブで開くときは普通のリンク
      ev.preventDefault();
      frame.src = frame.dataset.src;
      box.classList.add('playing');
      frame.addEventListener('load', () => { try { frame.focus(); } catch (e) { /* なにもしない */ } }, { once: true });
    });
  });
})();

// Google AdSense の設定。審査に通ったら client（ca-pub-…）と slot（広告ユニット ID）を入れる。
// 空のままなら広告は出ず、外部への読み込みも発生しない。
const ADSENSE = { client: '', slot: '' };

if (ADSENSE.client && ADSENSE.slot) {
  document.querySelectorAll('[data-ad]').forEach((box) => {
    box.hidden = false;
    const ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.display = 'block';
    ins.dataset.adClient = ADSENSE.client;
    ins.dataset.adSlot = ADSENSE.slot;
    ins.dataset.adFormat = 'auto';
    ins.dataset.fullWidthResponsive = 'true';
    box.appendChild(ins);
    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) { /* 広告ブロッカー等 */ }
  });
  const s = document.createElement('script');
  s.async = true;
  s.crossOrigin = 'anonymous';
  s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + encodeURIComponent(ADSENSE.client);
  document.head.appendChild(s);
}

/* The cast: emotive SVG characters shared across the whole course.
   Cortex = the model (blue chip). Bit = you, the builder (gold, hard hat).
   Somni = the dreamer (world-model rival, F6+), soft violet cloud, eyes closed.

   Usage:
     <script src="../../../assets/cast.js"></script>
     <span class="chr" data-c="cortex" data-e="think"></span>
     <script> Cast.render(document); </script>   // fills every .chr

   Emotions: neutral | think | reach | read | panic | happy | confused
   (bit supports: neutral | think | panic | happy | confused) */
(function (global) {
  var DK = "#0f1216", INK = "#e9ebee", BL = "#58c4dd", GD = "#ffd35c";

  function eyes(x1, x2, cy, r, dx, dy, st) {
    if (st === "happy")
      return '<path d="M' + (x1 - r) + ',' + (cy + 2) + ' Q' + x1 + ',' + (cy - r) + ' ' + (x1 + r) + ',' + (cy + 2) + '" fill="none" stroke="' + DK + '" stroke-width="3.5" stroke-linecap="round"/>'
           + '<path d="M' + (x2 - r) + ',' + (cy + 2) + ' Q' + x2 + ',' + (cy - r) + ' ' + (x2 + r) + ',' + (cy + 2) + '" fill="none" stroke="' + DK + '" stroke-width="3.5" stroke-linecap="round"/>';
    var pr = st === "wide" ? r * 0.32 : r * 0.42;
    return '<circle cx="' + x1 + '" cy="' + cy + '" r="' + r + '" fill="#fff"/><circle cx="' + x2 + '" cy="' + cy + '" r="' + r + '" fill="#fff"/>'
         + '<circle cx="' + (x1 + dx) + '" cy="' + (cy + dy) + '" r="' + pr + '" fill="' + DK + '"/><circle cx="' + (x2 + dx) + '" cy="' + (cy + dy) + '" r="' + pr + '" fill="' + DK + '"/>';
  }
  function brows(x1, x2, y, t) {
    return '<line x1="' + (x1 - 9) + '" y1="' + (y + t) + '" x2="' + (x1 + 9) + '" y2="' + (y - t) + '" stroke="' + INK + '" stroke-width="3" stroke-linecap="round"/>'
         + '<line x1="' + (x2 - 9) + '" y1="' + (y - t) + '" x2="' + (x2 + 9) + '" y2="' + (y + t) + '" stroke="' + INK + '" stroke-width="3" stroke-linecap="round"/>';
  }

  /* Cousin variants (F8 capstone): the same Cortex chip re-tinted per attention
     bet, with one distinguishing accessory. Single-source rule: variants live
     HERE, widgets request them via data-v. */
  var COUSIN = {
    full:   { c: "#fc6255", fill: "#3a1d1c",
              badge: '<rect x="26" y="88" width="20" height="4" rx="2" fill="#fc6255"/><rect x="26" y="82" width="20" height="4" rx="2" fill="#fc6255" opacity=".75"/><rect x="26" y="76" width="20" height="4" rx="2" fill="#fc6255" opacity=".5"/>' }, // the ever-growing cache, carried proudly
    sparse: { c: "#ffd35c", fill: "#3a3112",
              badge: '<circle cx="72" cy="58" r="17" fill="none" stroke="#ffd35c" stroke-width="2.5"/><line x1="84" y1="70" x2="92" y2="78" stroke="#ffd35c" stroke-width="2.5" stroke-linecap="round"/>' }, // the indexer's scout lens
    linear: { c: "#83c167", fill: "#1c3018",
              badge: '<rect x="24" y="76" width="16" height="18" rx="2" fill="#0f1216" stroke="#83c167" stroke-width="2"/><line x1="27" y1="82" x2="37" y2="82" stroke="#83c167" stroke-width="1.6"/><line x1="27" y1="87" x2="37" y2="87" stroke="#83c167" stroke-width="1.6"/>' }, // the fixed notebook
    hybrid: { c: "#83c167", fill: "#1c3018",
              badge: '<circle cx="60" cy="20" r="4" fill="#ffd35c"/>' } // linear body, a few full-attention layers up top
  };

  function cortex(e, v) {
    var M = {
      neutral:  { dx: 0, dy: 2, mouth: '<path d="M50,80 Q60,86 70,80" fill="none" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: null, x: "" },
      think:    { dx: 5, dy: -4, mouth: '<line x1="52" y1="82" x2="66" y2="82" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: -3, x: '<text x="96" y="30" font-size="16" fill="' + BL + '">?</text>' },
      reach:    { dx: -7, dy: 0, mouth: '<line x1="52" y1="82" x2="66" y2="82" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: -3, x: "" },
      read:     { dx: 0, dy: 6, mouth: '<path d="M52,82 Q60,80 68,82" fill="none" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: -2, x: "" },
      panic:    { dx: 0, dy: 0, style: "wide", mouth: '<ellipse cx="60" cy="82" rx="7" ry="9" fill="' + DK + '"/>', brow: 6, x: '<path d="M92,44 q4,8 0,12 q-4,-4 0,-12z" fill="' + BL + '" opacity=".85"/>' },
      happy:    { style: "happy", mouth: '<path d="M48,78 Q60,92 72,78" fill="none" stroke="' + DK + '" stroke-width="3.5" stroke-linecap="round"/>', brow: null, x: '<path d="M96,26 l2,6 6,2 -6,2 -2,6 -2,-6 -6,-2 6,-2z" fill="' + GD + '"/>' },
      confused: { dx: -5, dy: 0, mouth: '<path d="M50,82 q6,-6 10,0 q4,6 10,0" fill="none" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: 4, x: '<text x="94" y="30" font-size="18" fill="' + BL + '">?</text>' }
    }[e] || {};
    var ey = M.style === "happy" ? eyes(48, 72, 58, 10, 0, 0, "happy") : eyes(48, 72, 58, 12, M.dx || 0, M.dy || 0, M.style);
    var VC = COUSIN[v], C = VC ? VC.c : BL, FILL = VC ? VC.fill : "#12303a";
    return '<svg viewBox="0 0 120 120">'
      + '<rect x="18" y="26" width="84" height="74" rx="20" fill="' + FILL + '" stroke="' + C + '" stroke-width="3"/>'
      + '<line x1="18" y1="50" x2="8" y2="50" stroke="' + C + '" stroke-width="3" stroke-linecap="round"/><line x1="18" y1="76" x2="8" y2="76" stroke="' + C + '" stroke-width="3" stroke-linecap="round"/>'
      + '<line x1="102" y1="50" x2="112" y2="50" stroke="' + C + '" stroke-width="3" stroke-linecap="round"/><line x1="102" y1="76" x2="112" y2="76" stroke="' + C + '" stroke-width="3" stroke-linecap="round"/>'
      + '<circle cx="60" cy="20" r="4" fill="' + C + '"/><line x1="60" y1="24" x2="60" y2="26" stroke="' + C + '" stroke-width="3"/>'
      + (M.brow != null ? brows(48, 72, 40, M.brow) : "") + ey + M.mouth + M.x + (VC ? VC.badge : "") + '</svg>';
  }

  function bit(e) {
    var M = {
      neutral:  { dx: 0, dy: 1, mouth: '<path d="M48,78 Q58,84 68,78" fill="none" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: null, x: "" },
      think:    { dx: 5, dy: -4, mouth: '<line x1="50" y1="80" x2="64" y2="80" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: -3, x: '<text x="92" y="30" font-size="15" fill="' + GD + '">...</text>' },
      panic:    { style: "wide", mouth: '<ellipse cx="58" cy="80" rx="6" ry="8" fill="' + DK + '"/>', brow: 6, x: '<path d="M90,46 q4,7 0,11 q-4,-4 0,-11z" fill="' + GD + '" opacity=".85"/>' },
      happy:    { style: "happy", mouth: '<path d="M46,76 Q58,90 70,76" fill="none" stroke="' + DK + '" stroke-width="3.5" stroke-linecap="round"/>', brow: null, x: '<path d="M94,24 l2,6 6,2 -6,2 -2,6 -2,-6 -6,-2 6,-2z" fill="' + BL + '"/>' },
      confused: { dx: -5, dy: 0, mouth: '<path d="M48,80 q6,-6 10,0 q4,6 10,0" fill="none" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: 4, x: '<text x="90" y="30" font-size="17" fill="' + GD + '">?</text>' }
    }[e] || { dx: 0, dy: 1, mouth: '<path d="M48,78 Q58,84 68,78" fill="none" stroke="' + DK + '" stroke-width="3" stroke-linecap="round"/>', brow: null, x: "" };
    var ey = M.style === "happy" ? eyes(46, 70, 56, 9, 0, 0, "happy") : eyes(46, 70, 56, 11, M.dx || 0, M.dy || 0, M.style);
    return '<svg viewBox="0 0 120 120">'
      + '<path d="M58,22 C86,22 96,44 96,66 C96,90 80,100 58,100 C36,100 20,90 20,66 C20,44 30,22 58,22 Z" fill="#3a2e10" stroke="' + GD + '" stroke-width="3"/>'
      + '<rect x="30" y="16" width="56" height="10" rx="5" fill="' + GD + '"/><rect x="52" y="8" width="12" height="10" rx="3" fill="' + GD + '"/>'
      + (M.brow != null ? brows(46, 70, 38, M.brow) : "") + ey + M.mouth + M.x + '</svg>';
  }

  // Somni (F6+): the world-model rival. Cloud-soft, eyes closed - it dreams outcomes
  // instead of speaking tokens. Design rule (in widgets): Somni shows a small WORLD in a
  // thought bubble rather than a word bubble; here we just draw the portrait.
  function somni(e) {
    var PU = "#b6a6ff", FL = "#2e2a4d";
    var body = '<circle cx="60" cy="66" r="30" fill="' + FL + '"/>'
             + '<circle cx="36" cy="74" r="19" fill="' + FL + '"/>'
             + '<circle cx="84" cy="74" r="19" fill="' + FL + '"/>'
             + '<circle cx="60" cy="82" r="20" fill="' + FL + '"/>';
    var eye = '<path d="M44,66 Q50,72 56,66" fill="none" stroke="' + PU + '" stroke-width="3" stroke-linecap="round"/>'
            + '<path d="M64,66 Q70,72 76,66" fill="none" stroke="' + PU + '" stroke-width="3" stroke-linecap="round"/>';
    var mouth = e === "happy"
      ? '<path d="M52,78 Q60,86 68,78" fill="none" stroke="' + PU + '" stroke-width="2.6" stroke-linecap="round"/>'
      : '<path d="M54,78 Q60,82 66,78" fill="none" stroke="' + PU + '" stroke-width="2.4" stroke-linecap="round"/>';
    var zz = (e === "think" || e === "dream")
      ? '<text x="88" y="36" font-size="15" fill="' + PU + '" opacity=".85">z</text><text x="99" y="24" font-size="11" fill="' + PU + '" opacity=".6">z</text>'
      : "";
    return '<svg viewBox="0 0 120 120">' + body + eye + mouth + zz + '</svg>';
  }

  function render(root) {
    (root || document).querySelectorAll(".chr").forEach(function (s) {
      s.innerHTML = s.dataset.c === "bit" ? bit(s.dataset.e || "neutral")
        : s.dataset.c === "somni" ? somni(s.dataset.e || "neutral")
        : cortex(s.dataset.e || "neutral", s.dataset.v);
    });
  }

  global.Cast = { cortex: cortex, bit: bit, somni: somni, render: render };

  // When embedded in a parent frame, report our content height so the host can size the
  // iframe flush to the page (no inner scrollbar). Works cross-origin (file:// included).
  if (global.parent && global.parent !== global) {
    var _pt;
    function _postH() {
      clearTimeout(_pt);
      _pt = setTimeout(function () {
        // +2px buffer: with fractional display scaling, an exact-fit height can overflow by
        // <1px, spawning an inner scrollbar that reflows content and re-reports -> flicker loop.
        try { global.parent.postMessage({ __embHeight: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight) + 2 }, "*"); } catch (e) {}
      }, 60);
    }
    global.addEventListener("load", _postH);
    global.addEventListener("resize", _postH);
    try { new MutationObserver(_postH).observe(document.documentElement, { subtree: true, childList: true }); } catch (e) {}
    [80, 350, 800, 1500].forEach(function (t) { setTimeout(_postH, t); });
  }
})(window);

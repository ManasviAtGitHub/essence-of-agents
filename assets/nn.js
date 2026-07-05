/* Shared neural-net glyph for the models track.
   Draws a small, honest fully-connected net inside an <svg class="nn"> and
   returns handles to animate it three ways:
     - wave(on)         a phased activation wave flows left -> right (forward pass)
     - setCol(c, cls)   light one column ("fire" | "gold" | "bad" | "off" | null)
                        - columns double as EXPERTS in MoE scenes
     - setAll(cls) / clear()
   Styles + keyframes live in theme.css (svg.nn ...). No dependencies.

   Usage:
     const nn = NN.build(document.getElementById("nn"), { cols: 4, rows: 5 });
     nn.wave(true);            // forward pass
     nn.setCol(2, "fire");     // expert 2 activates
*/
(function (global) {
  function build(svg, opts) {
    opts = opts || {};
    var cols = opts.cols || 4, rows = opts.rows || 5;
    var w = opts.w || 210, h = opts.h || 150, r = opts.r || 5.5;
    var padX = opts.padX || 22, padY = opts.padY || 16;
    svg.setAttribute("viewBox", "0 0 " + w + " " + h);
    svg.classList.add("nn");

    var xs = [], ys = [];
    for (var c = 0; c < cols; c++) xs.push(cols === 1 ? w / 2 : padX + c * (w - 2 * padX) / (cols - 1));
    for (var i = 0; i < rows; i++) ys.push(rows === 1 ? h / 2 : padY + i * (h - 2 * padY) / (rows - 1));

    var html = "";
    for (c = 0; c < cols - 1; c++)
      for (var a = 0; a < rows; a++)
        for (var b = 0; b < rows; b++)
          html += '<line class="nn-edge" data-c="' + c + '" x1="' + xs[c] + '" y1="' + ys[a] +
                  '" x2="' + xs[c + 1] + '" y2="' + ys[b] +
                  '" style="animation-delay:' + (c * 0.32 + 0.16).toFixed(2) + 's"/>';
    for (c = 0; c < cols; c++)
      for (i = 0; i < rows; i++)
        html += '<circle class="nn-node" data-c="' + c + '" cx="' + xs[c] + '" cy="' + ys[i] +
                '" r="' + r + '" style="animation-delay:' + (c * 0.32).toFixed(2) + 's"/>';
    svg.innerHTML = html;

    var STATES = ["fire", "gold", "bad", "off"];
    function strip(el) { STATES.forEach(function (s) { el.classList.remove(s); }); }
    function each(sel, fn) { svg.querySelectorAll(sel).forEach(fn); }

    return {
      svg: svg, cols: cols, rows: rows,
      wave: function (on) { svg.classList.toggle("wave", !!on); },
      setCol: function (c, cls) {
        each('.nn-node[data-c="' + c + '"]', function (n) { strip(n); if (cls) n.classList.add(cls); });
      },
      setAll: function (cls) {
        each(".nn-node", function (n) { strip(n); if (cls) n.classList.add(cls); });
      },
      clear: function () {
        svg.classList.remove("wave");
        each(".nn-node", strip); each(".nn-edge", strip);
      },
    };
  }
  global.NN = { build: build };
})(window);

/* Shared animation engine for the course.
   A Timeline drives a scene through discrete, SCRUBBABLE steps (play / pause /
   step / drag). Each scene supplies onStep(index, dir); CSS transitions do the
   in-between motion. Respects prefers-reduced-motion. No dependencies.

   Usage:
     const tl = new Anim.Timeline({ length: N, onStep: (i, dir) => render(i, dir), autoMs: 1200 });
     Anim.scrubber(document.getElementById("scrub"), tl, { label: i => "token " + (i+1) });
     tl.render(0);
*/
(function (global) {
  function reduced() {
    try { return matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { return false; }
  }

  function Timeline(opts) {
    this.length = opts.length;
    this.onStep = opts.onStep || function () {};
    this.onState = opts.onState || function () {};
    this.autoMs = opts.autoMs || 1100;
    this.i = 0; this.playing = false; this.timer = null;
  }
  Timeline.prototype.state = function () {
    return { i: this.i, length: this.length, playing: this.playing,
             atStart: this.i === 0, atEnd: this.i === this.length - 1 };
  };
  Timeline.prototype.render = function (dir) { this.onStep(this.i, dir || 0); this.onState(this.state()); };
  Timeline.prototype.seek = function (i) {
    i = Math.max(0, Math.min(this.length - 1, i | 0));
    var dir = i > this.i ? 1 : (i < this.i ? -1 : 0);
    this.i = i; this.render(dir);
  };
  Timeline.prototype.next = function () {
    if (this.i < this.length - 1) { this.i++; this.render(1); return true; }
    this.pause(); return false;
  };
  Timeline.prototype.prev = function () { if (this.i > 0) { this.i--; this.render(-1); } };
  Timeline.prototype.restart = function () { this.pause(); this.i = 0; this.render(0); };
  Timeline.prototype.play = function () {
    if (this.playing) return;
    if (this.i >= this.length - 1) { this.i = 0; this.render(0); }
    this.playing = true; this.onState(this.state()); this._tick();
  };
  Timeline.prototype.pause = function () {
    this.playing = false; if (this.timer) clearTimeout(this.timer); this.timer = null; this.onState(this.state());
  };
  Timeline.prototype.toggle = function () { this.playing ? this.pause() : this.play(); };
  Timeline.prototype._tick = function () {
    var self = this, ms = reduced() ? 280 : this.autoMs;
    this.timer = setTimeout(function () {
      if (!self.playing) return;
      if (!self.next()) { self.pause(); return; }
      self._tick();
    }, ms);
  };

  /* A shared scrubber bound to a Timeline.
     opts.acts = [["name", len], ...] additionally renders a clickable act bar
     above the controls; clicking an act seeks to its first step. */
  function scrubber(container, tl, opts) {
    opts = opts || {};
    container.classList.add("scrub");
    container.setAttribute("role", "group");
    container.setAttribute("aria-label", "Animation playback controls");
    var actBar = null, actStarts = [];
    if (!opts.acts) {
      var stale = container.parentElement && container.parentElement.querySelector(".scrub-acts");
      if (stale) stale.remove();
    }
    if (opts.acts) {
      var host = container.parentElement;
      actBar = host.querySelector(".scrub-acts");
      if (!actBar) { actBar = document.createElement("div"); actBar.className = "scrub-acts"; host.insertBefore(actBar, container); }
      var off = 0;
      actBar.innerHTML = opts.acts.map(function (a, k) {
        actStarts.push(off); off += a[1];
        return '<button class="act-chip" data-k="' + k + '" aria-label="Jump to act ' + (k + 1) + '">' +
               '<span class="an">act ' + (k + 1) + '</span>' + a[0] + '</button>';
      }).join('<span class="act-sep">&rarr;</span>');
      actBar.querySelectorAll(".act-chip").forEach(function (b) {
        b.onclick = function () { tl.pause(); tl.seek(actStarts[+b.dataset.k]); };
      });
    }
    container.innerHTML =
      '<button class="scrub-btn" data-a="restart" title="Restart" aria-label="Restart">&#8635;</button>' +
      '<button class="scrub-btn" data-a="prev" title="Step back" aria-label="Step back">&#9664;</button>' +
      '<button class="scrub-btn play" data-a="toggle" title="Play / pause" aria-label="Play or pause">&#9654;</button>' +
      '<button class="scrub-btn" data-a="next" title="Step forward" aria-label="Step forward">&#9654;&#9654;</button>' +
      '<input class="scrub-range" type="range" min="0" max="' + (tl.length - 1) + '" value="0" aria-label="Step" />' +
      '<span class="scrub-count" aria-live="polite"></span>' +
      '<span class="scrub-note" title="This is a scripted simulation. Each step labels which numbers are computed live and which are illustrative anchors.">simulation</span>';
    var range = container.querySelector(".scrub-range");
    var count = container.querySelector(".scrub-count");
    var play = container.querySelector('[data-a="toggle"]');
    container.querySelectorAll(".scrub-btn").forEach(function (b) {
      b.onclick = function () {
        var a = b.dataset.a;
        if (a === "toggle") tl.toggle();
        else { tl.pause(); tl[a](); }
      };
    });
    range.oninput = function () { tl.pause(); tl.seek(+range.value); };
    tl.onState = function (s) {
      range.value = s.i;
      count.textContent = opts.label ? opts.label(s.i) : (s.i + 1) + " / " + s.length;
      play.innerHTML = s.playing ? "&#10074;&#10074;" : "&#9654;";
      play.classList.toggle("on", s.playing);
      if (actBar) {
        var cur = 0;
        for (var k = 0; k < actStarts.length; k++) if (s.i >= actStarts[k]) cur = k;
        actBar.querySelectorAll(".act-chip").forEach(function (b, j) { b.classList.toggle("on", j === cur); });
      }
    };
  }

  /* Act-structured labels for long mechanism scenes (models track).
     acts = [["one turn", 7], ["the knobs", 7], ...] ->
     label(i) = "act 2 . the knobs . 3/7" */
  function actLabel(acts) {
    return function (i) {
      var k = 0, off = 0;
      while (k < acts.length - 1 && i >= off + acts[k][1]) { off += acts[k][1]; k++; }
      return "act " + (k + 1) + " . " + acts[k][0] + " . " + (i - off + 1) + "/" + acts[k][1];
    };
  }

  global.Anim = { reduced: reduced, Timeline: Timeline, scrubber: scrubber, actLabel: actLabel };
})(window);

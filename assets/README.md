# Shared library (`/assets`)

One source of truth for the whole project (course + production + launcher). Three files,
no build, no dependencies, ASCII-only:

| File | What it is |
|------|------------|
| `theme.css` | Dark 3Blue1Brown palette (CSS variables) + shared components: the cast (`.chr`, `.scene`, `.bubble`, `.react`, `.say`) and the animation scrubber (`.scrub*`). |
| `cast.js` | The cast. `window.Cast` = `{ cortex(e), bit(e), render(root) }`. The ONLY place characters are defined. |
| `anim.js` | The animation engine. `window.Anim` = `{ reduced(), Timeline, scrubber(el, tl, opts) }`. Scrubbable, deterministic scenes. |

Everything is **simulation** by default -- no page calls a real model. (The one opt-in "run it
for real" path is `production/server.py` + `/?live`; see `ARCHITECTURE.md`.)

## Cast (`cast.js`)

```html
<span class="chr" data-c="cortex" data-e="think"></span>   <!-- or data-c="bit" -->
<script src="../../../../assets/cast.js"></script>
<script> Cast.render(document); </script>                 <!-- fills every .chr with an SVG -->
```

- `Cast.cortex(emotion)` / `Cast.bit(emotion)` -> an SVG string.
- `Cast.render(root)` -> fills every `.chr[data-c][data-e]` under `root`.
  Call it again after any innerHTML re-render, or faces go blank.
- Emotions -- **cortex**: `neutral think reach read panic happy confused` ; **bit**: `neutral think panic happy confused`.
- Roles: **Cortex** = the model (thinking / memory / output). **Bit** = you, the builder (building / safety / cost / shipping).

## Animation engine (`anim.js`)

A `Timeline` walks a scene through discrete, **scrubbable** steps; CSS transitions do the
in-between motion. Respects `prefers-reduced-motion` (adds `body.reduce`).

```js
const tl = new Anim.Timeline({ length: STEPS.length, onStep: renderStep, autoMs: 1200 });
Anim.scrubber(document.getElementById("scrub"), tl, { label: i => "step " + (i + 1) });
tl.render(0);
```

- `Timeline({length, onStep(i, dir), autoMs})` -- methods: `play() pause() toggle() next() prev() seek(i) restart() render(dir)`.
- `onStep(i, dir)` is your renderer; `dir` is +1 / -1 / 0 (forward / back / seek) so you can
  animate only on forward steps.
- `Anim.scrubber(container, tl, {label})` -- renders the shared control bar bound to `tl`.
- `Anim.reduced()` -- true if the user prefers reduced motion.

## Writing a new animated scene (the recipe)

1. Copy `assets/scene-template.html` into `agentic-course/module-XX/.../widgets/NAME/index.html`.
2. Fill in `STEPS` (your scene data) and `renderStep(i, dir)` (draw step `i`; grow bars / move
   packets on `dir > 0`).
3. Add it to the `NAV` array in `agentic-course/index.html`.
4. Verify: `node tools/gallery.mjs` (contact sheet) and `python tests/test_modules.py`.

**Rules that keep this from drifting** (enforced by `tests/test_structure.py`):
- Never re-inline a character -- always use `cast.js`.
- Every widget links `theme.css` + `cast.js`.
- No default surface calls a live model. Keep it a simulation.
- Keep every file ASCII (use `-`, `&mdash;`, `&rarr;`).

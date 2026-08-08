// Capture a widget as an animated GIF (no ffmpeg) - cutoff-proof.
// Deps: playwright (present), plus `npm i --no-save gifenc pngjs`.
//   node tools/make_gif.mjs <abs_widget_html> <out.gif> [steps] [fps] [perStep] [captureSel] [clickSel]
// captureSel: element to film (default: #canvas / #cv / canvas). clickSel: control to
// click between steps (default: the scrubber's next button; e.g. "#run" for run-driven widgets).
//
// WHY IT CANNOT CUT OFF: widgets grow and shift while animating, and a GIF's canvas is
// fixed - so any pre-measured clip is a bet. Instead, every frame screenshots THE
// ELEMENT itself (an element shot always contains the whole element, by definition).
// Frames of different sizes are then padded onto one canvas sized to the LARGEST frame
// before encoding. No measuring pass, no timing bets - containment is structural.
// Set GIF_AUDIT=1 to also write <out>.last.png (the final composited frame) for review.
import { chromium } from "playwright";
import { pathToFileURL } from "url";
import gifenc from "gifenc";
const { GIFEncoder, quantize, applyPalette } = gifenc;
import pngjs from "pngjs";
const { PNG } = pngjs;
import { writeFileSync } from "fs";

const [, , widgetArg, out, stepsArg, fpsArg, perArg, selArg, clickArg] = process.argv;
// The widget path may carry a #hash (e.g. index.html#film) to trigger a capture-only mode
// inside the widget. pathToFileURL would mangle it, so split it off and re-append to the URL.
const hashAt = widgetArg.indexOf("#");
const widget = hashAt >= 0 ? widgetArg.slice(0, hashAt) : widgetArg;
const urlHash = hashAt >= 0 ? widgetArg.slice(hashAt) : "";
const STEPS = +(stepsArg || 8), FPS = +(fpsArg || 12), PER = +(perArg || 6);
const DELAY = Math.round(1000 / FPS);
const NEXT = clickArg || '.scrub-btn[data-a="next"]';
// READING PACE: after each step's entry animation, hold a settled frame this long so a
// human can actually read the state (GIFs allow per-frame delays). Override: GIF_HOLD=ms.
// 4200 was calibrated against the series' caption-heavy widgets (user-picked, 2026-07).
const HOLD = +(process.env.GIF_HOLD || 4200);
// CRISPNESS: GIF_SCALE = deviceScaleFactor (render at Nx for sharp small text/lines); GIF_VW widens
// the viewport so canvases authored wider than 680 aren't downscaled before capture. Both default to
// the original behavior - only text-dense widgets that read fuzzy at 1x need to raise them.
const SCALE = +(process.env.GIF_SCALE || 1), VW = +(process.env.GIF_VW || 680);
// START: advance this many steps before capturing, to split one widget's arc into several GIFs
// (e.g. GIF 1 = step 0, GIF 2 = steps 1..n). Default 0 = from the beginning.
const START = +(process.env.GIF_START || 0);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: VW, height: 2200 }, deviceScaleFactor: SCALE });

async function findTarget() {
  return selArg
    ? await page.$(selArg)
    : (await page.$("#canvas")) || (await page.$("#cv")) || (await page.$("canvas"));
}

await page.goto(pathToFileURL(widget).href + urlHash, { timeout: 15000 });
await page.waitForTimeout(700);
if (!(await findTarget())) { console.error("no capture target (" + (selArg || "canvas") + ") in " + widget); process.exit(1); }

// advance to the START step (for GIFs that film a later slice of one widget's arc)
for (let j = 0; j < START; j++) {
  const b = await page.$(NEXT);
  if (b) { try { await b.click({ timeout: 1000 }); } catch {} }
  await page.waitForTimeout(DELAY);
}

// ---- collect: one ELEMENT screenshot per frame (always whole, sizes may vary) ----
// Per step: PER animation frames at DELAY pace, then one settled frame held for HOLD ms
// (the last step holds a little longer before the loop restarts).
const shots = [];                                       // { buf, delay }
async function shoot(delay) {
  const el = await findTarget();                        // re-locate: survives re-renders
  if (el) { try { shots.push({ buf: await el.screenshot({ type: "png" }), delay }); } catch {} }
}
for (let s = 0; s < STEPS; s++) {
  for (let k = 0; k < PER; k++) { await shoot(DELAY); await page.waitForTimeout(DELAY); }
  await page.waitForTimeout(380);                       // let the step's easing settle
  await shoot(s === STEPS - 1 ? HOLD + 800 : HOLD);     // the readable hold
  const b = await page.$(NEXT);
  if (b) { try { await b.click({ timeout: 1000 }); } catch {} }
}
await browser.close();
if (!shots.length) { console.error("captured 0 frames from " + widget); process.exit(1); }

// ---- compose: pad every frame onto a canvas sized to the largest frame ----
const frames = shots.map(s => ({ png: PNG.sync.read(s.buf), delay: s.delay }));  // RGBA
const W = Math.max(...frames.map(f => f.png.width));
const H = Math.max(...frames.map(f => f.png.height));
const bg = [frames[0].png.data[0], frames[0].png.data[1], frames[0].png.data[2]];  // widget's own corner color

const gif = GIFEncoder();
let lastCanvas = null;
for (const f of frames) {
  const canvas = Buffer.alloc(W * H * 4);
  for (let i = 0; i < W * H; i++) { canvas[i*4] = bg[0]; canvas[i*4+1] = bg[1]; canvas[i*4+2] = bg[2]; canvas[i*4+3] = 255; }
  const x0 = Math.floor((W - f.png.width) / 2);         // center horizontally, top-align
  for (let y = 0; y < f.png.height; y++)
    f.png.data.copy(canvas, ((y * W) + x0) * 4, y * f.png.width * 4, (y + 1) * f.png.width * 4);
  const palette = quantize(canvas, 256);
  const index = applyPalette(canvas, palette);
  gif.writeFrame(index, W, H, { palette, delay: f.delay });
  lastCanvas = canvas;
}
gif.finish();
writeFileSync(out, gif.bytes());
if (process.env.GIF_AUDIT && lastCanvas) {
  const png = new PNG({ width: W, height: H });
  lastCanvas.copy(png.data);
  writeFileSync(out + ".last.png", PNG.sync.write(png));
}
console.log("wrote", out, (gif.bytes().length / 1048576).toFixed(2) + "MB,", frames.length, "frames,", W + "x" + H);

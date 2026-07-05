// Runtime gate + automated QA: load every widget, exercise its steps and toggles,
// and FAIL on any console error, uncaught exception, blank render, or a scene whose
// scrubber / characters did not build. This is what the text-only tests can't see.
// A widget is retried once, so a transient flake does not fail the gate -- only a
// persistent problem (fails twice) counts.
//   node tools/check_widgets.mjs
import { chromium } from "playwright";
import { pathToFileURL } from "url";
import { readdirSync } from "fs";
import { resolve, join } from "path";

function walk(dir, out = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) { if (e.name !== "node_modules") walk(p, out); }
    else if (e.name === "index.html") out.push(p);
  }
  return out;
}

// Every course widget + the hub pages + all of production (hub, stage, scenes) + the models track.
const seen = new Set();
const targets = [
  ...walk(resolve("agentic-course")),
  resolve("agentic-course/about.html"),
  ...walk(resolve("production")),
  ...walk(resolve("models")),
].filter(p => (seen.has(p) ? false : seen.add(p)));

// Safe in-widget controls to click (never navigation links).
const CONTROLS = [".modebtn", ".runbtn", ".dt", ".tab", "#run", ".chip", ".ex"];
const NEXT = '.scrub-btn[data-a="next"]';

const browser = await chromium.launch();

async function check(file) {
  const errors = [];
  const page = await browser.newPage({ viewport: { width: 1000, height: 720 } });
  page.on("console", m => { if (m.type() === "error") errors.push("console: " + m.text()); });
  page.on("pageerror", e => errors.push("pageerror: " + e.message));
  try {
    await page.goto(pathToFileURL(file).href, { timeout: 8000 });
    await page.waitForTimeout(300);
    // step forward through a scrubber if present
    for (let i = 0; i < 12; i++) {
      const n = await page.$(NEXT);
      if (!n) break;
      try { await n.click({ timeout: 1500 }); } catch {}
      await page.waitForTimeout(150);
    }
    // toggle every mode/control, re-stepping a little after each
    for (const sel of CONTROLS) {
      const count = await page.$$eval(sel, els => els.length).catch(() => 0);
      for (let i = 0; i < count; i++) {
        const els = await page.$$(sel);
        if (!els[i]) continue;
        try { await els[i].click({ timeout: 1500 }); await page.waitForTimeout(180); } catch {}
        for (let s = 0; s < 3; s++) {
          const n = await page.$(NEXT);
          if (n) { try { await n.click({ timeout: 1000 }); } catch {} await page.waitForTimeout(110); }
        }
      }
    }
    // backward + restart (catches scrub-back bugs)
    for (const a of ["prev", "prev", "restart"]) {
      const b = await page.$(`.scrub-btn[data-a="${a}"]`);
      if (b) { try { await b.click({ timeout: 1000 }); } catch {} await page.waitForTimeout(140); }
    }
    // correctness signals
    const checks = await page.evaluate(() => {
      const out = [];
      if (document.body.innerText.trim().length < 5) out.push("blank render (no text)");
      if (document.querySelector("#scrub") && !document.querySelector("#scrub .scrub-btn")) out.push("scrubber did not build (anim.js?)");
      const chr = document.querySelectorAll(".chr");
      if (chr.length) {
        const filled = [...chr].filter(c => c.querySelector("svg")).length;
        if (filled === 0) out.push(".chr present but no SVG (cast.js render?)");
      }
      return out;
    });
    errors.push(...checks);
  } catch (e) {
    errors.push("load error: " + String(e).split("\n")[0]);
  }
  await page.close();
  return errors;
}

const results = [];
for (const file of targets) {
  const rel = file.replace(resolve(".") + "\\", "").replace(/\\/g, "/");
  let errors = await check(file);
  if (errors.length) errors = await check(file);  // retry once: a real bug fails twice
  results.push({ rel, ok: errors.length === 0, errors });
}
await browser.close();

let bad = 0;
for (const r of results) {
  if (r.ok) console.log("ok   " + r.rel);
  else { bad++; console.log("FAIL " + r.rel); r.errors.slice(0, 4).forEach(e => console.log("       - " + e)); }
}
console.log(`\n${results.length - bad}/${results.length} widgets clean` + (bad ? ` -- ${bad} FAILED (persisted through a retry)` : ""));
process.exit(bad ? 1 : 0);

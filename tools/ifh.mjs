// Measure each chapter's embedded-scene iframe: does its height match its content
// (i.e. no inner scrollbar)?  node tools/ifh.mjs
import { chromium } from "playwright";
import { pathToFileURL } from "url";
import { resolve } from "path";
const HUB = resolve("production/index.html");
const CH = ["retries", "budget", "guardrail", "observe", "eval", "compact", "serve", "chat"];
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1100, height: 800 } });
await p.goto(pathToFileURL(HUB).href);
for (const c of CH) {
  await p.click(`[data-id="${c}"]`);
  await p.waitForTimeout(1200);
  const r = await p.evaluate(() => {
    const f = document.querySelector("iframe.scene-embed");
    if (!f) return null;
    let ch = -1; try { ch = f.contentDocument.body.scrollHeight; } catch (e) {}
    return { h: f.offsetHeight, content: ch };
  });
  const fits = r && (r.content < 0 ? "n/a" : (Math.abs(r.h - r.content) <= 24 ? "FITS (no inner scroll)" : "SCROLLS by " + (r.content - r.h)));
  console.log(c.padEnd(10), r ? `iframe=${r.h}px content=${r.content}px -> ${fits}` : "no scene");
}
await b.close();

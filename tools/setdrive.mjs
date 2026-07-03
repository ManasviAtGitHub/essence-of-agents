// Set a range input's value, then click a selector N times, then screenshot.
//   node tools/setdrive.mjs <file> <out.png> <rangeSel> <value> <clickSel> <n>
import { chromium } from "playwright";
import { pathToFileURL } from "url";
const [, , file, out, rangeSel, value, clickSel, n] = process.argv;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1000, height: 800 } });
await p.goto(pathToFileURL(file).href);
await p.waitForTimeout(300);
if (rangeSel && value) {
  await p.$eval(rangeSel, (el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, value);
  await p.waitForTimeout(200);
}
for (let i = 0; i < (+n || 0); i++) { try { await p.click(clickSel, { timeout: 1500 }); } catch {} await p.waitForTimeout(200); }
await p.screenshot({ path: out, fullPage: true });
await b.close();
console.log("wrote", out);

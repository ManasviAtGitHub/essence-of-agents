import { chromium } from "playwright";
import { pathToFileURL } from "url";
const f = process.argv[2];
const b = await chromium.launch();
const p = await b.newPage();
await p.goto(pathToFileURL(f).href);
try { await p.click("#run", { timeout: 2000 }); } catch {}
await p.waitForTimeout(300);
const info = await p.evaluate(() => {
  const n = document.querySelector(".node");
  if (!n) return { error: "no .node" };
  const cs = getComputedStyle(n);
  return { bg: cs.backgroundColor, color: cs.color, sheets: [...document.styleSheets].map(s => (s.href || "inline")) };
});
console.log(JSON.stringify(info, null, 2));
const n = await p.$(".node");
if (n) await n.screenshot({ path: "tools/shot-node-crop.png" });
await b.close();

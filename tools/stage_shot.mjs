// Drive the LIVE served stage UI: open the running server, give Cortex a task,
// wait for the streamed answer to render, screenshot it.
//   node tools/stage_shot.mjs [url] [task] [out.png]
import { chromium } from "playwright";

const URL = process.argv[2] || "http://127.0.0.1:8088";
const TASK = process.argv[3] || "What is 17 * 23? Use the calculator, then state just the number.";
const OUT = process.argv[4] || "tools/shot-stage-live.png";

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1100, height: 820 } });

for (let i = 0; i < 30; i++) {
  try { await page.goto(URL, { timeout: 2000 }); break; }
  catch { await page.waitForTimeout(500); }
}

await page.fill("#q", TASK);
await page.click("#run");

await page.waitForFunction(() => {
  const a = document.querySelector(".answerbox");
  return a && a.textContent && a.textContent.trim().length > 0;
}, { timeout: 90000 });

await page.waitForTimeout(600);
await page.screenshot({ path: OUT, fullPage: true });
await browser.close();
console.log("wrote", OUT);

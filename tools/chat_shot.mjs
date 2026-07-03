// Drive the live chat UI: open the running server, type a task, wait for the real
// answer to render, screenshot it.
//   node tools/chat_shot.mjs [url] [task] [out.png]
import { chromium } from "playwright";

const URL = process.argv[2] || "http://127.0.0.1:8088";
const TASK = process.argv[3] || "What is 17*23? Use the calculator tool, then state just the number.";
const OUT = process.argv[4] || "tools/shot-chat-live.png";

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 900, height: 600 } });

// retry until the server is up
for (let i = 0; i < 30; i++) {
  try { await page.goto(URL, { timeout: 2000 }); break; }
  catch { await page.waitForTimeout(500); }
}

await page.fill("#q", TASK);
await page.click("#send");

// wait for the bot bubble to stop showing the "..." placeholder
await page.waitForFunction(() => {
  const els = document.querySelectorAll(".bot");
  const last = els[els.length - 1];
  return last && last.textContent && last.textContent.trim() !== "...";
}, { timeout: 90000 });

await page.waitForTimeout(400);
await page.screenshot({ path: OUT, fullPage: true });
await browser.close();
console.log("wrote", OUT);

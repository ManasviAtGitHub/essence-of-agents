// Screenshot a local HTML widget, optionally clicking a sequence of selectors first,
// so the rendered result can be inspected as a PNG.
//
//   node tools/shoot.mjs <abs_html> <out_png> [selector ...]
//
// Each selector is clicked once, in order, with a wait between (so streaming/animation
// settles). To click the same control twice, pass it twice. Examples:
//   node tools/shoot.mjs run-again/index.html shot.png "#run" "#run"
//   node tools/shoot.mjs distribution/index.html shot.png "#run" "#run" "#door"
import { chromium } from "playwright";
import { pathToFileURL } from "url";

const [, , html, out, ...clicks] = process.argv;
if (!html || !out) {
  console.error("usage: node tools/shoot.mjs <abs_html> <out_png> [selector ...]");
  process.exit(1);
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1100, height: 780 } });
await page.goto(pathToFileURL(html).href);

for (const sel of clicks) {
  await page.click(sel);
  await page.waitForTimeout(1500);
}
await page.waitForTimeout(1000);
await page.screenshot({ path: out, fullPage: true });
await browser.close();
console.log("wrote", out);

// Narrow-viewport screenshot to check responsiveness.
//   node tools/nshot.mjs <file> <out.png> [width]
import { chromium } from "playwright";
import { pathToFileURL } from "url";
const [, , file, out, w = "430"] = process.argv;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: 720 } });
await p.goto(pathToFileURL(file).href);
await p.waitForTimeout(500);
await p.screenshot({ path: out, fullPage: true });
await b.close();
console.log("wrote", out, "at", w + "px");

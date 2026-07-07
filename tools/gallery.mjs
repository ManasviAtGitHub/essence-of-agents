// Contact-sheet harness: screenshot every page + widget into tools/gallery/,
// then render a single index.html grid and screenshot THAT as _contact.png.
// One command to eyeball the whole repo after any change.
//   node tools/gallery.mjs
import { chromium } from "playwright";
import { pathToFileURL } from "url";
import { mkdirSync, writeFileSync } from "fs";
import { resolve } from "path";

// name, path (repo-relative), optional click selectors to reach a representative state
const TARGETS = [
  ["launcher", "index.html"],
  ["course-hub", "agentic-course/index.html"],
  ["models-hub", "models/index.html"],
  ["models m0 next-token-loop", "models/module-00-autoregression/widgets/next-token-loop/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m1 token-lens", "models/module-01-tokens/widgets/token-lens/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m2 attention-lens", "models/module-02-attention/widgets/attention-lens/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m3 kv-cache", "models/module-03-kv-cache/widgets/kv-cache/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m4 expert-router", "models/module-04-moe/widgets/expert-router/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m5 mla-mtp", "models/module-05-deepseek/widgets/mla-mtp/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m6 four-manners", "models/module-06-training/widgets/four-manners/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m7 verifier-teacher", "models/module-07-reasoning/widgets/verifier-teacher/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m8 shrink-it", "models/module-08-small-models/widgets/shrink-it/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["models m9 landscape", "models/module-09-atlas/widgets/landscape/index.html", ['.chip[data-res="mem"]', '.chip[data-cat="0"]']],
  ["models m9 assemble", "models/module-09-atlas/widgets/assemble/index.html", ['.part[data-id="tok"]', '.part[data-id="emb"]']],
  ["models m9 budget", "models/module-09-atlas/widgets/budget/index.html", ['.trick[data-id="mla"]', '.trick[data-id="moe"]']],
  ["models cap compile-live", "models/module-10-compiler/widgets/compile-live/index.html", ['.req', '#run']],
  ["models cap architecture", "models/module-10-compiler/widgets/architecture/index.html", []],
  ["about", "agentic-course/about.html"],
  ["production-hub", "production/index.html"],
  ["prod-stage (offline)", "production/web/index.html"],
  ["m0 run-again", "agentic-course/module-00-smallest-agent/widgets/run-again/index.html", ["#run"]],
  ["m2 loop-cycle", "agentic-course/module-02-the-loop/widgets/loop-cycle/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m2 think-toggle", "agentic-course/module-02-the-loop/widgets/think-toggle/index.html", ["#run"]],
  ["m3 context-lever", "agentic-course/module-03-context/widgets/context-lever/index.html"],
  ["m3 distribution", "agentic-course/module-03-context/widgets/distribution/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m3 context-window", "agentic-course/module-03-context/widgets/context-window/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m4 librarian", "agentic-course/module-04-memory/widgets/librarian/index.html", ["#run"]],
  ["m5 plan-replan", "agentic-course/module-05-planning/widgets/plan-replan/index.html", ["#run"]],
  ["m9 prompt-injection", "agentic-course/module-09-security/widgets/prompt-injection/index.html", ["#run"]],
  ["m12 capstone", "agentic-course/module-12-capstone/widgets/capstone-chooser/index.html", [".chip"]],
  ["m12 capstone-sim", "agentic-course/module-12-capstone/widgets/capstone-sim/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m1 growing-hands", "agentic-course/module-01-hands/widgets/growing-hands/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m4 similarity-space", "agentic-course/module-04-memory/widgets/similarity-space/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m5 plan-rewrite", "agentic-course/module-05-planning/widgets/plan-rewrite/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m6 verify-loop", "agentic-course/module-06-verification/widgets/verify-loop/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m7 inside-outside", "agentic-course/module-07-reasoning/widgets/inside-outside/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m8 team-flow", "agentic-course/module-08-multi-agent/widgets/team-flow/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m9 injection-flow", "agentic-course/module-09-security/widgets/injection-flow/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m10 eval-grid", "agentic-course/module-10-evaluation/widgets/eval-grid/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["m11 feedback-loop", "agentic-course/module-11-shipping/widgets/feedback-loop/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod retries", "production/scenes/retries/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod budget", "production/scenes/budget/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod guardrail", "production/scenes/guardrail/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod tracing", "production/scenes/tracing/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod evalgate", "production/scenes/evalgate/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod compaction", "production/scenes/compaction/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod serve", "production/scenes/serve/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod multiagent", "production/scenes/multiagent/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod mcp", "production/scenes/mcp/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
  ["prod callgraph", "production/scenes/callgraph/index.html", ['.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]', '.scrub-btn[data-a="next"]']],
];

const OUT = resolve("tools/gallery");
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch();
const cards = [];
for (const [name, rel, clicks = []] of TARGETS) {
  const page = await browser.newPage({ viewport: { width: 900, height: 620 } });
  const file = name.replace(/[^a-z0-9]+/gi, "-").toLowerCase() + ".png";
  try {
    await page.goto(pathToFileURL(resolve(rel)).href, { timeout: 8000 });
    for (const c of clicks) { try { await page.click(c, { timeout: 3000 }); await page.waitForTimeout(700); } catch {} }
    await page.waitForTimeout(500);
    await page.screenshot({ path: resolve(OUT, file) });
    cards.push({ name, file, ok: true });
  } catch (e) {
    cards.push({ name, file: null, ok: false, err: String(e).split("\n")[0] });
  }
  await page.close();
}

const grid = cards.map(c =>
  `<figure>${c.ok ? `<img src="${c.file}">` : `<div class="fail">FAILED<br>${c.err || ""}</div>`}<figcaption>${c.name}</figcaption></figure>`
).join("");
const html = `<!doctype html><meta charset="utf-8"><style>
  body{background:#0f1216;color:#e9ebee;font:13px system-ui,sans-serif;margin:16px;}
  h1{font:600 18px Georgia,serif;}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
  figure{margin:0;border:1px solid #2a2f38;border-radius:8px;overflow:hidden;background:#171b21;}
  img{width:100%;display:block;}
  .fail{padding:40px 12px;color:#fc6255;text-align:center;}
  figcaption{padding:6px 8px;color:#98a2b0;font:12px ui-monospace,Consolas,monospace;}
</style><h1>Essence of Agents - contact sheet (${cards.filter(c=>c.ok).length}/${cards.length} ok)</h1>
<div class="grid">${grid}</div>`;
const indexPath = resolve(OUT, "index.html");
writeFileSync(indexPath, html);

const sheet = await browser.newPage({ viewport: { width: 1200, height: 900 } });
await sheet.goto(pathToFileURL(indexPath).href);
await sheet.waitForTimeout(600);
await sheet.screenshot({ path: resolve(OUT, "_contact.png"), fullPage: true });
await browser.close();

const bad = cards.filter(c => !c.ok);
console.log(`gallery: ${cards.length - bad.length}/${cards.length} ok -> tools/gallery/_contact.png`);
if (bad.length) console.log("FAILED:", bad.map(b => b.name).join(", "));

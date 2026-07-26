const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch(); const page = await b.newPage();
  const errors = []; page.on("pageerror", e => errors.push(String(e)));
  await page.goto("http://localhost:8123/episode1.html");
  await page.waitForFunction(() => typeof sceneStageDuo === "function" && typeof SCENES !== "undefined", null, { timeout: 15000 });
  const trace = await page.evaluate(() => {
    sceneMode = true; activeScene = { id:"crimson_nova", duo:true, steps:SCENES.crimson_nova.steps };
    _duoSlots=[null,null]; _lastCrew=null; present=[]; exprOf={}; castEl.classList.add("duo");
    const out = [];
    for (const s of SCENES.crimson_nova.steps) {
      if (s.who === undefined) continue;
      sceneStageDuo(s.who);
      out.push({ who: s.who, present: present.slice() });
    }
    return out;
  });
  // invariants
  let ok = true, prevCrew = null, fails = [];
  for (const e of trace) {
    const crew = e.present.filter(p => p !== "Crimson");
    if (e.present[e.present.length-1] !== "Crimson") { ok=false; fails.push("Crimson not rightmost @ "+e.who); }
    if (e.present.filter(p=>p==="Crimson").length !== 1) { ok=false; fails.push("Crimson not exactly once @ "+e.who); }
    if (crew.length > 2) { ok=false; fails.push(">2 crew @ "+e.who+": "+crew.join(",")); }
    if (e.who !== "Crimson" && !e.present.includes(e.who)) { ok=false; fails.push("speaker not staged @ "+e.who); }
    if (e.who !== "Crimson" && e.who !== prevCrew && prevCrew && !e.present.includes(prevCrew)) { ok=false; fails.push("prev crew "+prevCrew+" dropped when "+e.who+" spoke"); }
    if (e.who !== "Crimson") prevCrew = e.who;
  }
  console.log("first 8:", JSON.stringify(trace.slice(0,8)));
  console.log("sample mid:", JSON.stringify(trace.slice(20,26)));
  console.log("fails:", fails.slice(0,6));
  console.log("errors:", errors);
  console.log(ok && errors.length===0 ? "PASS" : "FAIL");
  await b.close();
  process.exit(ok && errors.length===0 ? 0 : 1);
})();

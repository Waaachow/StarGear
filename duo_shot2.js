const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1366, height: 768 } });
  await page.goto("http://localhost:8123/episode1.html");
  await page.waitForFunction(() => typeof startScene === "function", null, { timeout: 15000 });
  await page.evaluate(() => { startOverlay.classList.add("hidden"); document.getElementById("fadeBlack").classList.remove("on"); started=true; startScene("crimson_nova"); });
  await page.waitForTimeout(1000);
  // advance to the Kael/Rex exchange (two crew on the left)
  for (let i=0;i<21;i++){ await page.evaluate(()=>advance()); await page.waitForTimeout(230); }
  await page.evaluate(()=>finishTyping && finishTyping());
  await page.waitForTimeout(150);
  const s = await page.evaluate(()=>({ present: present.slice(), name: nameplate.textContent, text: document.getElementById("text").textContent }));
  console.log(JSON.stringify(s));
  await page.screenshot({ path: "duo_stage2.png" });
  await b.close();
})();

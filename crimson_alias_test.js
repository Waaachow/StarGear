const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch(); const page = await b.newPage();
  const errs = []; page.on("pageerror", e => errs.push(String(e)));
  await page.goto("http://localhost:8123/episode1.html");
  await page.waitForFunction(() => typeof charFile === "function", null, { timeout: 15000 });
  const r = await page.evaluate(() => {
    const crimson = {
      "Eyes Closed Smile": charFile("Crimson","Eyes Closed Smile"),
      "Confident": charFile("Crimson","Confident"),
      "Humble Smile": charFile("Crimson","Humble Smile"),
      "Soft Smile": charFile("Crimson","Soft Smile"),
      "Grinning": charFile("Crimson","Grinning"),
      "Smile": charFile("Crimson","Smile"),
      "Professional": charFile("Crimson","Professional"),
      "Heroic": charFile("Crimson","Heroic"),
    };
    const crew = {   // must NOT regress
      "Astra|Soft Smile": charFile("Astra","Soft Smile"),
      "Voss|Smile": charFile("Voss","Smile"),
      "Rex|Grinning": charFile("Rex","Grinning"),
      "Tessa|Confident": charFile("Tessa","Confident"),
    };
    return { crimson, crew };
  });
  console.log(JSON.stringify(r, null, 2));
  // confirm every crimson fallback path actually serves 200
  const urls = Object.values(r.crimson);
  const codes = {};
  for (const u of urls) { const res = await page.request.get("http://localhost:8123/" + u); codes[u] = res.status(); }
  console.log("crimson fallback HTTP:", JSON.stringify(codes, null, 2));
  console.log("errs:", errs.filter(e => !/Failed to load resource/.test(e)));
  await b.close();
})();

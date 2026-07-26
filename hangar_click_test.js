const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1366, height: 900 } });
  const errors = [];
  page.on("pageerror", e => errors.push("page:" + e));
  await page.goto("http://localhost:8123/episode1.html?freeplay=1");
  // wait for the embedded iso to boot
  await page.waitForFunction(() => { const f = document.getElementById("gpFrame"); try { return typeof f.contentWindow.enterHangar === "function"; } catch(e){ return false; } }, null, { timeout: 20000 });
  const frame = page.frames().find(f => f.url().includes("iso_grid_prototype"));
  await frame.waitForFunction(() => typeof world !== "undefined" && typeof CRIMSON_HANGAR !== "undefined", null, { timeout: 20000 });
  frame.on("pageerror", e => errors.push("iso:" + e));
  const parentFreePlay = await page.evaluate(() => freePlay);

  // dismiss any first-flight tutorial, park the ship at the hangar, wait for the prompt
  const prep = await frame.evaluate(async () => {
    for (let i=0;i<20 && typeof closeTutorial==="function" && document.getElementById("tut") && document.getElementById("tut").classList.contains("show"); i++) closeTutorial();
    if (typeof setTipsOn==="function") setTipsOn(false); tutorialOpen=false;
    world.worldOriginX = CRIMSON_HANGAR.ax - CENTER; world.worldOriginY = CRIMSON_HANGAR.ay - CENTER;
    world.moving=false; world.lateral=null; dockedAt=null; hangarDeclined=false; hangarPrompt=null; sceneActive=false;
    await new Promise(r=>setTimeout(r,350));
    return { promptUp: !!hangarPrompt, hasYesRect: !!(_hangarPromptHit && _hangarPromptHit.yes), storyTarget: !!storyTarget };
  });
  console.log("parentFreePlay:", parentFreePlay, "| prep:", JSON.stringify(prep));

  // real click on the ENTER (Y) button
  await frame.evaluate(() => {
    const r = canvas.getBoundingClientRect(), b = _hangarPromptHit.yes;
    canvas.dispatchEvent(new MouseEvent("click", { clientX: r.left + b.x + b.w/2, clientY: r.top + b.y + b.h/2, bubbles: true }));
  });
  await page.waitForTimeout(400);
  const after = await page.evaluate(() => ({ sceneMode, sceneId: activeScene && activeScene.id, gameplayHidden: gameplay.classList.contains("hidden") }));
  const isoAfter = await frame.evaluate(() => ({ sceneActive }));
  console.log("afterClick parent:", JSON.stringify(after), "| iso:", JSON.stringify(isoAfter));
  await page.waitForTimeout(1100);
  const line = await page.evaluate(() => ({ name: nameplate.textContent, text: document.getElementById("text").textContent }));
  console.log("firstLine:", JSON.stringify(line));

  console.log("errors:", errors);
  const pass = errors.length===0 && parentFreePlay===true && prep.promptUp===true && prep.storyTarget===false
    && after.sceneMode===true && after.sceneId==="crimson_nova" && after.gameplayHidden===true && isoAfter.sceneActive===true;
  console.log(pass ? "PASS" : "FAIL");
  await browser.close();
  process.exit(pass?0:1);
})();

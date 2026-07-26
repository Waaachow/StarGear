const { chromium } = require("playwright");
async function bootIsoAndEnter(frame, page) {
  const prep = await frame.evaluate(async () => {
    for (let i=0;i<20 && typeof closeTutorial==="function" && document.getElementById("tut") && document.getElementById("tut").classList.contains("show"); i++) closeTutorial();
    if (typeof setTipsOn==="function") setTipsOn(false); tutorialOpen=false;
    world.worldOriginX = CRIMSON_HANGAR.ax - CENTER; world.worldOriginY = CRIMSON_HANGAR.ay - CENTER;
    world.moving=false; world.lateral=null; dockedAt=null; hangarDeclined=false; hangarPrompt=null; sceneActive=false;
    await new Promise(r=>setTimeout(r,350));
    return { promptUp: !!hangarPrompt, storyTarget: !!storyTarget, mission: MISSION_MODE };
  });
  await frame.evaluate(() => { const r = canvas.getBoundingClientRect(), b = _hangarPromptHit.yes;
    canvas.dispatchEvent(new MouseEvent("click", { clientX: r.left + b.x + b.w/2, clientY: r.top + b.y + b.h/2, bubbles: true })); });
  await page.waitForTimeout(400);
  return prep;
}
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1366, height: 900 } });
  const errors = []; page.on("pageerror", e => errors.push("page:"+e));

  // ---- STORY TRAVEL BEAT path ----
  await page.goto("http://localhost:8123/episode1.html");
  await page.waitForFunction(() => typeof runBeat === "function" && EP1[1] && EP1[1].type === "travel", null, { timeout: 15000 });
  const beatType = await page.evaluate(() => { startOverlay.classList.add("hidden"); document.getElementById("fadeBlack").classList.remove("on"); started=true; runBeat(1); return EP1[1].type; });
  await page.waitForFunction(() => { const f=document.getElementById("gpFrame"); try { return typeof f.contentWindow.enterHangar==="function"; } catch(e){ return false; } }, null, { timeout: 20000 });
  let frame = page.frames().find(f => f.url().includes("iso_grid_prototype"));
  await frame.waitForFunction(() => typeof CRIMSON_HANGAR !== "undefined", null, { timeout: 20000 });
  frame.on("pageerror", e => errors.push("iso:"+e));
  const freePlayDuringStory = await page.evaluate(() => freePlay);
  const prep1 = await bootIsoAndEnter(frame, page);
  const story = await page.evaluate(() => ({ sceneMode, sceneId: activeScene && activeScene.id, beatIdx, gameplayHidden: gameplay.classList.contains("hidden") }));
  // end scene → confirm story beat intact
  const resume = await page.evaluate(() => { endScene(); return { sceneMode, beatIdx, gameplayShown: !gameplay.classList.contains("hidden") }; });
  console.log("STORY: beatType=",beatType,"freePlay=",freePlayDuringStory,"prep=",JSON.stringify(prep1),"scene=",JSON.stringify(story),"resume=",JSON.stringify(resume));

  console.log("errors:", errors);
  const pass = errors.length===0 && beatType==="travel" && freePlayDuringStory===false
    && prep1.promptUp===true && prep1.storyTarget===true && prep1.mission===false
    && story.sceneMode===true && story.sceneId==="crimson_nova" && story.gameplayHidden===true && story.beatIdx===1
    && resume.sceneMode===false && resume.beatIdx===1 && resume.gameplayShown===true;
  console.log(pass ? "PASS" : "FAIL");
  await browser.close();
  process.exit(pass?0:1);
})();

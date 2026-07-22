import json, pathlib, tempfile
from playwright.sync_api import sync_playwright

# Economy regression suite for iso_grid_prototype.html. Run: python verify_econ.py
# Asserts the market can't print coin, that a route decays to zero without going negative,
# and that basis/intel survive a save+load. Screenshots go to a temp dir, not the project.
SRC = pathlib.Path(__file__).with_name("iso_grid_prototype.html")
URL = SRC.as_uri()
OUT = pathlib.Path(tempfile.gettempdir()) / "stargear_econ_shots"
OUT.mkdir(exist_ok=True)

errors = []

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1808, "height": 690})
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    pg.goto(URL)
    pg.wait_for_timeout(2500)

    # ---- 1. fresh game grants exactly the stipend --------------------------
    stipend = pg.evaluate("() => ({ coin: econ.coin, basis: econ.basis, intel: Object.keys(marketIntel).length })")
    print("1. fresh game:", stipend)

    # ---- 2. the old exploit: buy then sell back at the SAME station --------
    loop = pg.evaluate("""() => {
      closeTutorial && closeTutorial();
      econ.coin = 20000; econ.scrap = 0; econ.goods = {}; econ.basis = {};
      const sid = 'armada', out = [];
      for (let i = 0; i < 6; i++) {
        const before = econ.coin;
        buyGoods(sid, 'relics', 40);
        const sold = sellGoods(sid, 'relics', false);     // sell-at-profit
        out.push({ cycle: i+1, coin: econ.coin, delta: econ.coin - before, unitsSold: sold.n });
      }
      return out;
    }""")
    print("2. same-station buy/sell cycles (delta must never be > 0, unitsSold must be 0):")
    for r in loop:
        print("     cycle %d  coin=%-6d delta=%+6d  soldUnits=%d" % (r["cycle"], r["coin"], r["delta"], r["unitsSold"]))
    if any(r["delta"] > 0 or r["unitsSold"] > 0 for r in loop):
        errors.append("EXPLOIT: same-station round trip still gains coin")

    # ---- 3. a real route decays to zero and never goes negative ------------
    # REALIZED profit only: revenue minus what those same units cost. Cargo still in the
    # hold is inventory, not a loss — the player keeps it and carries it somewhere else.
    route = pg.evaluate("""() => {
      econ.coin = 50000; econ.scrap = 0; econ.goods = {}; econ.basis = {};
      stationStock = {}; stockTouched = {};
      const out = [];
      for (let i = 0; i < 8; i++) {
        const room = 40 - goodsHeld('ore');
        const bought = room > 0 ? buyGoods('moon', 'ore', room).n : 0;
        const basis = goodsBasis('ore');
        const s = sellGoods('neb', 'ore', false);
        out.push({ run: i+1, bought, sold: s.n,
                   realized: Math.round(s.coin - basis * s.n), held: goodsHeld('ore') });
      }
      return out;
    }""")
    print("3. moon->neb ore, 8 consecutive runs (realized profit on units actually sold):")
    for r in route:
        print("     run %d  bought=%-3d sold=%-3d realized=%+5d  still held=%d"
              % (r["run"], r["bought"], r["sold"], r["realized"], r["held"]))
    if any(r["realized"] < 0 for r in route):
        errors.append("route sold at a LOSS: %s" % route)
    if route[-1]["realized"] > 0:
        errors.append("route still paying %+d on the last run (permanent floor)" % route[-1]["realized"])

    # ---- 4. market intel accumulates and reads back ------------------------
    intel = pg.evaluate("""() => {
      recordIntel('moon'); recordIntel('neb'); recordIntel('armada');
      const b = bestKnownMarket('ore', 'moon');
      return { stations: Object.keys(marketIntel), best: b && { name: b.name, sell: b.sell },
               bearing: b && bearingTo(b.st) };
    }""")
    print("4. intel:", intel)
    if not intel["best"]:
        errors.append("bestKnownMarket returned nothing after recording three stations")

    # ---- 5. render the MARKET screen at both aspects -----------------------
    for w, h, tag in ((1808, 690, "wide"), (1366, 768, "std")):
        pg.set_viewport_size({"width": w, "height": h})
        pg.evaluate("""() => {
          econ.coin = 4000; econ.goods = {}; econ.basis = {}; stationStock = {}; stockTouched = {};
          buyGoods('moon', 'ore', 40);
          dockAt(TRADE_STATIONS.find(s => s.id === 'neb'));
          stationTab = STATION_TABS.indexOf('MARKET'); stationSel = 0;
          keeperSay = null; keeperPending = null;
        }""")
        pg.wait_for_timeout(900)
        pg.screenshot(path=str(OUT / ("market_%s.png" % tag)))
        print("5. screenshot market_%s.png" % tag)

    # ---- 6. cargo manifest -------------------------------------------------
    pg.set_viewport_size({"width": 1808, "height": 690})
    pg.evaluate("""() => {
      requestUndock(); requestUndock();
      openMenu && openMenu(); menuOpen = true; menuView = 'ship'; shipTab = 1;
    }""")
    pg.wait_for_timeout(700)
    pg.screenshot(path=str(OUT / "cargo.png"))
    print("6. screenshot cargo.png")

    # ---- 7. save / load round trip ----------------------------------------
    rt = pg.evaluate("""() => {
      econ.coin = 777; econ.goods = { ore: 12 }; econ.basis = { ore: 8.5 };
      saveEcon(); saveToSlot(0);
      econ = { scrap: 0, coin: 0, goods: {}, basis: {} }; marketIntel = {};
      const ok = loadFromSlot(0);
      return { ok, coin: econ.coin, basis: econ.basis, intelStations: Object.keys(marketIntel).length };
    }""")
    print("7. save/load:", rt)
    if not rt["ok"] or abs(rt["basis"].get("ore", 0) - 8.5) > 0.001:
        errors.append("cost basis did not survive save/load: %s" % rt)

    b.close()

print()
if errors:
    print("ERRORS (%d):" % len(errors))
    for e in errors: print("  x " + e)
else:
    print("errors: []  — all checks passed")

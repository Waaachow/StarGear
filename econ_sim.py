# Mirrors the iso_grid_prototype.html market model exactly (no browser needed).
# Run: python econ_sim.py   — asserts the three properties the economy must hold:
#   1. a same-station buy/sell round trip can never net coin (the spread kills it)
#   2. every profitable route decays to zero, never negative, never floors positive
#   3. sustained coin/min is comparable across all four commodities
# Keep these constants in step with the TRADE COMMODITIES block in the HTML.
import math

def rnd(x): return math.floor(x + 0.5)

PRICES = {
 "hub":    {"ore":1.00, "parts":1.00, "meds":1.00, "relics":1.00},
 "neb":    {"ore":1.35, "parts":1.15, "meds":1.30, "relics":0.65},
 "moon":   {"ore":0.60, "parts":0.80, "meds":1.35, "relics":1.25},
 "armada": {"ore":1.20, "parts":0.65, "meds":0.85, "relics":1.40},
}
BASE    = {"ore":12, "parts":30, "meds":55, "relics":90}
RESTOCK = {"ore":8, "parts":14, "meds":24, "relics":40}   # seconds per unit

SPREAD = 0.85
DEPTH  = 200
K      = 0.55
LO, HI = 0.55, 1.60
HOLD   = 40

def factor(st):
    return max(LO, min(HI, 1 - K * ((st - DEPTH) / DEPTH)))
def buyp(st, s, c):
    return max(1, rnd(BASE[c] * PRICES[s][c] * factor(st)))
def sellp(st, s, c):
    return max(1, rnd(buyp(st, s, c) * SPREAD))

# ---- property 1: same-station round trip -----------------------------------
def roundtrip(s, c, n=HOLD):
    """Buy n, then sell back under the cost-basis guard. Returns (sold, net)."""
    st = DEPTH; cost = 0; bought = 0
    while bought < n:
        cost += buyp(st, s, c); st -= 1; bought += 1
    basis = cost / bought
    earn = 0; sold = 0; carry = bought
    while carry > 0:
        p = sellp(st, s, c)
        if p < basis: break                     # sell-at-profit guard
        earn += p; st += 1; carry -= 1; sold += 1
    return sold, earn - cost, carry

# ---- property 2: route decay ------------------------------------------------
def route(bs, ss, c, runs=10):
    """A rational trader: only buys units it can currently sell at a profit."""
    stB = DEPTH; stS = DEPTH; out = []
    for _ in range(runs):
        # buy while the unit is worth carrying (destination price is visible via intel)
        n = 0; cost = 0
        while n < HOLD and stB > 0:
            bp = buyp(stB, bs, c)
            sp = sellp(stS + n, ss, c)          # price it will fetch as the nth unit sold
            if sp <= bp: break
            cost += bp; stB -= 1; n += 1
        earn = 0
        for _ in range(n):
            earn += sellp(stS, ss, c); stS += 1
        out.append(earn - cost)
    return out

# ---- property 3: sustainable rate ------------------------------------------
def sustained(c):
    """coin/min a route can emit long-run = restock rate x baseline margin."""
    best = 0
    for bs in PRICES:
        for ss in PRICES:
            if bs == ss: continue
            m = sellp(DEPTH, ss, c) - buyp(DEPTH, bs, c)
            best = max(best, m)
    return best, best * (60.0 / RESTOCK[c])

fails = []

print("=" * 74)
print("PROPERTY 1 — same-station round trip must sell 0 units and net < 0")
print("=" * 74)
for s in PRICES:
    cells = []
    for c in BASE:
        sold, net, carry = roundtrip(s, c)
        if sold != 0 or net >= 0:
            fails.append("roundtrip %s/%s sold=%d net=%+d" % (s, c, sold, net))
        cells.append("%-6s sold=%d" % (c, sold))
    print("  %-7s %s" % (s, "   ".join(cells)))

print()
print("=" * 74)
print("PROPERTY 2 — every profitable route decays to 0, never floors positive,")
print("             never goes negative")
print("=" * 74)
for c in BASE:
    for bs in PRICES:
        for ss in PRICES:
            if bs == ss: continue
            rr = route(bs, ss, c)
            if rr[0] <= 0: continue
            if min(rr) < 0:
                fails.append("route %s->%s %s went negative: %s" % (bs, ss, c, rr))
            if rr[-1] > 0:
                fails.append("route %s->%s %s still paying %+d on run 10" % (bs, ss, c, rr[-1]))
            print("  %-6s -> %-6s %-6s  %s" % (bs, ss, c, " ".join("%+5d" % p for p in rr)))

print()
print("=" * 74)
print("PROPERTY 3 — sustained coin/min per good should be within ~2x of each other")
print("=" * 74)
rates = {}
for c in BASE:
    m, r = sustained(c)
    rates[c] = r
    print("  %-7s best margin %+3d/unit   restock %2ds/unit   -> %5.0f coin/min" % (c, m, RESTOCK[c], r))
spread_ratio = max(rates.values()) / max(1e-9, min(rates.values()))
print("  ratio best/worst = %.2fx" % spread_ratio)
if spread_ratio > 2.5:
    fails.append("sustained rates spread %.2fx (>2.5x)" % spread_ratio)

print()
if fails:
    print("FAILURES (%d):" % len(fails))
    for f in fails: print("  x " + f)
else:
    print("ALL PROPERTIES HOLD")

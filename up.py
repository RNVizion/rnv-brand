#!/usr/bin/env python3
"""RNV-BRAND-BLUE — the register gains a second hue.

    python up.py             # apply, then run every check
    python up.py --check     # rehearse every edit in memory, write nothing

For rnv-brand, derived against a fresh clone at the live head.

RNV-DELIVERY-SCRIPT-DO-NOT-SWEEP. This script is a delivery tool, not register
source, and it names values it retires. That marker is what tells the fleet's
scanners to skip it.

WHAT LANDS.

  BRAND_BLUE       #6f94bc   dark-surface blue
  BRAND_DARK_BLUE  #456c91   light-surface blue

Both permanent, both resolvable, mixed in `paint` mode from the web violet, a
steel blue, brand gold and STATUS["success"], then placed at the status text
family's own two lightnesses.

WHY A PAIR. No single colour carries text on both of this brand's grounds.
4.5:1 on #1a1a1a needs relative luminance >= 0.221484; on #f5f5f5 it needs
<= 0.164022. The intervals do not meet, and the best any colour manages on
both at once is 3.9954:1. Arithmetic, not a search that gave up.

IT DOES NOT REACH THE APPLICATIONS OR THE WEBSITE. tokens() hardcodes the
names it emits rather than walking PERMANENT, so no new CSS token appears and
rnv-live's deploy is unaffected. All five applications' register-facing suites
were run against this register before the script was built: 393 passed.

FOUR CORRECTIONS TRAVEL WITH IT, all in BRAND_COLORS.md, all the same defect.
That file was publishing the RETIRED #b19145 as the current dark gold -- in
the apps-light usage line, the apps-dark shade line, the split paragraph, and
THE RESOLVER CONTRACT TABLE -- twenty-six days after rev 16 moved the value to
#8c7337. profile.json's own coupled_manual_work entry says to change the book
in the same commit as the source; this round is in that file, so it does.

A FIFTH IS A DIFFERENT SHAPE AND IS CORRECTED TOO. The split paragraph offered
"#b19145 appears zero times on rnvizion.dev" as evidence. That sentence became
UNFALSIFIABLE the day the value was retired -- a retired value appears zero
times everywhere. It was still true and had stopped meaning anything, which is
harder to see than being wrong.

AND THE PERMANENT COUNT. Its comment said "The six the brand commits to" while
the dict held seven, four lines above the comment announcing the seventh. It
now says nine and is spelled once.
"""
from __future__ import annotations

import argparse
import ast
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "rnv-brand"
SENTINEL_FILE = "engine/brand.py"
SENTINEL = "RNV-BRAND-BLUE"
GUARD = "engine/brand.py"
DESCRIPTION = "add BRAND_BLUE and BRAND_DARK_BLUE to the register"

SHADOWS = {"brand.py", "colors.py", "config.py", "conftest.py"}

#: rnv-brand has no pytest. Its guards run at import; see mk_blue.py.
GUARD_CMD = [sys.executable, "-c", "import engine.brand"]

VALUES = r"""
import engine.brand as b

assert b.BRAND_BLUE == "#6f94bc", b.BRAND_BLUE
assert b.BRAND_DARK_BLUE == "#456c91", b.BRAND_DARK_BLUE

# PERMANENT and RNV_BRAND are two lists of the same thing. _resolver_covers_
# permanent() already fails the import if one gains a member the other lacks;
# this asserts the members are the ONES THIS ROUND ADDED, which that guard
# cannot know.
assert b.PERMANENT["blue"] == b.BRAND_BLUE
assert b.PERMANENT["dark-blue"] == b.BRAND_DARK_BLUE
assert len(b.PERMANENT) == 9, len(b.PERMANENT)
for name in ("blue", "brand blue", "rnv blue"):
    assert b.RNV_BRAND[name] == b.BRAND_BLUE, name
for name in ("dark blue", "blue dark", "light-mode blue"):
    assert b.RNV_BRAND[name] == b.BRAND_DARK_BLUE, name

# The blue must NOT have leaked into the emitted token namespace. tokens()
# names what it emits rather than walking PERMANENT, and rnv-live rebuilds
# its stylesheet from this function on deploy -- so a colour arriving there
# silently is a change to the website that nobody asked for.
for surface in ("web", "app", "records"):
    leaked = [k for k, v in b.tokens(surface).items()
              if v in (b.BRAND_BLUE, b.BRAND_DARK_BLUE)]
    assert not leaked, (surface, leaked)

print("published values OK: 9 permanent, 6 resolver keys, 0 emitted tokens")
"""

BOOK = r"""
import pathlib, re

src = pathlib.Path("engine/brand.py").read_text(encoding="utf-8")
book = pathlib.Path("BRAND_COLORS.md").read_text(encoding="utf-8")

# "Nothing checks prose against prose" is written in this register's own
# profile.json. It is still true in general -- this closes it for the values
# this round touches, which is the only part it can honestly speak for.
#
# EVERY ASSERTION BELOW WAS TAMPERED WITH BEFORE THE SCRIPT WAS BUILT, and two
# of them did not fail. Both were the same shape -- "does this value appear
# anywhere in the document" -- which is true the moment the round writes a
# section mentioning it, however wrong the rest of the file is. What replaced
# them reads the ROW and the TABLE, so a typo in one cell is visible.

# THE REGISTER TABLE, checked by arithmetic rather than by eye. A row states a
# colour three ways -- name, hex, decimal triple -- and nothing has ever
# compared the last two. Eight rows today, all correct; the check exists so a
# ninth cannot arrive wrong.
ROW = re.compile(
    r"^\|([^|]+)\|\s*`(#[0-9a-f]{6})`\s*\|\s*(\d+),\s*(\d+),\s*(\d+)\s*\|", re.M)
rows = {}
for m in ROW.finditer(book):
    hexv = m.group(2).lstrip("#")
    want = tuple(int(hexv[i:i + 2], 16) for i in (0, 2, 4))
    got = tuple(int(m.group(i)) for i in (3, 4, 5))
    assert want == got, f"{m.group(1).strip()}: {m.group(2)} is {want}, book says {got}"
    rows[m.group(1).strip()] = m.group(2)

assert rows.get("Brand blue") == "#6f94bc", rows.get("Brand blue")
assert rows.get("Brand dark blue") == "#456c91", rows.get("Brand dark blue")
assert rows.get("Brand dark gold") == "#8c7337", rows.get("Brand dark gold")

for value in ("#6f94bc", "#456c91", "#8c7337"):
    assert value in src, f"{value} missing from engine/brand.py"

# The retired dark gold may be MENTIONED -- the changelog and the before/after
# table need it -- but never asserted as current. These four sentences did
# exactly that, and each one is checked by the claim it used to make.
for stale in (
    "the light theme's is `#b19145`",
    "shade and borders `#b19145`",
    "accent `#b19145` \u00b7 text",
    "| dark gold, gold dark, light-mode gold | `#b19145` |",
    "declared.** `#b19145` appears zero times on",
):
    assert stale not in book, f"BRAND_COLORS.md still asserts: {stale}"

# The resolver table is a CONTRACT. Every RNV_BRAND value must appear in it,
# or the document can omit a colour the server answers for -- which is how
# the dark-gold row went twenty-six days publishing a retired value while
# looking complete.
#
# BOUNDED TO THE TABLE'S OWN ROWS, not to a character count after the heading.
# The first version took 2000 characters and passed with a row DELETED, because
# the prose below the table happened to mention the value the row carried. A
# window wide enough to be safe is wide enough to answer the wrong question.
import sys
sys.path.insert(0, ".")
import engine.brand as b
after = book[book.index("## Resolver vocabulary"):].splitlines()
table = "\n".join(
    line for line in after[:60]
    if line.startswith("|")) or ""
missing = sorted({v for v in b.RNV_BRAND.values() if v not in table})
assert not missing, f"resolver table omits: {missing}"
assert table.count("\n") >= 9, f"resolver table has too few rows:\n{table}"

print("the book and the source agree on every value this round touches")
"""

SUITES = [("\"the published values\"", [sys.executable, "-c", VALUES]),
          ("\"the book against the source\"", [sys.executable, "-c", BOOK])]

EDITS = [('engine/brand.py', 'BRAND_BLACK = "#1a1a1a"  # brand black (charcoal)\n\n# ------------------------------------------------- the rest of the register\n', 'BRAND_BLACK = "#1a1a1a"  # brand black (charcoal)\n\n# ------------------------------------------------------------------- blue\n# RNV-BRAND-BLUE, 2026-09-12.\n# THE SECOND BRAND HUE, ruled 2026-09-12. Chris chose it; everything below is\n# measurement. It is the first colour in this register that is not gold, black\n# or white.\n#\n# HOW IT WAS MADE, and by what. Mixed through rnv-color-mcp\'s `mix_colors` in\n# `paint` mode -- Kubelka-Munk pigment physics, not a digital average -- from\n#\n#     2 parts  #b794ff   WEB["accent-violet"], a colour this register already\n#                        publishes, though see the note on its permanence below\n#     6 parts  #4682b4   CSS steelblue. The register had no blue; this is the\n#                        one ingredient brought in from outside\n#     1 part   #d2bc93   BRAND_GOLD\n#     2 parts  #926c89   STATUS["success"]\n#\n# giving #5c82a9, which is then placed at the two lightnesses below.\n#\n# `lab` MODE WAS TRIED FIRST AND IS RECORDED BECAUSE IT FAILED. An equal-weight\n# lab blend of the same four ingredients gives #968e9b -- a grey-mauve sitting\n# dE 2.5 from STATUS["success-text"] under deuteranopia, which is to say the\n# same colour. Averaging in a perceptual space moves toward the centroid and\n# the centroid of four hues is grey. Pigment mixing keeps the chroma. The\n# ingredient list did not change between those two results; only the model did.\n#\n# VIOLET ALONE WAS ALSO TRIED. accent-violet + gold + purple with no blue gives\n# #a885ae, dE 6.5 from STATUS["success-text"] -- too near the status purple to\n# separate from it. The blue is doing the work; the violet is why the blue has\n# a trace of red in it rather than reading as steel.\n#\n# THE PURPLE EARNS ITS PLACE, MEASURED. Without it the mix lands at a = -10.12\n# and dE 17.2 from success-text under deuteranopia; with it, a = -2.35 and dE\n# 19.4. It pushes b further negative, and b is the axis that SURVIVES\n# deuteranopia -- so the ingredient chosen on taste also improved the one\n# number a red-green viewer depends on. Recorded because the reverse was the\n# expectation.\n#\n# ------------------------------------------------------------------------\n# WHY THIS IS A PAIR AND NOT A VALUE. There is no single colour that carries\n# text on both of this brand\'s grounds, and that is arithmetic rather than a\n# search that gave up:\n#\n#     APP["panel"]           #1a1a1a   relative luminance 0.010330\n#     APP["surface-light-3"] #f5f5f5   relative luminance 0.913099\n#\n#     4.5:1 on the dark ground requires   Y >= 0.221484\n#     4.5:1 on the light ground requires  Y <= 0.164022\n#\n# The two intervals do not meet. Setting the two ratios equal gives\n# (Y + 0.05)^2 = 0.060330 * 0.963099, so the best ANY colour can do on both at\n# once is 3.9954:1 -- short of the floor, for every colour that exists. The\n# gold family already answers this with two values and so does STATUS; the blue\n# is the third family to do it, and the first to have the reason written down\n# here rather than rediscovered.\n#\n# THE PAIR IS ONE COLOUR AT TWO LIGHTNESSES, which is the family\'s own\n# construction rule read off the values that already shipped:\n#\n#     #ad85a3   L* 60.16   a 20.38   b -9.99    success-text\n#     #825d79   L* 44.17   a 19.97   b -9.77    success-text-light\n#\n# Same a, same b, L* moved by 16. The blue is built the same way: one hue,\n# placed at L* 60.06 and L* 44.28, holding hue to within 0.9 degrees. Asserted\n# at import by _blue_pair_holds_its_grounds() below, because a pair maintained\n# by remembering is a pair that drifts.\n#\n# ------------------------------------------------------------------------\n# COVERAGE, TRUNCATED NOT ROUNDED, and the failures are published with the\n# passes because a table that only lists what works is a permission slip.\n#\n#   BRAND_BLUE as TEXT, 4.5 floor\n#     on #000000  APP window        6.6380  pass\n#     on #0a0a0f  WEB_BLACK         6.2433  pass\n#     on #0a0a0a  APP canvas        6.2581  pass\n#     on #1a1a1a  APP panel         5.5014  pass   <- the job\n#     on #2a2a2a  APP card          4.5370  pass   <- the floor, and it is close\n#     on #3a3a3a  APP panel-hover   3.5954  FAIL\n#\n#   BRAND_DARK_BLUE as TEXT, 4.5 floor\n#     on #ffffff  WHITE             5.5162  pass\n#     on #fbfbfb  surface-light-2   5.3307  pass\n#     on #f5f5f5  surface-light-3   5.0597  pass   <- the job\n#     on #eeeeee  hover-light       4.7544  pass\n#     on #e8e8e8  ground floor      4.5020  pass   <- see the warning below\n#     on #e0e0e0  pressed-light     4.1787  FAIL\n#\n# THE #e8e8e8 FIGURE IS NOT A PERMISSION. It clears by 0.0020 -- two parts in\n# ten thousand, inside the byte grid\'s own resolution -- and this register has\n# already retired one value (#b19145) for resting a permission on a margin that\n# thin. GOLD_TEXT_GROUND_FLOOR is named for the gold family and stays that way;\n# the blue\'s guarded floor is APP["surface-light-3"], where it has room. Read\n# the 4.5020 as "it happens to reach" and never as "it is ruled to".\n#\n# AS A FILL, black reads 6.6380 on BRAND_BLUE and white 3.1635, so text on the\n# blue fill is BLACK in dark mode. On BRAND_DARK_BLUE white reads 5.5162 and\n# black 3.8069, so it is WHITE there. That is the opposite arrangement to the\n# golds, where black wins on both -- do not carry the gold rule across.\n#\n# ------------------------------------------------------------------------\n# IT IS PERMANENT BECAUSE THE BRAND ADOPTED IT, WHICH IS NOT THE SAME TRIGGER\n# AS A ROLE COLOUR. This register recorded on 2026-09-04 that the trigger for\n# registering a ROLE is a SECOND consumer, not a date. That rule is about\n# roles -- `running` as distinct from `succeeded` -- and it does not govern\n# here: a permanent colour is one the brand commits to, and gold did not wait\n# for a second consumer either. Stated so the next reader does not read this as\n# the rule being broken.\n#\n# AND IT IS NOT A PLATFORM BLUE. BRAND_COLORS.md excludes #0078d4 by name as a\n# platform convention. The distinction is not the hue, it is the provenance:\n# #0078d4 is Windows\' selection colour, adopted because it was there, and this\n# one is mixed from two colours this register already owns plus one ingredient\n# named above. A borrowed value and a derived one can sit a few degrees apart\n# on the wheel and still belong to different categories.\n#\n# #b794ff\'S OWN PERMANENCE IS STILL OPEN and this does not settle it.\n# BRAND_COLORS.md carries "open [confirm/fill]" against the two web secondary\n# accents. A mixture\'s ingredient does not inherit the mixture\'s status, and\n# nothing here should be read as having confirmed the violet by using it.\nBRAND_BLUE = "#6f94bc"       # dark-surface blue; text on panel and above\nBRAND_DARK_BLUE = "#456c91"  # light-surface blue -- darker BECAUSE the ground\n                             # is lighter, exactly as BRAND_DARK_GOLD is\n\n# ------------------------------------------------- the rest of the register\n', 1), ('engine/brand.py', '# The six the brand commits to. Gold on dark, dark gold on light; dark gold is\n# additionally gold\'s shade on dark, where full gold is too loud.\nPERMANENT = {\n    "gold": BRAND_GOLD,\n    "dark-gold": BRAND_DARK_GOLD,\n    # SEVENTH PERMANENT COLOUR, added 2026-08-23, and the first carrying a\n    # MEANING rather than a role. See BRAND_STILL_GOLD above for why it is\n    # registered and not derived.\n    "still-gold": BRAND_STILL_GOLD,\n    "charcoal": BRAND_BLACK,', '# The nine the brand commits to. Gold on dark, dark gold on light; dark gold is\n# additionally gold\'s shade on dark, where full gold is too loud. Blue on dark,\n# dark blue on light, by the same rule and for the same reason.\n#\n# THIS COMMENT SAID "six" UNTIL 2026-09-12 WHILE THE DICT HELD SEVEN. The\n# seventh was added on 2026-08-23 and announced itself in the comment three\n# lines below -- so the file both stated the count and corrected it, four lines\n# apart, for twenty days. Nothing compares a number written in prose to the\n# length of the thing it describes, which is the same gap as "nothing checks\n# prose against prose" and the reason the count is now spelled once.\nPERMANENT = {\n    "gold": BRAND_GOLD,\n    "dark-gold": BRAND_DARK_GOLD,\n    # SEVENTH PERMANENT COLOUR, added 2026-08-23, and the first carrying a\n    # MEANING rather than a role. See BRAND_STILL_GOLD above for why it is\n    # registered and not derived.\n    "still-gold": BRAND_STILL_GOLD,\n    # EIGHTH AND NINTH, added 2026-09-12 -- the first permanent colours that are\n    # not gold, black or white. They enter as a PAIR because no single value\n    # carries text on both grounds; see the derivation above BRAND_BLUE.\n    "blue": BRAND_BLUE,\n    "dark-blue": BRAND_DARK_BLUE,\n    "charcoal": BRAND_BLACK,', 1), ('engine/brand.py', '    "standby gold": BRAND_STANDBY_GOLD,\n    "standby-gold": BRAND_STANDBY_GOLD,\n    "black": TRUE_BLACK,', '    "standby gold": BRAND_STANDBY_GOLD,\n    "standby-gold": BRAND_STANDBY_GOLD,\n    # THE BLUE PAIR, 2026-09-12. Added in the SAME change that put them in\n    # PERMANENT, which is what _resolver_covers_permanent() exists to insist\n    # on -- still-gold went a day unreachable because the two lists were\n    # updated separately, and the guard below is the whole reason that cannot\n    # happen twice.\n    #\n    # "light-mode blue" is spelled the way "light-mode gold" is, because the\n    # confusion is identical: the light-mode value is the DARKER one, and\n    # someone asking out loud will say "the light one" meaning the mode.\n    "blue": BRAND_BLUE,\n    "brand blue": BRAND_BLUE,\n    "rnv blue": BRAND_BLUE,\n    "dark blue": BRAND_DARK_BLUE,\n    "blue dark": BRAND_DARK_BLUE,\n    "light-mode blue": BRAND_DARK_BLUE,\n    "black": TRUE_BLACK,', 1), ('engine/brand.py', '_deep_gold_clears_its_floor()\n\n\ndef _resolver_covers_permanent():', '_deep_gold_clears_its_floor()\n\n\ndef _blue_pair_holds_its_grounds():\n    """The blue pair must clear 4.5:1 on its own ground, and stay ONE COLOUR.\n\n    TWO COUPLINGS, AND NEITHER SURVIVES BEING REMEMBERED. BRAND_BLUE is\n    defined as the value that carries text on APP["panel"]; BRAND_DARK_BLUE as\n    the value that carries it on APP["surface-light-3"]. Each is written in\n    terms of a ground that has moved before -- the light ladder moved twice in\n    one fortnight -- so a change at either end leaves a claim here that no\n    longer holds, with nothing to say so.\n\n    AND THE PAIR IS THE POINT. The two values are one hue placed at two\n    lightnesses; that is what makes them a pair rather than two blues. Hue is\n    held to within 1.0 degree (measured 0.9) and the lightness step to\n    16 +/- 1 (measured 15.78). Change one and the assertion fires, which is the\n    only way a relationship between two literals stays true.\n\n    THE FLOOR IS surface-light-3 AND NOT GOLD_TEXT_GROUND_FLOOR. The blue\n    reaches #e8e8e8 at 4.5020, a margin of two parts in ten thousand. This\n    register retired #b19145 for exactly that -- a permission resting on a\n    figure too close to its threshold to be real -- so the margin is recorded\n    beside the value and is not guarded as though it were a rule.\n    """\n    def _lum(hexv):\n        c = [int(hexv.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]\n        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]\n        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]\n\n    def _cr(a, b):\n        la, lb = _lum(a), _lum(b)\n        hi, lo = max(la, lb), min(la, lb)\n        return (hi + 0.05) / (lo + 0.05)\n\n    def _lab(hexv):\n        import math\n        c = [int(hexv.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]\n        c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]\n        m = ((0.4124564, 0.3575761, 0.1804375),\n             (0.2126729, 0.7151522, 0.0721750),\n             (0.0193339, 0.1191920, 0.9503041))\n        xyz = [sum(row[i] * v for i, v in enumerate(c)) for row in m]\n        f = []\n        for v, w in zip(xyz, (0.95047, 1.0, 1.08883)):\n            v /= w\n            f.append(v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116)\n        return (116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2]))\n\n    for value, ground, name, gname in (\n            (BRAND_BLUE, APP["panel"], "BRAND_BLUE", \'APP["panel"]\'),\n            (BRAND_DARK_BLUE, APP["surface-light-3"], "BRAND_DARK_BLUE",\n             \'APP["surface-light-3"]\')):\n        ratio = _cr(value, ground)\n        if ratio < 4.5:\n            raise AssertionError(\n                f"{name} {value} reads {ratio:.4f} on {gname} {ground}, under "\n                f"the 4.5 text floor. One of the two moved without the other. "\n                f"The blue is DEFINED as the value that carries text on this "\n                f"ground, so if the ground moved, re-walk the value; if the "\n                f"value moved, say here what it is for now."\n            )\n\n    import math\n    la, aa, ba = _lab(BRAND_BLUE)\n    lb, ab, bb = _lab(BRAND_DARK_BLUE)\n    hue = abs((math.degrees(math.atan2(ba, aa))\n               - math.degrees(math.atan2(bb, ab)) + 180) % 360 - 180)\n    if hue > 1.0:\n        raise AssertionError(\n            f"BRAND_BLUE and BRAND_DARK_BLUE are {hue:.2f} degrees apart in "\n            f"hue, over the 1.0 ceiling. They are meant to be ONE colour at "\n            f"two lightnesses -- the mode picks which, and a viewer moving "\n            f"between modes should see the same blue get darker, not a "\n            f"different blue. Re-place the light value on the dark one\'s hue."\n        )\n    step = la - lb\n    if not 15.0 <= step <= 17.0:\n        raise AssertionError(\n            f"BRAND_BLUE sits {step:.2f} L* above BRAND_DARK_BLUE, outside the "\n            f"16 +/- 1 the status text family uses between its own pairs. The "\n            f"step is the family\'s, not this colour\'s; if it needs to change, "\n            f"change it for the family and say so here."\n        )\n\n\n_blue_pair_holds_its_grounds()\n\n\ndef _resolver_covers_permanent():', 1), ('BRAND_COLORS.md', 'Last locked: 2026-09-04 (rev 31 — ', 'Last locked: 2026-09-12 (rev 32 — **the register gains a second hue.** `BRAND_BLUE` `#6f94bc`\nand `BRAND_DARK_BLUE` `#456c91` are permanent, mixed in `paint` mode from the web violet, a steel\nblue, brand gold and `STATUS["success"]`, and placed at the status family\'s own two lightnesses.\n**They enter as a pair because no single value can carry text on both grounds** — 4.5:1 on\n`#1a1a1a` needs Y ≥ 0.221484 and on `#f5f5f5` needs Y ≤ 0.164022, and the best any colour manages\non both at once is 3.9954:1. **Four statements in this file were publishing the retired `#b19145`\nas current**, including the resolver contract table, and are corrected in the same change; the\nvalue moved in rev 16 and the prose did not follow. rev 31 — ', 1), ('BRAND_COLORS.md', "**The split is confirmed by the code, not just declared.** `#b19145` appears zero times on\nrnvizion.dev and zero times in the corpus Space — both all-dark surfaces, both gold-only.\nIn the apps, the dark theme's accent is `#d2bc93` and the light theme's is `#b19145`,\nwithout exception across all five.", '**The split is confirmed by the code, not just declared.** In the apps, the dark theme\'s accent\nis `#d2bc93` and the light theme\'s is `#8c7337`, without exception across all five; `#b19145`\nsurvives in them only inside the `RETIRED` tables that name it, which is mention and not use.\nNeither gold appears on rnvizion.dev\'s light surfaces because it has none — the site is all-dark\nand gold-only.\n\n**Corrected 2026-09-12 (rev 32).** This paragraph read `#b19145` as the apps\' current light accent\nfor twenty-six days after rev 16 moved the value, and offered "`#b19145` appears zero times on\nrnvizion.dev" as evidence for the split — a sentence that became **unfalsifiable** the moment the\nvalue was retired, since a retired value appears zero times everywhere. It was true and it had\nstopped meaning anything, which is harder to notice than being wrong.', 1), ('BRAND_COLORS.md', '### Black — the ground', '### Blue — the second hue, ruled 2026-09-12\n\n**There are two blues, for the same reason there are two golds.**\n\n| Color | Hex | RGB | Canonical use |\n|---|---|---|---|\n| Brand blue | `#6f94bc` | 111, 148, 188 | **On black and dark surfaces.** Carries text down to `#2a2a2a` |\n| Brand dark blue | `#456c91` | 69, 108, 145 | **On light surfaces.** Carries text down to `#eeeeee` |\n\n**It is mixed, not picked.** Through `rnv-color-mcp`\'s `mix_colors` in **`paint`** mode —\nKubelka-Munk pigment physics — from 2 parts `#b794ff` (the web violet), 6 parts CSS `steelblue`,\n1 part brand gold, 2 parts `STATUS["success"]`. That gives `#5c82a9`, which is then placed at\nL\\* 60.06 and L\\* 44.28 holding hue.\n\n**`lab` mode was tried first and failed, and the failure is the interesting half.** An equal-weight\n`lab` blend of the same four ingredients gives `#968e9b` — a grey-mauve sitting ΔE 2.5 from\n`success-text` under deuteranopia, which is to say the same colour. Averaging in a perceptual space\nwalks toward the centroid, and the centroid of four hues is grey. **The ingredient list did not\nchange between those two results; only the model did.**\n\n**The purple earns its place, measured.** Without it the mix lands at a = −10.12 and ΔE 17.2 from\n`success-text` under deuteranopia; with it, a = −2.35 and ΔE 19.4. It pushes b further negative,\nand b is the axis that *survives* deuteranopia — so the ingredient chosen on taste improved the one\nnumber a red-green viewer depends on. Recorded because the opposite was expected.\n\n**Why a pair and not a value.** 4.5:1 on `#1a1a1a` requires relative luminance ≥ 0.221484; on\n`#f5f5f5` it requires ≤ 0.164022. The intervals do not meet, and the best any single colour manages\non both at once is **3.9954:1**. This is arithmetic, not a search that gave up. The gold family and\n`STATUS` already answer it with two values each; the blue is the third, and the first to have the\nreason written down here rather than rediscovered.\n\n**Coverage, truncated not rounded, failures published with the passes:**\n\n| Usage | Floor | `#6f94bc` | `#456c91` |\n|---|---|---|---|\n| as text on `#000000` | 4.5 | 6.6380 | — |\n| as text on `#1a1a1a` (the job) | 4.5 | **5.5014** | — |\n| as text on `#2a2a2a` | 4.5 | 4.5370 | — |\n| as text on `#3a3a3a` | 4.5 | **3.5954 FAIL** | — |\n| as text on `#ffffff` | 4.5 | — | 5.5162 |\n| as text on `#f5f5f5` (the job) | 4.5 | — | **5.0597** |\n| as text on `#eeeeee` | 4.5 | — | 4.7544 |\n| as text on `#e8e8e8` | 4.5 | — | 4.5020 |\n| as text on `#e0e0e0` | 4.5 | — | **4.1787 FAIL** |\n| black on it, as a fill | 4.5 | 6.6380 | 3.8069 |\n| white on it, as a fill | 4.5 | 3.1635 | 5.5162 |\n\n**`4.5020` on `#e8e8e8` is not a permission.** It clears by two parts in ten thousand, inside the\nbyte grid\'s own resolution. This register retired `#b19145` for resting a permission on exactly\nthat kind of margin. `GOLD_TEXT_GROUND_FLOOR` stays named for the gold family; the blue\'s guarded\nfloor is `#f5f5f5`, where it has room.\n\n**Text on a blue fill is black in dark mode and white in light** — 6.6380 and 5.5162 respectively.\n**That is the opposite arrangement to the golds**, where black wins on both. Do not carry the gold\nrule across.\n\n**It is permanent because the brand adopted it.** The rule recorded on 2026-09-04 — that a *role*\ncolour is registered on a second consumer rather than a date — governs roles, not permanence. Gold\ndid not wait for a second consumer either. **And it is not a platform blue:** this file excludes\n`#0078d4` by name, and the distinction is provenance rather than hue. `#0078d4` is Windows\'\nselection colour, adopted because it was there; this one is mixed from colours the register already\nowns. Two values can sit a few degrees apart on the wheel and belong to different categories.\n\n**`#b794ff`\'s own permanence remains open** and this does not settle it — see "Canonical usage"\nbelow, which still carries `[confirm/fill]` against the two web secondary accents. A mixture\'s\ningredient does not inherit the mixture\'s status.\n\n### Black — the ground', 1), ('BRAND_COLORS.md', '**Apps, dark:** window `#000000` · raised `#1a1a1a` · card `#2a2a2a` · accent `#d2bc93` ·\nshade and borders `#b19145` · text on gold `#000000`, with neutral ramp steps between.\n\n**Apps, light:** ground and cards between `#f5f5f5` and `#ffffff` · accent `#b19145` · text\n`#000000` · text on gold `#000000`, with ramp steps between. Shipping in all five apps.', '**Apps, dark:** window `#000000` · raised `#1a1a1a` · card `#2a2a2a` · accent `#d2bc93` ·\nshade and borders `#8c7337` · text on gold `#000000`, with neutral ramp steps between.\n\n**Apps, light:** ground and cards between `#f5f5f5` and `#ffffff` · accent `#8c7337` · text\n`#000000` · text on gold `#000000`, with ramp steps between. Shipping in all five apps.\n\n*(Both lines said `#b19145` until 2026-09-12. The value was retired in rev 16 on 2026-08-17 and\nthis section was not swept with it.)*', 1), ('BRAND_COLORS.md', '| near-black, brand black, rnv black | `#1a1a1a` |\n| gold, brand gold, rnv gold | `#d2bc93` |\n| dark gold, gold dark, light-mode gold | `#b19145` |', "| near-black, near black, brand black, rnv black, charcoal | `#1a1a1a` |\n| gold, brand gold, rnv gold | `#d2bc93` |\n| dark gold, gold dark, light-mode gold | `#8c7337` |\n| blue, brand blue, rnv blue | `#6f94bc` |\n| dark blue, blue dark, light-mode blue | `#456c91` |\n| still gold, still-gold, stillness | `#9b907a` |\n| standby gold, standby-gold | `#ae986f` |\n| black, true black | `#000000` |\n| white, brand white | `#ffffff` |\n| web black | `#0a0a0f` |\n\n**This table published `#b19145` for the dark-gold row until 2026-09-12**, twenty-six days after\nrev 16 moved the value to `#8c7337`. The row is a *contract* — it states what the colour server\nanswers — so for that period the register's own document and the register's own source gave\ndifferent answers to `dark gold`. Nothing compared them. The table was also short by six rows\nagainst `RNV_BRAND`, which is why the omission of a whole colour would not have shown either;\nit is now complete, and completeness is what makes the next divergence visible.", 1), ('pyproject.toml', 'version = "31.0.0"          # the register revision, so `pip show` answers "which rev?"', 'version = "32.0.0"          # the register revision, so `pip show` answers "which rev?"', 1)]


def edits(tree) -> None:
    for rel, old, new, times in EDITS:
        tree.sub(rel, old, new, times)


def checks(tree) -> None:
    """Run against the in-memory tree, before anything reaches disk.

    THESE ARE NOT THE SUITES. The suites run the register after it is written
    and can only see what imports; these see the TEXT, which is where the
    prose defects live. A round that edits a document has to be able to check
    a document.
    """
    src = tree.read("engine/brand.py")
    book = tree.read("BRAND_COLORS.md")
    proj = tree.read("pyproject.toml")

    for name, value in (("BRAND_BLUE", "#6f94bc"),
                        ("BRAND_DARK_BLUE", "#456c91")):
        line = f'{name} = "{value}"'
        if line not in src:
            raise SystemExit(f"engine/brand.py: {line} did not land")

    if src.count("RNV-BRAND-BLUE") != 1:
        raise SystemExit("engine/brand.py: the sentinel must appear exactly once")

    # THE COUNT THE OLD COMMENT GOT WRONG, checked rather than written. Read
    # off the parsed dict, so the number in the prose above it is compared to
    # the length of the thing it describes -- which is precisely what nothing
    # did for twenty days.
    tree_ast = ast.parse(src)
    permanent = next(
        (n.value for n in ast.walk(tree_ast)
         if isinstance(n, ast.Assign) and len(n.targets) == 1
         and isinstance(n.targets[0], ast.Name)
         and n.targets[0].id == "PERMANENT"), None)
    if permanent is None or len(permanent.keys) != 9:
        raise SystemExit(
            f"PERMANENT holds "
            f"{0 if permanent is None else len(permanent.keys)} entries, not 9")
    if "# The nine the brand commits to" not in src:
        raise SystemExit("the PERMANENT comment still states the old count")

    # HEX IS LOWERCASE IN THIS FILE, WITHOUT EXCEPTION -- the register says so
    # at line 38 and says a case-sensitive comparison is what enforces it.
    for value in ("#6F94BC", "#456C91"):
        if value in src or value in book:
            raise SystemExit(f"{value} is capitalised; this register is lower")

    if 'version = "32.0.0"' not in proj:
        raise SystemExit("pyproject.toml: the register revision did not move")
    if "rev 32" not in book:
        raise SystemExit("BRAND_COLORS.md: no rev 32 entry")

    # The four sentences that asserted a retired value, and the fifth that had
    # stopped being falsifiable. Checked here rather than only in the suite so
    # --check reports them without writing anything.
    # EACH ENTRY CARRIES ENOUGH CONTEXT TO BE A USE RATHER THAN A MENTION,
    # and the last one is why that sentence is here at all. Written first as
    # the bare fragment "`#b19145` appears zero times on", it landed red on
    # the correction note that QUOTES the sentence it retires -- which is the
    # use/mention failure this programme has now hit sixteen times, the
    # sixteenth being in the checker written to catch the fifteenth. The fix
    # is never to loosen the rule; it is to match the claim, which begins
    # "declared.**", and not the quotation, which does not.
    for stale in ("the light theme's is `#b19145`",
                  "shade and borders `#b19145`",
                  "accent `#b19145` · text",
                  "| dark gold, gold dark, light-mode gold | `#b19145` |",
                  "declared.** `#b19145` appears zero times on"):
        if stale in book:
            raise SystemExit(f"BRAND_COLORS.md still asserts: {stale}")

    # And the mentions must SURVIVE. A sweep that rewrote #b19145 everywhere
    # would turn the changelog into "moved from #8c7337 to #8c7337" and the
    # before/after table into two identical columns -- the use/mention failure
    # this programme has now hit fifteen times, and the one a value-replacing
    # fix is most likely to commit.
    for mention in ("moved from `#b19145` to `#8c7337`",
                    "Was `#b19145` until 2026-08-17",
                    "| Usage | Floor | `#b19145` | `#8c7337` |"):
        if mention not in book:
            raise SystemExit(
                f"BRAND_COLORS.md lost a MENTION it needs: {mention}")

    print("checks: 9 permanent, both values lower-case, rev 32, "
          "4 stale claims gone, 3 mentions intact")


# ------------------------------------------------------------------ plumbing
def refuse_to_shadow() -> None:
    name = Path(__file__).name
    if name in SHADOWS:
        sys.exit(f"refusing to run as {name} -- it would shadow a module on "
                 f"sys.path. Rename to up.py and run again.")


class Tree:
    """Every edit lands here first. Disk is written only after all guards pass,
    so --check is a real rehearsal and a half-applied state is impossible."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.files: dict[str, str] = {}
        self.deleted: set[str] = set()

    def read(self, rel: str) -> str:
        if rel not in self.files:
            p = self.root / rel
            if not p.exists():
                raise SystemExit(f"missing file: {rel}")
            self.files[rel] = p.read_text(encoding="utf-8")
        return self.files[rel]

    def write(self, rel: str, text: str) -> None:
        self.files[rel] = text

    def delete(self, rel: str) -> None:
        """Mark a file for removal. Nothing leaves disk until flush().

        Added for the round that retired the last CI deselect: with no
        deselects left, tests/test_ci_deselects.py swept an empty set and
        would have passed over nothing. Its own failure message said to
        delete it in the commit that removed the last one, so the harness
        needed to be able to.
        """
        if not (self.root / rel).exists() and rel not in self.files:
            raise SystemExit(f"cannot delete {rel}: it is not in this checkout")
        self.files.pop(rel, None)
        self.deleted.add(rel)

    def sub(self, rel: str, old: str, new: str, times: int = 1) -> None:
        src = self.read(rel)
        found = src.count(old)
        if found != times:
            raise SystemExit(
                f"{rel}: expected {times} occurrence(s) of the anchor, found "
                f"{found}. The file moved; re-derive this edit before trusting "
                f"the script.")
        self.write(rel, src.replace(old, new, times))

    def flush(self) -> list[str]:
        """Compare and write BYTES, not decoded text.

        read_text('utf-8') here raised on a file that was not valid UTF-8 --
        which is precisely the file some scripts exist to fix. Bytes compare
        identically for everything else and cannot refuse to look."""
        touched = []
        for rel in sorted(self.deleted):
            p = self.root / rel
            if p.exists():
                p.unlink()
                touched.append(f"{rel} (deleted)")
        for rel, text in self.files.items():
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            data = text.encode("utf-8")
            if not p.exists() or p.read_bytes() != data:
                p.write_bytes(data)
                touched.append(rel)
        return touched


def _tail(out: str, lines: int = 40) -> str:
    text = out.strip()
    marker = "short test summary info"
    if marker in text:
        return text[max(0, text.rindex(marker) - 30):]
    return "\n".join(text.splitlines()[-lines:])


def _outcome(code: int, out: str) -> str:
    """"pass", "fail", "abort" or "env" -- only exit code 1 means a test failed.

    pytest exits 0 passed, 1 tests failed, 2 interrupted, 3 internal error,
    4 usage error, 5 nothing collected; a native abort arrives as 134 or -6.
    Treating every non-zero code as a failing assertion is how a tool reports
    a regression that never happened.
    """
    if code == 0:
        return "pass"
    if code in (-9, 137, -15, 143):
        return "killed"
    if code in (134, -6, 139, -11) or "Fatal Python error" in out:
        return "abort"
    if code == 1 and "INTERNALERROR" not in out:
        return "fail"
    return "env"


ENV_HELP = """\
THE ENVIRONMENT IS NOT READY. NO TEST DISAGREED WITH THIS CHANGE -- the run
did not get far enough to ask one.

PyQt6 needs system libraries a fresh container does not ship; the give-away is
`ImportError: libGL.so.1`. Install those, then the Python packages:

    sudo apt-get update
    sudo apt-get install -y libgl1 libegl1 libxkbcommon-x11-0 libdbus-1-3 \\
      libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \\
      libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-sync1 \\
      libxcb-xfixes0 libxcb-xkb1

    pip install -r requirements.txt -r tests/requirements-dev.txt
    python up.py --verify
"""

ABORT_HELP = """\
PYTHON ABORTED NATIVELY. That is not a failing assertion. On offscreen Linux
these suites can abort in Qt's thread teardown -- it surfaces during whatever
work is in flight and reads exactly like a regression in it.

Re-run:

    python up.py --verify

If it aborts every time on the same test, that is worth looking at. If it
comes and goes, this change is not involved.
"""


KILLED_HELP = """\
THE TEST PROCESS WAS KILLED FROM OUTSIDE. No test failed and nothing crashed --
something stopped the run, and on a small runner that is almost always the
out-of-memory killer arriving part way through a long Qt suite.

Re-run:

    python up.py --verify

If it keeps dying at roughly the same point, run the suite on its own so you
can watch it, and close anything else heavy first:

    QT_QPA_PLATFORM=offscreen python -m pytest tests/ -q
"""


def run(label: str, args: list[str]) -> tuple[int, str]:
    """Stream to a temp file rather than capture_output: a long Qt suite emits
    megabytes, and buffering that in memory can get the run killed, which looks
    exactly like a failure."""
    print(f"  {label} ...", flush=True)
    env = dict(os.environ)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8",
                                errors="replace") as fh:
        proc = subprocess.run(args, stdout=fh, stderr=subprocess.STDOUT, env=env)
        fh.seek(0)
        out = fh.read()
    return proc.returncode, out


def _step(label: str, args: list[str]) -> int:
    code, out = run(label, args)
    verdict = _outcome(code, out)
    print(_tail(out) if verdict != "pass"
          else "\n".join(out.strip().splitlines()[-3:]))
    if verdict == "env":
        print("\n" + ENV_HELP)
    elif verdict == "abort":
        print("\n" + ABORT_HELP)
    elif verdict == "killed":
        print("\n" + KILLED_HELP)
    elif verdict == "fail":
        print("\nFAILED -- the suite is not green. Nothing was reverted; "
              "`git diff` shows exactly what landed.")
    return code


def verify() -> int:
    # A script that changes the ENVIRONMENT its suites run in does it here,
    # not in checks(): checks() runs against the in-memory tree before
    # anything is on disk. The register pin is the case that needed it -- it
    # writes a dependency line and then runs tests that import what the line
    # declares, and DECLARING IS NOT INSTALLING.
    #
    # In verify() rather than apply() so that `--verify` gets it too; that is
    # the entry point someone uses to re-check a repository, and it has to
    # prepare the same environment.
    hook = globals().get("post_write")
    if hook is not None:
        hook()
        print()

    # GUARD_CMD is OPTIONAL and exists for a repository with no pytest. Every
    # round until 2026-09-12 ran inside one of the five applications, where a
    # guard is a test file; rnv-brand has no tests directory, no pytest
    # dependency, and a deliberate ZERO-IMPORT policy in engine/brand.py --
    # its own idiom is a function that runs AT IMPORT and raises. Installing
    # pytest there to satisfy this harness would change the shape of someone
    # else's repository to suit a tool, which is backwards. GUARD still names
    # the file that holds the check; GUARD_CMD says how to run it.
    guard_cmd = globals().get("GUARD_CMD") or [
        sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", GUARD]
    code = _step("guard", guard_cmd)
    if code != 0:
        return code
    for label, args in SUITES:
        code = _step(label, args)
        if code != 0:
            return code
    print("\nGreen.")
    return 0


def apply(check_only: bool) -> int:
    root = Path.cwd()
    if not (root / SENTINEL_FILE).exists():
        # A script whose sentinel file is created by an EARLIER script cannot
        # tell "wrong directory" from "prerequisite not run", and the default
        # message asserts the first while the second is more likely. Such a
        # script sets MISSING_HELP and says which one to run.
        raise SystemExit(globals().get("MISSING_HELP") or
                         f"run this from the root of a {REPO} checkout "
                         f"(no {SENTINEL_FILE} here)")
    if SENTINEL in (root / SENTINEL_FILE).read_text(encoding="utf-8"):
        raise SystemExit(f"already applied -- {SENTINEL!r} is present in "
                         f"{SENTINEL_FILE}")

    tree = Tree(root)
    edits(tree)
    # GUARD_SOURCE is OPTIONAL. Every round until 2026-09-12 installed a new
    # guard file, so the harness assumed one; the ramp-condense round adopts
    # three that already exist -- the mixer's SPLITS table and two RETIRED
    # tuples -- and adding a fourth rule for what they already watch is how a
    # suite grows checks that disagree. GUARD still names the file verify()
    # runs first; it just does not have to be a file this script wrote.
    source = globals().get("GUARD_SOURCE")
    if source is not None:
        tree.write(GUARD, source)
    checks(tree)

    if check_only:
        print("--check: every edit composes and every guard passes. "
              "Nothing written.")
        return 0

    touched = tree.flush()
    print("wrote: " + ", ".join(touched) + "\n")
    return verify()


def finish() -> None:
    me = Path(__file__).resolve()
    print(f"removing {me.name}")
    me.unlink()


def main() -> int:
    refuse_to_shadow()
    ap = argparse.ArgumentParser(description=DESCRIPTION)
    ap.add_argument("--check", action="store_true",
                    help="rehearse every edit in memory, write nothing")
    ap.add_argument("--verify", action="store_true",
                    help="run the suites only, change nothing")
    ap.add_argument("--finish", action="store_true", help="delete this script")
    args = ap.parse_args()
    if args.finish:
        finish()
        return 0
    if args.verify:
        return verify()
    return apply(args.check)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""BRAND_COLORS.md rev 13 -> rev 14.

Built against rnv-brand/BRAND_COLORS.md @ main, fetched 2026-08-14 (rev 13,
534 lines). Fails loudly if the base has moved. Run from repo root, and run it
AFTER both ring pushes land, since it states them.

Three facts moved under this file after rev 13:
  - the hero dot's fill went 8px -> 10px
  - the ring went 1px -> 0.75px on BOTH surfaces in one pass
  - the hero dot had been rendering as an ellipse at every viewport width,
    squeezed by flex, which nobody had noticed because everyone was looking at
    the colour rather than the proportions
"""
import pathlib

P = pathlib.Path("BRAND_COLORS.md")
s = P.read_text(encoding="utf-8")

EDITS = [
    (
        "with a 1px gold ring, identical in all states, so the ring signals nothing and is simply the\n"
        "component's chrome. It carries the WCAG 1.4.11 boundary \u2014 10.15:1 on the site's pill ground\n"
        "(`bg-2`), 10.68:1 on `rnv-live`'s (`bg`) \u2014 **at every frame**, because the fill breathes and the\n"
        "ring does not. That is what frees the fill to sit at 2.43:1. Remove the ring and\n"
        "every value in the set fails.",

        "with a **0.75px** gold ring, identical in all states and on both surfaces, so the ring signals\n"
        "nothing and is simply the component's chrome. It carries the WCAG 1.4.11 boundary **at every\n"
        "frame**, because the fill breathes and the ring does not. That is what frees the fill to sit\n"
        "at 2.43:1. Remove the ring and every value in the set fails.\n"
        "\n"
        "**The ring thinned from 1px to 0.75px on 2026-08-14, on both surfaces in one pass.**\n"
        "\n"
        "| Surface | Ground | Composited at 0.75 coverage | Boundary |\n"
        "|---|---|---|---|\n"
        "| `rnvizion.dev` hero | `bg-2` | `#a19174` | **6.09:1** |\n"
        "| `rnv-live` | `bg` | `#a08f72` | **6.27:1** |\n"
        "\n"
        "Sub-pixel spread antialiases rather than vanishing, and partial coverage costs contrast in\n"
        "proportion. Both clear the 3:1 UI floor by roughly 2x, down from 3.4x. **0.5px was rejected**\n"
        "at ~3.35:1 \u2014 a bare pass with no margin, on the one element carrying the boundary for a fill\n"
        "that cannot.\n"
        "\n"
        "**Both surfaces moved together, deliberately, and the reasoning is worth keeping.** Holding\n"
        "`rnv-live` at 1px was considered and rejected. It would have confined an unverified value to\n"
        "one surface, but at the cost of a divergence in the one property whose sameness is the stated\n"
        "justification for a sub-floor fill. **A tracked mismatch becomes intentional by age**, and one\n"
        "revert later is cheaper than a difference nobody remembers the reason for. The risk is\n"
        "symmetric either way; the revert is the same one-character change on each.\n"
        "\n"
        "**[confirm/fill] 0.75px is unverified below 3x, now on both surfaces.** Observed only on a 3x\n"
        "phone, where it renders 2.25 device pixels; a 1x display gets 0.75 and leans entirely on\n"
        "antialiasing. **If it reads absent rather than merely finer, revert both to 1px in one pass**\n"
        "\u2014 the fills at 2.43:1 and 2.56:1 cannot replace it. Resolve at the next desktop sighting.",
    ),
    (
        "Sizes are **not** matched and were not made to match: 8px on the site, 0.45rem on `rnv-live`.",

        "Sizes are **not** matched and were not made to match: 10px on the site (8px until 2026-08-14,\n"
        "grown by eye), 0.45rem on `rnv-live`. The two pills differ in type size and padding, so equal\n"
        "pixels would not read as equal marks. **Ring weight is matched and size is not**, which is not\n"
        "a contradiction: the ring is the element carrying the accessibility boundary and the thing\n"
        "the parity claim rests on, while the fill's diameter is tuned per surface by eye.\n"
        "\n"
        "**Both dots also gained `flex-shrink: 0` on 2026-08-14, and the reason is a defect worth\n"
        "recording.** The site's hero dot had been rendering as an **ellipse at every viewport width** \u2014\n"
        "measured at 5.6px wide by 10.4px tall against a specified 10 by 10. Its flex parent was\n"
        "squeezing it on the main axis while `align-items: center` held its height, and the 1px ring\n"
        "traced the distortion, which is why each size increase made the outline look heavier rather\n"
        "than better. It survived three passes of deliberate work on this component because every pass\n"
        "was about colour. **A component can be audited repeatedly on the axis someone is thinking\n"
        "about and stay broken on the one nobody is.**",
    ),
]

for i, (old, new) in enumerate(EDITS, 1):
    n = s.count(old)
    assert n == 1, f"edit {i}: expected 1 match, found {n}. Base has moved:\n{old[:90]}"
    s = s.replace(old, new)

OLD_H = "Last locked: 2026-08-14 (rev 13 \u2014 **third revision on this date; the sequence is in the rev"
NEW_H = (
    "Last locked: 2026-08-14 (rev 14 \u2014 the hero dot's fill grew to 10px and the ring thinned to\n"
    "0.75px on **both surfaces in one pass**, dropping the boundary from 10.15:1 to 6.09:1 on the\n"
    "site and 10.68:1 to 6.27:1 on `rnv-live`. Aligning rather than diverging was the call: ring\n"
    "sameness is the stated justification for a sub-floor fill, and a tracked mismatch becomes\n"
    "intentional by age. Carried as a `[confirm/fill]`, since the value is unverified below 3x. Also\n"
    "records a defect: the hero dot had been an ellipse at every viewport width, squeezed by flex,\n"
    "through three passes of work on this same component \u2014 every one of which was about colour.\n"
    "Rev 13 \u2014 **third revision on this date; the sequence is in the rev"
)
n = s.count(OLD_H)
assert n == 1, f"header: expected 1 match, found {n}"
s = s.replace(OLD_H, NEW_H)

assert "8px on the site," not in s, "stale size survives"
assert "with a 1px gold ring, identical in all states" not in s, "stale ring claim survives"
assert "rev 14" in s, "header not bumped"
assert s.count("[confirm/fill] 0.75px is unverified below 3x") == 1, "the open item did not land"
assert "identical in all states and on both surfaces" in s, "alignment not recorded"

P.write_text(s, encoding="utf-8")
print("BRAND_COLORS.md -> rev 14")

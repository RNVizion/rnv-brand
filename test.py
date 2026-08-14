#!/usr/bin/env python3
"""BRAND_COLORS.md rev 11 -> rev 12.

Built against rnv-brand/BRAND_COLORS.md @ main, fetched 2026-08-14 (rev 11,
470 lines, 25351 bytes). Fails loudly if the base has moved. Run from repo root.
Run it AFTER the two dot splits are pushed, not before -- rev 12 states them as
landed, and a doc that claims a landing ahead of the push is the security.txt
Policy: failure again.

Two edits:
  1. The ring clause. Rev 11 said the ring carries 1.4.11 "at 10.15:1, and
     3.35:1 at the breathe animation's dim end." The ring no longer animates,
     so there is no dim end for it. Leaving the number would leave a floor
     documented that nothing enforces and nothing needs.
  2. A landing paragraph for the split, and the reason the number in the
     keyframe survived its own justification.
"""
import pathlib

P = pathlib.Path("BRAND_COLORS.md")
s = P.read_text(encoding="utf-8")

EDITS = [
    # ------------------------------------------------------- 1. the ring clause
    (
        "**The ring is load-bearing.** Every signal dot is drawn with a 1px gold ring, identical in all\n"
        "states, so the ring signals nothing and is simply the component's chrome. It carries the WCAG\n"
        "1.4.11 boundary at 10.15:1, and 3.35:1 at the breathe animation's dim end. That is what frees the\n"
        "fill to be a deep wine at 2.37:1. Remove the ring and every value in the set fails.",
        "**The ring is load-bearing, and since 2026-08-14 it is also still.** Every signal dot is drawn\n"
        "with a 1px gold ring, identical in all states, so the ring signals nothing and is simply the\n"
        "component's chrome. It carries the WCAG 1.4.11 boundary \u2014 10.15:1 on the site's pill ground\n"
        "(`bg-2`), 10.68:1 on `rnv-live`'s (`bg`) \u2014 **at every frame**, because the fill breathes and the\n"
        "ring does not. That is what frees the fill to be a deep wine at 2.37:1. Remove the ring and\n"
        "every value in the set fails.\n"
        "\n"
        "**A dim-end figure used to live in this paragraph and is retired.** While the ring animated with\n"
        "the fill, the boundary was only as good as the animation's worst frame \u2014 3.35:1 at a 0.5 dip,\n"
        "2.57:1 at 0.4 \u2014 so the keyframe carried a floor. Splitting the fill onto a pseudo-element\n"
        "removed the coupling and the floor with it. **The number is gone rather than corrected**, which\n"
        "is the point: a constraint that stops applying should not be left standing as a figure someone\n"
        "later re-derives a rule from.",
    ),
    # --------------------------------------------------------- 2. landing record
    (
        "**Case is part of the value here, not formatting.**",
        "**The two dots were split on 2026-08-14, in one pass across both surfaces.** The ring moved to\n"
        "the element and the fill to its `::after`, so only the fill animates. It was done on both at\n"
        "once deliberately: *one recognisable mark across two mediums* is the stated justification for a\n"
        "fill sitting under the contrast floor, and a structural change to one dot and not the other\n"
        "would have quietly retired that justification while leaving the sentence in place.\n"
        "\n"
        "**The 0.5 dip survived the argument that produced it, and that is worth naming.** It was chosen\n"
        "as a floor \u2014 the shallowest dip the animated ring could take and still clear 3:1. The split\n"
        "retired the floor, and the value stayed, so it is now held for parity between the two surfaces\n"
        "and for nothing else. **A number that outlives its reason needs a new one recorded or it will\n"
        "be defended with the old one.** Change it on one surface and it must change on both.\n"
        "\n"
        "Sizes are **not** matched and were not made to match: 8px on the site, 0.45rem on `rnv-live`.\n"
        "The two pills differ in type size and padding, so equal pixels would not read as equal marks.\n"
        "\n"
        "**Case is part of the value here, not formatting.**",
    ),
]

for i, (old, new) in enumerate(EDITS, 1):
    n = s.count(old)
    assert n == 1, f"edit {i}: expected 1 match, found {n}. Base has moved:\n{old[:100]}"
    s = s.replace(old, new)

# header bump
OLD_H = "Last locked: 2026-08-14 (rev 11 \u2014 **rev 10's header was stale against its own body:** it read"
NEW_H = (
    "Last locked: 2026-08-14 (rev 12 \u2014 the signal dot's ring was decoupled from its fill on both\n"
    "surfaces, so the ring no longer dims and the dim-end contrast figure in the signal section is\n"
    "retired rather than corrected. Records the split as landed, and records that `breathe`'s 0.5 dip\n"
    "now stands on parity rather than on the accessibility floor that originally set it. Rev 11 \u2014\n"
    "**rev 10's header was stale against its own body:** it read"
)
n = s.count(OLD_H)
assert n == 1, f"header: expected 1 match, found {n}"
s = s.replace(OLD_H, NEW_H)

assert "3.35:1 at the breathe animation's dim end" not in s, "retired dim-end figure survives"
assert "rev 12" in s, "header not bumped"

P.write_text(s, encoding="utf-8")
print("BRAND_COLORS.md -> rev 12")

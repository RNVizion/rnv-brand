#!/usr/bin/env python3
"""BRAND_COLORS.md rev 12 -> rev 13.

Built against rnv-brand/BRAND_COLORS.md @ main, fetched 2026-08-14 (rev 12,
498 lines, 27448 bytes). Fails loudly if the base has moved. Run from repo root.

TWO JOBS, and they are opposite directions:

  LAND a value change. `signal-live` moved #8b2c3b -> #a5034e at the source on
  2026-08-14. Line 318 -- the sentence that STATES the value -- still carries
  the old one. Contrast on bg-2 moves 2.37:1 -> 2.43:1 with it.

  REVERT four mentions. A blind lowercase sweep and a hex swap ran over this
  file after rev 12 and hit exactly the sentences that are ABOUT hex case. The
  pass changed every MENTION of a value and left the one USE stale, which is
  the wrong half in both directions at once.

Restored: #FFC107 at lines 16, 290, 365 (each names the uppercase instance that
IS the hazard; lowercasing them deletes the referent), and the #8B2C3B/#8b2c3b
pair at 363 (the illustration compared one value in two cases; the swap made it
compare two different colours, so it demonstrated nothing).

NOT touched: #ffc107 at 276, 281 and 367. Those are uses, not mentions, and
lowercase is correct there. That distinction is the whole finding.

Also NOT touched: line 15, rev 11's own note that it normalised #8b2c3b. That
was true when written. A revision log records what happened, and editing it to
match the present is how an audit trail stops being one.
"""
import pathlib

P = pathlib.Path("BRAND_COLORS.md")
s = P.read_text(encoding="utf-8")

EDITS = [
    # -------------------------------------------------- 1. the value statement
    (
        "`#8b2c3b` live, `#5a5a72` offline, `#ffd166` down.",
        "`#a5034e` live, `#5a5a72` offline, `#ffd166` down.",
    ),
    # ------------------------------------- 2. the fill's ratio, and its name
    (
        "ring does not. That is what frees the fill to be a deep wine at 2.37:1. Remove the ring and",
        "ring does not. That is what frees the fill to sit at 2.43:1. Remove the ring and",
    ),
    # ------------------------------------------- 3. the case paragraph, restored
    (
        "**Case is part of the value here, not formatting.** `#8b2c3b` is lowercase in this file and\n"
        "must be lowercase at the source: a case-sensitive comparison reads `#a5034e` and `#8b2c3b` as\n"
        "two colors, which is precisely the failure recorded one section above about `rnv-icon-builder`\n"
        "and `#ffc107`. Naming a hazard and then committing it is how a house style stops being one.",
        "**Case is part of the value here, not formatting.** Hex is lowercase in this file and must be\n"
        "lowercase at the source: a case-sensitive comparison reads `#8B2C3B` and `#8b2c3b` as two\n"
        "colors, which is precisely the failure recorded one section above about `rnv-icon-builder` and\n"
        "`#FFC107`. Naming a hazard and then committing it is how a house style stops being one.\n"
        "\n"
        "**That pair is kept in its original case on purpose, and it was destroyed once already.** A\n"
        "blind pass ran over this file after rev 12 and replaced `#8B2C3B` here with `#a5034e`, leaving\n"
        "a sentence claiming a case-sensitive comparison reads two *different colours* as different \u2014\n"
        "which they are, so the example proved nothing. The same pass lowercased `#FFC107` in the three\n"
        "places that name it *as the uppercase instance*, and left line 318, the only place that\n"
        "actually stated a value, carrying a retired one.\n"
        "\n"
        "**The rule that failure earns: a mechanical pass must skip the sentences that are about the\n"
        "value being replaced.** A worked example, a \"do not write it this way,\" a before-and-after \u2014\n"
        "each is a *mention*, and a find-and-replace cannot tell a mention from a use, because in the\n"
        "text they are the same string. If a file explains a rule about a value's form, that file\n"
        "cannot be swept for that value; search it, read the hits, edit by hand. In this document\n"
        "`#ffc107` is lowercase wherever it is used and uppercase wherever a sentence names the\n"
        "uppercase instance as the fault. **No count of either is published here on purpose** \u2014 an\n"
        "occurrence count changes on every edit, and a figure that moves without a decision is the\n"
        "kind this file does not carry.",
    ),
    # --------------------------------------- 4. rev 11's header, referent back
    (
        "hazard this file already names about `#ffc107`. Retires the typography block (R3) \u2014 it was not",
        "hazard this file already names about `#FFC107`. Retires the typography block (R3) \u2014 it was not",
    ),
    # -------------------------------------- 5. the icon-builder sentence, back
    (
        "inconsistent before this ruling and nothing compared the two. `rnv-icon-builder` writes `#ffc107`\n"
        "in uppercase \u2014 the same value, but a case-sensitive comparison reads it as drift.",
        "inconsistent before this ruling and nothing compared the two. `rnv-icon-builder` writes `#FFC107`\n"
        "in uppercase \u2014 the same value, but a case-sensitive comparison reads it as drift.",
    ),
    # ------------------------------------------- 6. the value change, recorded
    (
        "**Signals are not status.** Status is the result of a user's action inside an app and moves when a",
        "**`signal-live` changed on 2026-08-14, from `#8b2c3b` to `#a5034e`.** Hue moved 350.5\u00b0 to 332.2\u00b0\n"
        "and saturation 52% to 96%. **It was decided on the check that mattered rather than on taste:** a\n"
        "move toward magenta could have narrowed the gap to the error red, which was always this value's\n"
        "nearest neighbour in the system, and instead widened it \u2014 CIEDE2000 18.22 against `#dc3545`\n"
        "where the retired value was 17.40. Against the dark-theme error text it reads 25.92. Contrast on\n"
        "`bg-2` moves 2.37:1 to 2.43:1, immaterial either way, because the ring carries the boundary and\n"
        "the fill was never asked to.\n"
        "\n"
        "**\"Wine\" describes the retired value and should not be carried forward.** At 96% saturation the\n"
        "current value is not the muted red that word implies, and `engine/brand.py` already uses \"wine\"\n"
        "for what it replaced. This file now says `signal-live` or gives the hex. A descriptor that\n"
        "survives the thing it described starts naming the wrong colour to everyone who reads it.\n"
        "\n"
        "**Signals are not status.** Status is the result of a user's action inside an app and moves when a",
    ),
]

for i, (old, new) in enumerate(EDITS, 1):
    n = s.count(old)
    assert n == 1, f"edit {i}: expected 1 match, found {n}. Base has moved:\n{old[:100]}"
    s = s.replace(old, new)

# ------------------------------------------------------------------ header bump
OLD_H = "Last locked: 2026-08-14 (rev 12 \u2014 the signal dot's ring was decoupled from its fill on both"
NEW_H = (
    "Last locked: 2026-08-14 (rev 13 \u2014 **third revision on this date; the sequence is in the rev\n"
    "number, not the stamp.** Lands `signal-live` at `#a5034e` and moves the fill's ratio to 2.43:1;\n"
    "retires \"wine\" as a descriptor for the current value. Repairs a blind pass that ran over rev 12\n"
    "and hit only the sentences that are *about* hex case: three mentions of `#FFC107` lowercased into\n"
    "meaninglessness, the `#8B2C3B`/`#8b2c3b` illustration replaced with two different colours, and the\n"
    "one line that actually stated a value left carrying a retired one. **A find-and-replace cannot\n"
    "tell a mention from a use.** Rev 12 \u2014 the signal dot's ring was decoupled from its fill on both"
)
n = s.count(OLD_H)
assert n == 1, f"header: expected 1 match, found {n}"
s = s.replace(OLD_H, NEW_H)

# ------------------------------------------------------------- post-conditions
assert s.count("`#a5034e` live") == 1, "value statement not landed"
assert "`#8b2c3b` live" not in s, "retired value still stated as current"
# The three mentions that must be uppercase, checked by their sentence rather than
# by a global count -- this rev adds prose that discusses them, and a count would
# be perturbed by the discussion. Checking the sentence is the point of the rev.
for frag in (
    "hazard this file already names about `#FFC107`",
    "`rnv-icon-builder` writes `#FFC107`\nin uppercase",
    "one section above about `rnv-icon-builder` and\n`#FFC107`",
):
    assert frag in s, f"uppercase mention not restored: {frag[:50]}"
assert "reads `#8B2C3B` and `#8b2c3b` as two" in s, "case illustration not restored"
# and no lowercase form may appear inside a clause asserting uppercase
assert "`#ffc107`\nin uppercase" not in s, "an uppercase claim still carries a lowercase referent"
assert "deep wine at 2.37:1" not in s, "stale ratio and descriptor survive"
assert "rev 13" in s, "header not bumped"

P.write_text(s, encoding="utf-8")
print("BRAND_COLORS.md -> rev 13")

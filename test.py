#!/usr/bin/env python3
"""BRAND_COLORS.md rev 10 -> rev 11.

Built against rnv-brand/BRAND_COLORS.md @ main, fetched 2026-08-14 (rev 10,
445 lines, 22994 bytes). Fails loudly if the base has moved. Run from repo root.

Four edits:
  1. rev header  -- rev 10's header said 2026-08-10 while carrying two sections
                    ruled 2026-08-13; the version field was lying about its own body.
  2. signal hex  -- #8B2C3B -> #8b2c3b, the only uppercase hex in engine/brand.py's
                    38 and one of two in this file. The doc names this exact hazard
                    two sections earlier, about #FFC107.
  3. signal note -- record that both surfaces have landed, so the "unfinished work"
                    reading of a #4ade80 sighting expires.
  4. typography  -- R3. The block stated three facts retired by Brand Book decision
                    #15 and F2. Replaced by a pointer, not a corrected restatement.
"""
import pathlib

P = pathlib.Path("BRAND_COLORS.md")
s = P.read_text(encoding="utf-8")

EDITS = [
    # ---------------------------------------------------------------- 1. header
    (
        "Last locked: 2026-08-10 (rev 10 \u2014 the two-dark rule re-derived from measurement after the",
        "Last locked: 2026-08-14 (rev 11 \u2014 **rev 10's header was stale against its own body:** it read\n"
        "2026-08-10 while carrying two sections ruled 2026-08-13, so this file's version field described\n"
        "a document that no longer existed. A dated header is the only thing that surfaces a stale-base\n"
        "clobber, and it cannot do that job while it is itself behind. Rev 11 closes the signal ruling:\n"
        "`rnvizion.dev` landed the change, so both surfaces are clean and `#4ade80` is gone from the\n"
        "ecosystem rather than merely retired at the source. Normalises `#8b2c3b` to lowercase, the case\n"
        "hazard this file already names about `#FFC107`. Retires the typography block (R3) \u2014 it was not\n"
        "merely redundant with Brand Book \u00a73.2, it stated three facts that \u00a73.2 had already retired.\n"
        "Rev 10 \u2014 the two-dark rule re-derived from measurement after the",
    ),
    # ------------------------------------------------------------- 2. hex case
    (
        "`#8B2C3B` live, `#5a5a72` offline, `#ffd166` down.",
        "`#8b2c3b` live, `#5a5a72` offline, `#ffd166` down.",
    ),
    # ---------------------------------------------------------- 3. landing note
    (
        "**One legibility note, app-level and not a brand matter:** `#ffc107` reads 1.63:1 on white and",
        "**Both surfaces have landed, 2026-08-14.** `rnv-live` took the set in the ruling change;\n"
        "`rnvizion.dev` followed on 2026-08-14, replacing the hero dot's fill and dropping its outer\n"
        "glow, since a ring plus a glow is two treatments doing one job and the ring is the one carrying\n"
        "contrast. `#4ade80` now appears in no RNVizion source. **The reading of a sighting changes with\n"
        "this:** while the change was outstanding, finding the hex meant unfinished work; finding it now\n"
        "means a surface has regressed or a new one was built from a stale base. `engine/brand.py`\n"
        "carries a comment stating the former \u2014 it expires with this line.\n"
        "\n"
        "**Case is part of the value here, not formatting.** `#8b2c3b` is lowercase in this file and\n"
        "must be lowercase at the source: a case-sensitive comparison reads `#8B2C3B` and `#8b2c3b` as\n"
        "two colors, which is precisely the failure recorded one section above about `rnv-icon-builder`\n"
        "and `#FFC107`. Naming a hazard and then committing it is how a house style stops being one.\n"
        "\n"
        "**One legibility note, app-level and not a brand matter:** `#ffc107` reads 1.63:1 on white and",
    ),
    # ------------------------------------------------------------ 4. typography
    (
        "## Typography (reference)\n"
        "\n"
        "- Display: Bricolage Grotesque\n"
        "- Serif (emphasis / italics): Instrument Serif\n"
        "- Mono (wordmark, labels, footer): JetBrains Mono\n"
        "- Body: Inter / system stack\n"
        "\n"
        "Social and OG-card typography is tracked separately.",
        "## Typography \u2014 not here\n"
        "\n"
        "**Brand Book \u00a73.2 owns type. This file owns color.** The reference list that stood here is\n"
        "retired rather than corrected, and the distinction matters: it was not a stale copy of a\n"
        "current fact, it was three retired ones. It gave the wordmark to JetBrains Mono, which\n"
        "decision #15 took away and gave to Montserrat Black; it wrote body as \"Inter / system stack,\"\n"
        "one phrase describing two different things, which F2 split; and it had no row for the mark\n"
        "face at all.\n"
        "\n"
        "**A convenience copy is a second canonical entry wearing a disclaimer.** \"(reference)\" did not\n"
        "stop this list from being read and followed, and two canonical entries that disagree are\n"
        "invisible to review \u2014 each reads coherently alone. The ownership table at the top of this file\n"
        "exists to prevent exactly this, and this block was the standing exception to it.",
    ),
]

for i, (old, new) in enumerate(EDITS, 1):
    n = s.count(old)
    assert n == 1, f"edit {i}: expected 1 match, found {n}. Base has moved:\n{old[:100]}"
    s = s.replace(old, new)

# post-conditions
# The uppercase form survives exactly once, on purpose: the case note quotes it as
# the wrong half of the comparison it is warning about. Anything else is a real one.
assert s.count("#8B2C3B") == 1, f"uppercase signal hex appears {s.count('#8B2C3B')}x, expected 1"
assert "reads `#8B2C3B` and `#8b2c3b` as" in s, "the one survivor is not the illustration"
assert "Mono (wordmark, labels, footer)" not in s, "the retired type claim survives"
assert "rev 11" in s, "header not bumped"

P.write_text(s, encoding="utf-8")
print("BRAND_COLORS.md -> rev 11")

#!/usr/bin/env python3
"""BRAND_TYPE.md rev 6 -> rev 7. Inline code, and what it took with it.

Built against rnv-brand/BRAND_TYPE.md @ main, fetched 2026-09-12 (rev 6, 491
lines). Fails loudly if the base has moved. Run from repo root.

WHAT PROMPTED IT: a draft post carries a styled inline code token, byte-identical
to _templates/post-template.html, documented in neither register. Decision #19's
shape -- a convention enforced by files agreeing and nothing else.

The token has NEVER RENDERED ON A LIVE PAGE. Checked across all six published
posts: none defines `article code` and none uses `<code>`. Only the template
does. A register entry for a treatment nobody has seen in context, which is the
cheapest moment to rule on it.

FIGURES VERIFIED INDEPENDENTLY rather than carried from the note that set them:
#00b0a0 reads 6.3277 on bg-3, 6.8974 on bg-2, 7.2588 on bg, and gold reads
9.3098 on the same chip. All four reproduce to four places.
"""
import pathlib

P = pathlib.Path("BRAND_TYPE.md")
s = P.read_text(encoding="utf-8")

assert "article code" not in s, "already documented"
assert "rev 6" in s, "expected rev 6 as the base"

OLD_ROW = ("| Labels, kickers, long form | JetBrains Mono | 400 / 500 / 600 / 700 | The tracked long "
           "form beneath a mark, uppercase tracked kickers, footers, captions |")
NEW_ROW = ("| Labels, kickers, long form | JetBrains Mono | 400 / 500 / 600 / 700 | The tracked long "
           "form beneath a mark, uppercase tracked kickers, footers, captions, **and inline code in "
           "prose \u2014 see below** |")
n = s.count(OLD_ROW)
assert n == 1, f"mono row: expected 1 match, found {n}. Base has moved."
s = s.replace(OLD_ROW, NEW_ROW)

SECTION = """## Inline code in prose

**Ruled 2026-09-12.** Inline `<code>` inside `article` is JetBrains Mono at `0.88em`, **web-code
teal `#00b0a0`**, on a `--bg-3` chip with 4px corners and `1px 6px` of padding. The rule lives in
`_templates/post-template.html` and is inherited by every post built from it.

**`0.88em` is a correction, not a shrink.** Mono carries a larger x-height than Inter at the same
point size, so setting it at parity makes code look bigger than the text around it. At 17px body
this computes to **14.96px \u2014 normal text** for WCAG, so the floor is 4.5 rather than 3.0. Written
down because the size is doing as much work as the colour: a couple of pixels larger and the
feasible region for the colour would have widened.

### The chip carries it. The border does not.

| | measured |
|---|---|
| chip against the page | **1.147:1** |
| border against the chip | **1.049:1** |

**Both are low ratios and only one of them is invisible.** Rendered at 4x against the real faces,
the chip reads plainly as a distinct object; the bordered and unbordered versions are
indistinguishable. **Remove the border.** It costs a declaration, reads as nothing, and looks
load-bearing to anyone reading the rule rather than the render.

**The rule that generalises, bought by getting this wrong first:**

> **A contrast ratio measures a relationship, not a visibility.** Area and stroke width change what
> a given ratio buys: a filled shape can read clearly at a ratio where a hairline of the same value
> disappears. A ratio decides whether a thing *passes*; only a render decides whether it *shows*.

This project computed both figures, called the box dead as a unit, and was half wrong in the half it
stated most confidently. **Measure to rule; render to see.**

### The chip costs AAA, and that is the trade

`#00b0a0` reads **7.2588** on the page and clears AAA; on its own chip it reads **6.3277** and does
not. **The chip buys separation and spends 0.93 of contrast for it.** Recorded because the binding
figure is the chipped one \u2014 inline code is always chipped, so `--bg-3` is the only ground it ever
sits on \u2014 and a later reader finding the unchipped figure could reasonably conclude AAA is met.

### Code left gold, and that is the shared-hue rule working

Until 2026-09-12 gold carried three jobs in prose, separated by face and weight rather than colour.
Code has taken its own hue, the strongest channel available, and gold is left with two:

| | weight | face | hue | box |
|---|---|---|---|---|
| `a` | 400 | Inter | gold | \u2014 |
| `strong` | 600 | Inter | gold | \u2014 |
| `code` | 400 | **JetBrains Mono** | **web-code** | chip |

> **Gold in body copy is a shared hue. Any element that takes it must declare which channel
> separates it \u2014 face, weight, or box \u2014 and that channel must be perceptible without colour.**

The rule did not stop code taking gold. It made the question askable, and the answer was to leave.
**`strong` now separates by weight alone**, which is thin but real, and it is the last element
sharing gold with links.

CIEDE2000 from `#00b0a0` at normal vision: **31.27** from gold, and clear of the whole signal set \u2014
the closest is stillness gold at 26.82. The binding figure is `engine/brand.py`'s worst-of-four
simulation, and it lives there rather than here.

---

## Open

**[confirm/fill] No surface consumes the value yet.** `article code` still sets
`color: var(--accent)`, and the site mirrors brand values into its own unprefixed `:root`, which
carries no code token at all. **The value is registered and the page is still painting code gold.**
Until the site mirrors it, everything above describes an intent rather than a surface.

**[confirm/fill] Prose links separate by colour alone and fail WCAG 1.4.1.** `article a` and `.bio a`
are gold at `text-decoration: none`, underlined on hover only \u2014 and hover does not exist on touch
and is absent while a page is being read. Colour-alone requires **3:1 against surrounding text**;
this is 1.517:1. Present in every post and in the template. The fix is a rest-state underline scoped
to prose links, leaving nav, footer and post-footer alone, since those are link regions rather than
links embedded in running text. Raised 2026-09-12; the change belongs to the site, not this register.

**[confirm/fill] The token has never rendered on a published page.** Verified across all six live
posts 2026-09-12: none defines `article code`, none uses `<code>`. Everything above is ruled from
measurement and specimens. Confirm against a real post the first time one ships with code in it.

---

"""

ANCHOR = "## The initiative-page exception"
n = s.count(ANCHOR)
assert n == 1, f"anchor: expected 1 match, found {n}. Base has moved."
s = s.replace(ANCHOR, SECTION + ANCHOR)

OLD_H = "Last locked: 2026-08-16 (rev 6 \u2014 **the coverage boundary rev 5 stated has moved, and a register"
NEW_H = (
    "Last locked: 2026-09-12 (rev 7 \u2014 **inline code is ruled, it has left gold, and a box nobody had\n"
    "looked at turns out to be half dead.** The token existed byte-identical in the post template and\n"
    "a draft and was documented nowhere \u2014 decision #19's shape, a convention enforced by files\n"
    "agreeing and nothing else. It has **never rendered on a live page.** The chip reads 1.147:1 and\n"
    "the border does not at 1.049:1, which is this rev's transferable half \u2014 **a contrast ratio\n"
    "measures a relationship, not a visibility**, and this project called the whole box dead from\n"
    "arithmetic before rendering it. Gold carried three jobs in prose; **the shared-hue rule made\n"
    "that askable and the answer was for code to leave**, taking `web-code` #00b0a0, so gold is down\n"
    "to links and `strong` separated by weight alone. Checking that turned up **prose links failing\n"
    "WCAG 1.4.1 at 1.517:1**, which predates the code token by months and surfaced only because a\n"
    "third gold role made someone ask how the roles separate. rev 6 \u2014 **the coverage boundary rev 5 "
    "stated has moved, and a register"
)
n = s.count(OLD_H)
assert n == 1, f"header: expected 1 match, found {n}"
s = s.replace(OLD_H, NEW_H)

assert s.count("## Inline code in prose") == 1, "section did not land"
assert "#00b0a0" in s, "the registered value did not land"
assert "rev 7" in s, "header not bumped"
# Scoped to the ruling section. The rev note above quotes the same two figures,
# which is correct -- a rev note records what that rev did and is historical, not
# a second canonical entry. A whole-file count would read the summary as one.
sec = s[s.index("## Inline code in prose"):s.index("## The initiative-page exception")]
assert sec.count("1.049:1") == 1 and sec.count("1.147:1") == 1, "figures duplicated inside the ruling"

P.write_text(s, encoding="utf-8")
print("BRAND_TYPE.md -> rev 7  (%d lines)" % len(s.splitlines()))

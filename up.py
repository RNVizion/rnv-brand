#!/usr/bin/env python3
"""BRAND_TYPE.md rev 7 -> rev 8. Close the consumption item; the site landed.

Built against rnv-brand/BRAND_TYPE.md @ main, fetched 2026-09-12 (rev 7, 585
lines). Fails loudly if the base has moved. Run from repo root.

Rev 7 recorded `[confirm/fill] No surface consumes the value yet`, which was true
when written and false within the hour. Verified on rnvizion.github.io@main with
cache-busting: the template carries `--code: #00b0a0`, `article code` sets
`color: var(--code)`, the border is gone from that rule, and the prose-link
underline is in the template and all six posts.

CLOSED WITH EVIDENCE AND ITS DATE KEPT, not deleted. The item recorded a real
gap that really existed for the hour between registration and mirroring -- and
that gap is the finding, not an embarrassment to tidy away. A value can be
registered, reasoned about at length, and painting nothing.

THE LINK ITEM MOVES FROM OPEN TO PARTLY CLOSED, and the remainder is named
rather than rounded off: bio/index.html (1 prose link) and aiii/index.html (2)
carry prose outside <article> and outside .bio, so the scoped selector does not
reach them. Two pages, three links, still failing 1.4.1.
"""
import pathlib

P = pathlib.Path("BRAND_TYPE.md")
s = P.read_text(encoding="utf-8")

assert "rev 7" in s, "expected rev 7 as the base"
assert "No surface consumes the value yet" in s, "the item is already closed"

# ------------------------------------------------ 1. the consumption item closes
OLD_1 = """**[confirm/fill] No surface consumes the value yet.** `article code` still sets
`color: var(--accent)`, and the site mirrors brand values into its own unprefixed `:root`, which
carries no code token at all. **The value is registered and the page is still painting code gold.**
Until the site mirrors it, everything above describes an intent rather than a surface."""
NEW_1 = """**CLOSED 2026-09-12 \u2014 the site mirrors the value.** Raised the same day, when `article code` still
set `color: var(--accent)` and the site's unprefixed `:root` carried no code token at all: the value
was registered, reasoned about at length, and painting nothing. Verified on
`rnvizion.github.io@main`: the template carries `--code: #00b0a0`, `article code` sets
`color: var(--code)`, the border is gone from that rule, and the prose-link underline reached the
template and all six posts.

**Kept with its date rather than deleted**, because the gap is the finding. **A value can be
registered, measured against forty-six others, argued through two revisions \u2014 and still be painting
nothing**, and nothing in either register would have said so. The interval was an hour here. It is
only ever an hour when somebody is watching."""
n = s.count(OLD_1)
assert n == 1, f"consumption item: expected 1 match, found {n}. Base has moved."
s = s.replace(OLD_1, NEW_1)

# ------------------------------------------- 2. the link item narrows to what is left
OLD_2 = """to prose links, leaving nav, footer and post-footer alone, since those are link regions rather than
links embedded in running text. Raised 2026-09-12; the change belongs to the site, not this register."""
NEW_2 = """to prose links, leaving nav, footer and post-footer alone, since those are link regions rather than
links embedded in running text.

**Partly closed 2026-09-12.** `article p a`, `article li a` and `.bio a` are underlined at rest in
the template and all six posts. **Two pages and three links remain**, named rather than rounded off:
`bio/index.html` carries one prose link and `aiii/index.html` two, both outside `<article>` and
outside `.bio`, so the scoped selector does not reach them. They need their own selectors and were
left rather than guessed at. `resume/`, `index.html` and `blog/index.html` have none \u2014 every link on
them sits in a region."""
n = s.count(OLD_2)
assert n == 1, f"link item: expected 1 match, found {n}. Base has moved."
s = s.replace(OLD_2, NEW_2)

# ------------------------------------------------------------------ 3. header
OLD_H = "Last locked: 2026-09-12 (rev 7 \u2014 **inline code is ruled, it has left gold, and a box nobody had"
NEW_H = (
    "Last locked: 2026-09-12 (rev 8 \u2014 **the consumption item closes within the hour it was opened, and\n"
    "the gap it recorded is worth more than the fix.** Rev 7 shipped saying no surface consumed\n"
    "`web-code`; the site mirrored it the same afternoon. Closed with evidence and its date kept,\n"
    "because **a value can be registered, measured against forty-six others and argued through two\n"
    "revisions while painting nothing** \u2014 and no register would have reported it. The prose-link item\n"
    "is **partly** closed: template and six posts underlined, **two pages and three links still\n"
    "failing 1.4.1**, named rather than rounded off. rev 7 \u2014 **inline code is ruled, it has left gold,\n"
    "and a box nobody had"
)
n = s.count(OLD_H)
assert n == 1, f"header: expected 1 match, found {n}"
s = s.replace(OLD_H, NEW_H)

assert "rev 8" in s, "header not bumped"
assert "No surface consumes the value yet" not in s, "stale item survives"
assert "Partly closed 2026-09-12" in s, "link item not narrowed"
# Checked by name, not by count. This file carries six other [confirm/fill]
# items in sections this rev never touches; a whole-file count measures the
# document when the claim is about two paragraphs. Seventh time this trap has
# fired here -- the habit is: never count against a whole file.
assert "The token has never rendered on a published page" in s, "third item lost"
assert "Prose links separate by colour alone" in s, "link item lost"

P.write_text(s, encoding="utf-8")
print("BRAND_TYPE.md -> rev 8  (%d lines)" % len(s.splitlines()))

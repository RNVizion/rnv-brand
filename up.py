#!/usr/bin/env python3
"""BRAND_TYPE.md rev 8 -> rev 9. Correct a count, and close the link item.

Built against rnv-brand/BRAND_TYPE.md @ main, fetched 2026-09-12 (rev 8, 606
lines). Fails loudly if the base has moved. Run from repo root.

Rev 8 recorded "two pages and three links remain", naming bio/index.html with
one prose link and aiii/index.html with two, both said to need their own
selectors. **Every part of that is wrong**, and it is wrong because of how it was
counted rather than because the pages moved.

  bio/index.html has FOUR prose links, not one, and needed NO new selector --
  its prose is inside <article>, exactly like every post, so the existing rule
  reaches it. It was simply absent from the file list.

  aiii/index.html needed NOTHING and never did. Its `.byline a` and
  `footer.foot a` carry `border-bottom: 1px solid var(--hair)` -- a non-colour
  cue at rest, which is what 1.4.1 asks for -- and it has no links inside
  <article> at all.

THE METHOD IS THE FINDING. The count came from a regex matching `<p...>`
followed immediately by `<a `, which cannot see a link that appears later in the
paragraph. It undercounted, and an undercount reports a smaller problem rather
than a broken method. The conclusion "needs its own selectors" was then drawn
from the bad count instead of from reading the page.
"""
import pathlib

P = pathlib.Path("BRAND_TYPE.md")
s = P.read_text(encoding="utf-8")

assert "rev 8" in s, "expected rev 8 as the base"
assert "Two pages and three links remain" in s, "the claim being corrected is not here"

OLD = """**Partly closed 2026-09-12.** `article p a`, `article li a` and `.bio a` are underlined at rest in
the template and all six posts. **Two pages and three links remain**, named rather than rounded off:
`bio/index.html` carries one prose link and `aiii/index.html` two, both outside `<article>` and
outside `.bio`, so the scoped selector does not reach them. They need their own selectors and were
left rather than guessed at. `resume/`, `index.html` and `blog/index.html` have none \u2014 every link on
them sits in a region."""

NEW = """**CLOSED 2026-09-12.** `article p a`, `article li a` and `.bio a` are underlined at rest in the
template, all six posts, and `bio/index.html`. Every link on `resume/`, `index.html` and
`blog/index.html` sits in a region, and `aiii/index.html` was never failing: its `.byline a` and
`footer.foot a` carry `border-bottom: 1px solid var(--hair)`, a non-colour cue at rest, and it holds
no links inside `<article>` at all.

**Rev 8 said something different and it was wrong in both directions.** It recorded *two pages and
three links remaining*, with `bio/index.html` at one prose link, `aiii/index.html` at two, and both
said to need their own selectors. `bio/index.html` has **four**, needed **no** new selector \u2014 its
prose is inside `<article>` like every post, so the existing rule reaches it, and the page was simply
absent from the file list. `aiii/` needed nothing.

**The method is the finding, not the number.** The count came from a pattern matching `<p...>`
followed immediately by `<a `, which cannot see a link appearing later in the same paragraph. Three
of bio's four sit mid-sentence and were invisible to it.

> **An enumeration that undercounts reports success, not failure.** A search that misses returns
> fewer hits, which looks exactly like a smaller problem \u2014 nothing in the output says the method
> was wrong. A guard that false-fails announces itself; a guard that false-passes does not.

**And the conclusion travelled further than the count.** "Needs its own selectors" was inferred from
the bad number rather than read off the page, so a wrong figure became a wrong plan, and the plan
read as though someone had looked. **Verify the consumer, not the declaration** applies to a count
as much as to a flag: the question was never *how many did the pattern find*, it was *what does the
page contain*."""

n = s.count(OLD)
assert n == 1, f"link item: expected 1 match, found {n}. Base has moved."
s = s.replace(OLD, NEW)

OLD_H = "Last locked: 2026-09-12 (rev 8 \u2014 **the consumption item closes within the hour it was opened, and"
NEW_H = (
    "Last locked: 2026-09-12 (rev 9 \u2014 **the prose-link item closes, and rev 8's count of what remained\n"
    "was wrong in both directions.** `bio/index.html` had four prose links rather than one and needed\n"
    "no new selector, its prose being inside `<article>` like every post; `aiii/index.html` was never\n"
    "failing at all, its links already carrying a `border-bottom` at rest. **The method is the\n"
    "finding:** the count came from a pattern that could not see a link appearing later in a\n"
    "paragraph, and **an enumeration that undercounts reports success rather than failure** \u2014 fewer\n"
    "hits look like a smaller problem, and nothing in the output says the method was wrong. The\n"
    "conclusion then travelled further than the count: *needs its own selectors* was inferred from a\n"
    "bad number instead of read off the page. rev 8 \u2014 **the consumption item closes within the hour "
    "it was opened, and"
)
n = s.count(OLD_H)
assert n == 1, f"header: expected 1 match, found {n}"
s = s.replace(OLD_H, NEW_H)

assert "rev 9" in s, "header not bumped"
assert "Two pages and three links remain" not in s, "the wrong claim survives"
assert "An enumeration that undercounts reports success" in s, "the rule did not land"
assert "The token has never rendered on a published page" in s, "the remaining open item was lost"

P.write_text(s, encoding="utf-8")
print("BRAND_TYPE.md -> rev 9  (%d lines)" % len(s.splitlines()))

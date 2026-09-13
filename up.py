#!/usr/bin/env python3
"""BRAND_TYPE.md rev 9 -> rev 10. The item rev 9 closed was not closed.

Built against rnv-brand/BRAND_TYPE.md @ main, fetched 2026-09-12 (rev 9, 633
lines). Fails loudly if the base has moved. Run from repo root.
Run AFTER fix.py has landed on the site, since this states it.

Rev 9 closed the prose-link item on a count of six posts. There are EIGHT.
honest-and-wrong and the-margin-not-the-price were live on main and had no rule.

  Rev 8 got it wrong by undercounting links with a bad pattern.
  Rev 9 corrected that, recorded a rule about it, and closed the item -- while
  undercounting POSTS from a hardcoded list built in August.

Two revisions in a row, two different enumerations, the same root. Rev 9's own
sentence applies to rev 9: an enumeration that undercounts reports success.
"""
import pathlib

P = pathlib.Path("BRAND_TYPE.md")
s = P.read_text(encoding="utf-8")

assert "rev 9" in s, "expected rev 9 as the base"
assert "**CLOSED 2026-09-12.** `article p a`" in s, "the closure being corrected is not here"

OLD = """**CLOSED 2026-09-12.** `article p a`, `article li a` and `.bio a` are underlined at rest in the
template, all six posts, and `bio/index.html`."""
NEW = """**CLOSED 2026-09-12, on the second attempt.** `article p a`, `article li a` and `.bio a` are
underlined at rest in the template, `bio/index.html`, and **all eight posts** \u2014 verified by globbing
`blog/*/index.html` rather than by consulting a list.

**Rev 9 closed this on a count of six, and there were eight.**
`blog/honest-and-wrong/` and `blog/the-margin-not-the-price/` were live on `main`, linked from the
blog index, and carried no rule. The pass that was supposed to reach every post carried a hardcoded
list built from a blog-index scrape in August; two posts shipped after it, and a list cannot know
that.

**This is the second consecutive revision to close this item on a bad enumeration, by a different
method each time.** Rev 8 undercounted *links* with a pattern that could not see past a tag. Rev 9
corrected that, wrote down the rule it earned, and then undercounted *posts* from a stale list \u2014 so
rev 9's own sentence applies to rev 9. Recording the rule did not prevent the next instance, because
the rule named the symptom and the habit had two forms.

> **A list of what exists is a snapshot, and it stops being true without changing.** A count can be
> re-derived and checked; a list cannot be distinguished from a correct one by looking at it.
> **Enumerate by walking the surface, and let the number be whatever it is** \u2014 which is Domain 1's
> standing rule, written in August about the nav dot and set aside a month later by the project that
> wrote it.

The fix walks. It reports the total it found before it edits anything, so a future gap shows up as a
number that moved rather than as silence."""

n = s.count(OLD)
assert n == 1, f"closure: expected 1 match, found {n}. Base has moved."
s = s.replace(OLD, NEW)

OLD_H = "Last locked: 2026-09-12 (rev 9 \u2014 **the prose-link item closes, and rev 8's count of what remained"
NEW_H = (
    "Last locked: 2026-09-12 (rev 10 \u2014 **rev 9 closed the prose-link item on a count of six posts and\n"
    "there are eight.** `honest-and-wrong` and `the-margin-not-the-price` were live and carried no\n"
    "rule; the pass that should have reached them used a hardcoded list built in August, and two posts\n"
    "shipped after it. **Second consecutive revision to close this item on a bad enumeration, by a\n"
    "different method each time** \u2014 rev 8 undercounted links with a blind pattern, rev 9 recorded the\n"
    "rule that earned and then undercounted posts from a stale list. **Recording a rule did not\n"
    "prevent the next instance, because the rule named the symptom and the habit had two forms.** The\n"
    "fix walks and reports its total before editing. Also retires a comment inside the code rule that\n"
    "still read *existing tokens only; no new colours or faces*, false since `--code` arrived in the\n"
    "very pass that left it standing. rev 9 \u2014 **the prose-link item closes, and rev 8's count of what "
    "remained"
)
n = s.count(OLD_H)
assert n == 1, f"header: expected 1 match, found {n}"
s = s.replace(OLD_H, NEW_H)

assert "rev 10" in s, "header not bumped"
assert "all eight posts" in s, "the corrected count did not land"
assert "A list of what exists is a snapshot" in s, "the rule did not land"
assert "The token has never rendered on a published page" in s, "the remaining open item was lost"

P.write_text(s, encoding="utf-8")
print("BRAND_TYPE.md -> rev 10  (%d lines)" % len(s.splitlines()))

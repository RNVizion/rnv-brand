# RNVizion Brand Type

The register of RNVizion's **type system**. Machine source: `engine/brand.py` (`TYPE`) —
import from there; never hardcode. This doc is the human-readable explanation.

Last locked: 2026-08-16 (rev 5 — **R2 is built, and it found this register's own worst case live on
a deployed surface.** `rnv-live` rendered the brand mark in JetBrains Mono at 700 with `0.02em` —
four revisions after decision #15 retired the wordmark from mono, on the one surface nothing had
ever read. Fixed to Montserrat 900 at `0.09em`, the nav value, because it is a nav mark by role.
**That fix was three files, not one**, and the coupling is recorded below. `verify_type` now guards
the mark across every HTML and `.astro` in the ecosystem, **with its coverage boundary stated: it
checks the face, not the weight or the tracking**, which are declared on the same rule. rev 4 — **three implementation facts the ruling did not carry, and one
figure this project published wrong.** The tracking helper is duplicated across all three
generators, so **a change to raster tracking is a three-file change**; per-glyph drawing discards
kerning, which widens the mark by a fraction of a pixel; and the measured width change is +13.0%
at 20px and +8.7% at 30px, not the single "12%" the handoff gave. That handoff also printed the
30px tracked width as 167px when it is 161px — **it applied the nav's `0.09em` to a row the ruling
puts at `0.06em`**, which is the inverse-idiom failure this very section warns about, committed in
the table demonstrating the ruling. Corrected below. rev 3 — **the raster surfaces are ruled and the tracking system is now
two systems, not two values.** The OG generators drew the mark at zero tracking while every web
surface tracked it, so the same wordmark had two letterforms depending on where it was seen.
Ruled: **raster is an absolute 1.8px gap; the web keeps its em values unchanged.** The reasoning is
below and it is the more useful half — an em value exists so tracking scales with type size, and a
raster mark has no type size to scale with. A constant absolute gap was considered for the web too
and rejected on measurement, not taste. rev 2 — **R1 is closed at the source and this register's mono row was
wrong.** `engine/brand.py`'s `TYPE` was reshaped from `role -> family` to `role -> {family,
weights}` and gained the `mark` role, so `--rnv-font-mark` is emittable for the first time and the
five roles below are five roles at the source. **The reshape was forced by this file:** a map of
role to family string cannot express "Montserrat *Black*" or F8's weight-axis standard, so both
rulings were unenforceable no matter how carefully they were written here. Rev 1's mono row said
400/500/600 while the shipped link requested four weights and the site draws 600 and 700 — ruled
below rather than routed, because this register is maintained by the project that runs the repo.
rev 1 — created because type had outgrown its section. Brand Book §3.2
and §3.3 had reached 11,368 characters against §3.1's 1,274, which is a register wearing a
section number rather than a summary. Four of the last five Brand Book decisions were type
decisions, and a parallel register had already formed on its own: the F-series prefixed its
items with `F` **specifically to avoid colliding with the Brand Book decision log**, which is
the system reporting that type needed a home and improvising one. That register retires here.
Brand Book §3.2/§3.3 were reduced to pointers **in the same change**, because a convenience
copy is a second canonical entry wearing a disclaimer — see the note on that under Who owns
what.)

---

## Who owns what

Three artifacts describe type, and two of them describing the same thing twice is the drift
this system exists to prevent. The split, so nothing is stated in two places:

| Artifact | Owns |
|---|---|
| **Brand Book §3.2 / §3.3** | The summary and the fact that a ruling exists. Points here; does not restate |
| **`BRAND_TYPE.md`** (this file) | The register, the rules, the exemptions, and the reasoning behind them |
| **`engine/brand.py`** (`TYPE`) | The values. Every consumer imports them from there |

**This mirrors the colour split deliberately, including the reason it exists.** `BRAND_COLORS.md`
carried a typography block for months as a "(reference)" convenience copy. Rev 14 retired it and
recorded why: it was not a stale copy of a current fact but **three retired ones at once** — it
gave the wordmark to JetBrains Mono after decision #15 took it away, wrote body as "Inter /
system stack" after F2 split that phrase, and had no row for the mark face at all. The label
"(reference)" did not stop it being read and followed.

**Two canonical entries that disagree are invisible to review, because each reads coherently
alone.** That is not a hypothetical here: decision #15 exists *because* §3.2's roles list and
§3.3's lockup template disagreed about the wordmark for five revisions, and neither review nor
re-reading caught it. **It was caught by building** — the card generator followed the roles
list, produced a mark that did not match the AIII lockup already shipping, and was corrected on
sight.

---

## What makes a face a brand face

A face is in this register when it is **shipped, versioned and controllable** — downloaded into
the repo or requested from a pinned font link, and drawable by both the web and raster pipelines.

**Fallback names are not brand faces.** `system-ui`, `-apple-system`, `Segoe UI`, `ui-monospace`,
`Georgia`, and the bare generics are what renders when a brand face does not arrive. They are
recorded where they appear because they describe the degraded state, not the intended one.

**Five faces are yours.** Bricolage Grotesque, Montserrat, Instrument Serif, JetBrains Mono, Inter.

---

## The register

| Role | Face | Weight / axis | Where it lives |
|---|---|---|---|
| **Mark** | **Montserrat** | **900 (Black)** | The RNVizion mark at every size and in every medium; initiative lockup letterforms; IG aphorism cards and carousels |
| Display | Bricolage Grotesque | variable, 300–800 | Site headings, blog titles, OG share titles, the name block on résumé cards |
| Emphasis | Instrument Serif | italic **and roman** | Pull lines, deks, the italicised signature phrases, the card back — **and the blog drop cap, which is roman** |
| Labels, kickers, long form | JetBrains Mono | 400 / 500 / 600 / 700 | The tracked long form beneath a mark, uppercase tracked kickers, footers, captions |
| Body | Inter | 400 / 500 / 600 | Running text |

**The JetBrains Mono row no longer claims wordmarks and no longer claims the nav.** It was
narrowed on 2026-08-11 when decision #15 gave the mark to Montserrat Black, then narrowed again
the same day when the nav ruling turned out to be global rather than size-scoped.

**The Emphasis row said italic and the face is drawn both ways.** Measured across the site
2026-08-15: twenty-four rules set `--font-serif` with `font-style: italic`; **eight draw
`article p:first-of-type::first-letter` — the blog drop cap — in roman**, with no italic in the
rule or either parent. The row understated the face's job by half of one axis, and the font link's
`ital@0;1` is therefore **correct** rather than an over-request. `TYPE` carries `ital: (0, 1)`.

**That evidence reversed a naming argument this project had already made in writing.** The source
key was `serif-italic`, the site's forty-four references say `--font-serif`, and the case for
moving the site was that `serif-italic` carried a ruling the shorter name would lose — the face is
only ever italic. **It is not**, and the longer name misdescribed a third of its own uses. The
source moved instead: one key here, one reference in `rnv-live`, and twelve site files untouched.

**The rule that survives the reversal, stated so the next collision does not turn on memory:**
prefer the name that carries more of the ruling — *and check that the ruling is true* before
deciding which name that is. Where the names carry the same, prefer the published surface. Both
collisions this week resolved the same direction once the artifact was read, and the ground ramp
got there faster only because nobody had a theory to defend.

**The mono row gained 700 on 2026-08-15, and rev 1 was wrong to omit it.** Traced from the
thirty-seven selectors that set `--font-mono`: weights **500, 600 and 700** are reachable from a
mono selector — 700 draws `code`, `.wordmark` and the close control; 600 draws list items; 500
draws buttons, kickers and two heading levels. The register claimed 400/500/600 while the shipped
font link requested `400;500;600;700`, so **the row understated by a weight that ships, and the
two have disagreed since the link was written.**

**400 stays in the request, marked unconfirmed rather than dropped. [confirm/fill]** No selector
reachable from `--font-mono` declares it, so it is either inherited from the body default or
requested and never drawn. F8 forbids requesting what is not drawn — but the failure modes are not
symmetric. An extra request costs bytes; a missing one **synthesises** the weight, which F8 forbids
outright and which fails silently. Confirm before removing.

**F8 was unenforceable in both directions until today.** The ruling says *request the weights
actually drawn and nothing synthesised*, and nothing could check it, because the source held
families and no weights at all. That is why `TYPE` was reshaped rather than merely extended.

**The body row was one phrase describing two things.** "Inter / system stack" read as a single
answer while nine pages ran Inter and the two highest-traffic pages — homepage and blog index —
ran a bare system stack with no brand face at any position. Ruled to Inter on 2026-08-11 (F2) and
verified on `main`. **Running text is a bigger visible surface than the mark**: the mark is eight
characters of nav; this was every paragraph on the two pages most people see first.

---

## The mark

**Montserrat Black, gold on dark. Ruled 2026-08-11, founder-confirmed, Brand Book decision #15.**

**The ruling is global.** There is no size-scoped exception. A size-scoped reading was offered and
not taken; recorded plainly, because a rule with a quiet exception in it is what produced the
original contradiction.

**The string is `RNVizion`, in that casing, on every surface.** `RNVIZION` is not the spelled-out
long form and never was — the long form is *Research N' Vizion*. The two were confused because
tracked mono uppercase is also the house kicker treatment and they look alike at small size. One
raster generator drew `" ".join("RNVIZION")` for months on that confusion.

### Tracking is two systems, because the media differ

**Web — relative, unchanged.**

| Size | Tracking | Gap | Proven on |
|---|---|---|---|
| 14px (nav) | **`0.09em`** | 1.26px | ten nav pages + the post template |
| Display | **`0.06em`** | 2.06px at 2.15rem | `/card/` on screen and 25pt in print |

**Raster — absolute, ruled 2026-08-15.** Every generated mark carries a **1.8px** gap.

| Generator | Mark size | Expressed as | Gap |
|---|---|---|---|
| `generate_site_og.py` | 20px | `0.09em` | 1.80px |
| `generate_og.py` | 30px | `0.06em` | 1.80px |
| `generate_project_card.py` | 30px | `0.06em` | 1.80px |

**All three drew the mark at zero tracking until this ruling**, while every web surface tracked it.
The same wordmark had two letterforms depending on where it was seen, and the OG image is the
highest-reach artifact in the system — it renders in every link preview.

**WHY RASTER IS RULED IN PIXELS AND THE WEB IS NOT.** An `em` value exists so tracking scales with
type size. On the web that is right: type resizes, reflows, and responds to a root font size. **A
raster mark has no type size to scale with** — the generator fixes it, and the image renders at
that one size forever. So the thing to rule for raster is the optical gap itself; the em value is
only how each generator expresses it. That both expressions land on values already ruled for the
web is confirmation, not the reason.

**MEASURED WIDTHS, because the mark gets wider and the figure was published wrong once.**

| Mark size | Untracked | At 1.8px | Change |
|---|---|---|---|
| 20px | 98.6px | **111.4px** | **+13.0%** |
| 30px | 147.8px | **160.7px** | **+8.7%** |

The change differs by size because the gap is constant while the word is not — seven gaps of 1.8px
is a larger fraction of a 99px word than of a 148px one. **A single averaged figure hides that**,
and the handoff of 2026-08-15 published one: "a 12% width change", with the 30px row given as
167px. 167 is `0.09em` arithmetic — 30 × 0.09 × 7 gaps — applied to a row the ruling puts at
`0.06em`. **That is the inverse-idiom failure recorded three paragraphs above, committed inside the
table demonstrating the ruling.** Anyone re-measuring against 167 lands 6px off.

**Nothing in the three generators measures the mark**, verified: every right-aligned element anchors
to the canvas edge as `W - MARGIN - dw`. The width change is real and worth publishing, but there is
nothing downstream to re-measure in these files today.

**Per-glyph drawing discards kerning.** PIL has no letter-spacing, so tracking is drawn by advancing
`textlength(ch)` per character, which sums the individual advances and loses the pair adjustments a
single `draw.text()` would apply. The mark runs **0.20px wide at 20px and 0.30px at 30px** as a
result. Sub-pixel, recorded in each generator's docstring so a later reader does not file it as a
defect, and it does not move the ruled 1.8px gap — only the total.

**THE HELPER IS DUPLICATED IN ALL THREE GENERATORS, so a tracking change is a three-file change.**
Correct for standalone scripts with no shared import, and the same shape as the nav's inline CSS —
but written down here rather than discovered, because the failure mode is landing two of three and
having one OG surface disagree with the other two.

**A CONSTANT 1.8px ACROSS THE WEB TOO WAS CONSIDERED AND REJECTED ON MEASUREMENT.** It would have
moved the nav from `0.09em` to `0.129em` and the card from `0.06em` to `0.052em`. The card change
is invisible — 2.06px to 1.8px on a 182px wordmark. The nav change is not: **1.8px beside 14px
letterforms is 12.9% of the em, where beside 34px letterforms it is 5.2%.** The eye reads the
proportion, not the pixel count, which is the entire reason tracking is expressed in em. A constant
absolute gap makes small type read airy and large type read tight — the opposite of consistent —
and `0.129em` at 14px sits in the territory the kickers use for uppercase labels.

**Both values are positive, and the sign is the part worth holding.** Two earlier values were
retired: `-.015em`, carried from the pre-ruling card generator, and a single `+0.033em` that the
F-register ruled briefly before the size split emerged. The negative value was **a monospace
correction carried onto a proportional face** — wrong in sign, not merely in magnitude. A
monospace face pads its sidebearings by construction; a proportional black one does not.

**Small type wants more space, not less.** The display rule and the small-size rule point in
opposite directions, which is the inverse-idiom failure in a new domain: a correction that is
right at one size is not right at the other by implication.

**One loose phrase retired with them:** the original note said Montserrat Black needs tracking
pulled in "or the counters close up." Tracking moves the space *between* letters and does not
touch a counter at all.

### The lockup template

Established by the AIII mark: **mark letterforms in Montserrat Black gold, above a hairline gold
rule, with the spelled-out name beneath in tracked JetBrains Mono.** New initiative marks follow
this template so the family reads as one hand.

**This is the entry that won decision #15**, because it describes a constructed artifact the
ecosystem already ships rather than a category. The tiebreak was not seniority or specificity in
the abstract — **prefer the entry that describes an artifact that exists over the one that
describes a class**, because the artifact is checkable.

---

## Stacks, tokens and axes

**Ruled 2026-08-11** (F1, F3, F7, F8):

- **A brand face leads every stack; the system face is a fallback, never a first choice.** A stack
  with no brand face in it is not a stack, it is a surrender. This settled the body split without
  needing a separate decision.
- **Fallback chains run three tiers:** brand → system → generic. Two-tier chains satisfy the first
  rule but degrade to the browser default rather than the OS face. Both are legal; only one is
  graceful.
- **One token vocabulary: `--font-{role}`, with `--font-mark` added.** Three vocabularies were live
  for the same five roles — the main pages, `aiii/`'s shortened set, and the `--rnv-font-{role}`
  set emitted by `brand.py` that **no page consumes**.
- **One weight-axis standard per face.** Request the weights actually drawn and nothing synthesised.
  A standard that does not name its axes leaves the next page to pick its own.

**The mark gets its own token so it cannot move by accident.** Without `--font-mark`, the mark
borrows `--font-mono` or `--font-display` and shifts whenever someone retunes a face it was only
ever sharing a variable with — drift with no edit to the mark at all.

---

## The initiative-page exception

**Brand Book decision #16, register F13, ruled 2026-08-11.** The one documented exception, and it
is an exception **to a role rather than to a face**.

**Initiative pages set running text in the display face at weight 340, not in the body face.**
`aiii/index.html` is the template. The register exists to read differently from a post; that
difference is carried by the texture of the running text, so it is load-bearing rather than
decorative. Company briefings inherit it if that surface is ever built.

**What it does not license.** Only the body role is substituted. The mark stays Montserrat Black,
labels and kickers stay JetBrains Mono, emphasis stays Instrument Serif Italic. It does not extend
to blog posts, the résumé, the bio, or `/card/`, and it is not general permission to choose a face
per page — the substitute is the display face specifically, because it is the only other face the
page already carries at reading size.

**The enforceable half: the exception lives in the selector, never in the token.** The page
declares all five tokens at canonical values, then sets
`body { font-family: var(--font-display); font-weight: 340; }`. A page implementing it by
redefining `--font-body` to Bricolage Grotesque **has made its own tokens lie**, and every check
reading token values goes blind on that page while still reporting green.

Verified on `main` 2026-08-12: `aiii/index.html` declares all five tokens including `--font-mark`,
keeps `--font-body` at `'Inter', …`, and makes the substitution in the selector.

**[confirm/fill] The carve-out has no enumerable scope.** It is written for a class with exactly
one member. A check cannot infer "initiative page" from a page's contents, because the contents
are the thing being permitted — it needs a path allowlist or a naming convention. **A single-member
allowlist is honest and cheap; an inferred one is a hole.** Until one exists, the second initiative
page either ships into a guard that flags it as drift, or the guard was loose enough to be pointless.

---

## Type is owed to every publicly seen surface

**Ruled 2026-08-11 (F5).** HTML, raster image, print and social carry the same faces in the same
roles. **The rendering technology is not an exemption.** Internal surfaces hold to the same
standard at lower urgency.

This mattered immediately. The site handoff reached eleven HTML pages and stopped there, while the
**OG share images** — what renders in every link preview, and so the highest-reach surface in the
ecosystem — were drawing the wordmark in JetBrains Mono from three Python generators the note
never mentioned.

**`font.sh` (repo root) fetches three faces** into `assets/fonts/`: `BricolageGrotesque.ttf`,
`JetBrainsMono.ttf`, `Montserrat.ttf`. **Instrument Serif is deliberately not fetched** (F9), so no
raster surface can use it; `font.sh` carries what `scripts/` draws, and the roster of five lives
here.

**The raster side fails silently too.** `load_font()` falls back to `ImageFont.load_default()` on a
missing file with no error — a bitmap face, not even a system one. Same shape as the CSS fallback,
different pipeline.

---

## Exemptions a guard must not flag as drift

- **`/card/` does not carry the canonical font link, by decision.** It requests exactly the three
  faces and four weights it draws and nothing else. The rule is *a page requests every face it
  draws and no face it doesn't*; the twelve chrome pages share one string only because they happen
  to draw all five.
- **`aiii/` declares `--font-mark` and never uses it** — decision #18. The page carries no site
  nav, so there is no wordmark on it to set in the mark face; the Montserrat request was removed and
  the token declaration kept, so the five-token vocabulary stays identical on every page. A comment
  in the file names what to restore and when.
- **`/card/` is generated.** Its mark tracking lives in `scripts/generate_contact_card.py`, not in
  `card/index.html`. A checker reading the page reads a build artifact.

**The guard direction is the inverse of the condition that prompted it.** Loading the mark face and
never drawing it wastes a request and **renders correctly**. Drawing `var(--font-mark)` without
requesting the family puts the wordmark in a fallback and is **visibly wrong**. Only one of those is
a brand failure, and it is not the one that was found — so a check built naively from that finding
would guard the harmless direction.

---

## Two ways a type change fails silently

Both verified, both recorded because the next person will hit them.

**The face is not loaded.** Changing `font-family` without adding the face to the font link falls
through the stack to system sans — no error, no console warning, no visible failure except a mark
that is not the mark. Montserrat had **zero occurrences** on the site when decision #15 was made.

**A value carries across sizes that should not.** The nav's `-0.5px` was `-0.036em` at 14px, tuned
for a monospace face; the card's `-.015em` was the same error at display size. Both looked like
values to preserve and both were wrong.

**A THIRD, ADDED 2026-08-16: the face is loaded by a mechanism the change forgets.** `rnv-live`
loads faces through `@fontsource` npm imports rather than a font link, so pointing `.wordmark` at
`--rnv-font-mark` took **three files** — the import in `index.astro`, the dependency in
`package.json`, and the entry in `package-lock.json`. Two were pushed and the build failed on
`npm ci`, which refuses when the manifest and the lockfile disagree.

**That refusal is the behaviour to want.** `npm ci` would not resolve from the manifest and quietly
produce a dependency tree nobody had recorded; it failed at build time rather than deploying a page
whose mark fell through to `system-ui`. Same posture this register asks of its own guards. The
coupling was missed not because it was subtle but because it was **dull next to the interesting
one** — the import was the insight, the lockfile was bookkeeping, and the bookkeeping broke the
build.

**A font change on `rnv-live` is a three-file change.** Written here rather than rediscovered.

---

## Open

- **~~`engine/brand.py` cannot name the face that carries the mark.~~ CLOSED 2026-08-15.** `TYPE`
  now holds five roles as `{family, weights}`; `mark` is Montserrat at `(900,)` and
  `--rnv-font-mark` emits. Verified additive against live `main`: **no token name removed, no value
  changed, one token added**, and every `var(--rnv-*)` in `rnv-live` still resolves. The original
  finding kept, because its shape is the lesson — `TYPE` held four roles;
  Montserrat appears **zero times** in the file. Sharper, because it is checkable: `tokens()` builds
  font tokens by comprehension over `TYPE`, so the emitter can produce exactly as many font tokens
  as `TYPE` has roles — four. **`--rnv-font-mark` is not missing from a list; it is unemittable.**
  The site declared five tokens on every nav page against an emitter that could produce four.
- **No font fact exists in `profile.json`.** Nothing watches type; the nav could disagree with this
  register indefinitely and nothing would say so. Not a checker failure — no checker was pointed
  here. Handed as R2.
- **~~[confirm/fill] Tracking is undefined between the two ruled sizes.~~ RULED 2026-08-15.** See
  the raster table above: 1.8px absolute, expressed as `0.09em` at 20px and `0.06em` at 30px. The
  original finding is worth keeping because of how it was reached — the F-register closed the
  `generate_site_og.py` question partly on the arithmetic that `+0.033em` at 20px is 0.66px and
  therefore sub-pixel and safely dropped. **Two things were wrong with that.** The ruled nav value
  is `0.09em`, not `+0.033em`, so the figure being dismissed was not the ruled one; and at 30px the
  figure it *did* dismiss is 0.99px, which is not sub-pixel either. **A conclusion can survive its
  own reasoning being wrong, and this one did not — the generators shipped untracked.** Three
  generator edits are with the Brand Architect chat.
- **~~No font fact exists in `profile.json`.~~ CLOSED 2026-08-16 as R2.** `verify_type` runs
  unconditionally in the facts pass and **discovers surfaces rather than reading a list**, so any repo
  that grows an HTML or `.astro` file is checked from that moment. It asserts four things: the mark
  is drawn in the mark face; a page drawing that face also requests it; the shared font link does not
  drift on one page of the set; and no page redefines `--font-body` away from Inter. Seven arming
  tests, the exemptions among them.
  - **IT NEEDED TWO DISCRIMINATORS, AND THAT IS THE DESIGN LESSON. The mark is a role, not a
    string.** Text alone flags the blog byline, which renders the brand name as an author credit in
    mono on eight files and which the Labels row above explicitly permits. Class alone flags
    `aiii/`, where `.wordmark` is the AIII initiative mark in mono by decision — same class, two
    roles, one surface each. A check cannot infer "this is the wordmark" from contents, because the
    contents are the brand name either way.
  - **COVERAGE BOUNDARY, stated so nobody assumes more.** The guard checks the **face**. Weight and
    tracking are declared on the same rule and are **not** asserted. `rnv-live` carried a wrong face
    *and* wrong tracking, and only the face is why it failed — Montserrat 900 at `0.02em` would have
    passed. Weight is a small increment, always 900 with no variation. Tracking is not: the expected
    value depends on **role** rather than size, and a guard cannot infer role, so it needs an
    expected value recorded here per mark selector before any code.
  - **The three raster generators are outside it entirely** — Python drawing with PIL, no markup to
    parse. Their 1.8px is held true by the three-file coupling and nothing else.
- **[confirm/fill] A formal mark spec** — clearspace, minimum sizes, ratios. Deferred until the
  first external use demands it. Decision #15 settles the *face*, not the spec.

---

## The F-register, retired here

The working scan that carried these items is superseded by this file. Outcomes preserved; the
`F` prefix existed to avoid colliding with the Brand Book decision log and is kept for traceability.

| # | Decision | Outcome |
|---|---|---|
| F1 | Brand face leads every stack | Ruled — yes |
| F2 | Body face | Ruled — Inter, system behind it |
| F3 | Fallback chain depth | Ruled — three tiers |
| F4 | The `cards/` orphan | Closed — deleted 2026-08-12 |
| F5 | Is decision #15 global to the raster pipeline? | Ruled — yes |
| F6 | `generate_site_og.py`'s spaced `R N V I Z I O N` | Closed on evidence — the mark; face, case and spacing all fixed |
| F7 | One token vocabulary | Ruled — `--font-{role}` plus `--font-mark` |
| F8 | One weight-axis standard per face | Ruled — yes, nothing synthesised |
| F9 | Does `font.sh` fetch Instrument Serif? | Closed — no, by design |
| F10 | Mark tracking | **Superseded** — the single `+0.033em` gave way to the two-value system above |
| F11 | Type fact in `profile.json` | Open — R1 + R2 |
| F12 | `BRAND_COLORS.md` typography block | Closed — retired rev 14, now points here |
| F13 | Initiative-page body face | Ruled — narrow reading; Brand Book decision #16 |
| F14 | `profile.json` phone | Closed — resolved in v1.3.0 |

**Three items in that scan were stale when it was retired** — F10's `+0.033em`, a target section
still naming `-.015em`, and a nav description written before the change shipped. A working scan
pressed into service as a register goes stale the way any second canonical copy does, which is
part of why this file exists.

---

## Colour — not here

**`BRAND_COLORS.md` owns colour. This file owns type.** No colour value is restated here, including
the gold the mark is set in; where a colour is named above it is naming a surface, not defining a
value.

---

## Evidence base

Brand Book decisions **#15** (mark face), **#16** (initiative-page body), **#18** (`aiii/`
Montserrat request), **#19** (hex notation, colour but same discipline). Register F1–F14, retired
above. Verification against `main` on 2026-08-11, 08-12, 08-14 and 08-15; every figure in this file
was read from a shipped artifact rather than a handoff note.

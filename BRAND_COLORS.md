# RNVizion Brand Colors

The register of RNVizion's **permanent** colors. Machine source: `engine/brand.py`
(import from there; never hardcode). This doc is the human-readable explanation.

Last locked: 2026-08-30 (rev 23 — **the hover plate moves from `#e8e8e8` to `#eeeeee` one day after
being ruled, and a claim is withdrawn with it.** The first ruling measured separation from the base
and called the result dominance; it never measured **margin on the binding constraint**, where
`#e8e8e8` clears by 0.0334 and `#eeeeee` by 0.2875. `#e8e8e8` is the ground the light gold is
*calibrated against* — plate and gold would have failed on the same rounding. **Eleven hover keys
across four apps already held `#eeeeee` and zero held `#e8e8e8`**; the ruling reasoned from a
contrast table about a question the shipped code had settled. `#e8e8e8` keeps every other role.
**And rev 22's "two independent walks" claim is withdrawn as a tautology** — same equation, two
unknowns, and the crossing always lands on whatever ground you fed it. rev 22 — **the dark surface ladder is ruled with all four rungs
registered, and the light hover plate is settled at `#e8e8e8`.** `APP` gains `canvas` `#0a0a0a`,
`panel-hover` `#3a3a3a` and `hover-light` `#e8e8e8`; no existing value moved. **A correction from
this side is recorded rather than quietly dropped:** rev 21 called the dark ladder "two-thirds
specified" on the grounds that `border` `#333333` is not a rung — it is `grey(3)` on the ink grid,
an edge rather than a surface, and was never part of this ladder. The wrong reading is what sent the
app side hunting a gap that did not exist. rev 21 — **three rulings out of the ink-grid rollout, and two of them
came from applying the grid rather than from looking for defects.** **Coincidence is permitted and
must be named:** publishing the grid means an app ramp step can land on a registered value while
doing a different job, and the apps' `COINCIDENT` table is adopted as the recording form — the same
seam as `signal-offline` equalling `text-faint`, meeting an app ramp instead of two register
families. **`#d0d0d0` is retired as a light interaction ground**, found independently by two apps
and settled at the value rather than at either dialog. **And the light-surface ladder is NOT ruled
here** — the anchor offered for it does not hold, and the reason is in the ramp section below.
rev 20 — **the ink grid is ruled and `APP["text"]` moved onto it.**
`grey(n) = n * 0x11`; every ink and every edge lands on a step, in both modes, with no exceptions.
`#e0e0e0` was the single exception and it was **one hex doing two jobs** — ink in dark mode, a light
surface elsewhere — which is why it would not sit on a grid that governs inks. The ink half is now
`grey(13)` `#dddddd`; the surface half keeps `#e0e0e0` and the two contrast rows below are
unchanged. **The grid's scope is stated with the grid:** it governs inks and edges and never
surfaces, because `APP["panel"]` is `BRAND_BLACK` at n = 1.53 and a permanent does not move to fit a
ladder. rev 19 — **three corrections, and in two of them this register was the
document the apps had correctly ignored.** It carried a heading saying **there is no light-mode
error text** while Brand Book §9 ruled `#c82131` and three applications shipped it — under **two**
identifiers, which is the unpublished-derivation failure recurring in another family. Now published
as `STATUS["error-text-light"]`. **The hover-gold rename is reverted at source**: `BRAND_HOVER_GOLD`
retired an identifier in five of six repositories, 43 occurrences, and left the light-mode
counterpart unspellable — `BRAND_GOLD_HOVER`, which this register never stopped publishing, was
right. And `still-gold` was a permanent colour the brand's own resolver refused for a day; the
resolver keys and an import-time completeness guard both landed. rev 18 — **stamp dates in this file are the clock of the commit that
shipped the subject, with the short SHA beside them.** An earlier pass re-dated every 2026-08-17
stamp to "today" on the belief that nothing happened that day. **Seven commits carry it**, and the
gold value change demonstrably shipped in `1003a6c` on it. Corrected per stamp against
`git log -S`, which is the only witness that does not depend on anyone's memory. — **the ring stopped being chrome, and a claim in this register
stopped being true with it.** It was gold in every state and therefore signalled nothing; on
`rnv-live` it is now stateful across three states, so *"identical in all states"* is retired and the
four-channel table replaces it. **Three of the four channels order and the fill cannot** — it carries
hue identity rather than intensity, so live's fill is the dimmest of the three, and claiming
otherwise would be a claim the table inherits. `signal-down` is renamed **`signal-standby`**: `down`
asserted a fault the state does not have, where standby covers a build underway, maintenance, a
stream being prepped *and* a partial outage. Values unchanged. **Every figure here is truncated, not
rounded** — see the note under the contrast table. rev 17 — **the derivation rule is published, and a hole is named.** Three
applications derived `-14` from the same base independently; `rnv-color-picker` pointed out that
**three apps agreeing is luck, not design**, and that an unpublished derivation permits four *values*
for one colour — worse than four names, because a wrong value is invisible in a diff.
`engine/brand.py` now carries `lighten()` and both derivatives with their walks. **Dark-mode pressed
is recorded as OPEN**, since the two apps disagree and it is a design question rather than a
measurement. **And the light-mode error text is now published** as `STATUS["error-text-light"]` `#c82131`: `#dc3545` reads 4.1528 on a light panel, and
`error-text` is a dark-theme value that would make it *worse*. rev 16 — **`BRAND_DARK_GOLD` moved from `#b19145` to `#8c7337`, and the
reason is a rounding rather than a redesign.** This register read gold-on-white as 3.00:1 and
granted permissions on that figure. The true value is **2.997638** — under the 3.0 large-text and
non-text floors by 0.0024 — so every permission below the fill row was void. The old value passed
**one of six** jobs, not one well and three conditionally: its own "the border carries the signal"
clause failed, because a gold border on white *is* that same 2.9976. Nothing caught it because 3.00
is what a contrast tool **displays** — `rnv-color-mcp` returns `3.0` for this pair and flags
`AA_large_text: false` in the same response, and the number was read while the flags were not. The
constants are also renamed to **`BRAND_GOLD`** and **`BRAND_DARK_GOLD`** in every repo including
`engine/brand.py`, retiring the "identifiers are local by design" rule. rev 15 — **hex notation is
lowercase**, recorded below under names and
values; applied across the five desktop apps on 2026-08-15 and already true in `brand.py`.
**The ring's boundary figures drop to one decimal** and carry their display condition: the
two-decimal forms claimed a precision the estimate does not have, and the two files that held
them disagreed — this doc said 6.09/6.27, `brand.py` said 6.12/6.33, on the same blend. rev 14 —
the hero dot's fill grew to 10px and the ring thinned to
0.75px on **both surfaces in one pass**, dropping the boundary from ~10.2:1 to **~6.1:1** on the
site and ~10.7:1 to **~6.3:1** on `rnv-live`, both at 1x. Aligning rather than diverging was the call: ring
sameness is the stated justification for a sub-floor fill, and a tracked mismatch becomes
intentional by age. Carried as a `[confirm/fill]`, since the value is unverified below 3x. Also
records a defect: the hero dot had been an ellipse at every viewport width, squeezed by flex,
through three passes of work on this same component — every one of which was about colour.
Rev 13 — **third revision on this date; the sequence is in the rev
number, not the stamp.** Lands `signal-live` at `#a5034e` and moves the fill's ratio to 2.43:1;
retires "wine" as a descriptor for the current value. Repairs a blind pass that ran over rev 12
and hit only the sentences that are *about* hex case: three mentions of `#FFC107` lowercased into
meaninglessness, the `#8B2C3B`/`#8b2c3b` illustration replaced with two different colours, and the
one line that actually stated a value left carrying a retired one. **A find-and-replace cannot
tell a mention from a use.** Rev 12 — the signal dot's ring was decoupled from its fill on both
surfaces, so the ring no longer dims and the dim-end contrast figure in the signal section is
retired rather than corrected. Records the split as landed, and records that `breathe`'s 0.5 dip
now stands on parity rather than on the accessibility floor that originally set it. Rev 11 —
**rev 10's header was stale against its own body:** it read
2026-08-10 while carrying two sections ruled 2026-08-13, so this file's version field described
a document that no longer existed. A dated header is the only thing that surfaces a stale-base
clobber, and it cannot do that job while it is itself behind. Rev 11 closes the signal ruling:
`rnvizion.dev` landed the change, so both surfaces are clean and `#4ade80` is gone from the
ecosystem rather than merely retired at the source. Normalises `#8b2c3b` to lowercase, the case
hazard this file already names about `#FFC107`. Retires the typography block (R3) — it was not
merely redundant with Brand Book §3.2, it stated three facts that §3.2 had already retired.
Rev 10 — the two-dark rule re-derived from measurement after the
question was reopened: charcoal is a mid-tone in both ramps and a base in neither, so it
cannot replace the web ground. Rev 9 strikes "one edit updates every consumer," a mechanism this
file claimed and nothing ever implemented; records the mirror pattern that actually governs.
Renames the `#0a0a0f` register row from "web near-black" to **web black**, since "near-black"
already resolves to charcoal and one word cannot mean two darks. Rev 8 was the **first commit
into `rnv-brand`.** Revs 1–7 existed as a
document without a home while `engine/brand.py` and this repo's README both cited it by
name; that citation now resolves. Adds the three-artifact ownership split and re-frames the
ramp tables as dated census evidence rather than value listings, so this file points at the
machine source instead of restating it. Rev 7 named the warm register **Records** and settled
its routing rule; rev 6 published its steps as derived canon. Rev 5 settled the
two golds and their usage split. Rev 4 restructured this document from a usage catalogue
into a register of permanent colors; revs 1–3 predate that shape.)

---

## Who owns what

Three artifacts describe color, and two of them describing the same thing twice is the drift
this system exists to prevent. The split, so nothing is stated in two places:

| Artifact | Owns |
|---|---|
| **Brand Book §3.1** | The summary and the fact that a ruling exists. Points here; does not restate |
| **`BRAND_COLORS.md`** (this file) | The register, the rules, the exclusions, and the reasoning behind each |
| **`engine/brand.py`** | The values. Every consumer imports them from there |

**This file names the six permanent values because they are its subject.** It does not
restate derived ramps as current values; where a ramp appears below it is **dated census
evidence for a rule**, not a listing to keep in sync. An observation carries its date and
cannot go stale; a value table can.

---

## What makes a color a brand color

**Permanence.** A brand color is one the brand is committed to across media and time: it can
end up on a garment, a hangtag, a printed mark, a physical asset, a palette handed to a
manufacturer. Once it's here, it's permanent, and everything else modulates from it.

A color is **not** a brand color if it is any of the following:

| Class | What it is | Example |
|---|---|---|
| **Platform convention** | An OS or framework's semantic color, left alone deliberately because it fits | Selection blue `#0078d4`; Material and Bootstrap status colors |
| **Tool primitive** | Color math the software needs, not design | `#ff0000`, `#00ff00`, `#0000ff` |
| **Modulation** | Derived from a permanent color by opacity, lift, drop, tint, or mix | Scrollbar handles, hovers, pressed states, image-mode alphas |
| **Product decision** | Which permanent color a given surface uses where | Whether a panel is white or grey in one app's light theme |

**This is why the list is short.** A census across seven surfaces turned up roughly sixty
distinct hex values. Six are permanent. The rest are ramp steps, alphas, platform semantics,
tool primitives, or one product's call.

---

## The register

### Gold — the identity

**There are two golds. There is no third.**

| Color | Hex | RGB | Canonical use |
|---|---|---|---|
| Brand gold | `#d2bc93` | 210, 188, 147 | **The accent on black and dark surfaces.** Site, social, OG cards, wordmark, every app's dark theme |
| Brand dark gold | `#8c7337` | 140, 115, 55 | **The accent on light surfaces.** Every app's light theme; also gold's shade on dark, where full gold is too loud. Was `#b19145` until 2026-08-17 (`1003a6c`) — the contrast table below records why it moved and what it cost |

**The split is confirmed by the code, not just declared.** `#b19145` appears zero times on
rnvizion.dev and zero times in the corpus Space — both all-dark surfaces, both gold-only.
In the apps, the dark theme's accent is `#d2bc93` and the light theme's is `#b19145`,
without exception across all five.

**Dark gold's second job, which the split doesn't cover.** On dark surfaces it also serves as
gold's shade — `accent_dark` in the dark theme drives borders, hairlines, and pressed fills
where full gold would shout. And `SLOT_SELECTED_COLOR` uses dark gold deliberately because
the mark has to read in *both* modes. So: gold accents dark and dark gold accents light,
and dark gold is additionally the darker of the pair wherever gold needs one.

**Values between and beyond the two are modulations, and none of them is promoted.**
`#dcc9a3` (three apps) sits on the gold axis extended past brand gold by about 30%;
`#c4ab7e` (corpus button hover) and `#c4a458` (three apps) sit near it, hand-picked. A
surface that needs a lighter or darker gold derives it; it doesn't mint one.

### Black — the ground

| Color | Hex | RGB | Canonical use |
|---|---|---|---|
| True black | `#000000` | 0, 0, 0 | App window ground; text on gold, on both light and dark surfaces |
| Brand black (charcoal) | `#1a1a1a` | 26, 26, 26 | Raised surfaces in apps; the answer to "brand black" with no other context |
| Web black | `#0a0a0f` | 10, 10, 15 | rnvizion.dev base; social assets and OG cards |

**Three blacks, and each one is committed.** Measured rather than asserted (2026-08-10):

| Value | L* | Role |
|---|---|---|
| `#000000` | 0.00 | App ground; the neutral ramp's near anchor |
| `#0a0a0f` | 2.86 | Web ground; the floor the site's ramp is built up from |
| `#1a1a1a` | 9.26 | Charcoal; the answer to "brand black" with no context |

**Charcoal cannot replace the web ground, because charcoal is not a base in either system.**
It sits at L\* 9.26; the web ramp's *top* step `#1a1a26` sits at L\* 9.79. Flatten the site to
charcoal and it starts where its ramp currently ends, with the two darker steps having nowhere
to exist. The same is true of the apps, where charcoal is the middle step of
`#000000` → `#1a1a1a` → `#2a2a2a`. **Charcoal is a mid-tone in both systems and a base in
neither.**

The distinction is also visibly real, not a protected invisibility: `#0a0a0f` against `#1a1a1a`
is ΔE 6.81, roughly seven times the just-noticeable threshold. The blue lift alone carries
ΔE 8.91 between `#1a1a26` and `#1a1a1a` at nearly identical lightness, which is the
independent case for never flattening the tint to neutral.

One practical cost on top of the structural one: every social asset and OG card built to date
sits on `#0a0a0f`. Collapsing the darks re-renders all of them.

### White

| Color | Hex | RGB | Canonical use |
|---|---|---|---|
| White | `#ffffff` | 255, 255, 255 | Light-surface cards and inputs; SVG export ground; the other anchor of the neutral ramp |

---

## The ramps, which are rules and not lists

### The ink grid, ruled 2026-08-28

```
grey(n) = n * 0x11,  n in 0..15      TRUE_BLACK -> WHITE in fifteen steps
```

**Every ink and every edge lands on `grey(n)`, in both modes, with no exceptions.**

| role | key | value | n |
|---|---|---|---|
| ink | `APP["text"]` | `#dddddd` | **13** |
| ink | `APP["text-dim"]` | `#aaaaaa` | 10 |
| edge | `APP["border"]` | `#333333` | 3 |

**Primary text is one role with two mode values:** dark is a grey on the ink grid, light is
`TRUE_BLACK`. Already true in all five apps with no app disagreeing — it had simply never been
written down, which is why it read as a question rather than a rule.

**THE GRID GOVERNS INKS AND EDGES. IT DOES NOT GOVERN SURFACES AND IT NEVER CAN.** `APP["panel"]` is
`BRAND_BLACK` `#1a1a1a` at n = 1.53 and `APP["card"]` is `#2a2a2a` at n = 2.47. **`BRAND_BLACK` is a
permanent brand colour and will not move to fit a ladder.** The scope is stated here rather than
discovered by whoever extends the grid to surfaces and finds a permanent in the way — the same
failure as a coverage boundary that decays, arriving in a ramp.

### `APP["text"]` moved from `#e0e0e0` to `#dddddd` in the same change

It moved **only** to satisfy the grid, so the grid and the move are one ruling; neither is
defensible alone.

**The value was one hex doing two unrelated jobs.** Ink in dark mode; a light **surface** in the
apps' light palettes and in this register's own contrast tables below. It refused to sit on the grid
because **the grid governs inks and half its uses were not ink.** Split the roles and both halves
land — the ink half becomes `grey(13)`, the surface half keeps `#e0e0e0` and does not move. **The
two contrast rows further down are about the surface and stand unchanged.**

| ground | before | after |
|---|---|---|
| `#444444` pressed plate | 7.37 | **7.17** |
| `#3a3a3a` hover | 8.61 | 8.37 |
| `#333333` border | 9.57 | 9.30 |
| `#2a2a2a` card | 10.87 | 10.56 |
| `#1a1a1a` panel | 13.18 | 12.81 |
| `#000000` window | 15.90 | 15.46 |

Floor after the move is **7.17**, on the darkest ground it ever touches. Nothing approaches a bar.

**Checked rather than assumed:** nothing in `engine/brand.py` derives from it, `profile.json` does
not carry it, `rnv-live` emits from `--css web` and reads `WEB["text"]` `#e8e8f0` — so no web surface
moves — and all six existing uses of `#dddddd` across the five apps sit under **light** palettes.

### The light-surface ladder is not ruled, and here is what has to be true before it can be

**The problem is real and correctly diagnosed: nine light surfaces across four apps sit between grid
n = 12.24 and n = 15.00 — under three steps of `0x11`.** Nine distinguishable surfaces cannot live
in 2.76 steps of a ladder that steps by seventeen. The dark side does not have this problem because
it never used the ink grid for surfaces.

**But the anchor offered for the light ladder does not hold.** The claim was
`invert(#0a0a0a) = #f5f5f5` — *the light ground is the reflection of the dark canvas*. The
arithmetic is right and **`#0a0a0a` is not a value this brand holds.** The canvas is `WEB_BLACK`
`#0a0a0f`, and:

| dark value | registered | inverts to | in use on the light side |
|---|---|---|---|
| `TRUE_BLACK` `#000000` | yes | `#ffffff` | **yes, 32 uses** |
| `BRAND_BLACK` `#1a1a1a` | yes | `#e5e5e5` | **no uses at all** |
| `WEB_BLACK` `#0a0a0f` | yes | `#f5f5f0` | no — `#f5f5f5` is a near miss |
| `#0a0a0a` | **no** | `#f5f5f5` | 15 uses |

**Inversion anchors exactly one value in use, and it is `#ffffff`.** `#f5f5f5` looked anchored
because `#0a0a0a` is one byte from the canvas in the blue channel alone. That is a coincidence with a
colour the brand does not hold, and building a ladder on it would pin fifteen uses to a value nothing
in the register defines.

**The dark ladder that was offered as the model is also not published.** `BRAND_BLACK ± 0x10` gives
`#0a0a0a`, `#1a1a1a`, `#2a2a2a`, `#3a3a3a` — but `APP` holds `panel` `#1a1a1a`, `card` `#2a2a2a`,
and `border` `#333333`, which is **not** `#3a3a3a`. Two rungs of that ladder are in use, two are not,
and one value in the family is off it. **It is a pattern two values wide, not a published rule**, so
mirroring it would mean deriving the light side from something the dark side has not settled either.

**`#e8e8e8` does have independent standing** and that part is right: it is the published coverage
boundary for gold as text, and any ladder stepping over it makes that ruling harder to state.

**What has to happen first, in order:**

1. **Rule the dark surface ladder**, which is two-thirds specified and entirely within this register.
   Until `border` at `#333333` versus a `#3a3a3a` rung is settled, there is no model to mirror.
2. **Decide which of the nine light values are real distinctions.** Four carry 65 of the 71 uses —
   `#ffffff` 32, `#f5f5f5` 15, `#eeeeee` 11, `#e0e0e0` 7. The other five have nine uses between them.
   **That is a judgement about whether a user can tell a list-alternate row from a list header, and
   it is made by looking, not by measuring.**
3. **Then derive**, with `#e8e8e8` fixed as a rung because it is already load-bearing.

**Until then the dark half is what should be built**, and it is fully specified today.

### `#d0d0d0` is retired as a light interaction ground, ruled 2026-08-28

**Two applications reached this independently, which is the argument for the register holding it.**
`rnv-color-picker` already carried `#d0d0d0` in its `RETIRED` table as *"the tab hover ground no gold
cleared"*. `rnv-color-palette-manager` then hit the same wall in its About dialog: a hover plate at
`#d0d0d0` with a `BRAND_DARK_GOLD_DEEP` label reads **3.601:1**, under the 4.5 floor and well below
the published boundary.

**The register already ruled the outcome and the apps were violating it, not disagreeing with it:**
*below `#e8e8e8`, gold does not carry text.* `#d0d0d0` is grid n = 12.24, two full steps under.

**The fix is neither of the two the apps proposed.** Moving the plate above `#e8e8e8` treats one
dialog; dropping gold from the label treats one label. **The value is the defect** — a light
interaction ground dark enough that nothing in the gold family clears text on it, discovered twice
by two apps that never compared notes.

**Ruling: `#d0d0d0` is not a light interaction ground.** Light hover and pressed plates stay at or
above `#e8e8e8`, which is where the gold-as-text boundary already sits. That is one rule covering
both instances and every future one, rather than two fixes covering two dialogs.

### The dark surface ladder, ruled 2026-08-29 — all four rungs registered

```
BRAND_BLACK + n * 0x10,  n in -1..+2
```

| n | value | role | key |
|---|---|---|---|
| −1 | `#0a0a0a` | canvas, image-viewer ground | **`APP["canvas"]`** — was app-owned |
| 0 | `#1a1a1a` | panel | `APP["panel"]`, `BRAND_BLACK` |
| +1 | `#2a2a2a` | card | `APP["card"]` |
| +2 | `#3a3a3a` | panel hover | **`APP["panel-hover"]`** — was app-owned |

**The two ends were app-owned and are now registered.** A brand that publishes the middle of a
ladder and leaves the edges to applications is publishing a derivation nobody can check.

**`border` is not a rung, and its absence was never a gap.** An earlier reading from this side
called the ladder *"two-thirds specified"* because `APP["border"]` `#333333` is not `#3a3a3a`.
**`#333333` is `grey(3)` exactly on the ink grid, and that grid governs inks *and edges*.** A border
is an edge. It was measured against the wrong family and reported as a hole in this one — the
correction is recorded rather than quietly applied, because the wrong reading is what sent the app
side looking for a rung that does not exist.

**`#0a0a0a` is not `WEB_BLACK`, and the seam is deliberate.** The web canvas is `#0a0a0f` — same
lightness, blue channel lifted. This register already rules it: **app neutrals are pure grey,
R = G = B, without exception**, and the web ground carries a tint the apps do not. Two canvases one
byte apart is not drift.

**And that near-miss is what made the light-side inversion anchor look convincing.**
`invert(#0a0a0a) = #f5f5f5` is true of a colour the brand does not hold; `invert(#0a0a0f) = #f5f5f0`
is true of one it does. The same one-byte seam produced a correct-looking derivation on one side and
a false one on the other.

### The light hover plate is `#eeeeee` — corrected 2026-08-30, the day after it was ruled

**The first ruling put it on `#e8e8e8` and said the arithmetic left no choice. It measured one axis
and called the result dominance.**

| plate | gold `#7e6529` | margin | error-red `#c82131` | margin | separation from `#ffffff` |
|---|---|---|---|---|---|
| `#e8e8e8` | 4.5334 | **+0.0334** | 4.6100 | +0.1100 | 1.2252 |
| **`#eeeeee`** | 4.7875 | **+0.2875** | 4.8684 | +0.3684 | 1.1602 |

**The axis it did not measure is margin on the binding constraint.** `#e8e8e8` is the value at which
the next step down fails — and it is the ground `BRAND_DARK_GOLD_DEEP` is *calibrated against*,
marked `<- binding` in its own derivation. Putting every hover in every app on it couples plate to
gold so tightly that one rounding fails them together: `-13` instead of `-14` gives 4.4675 and both
go at once.

**A boundary is not a plate. A working state should not sit on the last value that works.**

**And the applications had already answered it.** Eleven hover keys across four apps hold `#eeeeee`;
**zero** hold `#e8e8e8`, whose every use is a static surface. **The ruling reasoned from a contrast
table about a question the shipped code had already settled.**

**`#e8e8e8` is not retired and not weakened.** It stays registered, stays the published gold-as-text
coverage boundary, and keeps its three surface uses and its role as the binding ground. It is doing
real work; it is simply not the hover.

### A claim withdrawn, in the same change

Rev 22 argued that the apps walking *up* from a failing plate and this register walking *down* from a
failing text colour and **both stopping at `#e8e8e8`** was *"a boundary two independent walks land on
is doing real work."*

**The walks were never independent.** It is one equation — `cr(gold, ground) >= 4.5` — solved for two
unknowns. The register fixed a set of grounds and took the **smallest step clearing its darkest
one**, which calibrates the gold *to* that ground. Asking afterwards which ground the gold clears
returns the ground you fed it:

| darkest ground fed | step chosen | crossing then lands at |
|---|---|---|
| `#eeeeee` | −10 | `#eeeeee` |
| `#e8e8e8` | −14 | `#e8e8e8` |
| `#e0e0e0` | −19 | `#e0e0e0` |
| `#dddddd` | −21 | `#dddddd` |

**Every time. That is arithmetic, not corroboration.**

**The gold-as-text ruling stands on the six-job table** — one value passing one job of six against
another passing five — which is real independent evidence. Raised by the app side, which was right to
refuse unsafe support for a ruling it agrees with.

### The neutral ramp

Every neutral in all five desktop apps — twenty-three distinct values from `#000000` to
`#ffffff` — is a **pure grey**, R = G = B, without exception. That isn't twenty-three
colors; it's one ramp with steps chosen per surface.

**The rule: neutrals are steps between the two anchors, and a step is a modulation.** A
surface picks the steps its layering needs. The brand doesn't publish them, doesn't count
them, and doesn't drift when an app adds one.

### The tint rules

Two tints of that ramp exist, each consistent enough to be a rule rather than a list, and
each now scoped to a category of surface.

| Tint | Rule | Carries |
|---|---|---|
| **Cool** | R = G, blue lifted | rnvizion.dev, the blog, social and OG. The identity surfaces, and Chris's own voice |
| **Records** (warm) | R > G > B, descending | Notes, patch notes, updates, newsletters, initiative pages. RNVizion issuing something consulted later |

**Both tints publish their steps, and publishing a derived value is not the same as making
it permanent.** A garment will never be `#9b978c`; a surface in the register should never
reinvent it either. The source emits both ramps so consumers derive nothing by hand, and the
permanent register above stays six values long.

**Cool — rnvizion.dev.** R and G stay equal; blue is lifted. Ten values, ten conform.
*Census of 2026-08-10; evidence for the rule, not the current value list — `brand.py` owns
those.*

| Value | R | G | B | R−G | G−B |
|---|---|---|---|---|---|
| `#0a0a0f` | 10 | 10 | 15 | 0 | −5 |
| `#11111a` | 17 | 17 | 26 | 0 | −9 |
| `#1a1a26` | 26 | 26 | 38 | 0 | −12 |
| `#25253a` | 37 | 37 | 58 | 0 | −21 |
| `#5a5a72` | 90 | 90 | 114 | 0 | −24 |
| `#9a9ab0` | 154 | 154 | 176 | 0 | −22 |
| `#e8e8f0` | 232 | 232 | 240 | 0 | −8 |

**Records — warm.** R above G above B, descending. Four values, four conform.
*Census of 2026-08-10; same standing as the cool table above.*

| Value | R | G | B | R−G | G−B |
|---|---|---|---|---|---|
| `#efece2` | 239 | 236 | 226 | +3 | +10 |
| `#e7e3d8` | 231 | 227 | 216 | +4 | +11 |
| `#9b978c` | 155 | 151 | 140 | +4 | +11 |
| `#6f6c64` | 111 | 108 | 100 | +3 | +8 |

`#0a0a0f` is the anchor the brand commits to; the cool ramp above it is modulation. Don't
flatten the tint to neutral — the layering is what it buys.

### Alpha

Opacity is a modulation, never a color. Image-mode chrome, scrollbar handles, hover and
pressed states, and the hairline gold rule at 18% are all alphas over a permanent color.
**A dark may be thinned; it may not be re-hued.** A new hex that approximates the blend is a
new color and needs a decision, which is the whole reason the rule exists.

The corollary wherever transparency meets state: **alpha carries the mode, value carries the
state.** A hover that raises opacity instead of value inverts direction depending on what
sits behind it.

---

## Records — the warm ink register

Named and promoted August 10, 2026 from the AIII page, where it had been running as a
page-local choice. **Records carries notes, patch notes, updates, newsletters, and initiative
pages** — the surfaces RNVizion issues and readers consult later. It uses the same ground and
the same gold as everything else; only the ink changes.

The name aligns deliberately with `records/` in `rnv-reports`; one is where a record lives and
the other is what it's set in, and nothing needs reconciling.

| Token | Value | On `#0a0a0f` | Drives |
|---|---|---|---|
| `--ink-bright` | `#efece2` | 16.71:1 | Ledes and opening paragraphs |
| `--ink` | `#e7e3d8` | 15.40:1 | Body copy, beat lines, headings, names |
| `--ink-mute` | `#9b978c` | 6.77:1 | Bylines, definitions, secondary text, footer links |
| `--ink-faint` | `#6f6c64` | 3.77:1 | Kickers, small labels, footer text |

Unchanged from the site: `#0a0a0f` ground, `#d2bc93` gold, hairline at
`rgba(210,188,147,.18)` — the canonical 18%. `#efece2` was hardcoded on the AIII lede and is
tokenized here as `--ink-bright`.

**The register is more legible than the one it sits beside, which is a real argument for it
rather than a decoration.** Warm faint reads 3.77:1 against cool faint's 2.95:1 — the cool
faint is under the 3:1 floor for large text and UI components, and the warm one clears it.
Separate finding, and it belongs to the site rather than to this ruling.

**One constraint: `--ink-faint` is for labels, never body.** At 3.77:1 it clears large text
and UI but sits under the 4.5:1 normal-text floor. The AIII page already uses it correctly —
kickers, small labels, footer — and the rule travels with the register.

**Newsletters are the surface most likely to break this, and it isn't the color's fault.**
Email clients force-invert dark grounds, strip custom properties, and get printed. If a
newsletter can't hold `#0a0a0f`, invert the ramp onto a light ground rather than abandoning
the register — the tint rule is what's canonical, not the direction it runs. `#6f6c64` is
the one step that reads either way (3.77:1 on near-black, 5.24:1 on white), which makes it
the safe value when the ground is out of your hands.

**The routing rule, settled with the name.** Cool is the identity layer and Chris's own
voice — the site, the blog, the bio, social. **Records is RNVizion issuing something a reader
will consult later.** That routes the blog to cool and an initiative page to Records without
anyone having to ask, which a list of surfaces can't do.

**Records routes by surface; the Institutional voice routes by speaker.** They cover
overlapping ground and are deliberately not the same instrument: a newsletter Chris writes
personally is set in Records ink in his own voice, and a release note in a repo README is
written in the Institutional voice with no warm ink anywhere near it. Different names because
they're different artifacts.

---

## Not brand colors, recorded so the question stops recurring

These appear in RNVizion software and are deliberately left alone. They belong to the
platform, not the brand; the brand neither owns them nor varies them.

| Value | Origin | Where |
|---|---|---|
| `#0078d4`, `rgba(0,120,215,200)` | Windows accent and selection | Checkboxes, progress fill, selection overlay |
| `#ff6b6b` | Inline error text variant | Palette manager |
| `#ff0000`, `#00ff00`, `#0000ff` | RGB primaries | Color math in the picker, mixer, palette manager |

**This table lost two rows on 2026-08-13 and the reason matters.** Status semantics and the
site's status indicator are no longer outside the brand. See the two sections below.

---

## App status — ruled 2026-08-13, no longer borrowed

The brand now issues one answer, and the answer is **Bootstrap's set**: `#28a745` success,
`#ffc107` warning, `#dc3545` error. Canonical in `engine/brand.py` as `STATUS`.

Bootstrap rather than Material because three applications already shipped Bootstrap's values in
source — the picker, the icon builder, the transformer. Choosing the set reality already holds
moved one dict in one file and no pixel anywhere; choosing Material would have made three apps
wrong on the day it landed. Warning was never in dispute; both systems use `#ffc107`.

**What this retires.** The previous claim that "there is no brand ruling on what red or green
means" is gone, and so is "the divergence between the Material and Bootstrap sets is not brand
drift." It is drift now, by decision. `#f44336` and `#4caf50` are the values to remove.

**Known non-conformance, recorded rather than assumed clean.** `rnv-color-picker` carries **both**
sets live: Bootstrap in its `PALETTE` dict and Material in `STATUS_SUCCESS_BG` / `STATUS_ERROR_BG`,
the latter consumed by `ui/settings_panel.py` and `utils/cache.py`. That app was internally
inconsistent before this ruling and nothing compared the two. `rnv-icon-builder` writes `#FFC107`
in uppercase — the same value, but a case-sensitive comparison reads it as drift.

**One measured regression, and the lift that answers it.** `#dc3545` reads 3.84:1 on the app panel
and 3.17:1 on a card — it clears the 3:1 non-text floor for fills, borders and badges but sits
**below the 4.5:1 text floor**, where Material's `#f44336` read 4.73:1 and passed.

`STATUS` therefore carries a fourth value, **`error-text` `#e56b77`**, for dark-theme text only.
Derived by rule rather than picked: hold hue and saturation, raise lightness, take the first step
clearing 4.5:1 on the worst dark ground. The walk is published in `engine/brand.py` beside the
value, in the same spirit as the two tint censuses above — a derived value is publishable without
being permanent, and the source emits it so nobody re-derives it by hand.

It reads **4.58:1 on a card**, 5.55 on panel, 6.70 on window, and **3.13:1 on white**, which fails.
That is why `error` stays `#dc3545` for light mode: one colour, two grounds, the same shape as
`GOLD` and `DARK_GOLD`. Cross-checked through `rnv-color-mcp` rather than trusted to arithmetic.

**It does not conform to the Records order and was not forced to.** Making R > G > B swung it to
`#e56d3c`, burnt orange — a different colour wearing the right lightness. The tint rules govern
the neutral ramps; a borrowed platform value that never conformed should not sprout a derived
variant that does.

---

## The site signal indicator — ruled 2026-08-13, no longer borrowed

`#4ade80` was Tailwind's green, printed on the site with no entry in any source. It is retired.
In its place, `engine/brand.py` carries a three-value **signal** set, distinct from `STATUS`:
`#a5034e` live, `#5a5a72` offline, `#ffd166` down.

**`signal-live` changed on 2026-08-14, from `#8b2c3b` to `#a5034e`.** Hue moved 350.5° to 332.2°
and saturation 52% to 96%. **It was decided on the check that mattered rather than on taste:** a
move toward magenta could have narrowed the gap to the error red, which was always this value's
nearest neighbour in the system, and instead widened it — CIEDE2000 18.22 against `#dc3545`
where the retired value was 17.40. Against the dark-theme error text it reads 25.92. Contrast on
`bg-2` moves 2.37:1 to 2.43:1, immaterial either way, because the ring carries the boundary and
the fill was never asked to.

**"Wine" describes the retired value and should not be carried forward.** At 96% saturation the
current value is not the muted red that word implies, and `engine/brand.py` already uses "wine"
for what it replaced. This file now says `signal-live` or gives the hex. A descriptor that
survives the thing it described starts naming the wrong colour to everyone who reads it.

**Signals are not status.** Status is the result of a user's action inside an app and moves when a
UI framework moves. A signal is the state of something the brand runs and moves when the brand
decides something. `signal-live` means *RNVizion is on*, not *a video stream is broadcasting* — it
carries the availability dot on the site as well as the broadcast dot on `rnv-live`.

**The ring is load-bearing, and since 2026-08-14 it is also still.** Every signal dot is drawn
with a **0.75px** ring, and it carries the WCAG 1.4.11 boundary **at every frame**, because the
fill breathes and the ring does not. That is what frees the fill to sit at 2.43:1. Remove the ring
and every value in the set fails.

**IT IS NO LONGER IDENTICAL IN ALL STATES, AND THAT CHANGED ON 2026-08-23.** It was gold everywhere
and therefore chrome — it signalled nothing. On `rnv-live` it became **stateful**, so every channel
agrees with the label instead of the fill carrying the meaning alone. The site's hero dot is
unaffected: it has one state and is always live, so its ring stays unconditional.

**Four channels, and three of the four order:**

| state | ring | fill | halo | breath |
|---|---|---|---|---|
| live | `signal-ring-live` `#d2bc93` | `signal-live` `#a5034e` | 12px, full | 3s, 0.5 trough |
| standby | `signal-ring-standby` `#ae986f` | `signal-standby` `#ffd166` | 8px, 55% | 5s, 0.7 trough |
| offline | `signal-ring-still` `#9b907a` | `signal-offline` `#5a5a72` | none | still |

```
ring     10.679 > 7.073 > 6.267     orders
halo     12px   > 8px   > none      orders
breath   3s/0.5 > 5s/0.7 > still    orders
fill      2.560 < 13.698 > 2.953    DOES NOT ORDER
```

**The fill carries hue identity, not intensity** — live is a deep wine and standby a bright amber,
so live's fill is the dimmest of the three. The ranking a reader gets comes from ring, halo and
breath. *Every channel steps down* would be a claim this table then inherits, and it is not true.

**The halo is dimmed on standby and that is not taste.** `signal-standby` carries **5.35x** the
luminance contrast of `signal-live` — 13.698 against 2.560 — so a 12px halo of it at full strength
reads *louder* than live's, inverting the ordering the states exist to express.

**Standby breathes, slower and shallower.** Offline means nothing is running; standby means
something is running but is not the main event. Motion reads as life, so making it a **gradient**
rather than a binary is what makes standby a genuine middle state rather than offline in another
colour. The ring does not animate, so the boundary holds at 7.073 at every frame.

**[confirm/fill] Live and standby have never been rendered.** `rnv-live`'s pill carries `OFFLINE`
by default and the other two states are applied by hand-editing markup. Every contrast figure above
is measured; **halo radius and alpha, breath rate and trough depth are eye calls no eye has made on
the real surface.** A state toggle on that page turns an unverifiable design into a checkable one.

**The ring thinned from 1px to 0.75px on 2026-08-14, on both surfaces in one pass.**

| Surface | Ground | Composited at 0.75 coverage | Boundary (1x estimate) |
|---|---|---|---|
| `rnvizion.dev` hero | `bg-2` | `#a19174` | **~6.1:1** |
| `rnv-live` | `bg` | `#a08f72` | **~6.3:1** |

**One decimal, and the condition travels with it.** Two independent measurements of this same
ring disagreed in the second decimal — 6.09 against 6.12, 6.27 against 6.33 — purely on whether
the blend was rounded to a hex before measuring. That difference is smaller than the model's own
uncertainty: a sub-pixel ring's rendered coverage depends on the rasterizer, the device pixel
ratio, and subpixel positioning, and **the figure is unverified below a 3x display.** Digits
beyond the evidence invite a later reader to treat noise as signal.

Sub-pixel spread antialiases rather than vanishing, and partial coverage costs contrast in
proportion. Both clear the 3:1 UI floor by roughly 2x, down from 3.4x. **0.5px was rejected**
at ~3.35:1 — a bare pass with no margin, on the one element carrying the boundary for a fill
that cannot.

**Both surfaces moved together, deliberately, and the reasoning is worth keeping.** Holding
`rnv-live` at 1px was considered and rejected. It would have confined an unverified value to
one surface, but at the cost of a divergence in the one property whose sameness is the stated
justification for a sub-floor fill. **A tracked mismatch becomes intentional by age**, and one
revert later is cheaper than a difference nobody remembers the reason for. The risk is
symmetric either way; the revert is the same one-character change on each.

**[confirm/fill] 0.75px is unverified below 3x, now on both surfaces.** Observed only on a 3x
phone, where it renders 2.25 device pixels; a 1x display gets 0.75 and leans entirely on
antialiasing. **If it reads absent rather than merely finer, revert both to 1px in one pass**
— the fills at 2.43:1 and 2.56:1 cannot replace it. Resolve at the next desktop sighting.

**A dim-end figure used to live in this paragraph and is retired.** While the ring animated with
the fill, the boundary was only as good as the animation's worst frame — 3.35:1 at a 0.5 dip,
2.57:1 at 0.4 — so the keyframe carried a floor. Splitting the fill onto a pseudo-element
removed the coupling and the floor with it. **The number is gone rather than corrected**, which
is the point: a constraint that stops applying should not be left standing as a figure someone
later re-derives a rule from.

**Both surfaces have landed, 2026-08-14.** `rnv-live` took the set in the ruling change;
`rnvizion.dev` followed on 2026-08-14, replacing the hero dot's fill and dropping its outer
glow, since a ring plus a glow is two treatments doing one job and the ring is the one carrying
contrast. `#4ade80` now appears in no RNVizion source. **The reading of a sighting changes with
this:** while the change was outstanding, finding the hex meant unfinished work; finding it now
means a surface has regressed or a new one was built from a stale base. `engine/brand.py`
carries a comment stating the former — it expires with this line.

**The two dots were split on 2026-08-14, in one pass across both surfaces.** The ring moved to
the element and the fill to its `::after`, so only the fill animates. It was done on both at
once deliberately: *one recognisable mark across two mediums* is the stated justification for a
fill sitting under the contrast floor, and a structural change to one dot and not the other
would have quietly retired that justification while leaving the sentence in place.

**The 0.5 dip survived the argument that produced it, and that is worth naming.** It was chosen
as a floor — the shallowest dip the animated ring could take and still clear 3:1. The split
retired the floor, and the value stayed, so it is now held for parity between the two surfaces
and for nothing else. **A number that outlives its reason needs a new one recorded or it will
be defended with the old one.** Change it on one surface and it must change on both.

Sizes are **not** matched and were not made to match: 10px on the site (8px until 2026-08-14,
grown by eye), 0.45rem on `rnv-live`. The two pills differ in type size and padding, so equal
pixels would not read as equal marks. **Ring weight is matched and size is not**, which is not
a contradiction: the ring is the element carrying the accessibility boundary and the thing
the parity claim rests on, while the fill's diameter is tuned per surface by eye.

**Both dots also gained `flex-shrink: 0` on 2026-08-14, and the reason is a defect worth
recording.** The site's hero dot had been rendering as an **ellipse at every viewport width** —
measured at 5.6px wide by 10.4px tall against a specified 10 by 10. Its flex parent was
squeezing it on the main axis while `align-items: center` held its height, and the 1px ring
traced the distortion, which is why each size increase made the outline look heavier rather
than better. It survived three passes of deliberate work on this component because every pass
was about colour. **A component can be audited repeatedly on the axis someone is thinking
about and stay broken on the one nobody is.**
The two pills differ in type size and padding, so equal pixels would not read as equal marks.

**Case is part of the value here, not formatting.** Hex is lowercase in this file and must be
lowercase at the source: a case-sensitive comparison reads `#8B2C3B` and `#8b2c3b` as two
colors, which is precisely the failure recorded one section above about `rnv-icon-builder` and
`#FFC107`. Naming a hazard and then committing it is how a house style stops being one.

**That pair is kept in its original case on purpose, and it was destroyed once already.** A
blind pass ran over this file after rev 12 and replaced `#8B2C3B` here with `#a5034e`, leaving
a sentence claiming a case-sensitive comparison reads two *different colours* as different —
which they are, so the example proved nothing. The same pass lowercased `#FFC107` in the three
places that name it *as the uppercase instance*, and left line 318, the only place that
actually stated a value, carrying a retired one.

**The rule that failure earns: a mechanical pass must skip the sentences that are about the
value being replaced.** A worked example, a "do not write it this way," a before-and-after —
each is a *mention*, and a find-and-replace cannot tell a mention from a use, because in the
text they are the same string. If a file explains a rule about a value's form, that file
cannot be swept for that value; search it, read the hits, edit by hand. In this document
`#ffc107` is lowercase wherever it is used and uppercase wherever a sentence names the
uppercase instance as the fault. **No count of either is published here on purpose** — an
occurrence count changes on every edit, and a figure that moves without a decision is the
kind this file does not carry.

**One legibility note, app-level and not a brand matter:** `#ffc107` reads 1.63:1 on white and
is carried unchanged by all five apps. Amber on white is a known trap; worth a look in
whichever app shows warnings on a light surface.

---

## Gold on light, the one usage constraint the brand keeps

Everything else leaves usage to the surface. This one stays because it protects the identity
color from being used where it stops reading.

**THIS TABLE WAS WRONG AND THE ERROR WAS ONE ROUNDING.** It read `#b19145` on `#ffffff` as
**3.00:1** and granted permissions on that figure. The true value is **2.997638:1** — short of the
3.0 large-text and non-text floors by 0.0024. Every permission below the fill row was void, and
nothing said so, because 3.00 is what a contrast tool *displays*: `rnv-color-mcp` returns `3.0` for
this pair and flags `AA_large_text: false` and `AA_ui_components: false` in the same response. **The
number was read and the flags were not.**

**The instrument is being changed as a result, ruled 2026-08-17 (`24c3fab`):** `ratio` returns the value
unrounded, and `display` shows **three decimals, truncated rather than rounded.** Truncation is the
part that matters — three decimals alone moves the trap without removing it, since a true 4.4996
still *rounds* onto 4.500. A figure that can only err toward *fail* cannot authorise a usage the
value does not support. Routed to the colour chat; the `wcag` flags are unchanged and were always
correct.

**Every other measured figure in this register was audited for the same problem. None sits within
0.02 of a WCAG bar**, so nothing else here could have been rounded across one.

---

### The table above was still incomplete, and the gap was structural

`rnv-text-transformer` found it in implementation: **the table measures gold as a *border* on
`#f5f5f5` and never as *text* on `#f5f5f5`.** Same pair, different floor — 4.1670 clears 3:1 and
fails 4.5:1. That app was doing it in seven places: group box titles, tab labels, button hover
labels, status text, tip text, the current line number.

**Rows are now per surface, not per usage.** The question an app asks is never *"may gold be text?"*
— it is *"may gold be text **here**."*

| ground | `BRAND_DARK_GOLD` `#8c7337` as text | `BRAND_DARK_GOLD_DEEP` `#7e6529` as text |
|---|---|---|
| `#ffffff` | **4.5429 pass** | 5.5547 pass |
| `#fafafa` | 4.3525 fail | 5.3217 pass |
| `#f5f5f5` | 4.1670 fail | 5.0949 pass |
| `#eeeeee` | 3.9156 fail | 4.7875 pass |
| `#e8e8e8` | 3.7078 fail | **4.5334 pass** |
| `#e0e0e0` | 3.4414 fail | 4.2078 fail |
| `#d0d0d0` | 2.9440 fail | 3.6013 fail |

**Below `#e8e8e8`, gold does not carry text.** A ruling, not a missing value.

### Two jobs are mutually exclusive, so a second value is structural

At the 4.5:1 floor, as luminance bands:

```
gold as a FILL with black text     needs  L >= 0.17500
gold as TEXT on #ffffff            needs  L <= 0.18333   overlap, 0.0083 wide
gold as TEXT on #f5f5f5            needs  L <= 0.16402   no overlap
gold as TEXT on #e8e8e8            needs  L <= 0.14043   no overlap
```

`#8c7337` sits at **L 0.18113**, inside the only band that exists — and that band exists on pure
white alone. **No single value can carry text on `#f5f5f5` or darker and also take black as a
fill.** This forecloses a fourth revision of the value.

**And the derivative hits the same wall one step down.** Covering `#d0d0d0` needs −29 → `#6f561a`,
which clears that ground at 4.5054 and then fails black-on-fill at **3.0219**.

### The unit of audit is the pairing, not the value

Every failure in this section has a **correct value on both sides**. `#8c7337` is the ruled gold and
`#f5f5f5` is the ruled surface. **A value census reports it clean** — as every census to date has,
including ones widened to RGB tuples and 8-digit `#AARRGGBB`.

The guard that catches them walks the generated stylesheets, **resolves each foreground against its
real background**, applies the floor, and carries an `ACCEPTED` dict where every exception names its
reason — with a companion test that fails when an entry goes stale. `rnv-text-transformer` shipped it
in roughly forty lines. **That is the ecosystem guard, not another value sweep.**

### The derivation rule, published 2026-08-21 (`60bd56d`)

**The brand holds two golds per mode and derives the rest.** That is the intended structure and a
third registered gold is the wrong fix. What was missing was the **rule**.

```python
lighten(color, step)   # uniform per-channel, clamped 0-255. Holds hue exactly.

BRAND_DARK_GOLD_DEEP = lighten(BRAND_DARK_GOLD, -14)   # #7e6529  light-mode TEXT
BRAND_GOLD_HOVER     = lighten(BRAND_GOLD,       13)   # #dfc9a0  dark-mode HOVER  <- this spelling stands
```

**Published because three applications derived the same value independently** — `rnv-text-transformer`,
`rnv-icon-builder` and `rnv-color-picker` each arrived at `-14` from the same base. As
`rnv-color-picker` put it: **three apps agreeing is luck, not design.** Nothing anywhere would have
caught a fourth picking `-13`.

**An unpublished derivation permits four *values* for one colour, which is worse than four names** —
a wrong name is visible in a diff and a wrong value is not. Same shape as the
`BRAND_GOLD_DARK` → `BRAND_DARK_GOLD` rename, one level down.

**Light pressed is an alias, not a value.** No darker pressed shade keeps black text on light.

**Dark pressed is OPEN and this register does not rule it.** `rnv-text-transformer` derives
`lighten(BRAND_GOLD, -23)`; `rnv-color-picker` returns pressed to the accent in both modes. Both are
legible as fills — black reads 8.79 on the derivative and 11.35 on the accent — so it is not a
contrast question but whether a pressed state must be *visibly distinct*. Until ruled, either is
permitted and an app should say which. **Hand-writing the value is not.**

**Hand-written variants are what this replaces.** They existed in every app as literals and **no two
agreed on method**: `#dcc9a3` at `+10/+13/+16`, `#b7a480` at `−27/−24/−19`, both hue-shifting,
because non-uniform steps do not hold hue. One of them, `#c4a458`, was a tint of a gold **already
retired** — orphaned, still rendering, nothing to flag it. **No contrast check would have: an
orphaned gold can be perfectly legible.**

### The light-mode error text, `#c82131` — published 2026-08-24

`STATUS["error"]` `#dc3545` is a **fill** colour. As text on a light panel it does not clear:

| ground | `#f44336` retired | `#dc3545` ruled | `#e56b77` error-text |
|---|---|---|---|
| `#f5f5f5` light panel | 3.3777 fail | **4.1528 fail** | **2.8745 fail** |
| `#ffffff` | 3.6824 fail | 4.5275 pass | 3.1338 fail |
| `#1a1a1a` dark panel | 4.7263 pass | 3.8441 fail | 5.5537 pass |
| `#2a2a2a` APP card | 3.8978 fail | 3.1703 fail | 4.5801 pass |

**`error-text` is a dark-theme value and applying it to a light panel makes things worse** — 2.8745
against the 3.3777 an app already had. **That advice was given in a handoff note and was wrong.** The
4.58 was measured on the APP card and the 3.84 on the dark panel: both real, **neither the ground the
app draws on.**

**RULED 2026-08-24: `STATUS["error-text-light"]` = `lighten(STATUS["error"], -20)` → `#c82131`.**

| ground | ratio |
|---|---|
| `#ffffff` | 5.6485 |
| `#f5f5f5` | 5.1810 |
| `#eeeeee` | 4.8684 |
| `#e8e8e8` | 4.6100 |

**This heading said the opposite for two days while Brand Book §9 said it was ruled and applied, and
three apps shipped it.** They derived `lighten(STATUS_ERROR, -20)` independently under **two**
identifiers — `STATUS_ERROR_LIGHT` in `rnv-color-picker` and `rnv-text-transformer`,
`STATUS_ERROR_TEXT_LIGHT` in `rnv-color-palette-manager`.

**That is exactly the condition publishing `BRAND_DARK_GOLD_DEEP` was meant to end**, recurring in
another family — and this time an unpublished derivation produced not only a risk of four values but
**two actual names.** The candidate `#d42d3d` this section previously floated is retired: the Book's
value was already ruled, already applied, and measures better.

**Apps: align to `error-text-light`.** The name is the light-mode sibling of `error-text` above and
the pair should read as a pair.

### Hover moves *away* from the ground, in both modes

| | ground | accent | hover | direction |
|---|---|---|---|---|
| dark | `#1a1a1a` | `#d2bc93` | `#dfc9a0` | lighter |
| light | `#f5f5f5` | `#8c7337` | `#7e6529` | **deeper** |

Stated as *away from the ground*, it is one rule for both modes. Stated as *"lighter tint for hover
feedback"* — which is what the apps' local docs said — it is **wrong half the time**. The old light
hover went lighter on a light ground, which is why white on it measured 2.3868. **Expect this in
every app with a light mode; it is inherited, not introduced.**

`BRAND_DARK_GOLD` moved to **`#8c7337`** on 2026-08-17 (`1003a6c`) as a result. Both columns below, so the
trade is visible rather than asserted:

| Usage | Floor | `#b19145` | `#8c7337` |
|---|---|---|---|
| Black on the fill | 4.5:1 | **7.0055** pass | **4.6226** pass |
| Gold as a border on `#ffffff` | 3:1 | **2.9976 FAIL** | 4.5429 pass |
| Gold as a border on `#f5f5f5` | 3:1 | **2.7495 FAIL** | 4.1670 pass |
| Gold as text on `#ffffff` | 4.5:1 | **2.9976 FAIL** | 4.5429 pass |
| White on the fill | 4.5:1 | **2.9976 FAIL** | 4.5429 pass |
| Gold as text on `#eeeeee` | 4.5:1 | **2.5837 FAIL** | **3.9156 FAIL** |
| Gold as text on `#e0e0e0` | 4.5:1 | **2.2700 FAIL** | **3.4400 FAIL** |

**One job of six passed under the old value, not one strongly and three conditionally.** The
"paired with a border or underline" permission failed on its own terms: if gold *is* the border, it
is the same 2.9976 on panel and 2.7495 on the window ground.

**The cost is real and is not hidden.** Black on the fill drops 7.0055 → 4.6226 — headroom traded
on the one job the old value did well, to bring four failing jobs across. The last two rows still
fail and are still not permitted.

**On light, gold fills, bounds and — as of the value change — carries text.** The old rule existed
because the old value could not carry text; it could not carry a border either, which the rule did
not know.

**TEXT ON GOLD: BLACK IS PREFERRED, WHITE IS PERMITTED WHERE IT SERVES A DELIBERATE INVERSION.**
At `#8c7337`, black is 4.6226 and white is 4.5429 — **both clear the 4.5 floor.** Black remains the
default and the better number. **The condition is the value:** at `#b19145` white measured 2.9976
and was *not* permitted, which was a compliance failure rather than a style choice. Ruled at the
request of `rnv-text-transformer`, which asked rather than choosing silently.

At `#8c7337`, black is 4.6226 and white is 4.5429. Black stays
correct and this rule survives the value change untouched. **Three apps paint white on the gold fill
against it** — `rnv-icon-builder`, `rnv-color-picker` and `rnv-text-transformer` — and that is a
separate fix, not something the value change licenses.

**A third artifact carried a fourth version of this.** `rnv-text-transformer/docs/RNV_Brand_Color_System.md`
holds its own contrast table: six of seven rows wrong, five understating harmlessly and one
overstating. It reads `#b19145` / `#ffffff` as **4.0:1, "AA (large text)"** and calls gold-on-white
"sufficient contrast" with none of this register's conditions. **The code implements the doc**:
`accent_text` and `selection_text` are `#ffffff` in that repo's light palette, the second reaching
eight widget classes. That is not drift from this register — it is a false number in a repo's own
document, faithfully followed. **A wrong figure with a citation outranks a right one without.**

---

## Canonical usage, for reference only

**These record where the permanent colors have been used. They are not rules about where
they must be.** A surface layers as its medium requires.

**Apps, dark:** window `#000000` · raised `#1a1a1a` · card `#2a2a2a` · accent `#d2bc93` ·
shade and borders `#b19145` · text on gold `#000000`, with neutral ramp steps between.

**Apps, light:** ground and cards between `#f5f5f5` and `#ffffff` · accent `#b19145` · text
`#000000` · text on gold `#000000`, with ramp steps between. Shipping in all five apps.

**Website:** base `#0a0a0f` with the cool ramp above it; accent `#d2bc93`, no dark gold
anywhere. Secondary accents `#b794ff` and `#ffd166` appear sparingly — **open
[confirm/fill]** on whether either is permanent.

**Social and OG:** `#d2bc93` on `#0a0a0f`; whichever dark reads darkest in the media format
is the correct dark.

---

## Names are local; values are canonical

Three naming schemes exist — `brand.py` kebab roles, `rnv-color-mcp` snake, Qt-shaped names
across the desktop apps — and none has to win. **The brand governs values, not identifiers.**
Consumers keep the names that suit their code; consistency is checked by value rather than by
matching strings across repositories.

One constraint on the source: **a role name may not be a widget name.** A role has to survive
a change of toolkit and be nameable on a hangtag.

### Notation is lowercase — ruled 2026-08-15

**A hex value is written lowercase in source: `#d2bc93`, never `#D2BC93`.** Names are local and
values are canonical; notation is the third axis, and unlike names it does not get to vary by
consumer. `brand.py` standardised on 2026-08-14 and the five desktop apps followed on
2026-08-15 — 357 values across five files, one colour source file per repo.

**This was adopting a convention, not repairing a defect.** The five apps agreed with each other
throughout; nothing rendered incorrectly at any point, and CSS and Qt both treat hex as
case-insensitive. The only inconsistency was against a source that had moved the day before.
That framing is kept because it governs how urgent this ever was, and how urgent the next one is.

**Three things learned doing it, each of which would have cost a day on its own:**

- **A value with no case cannot be normalised.** All-numeric hex (`#123456`) has no case to fold;
  326 such values sit in those five files. A folding pass matches them and reports no change,
  which reads like a broken pass rather than a correct skip. Exclude them from any count.
- **Case and shorthand are different axes.** `#fff` and `#ffffff` name the same colour, and
  expanding shorthand changes string length where folding case does not. **One axis per pass**,
  or a failure in either is indistinguishable from a failure in the other.
- **Prove a mechanical change is what it claims.** Every file was asserted with
  `before.lower() == after.lower()` before writing, so no *value* could move under cover of a
  notation pass. A notation change that silently altered a colour would be invisible in review
  precisely because reviewers stop reading hex closely once they know the diff is cosmetic.

**Now that source and consumers agree, a colour check should compare case-sensitively.** While
they disagreed, folding was the only workable comparison — a case-sensitive guard would have
produced hundreds of findings on its first run and been switched off. Against zero findings the
reasoning inverts: an exact comparison *enforces* the convention, where a folding one passes on
either notation and stops catching a regression. **Nothing caught the day the apps and
`brand.py` disagreed**, which is the argument for arming it.

---

## Resolver vocabulary (MCP)

What the color server resolves brand names to in chat. Defined once in `brand.py` as
`RNV_BRAND`; the resolver imports it. RNV names win over CSS names on collision (so `gold` =
brand gold, not CSS gold); use `css:gold` to force the universal one.

| You say | Resolves to |
|---|---|
| near-black, brand black, rnv black | `#1a1a1a` |
| gold, brand gold, rnv gold | `#d2bc93` |
| dark gold, gold dark, light-mode gold | `#b19145` |

**"near-black" resolves to charcoal `#1a1a1a`, not to the web ground.** The web ground is
`web black`. Both readings were in circulation — this file called `#0a0a0f` "web near-black"
until rev 9, and the Brand Book §0 still does. The resolver keeps the older reading because a
live contract is expensive to repoint and a document is cheap to reword; §0 gets the reword.
Repointing a name to a different value is the one change a resolver must never make quietly.

To teach the server a new brand color: add it to `RNV_BRAND` in `engine/brand.py`, then land
it in each consumer's mirror. **The register above is the test for what belongs there** —
permanent colors only, not ramp steps, not tints, not platform semantics.

### Consumers mirror; nothing propagates

**Each repo carries its own copy of the values it needs, sourced from `rnv-brand` and
corrected when drift is detected.** A program is never one network call away from knowing its
own colors, and a resolver on the hot path never has to answer what happens when a fetch
fails — every available answer there is bad: fail closed and it refuses everything, fall back
and it needs the local copy anyway, guess and it has broken its own rule.

Identifiers are local by design; the check compares values, never names.

**Struck in rev 9: "one edit updates every consumer."** That line survived from rev 1 and was
never true — nothing propagated, and the proof is that the alias `near black` lived in the MCP
mirror and not in the source for a month with nobody the wiser. **A documented mechanism that
was never built is worse than no mechanism, because it tells everyone to stop looking.**

---

## Typography — not here

**Brand Book §3.2 owns type. This file owns color.** The reference list that stood here is
retired rather than corrected, and the distinction matters: it was not a stale copy of a
current fact, it was three retired ones. It gave the wordmark to JetBrains Mono, which
decision #15 took away and gave to Montserrat Black; it wrote body as "Inter / system stack,"
one phrase describing two different things, which F2 split; and it had no row for the mark
face at all.

**A convenience copy is a second canonical entry wearing a disclaimer.** "(reference)" did not
stop this list from being read and followed, and two canonical entries that disagree are
invisible to review — each reads coherently alone. The ownership table at the top of this file
exists to prevent exactly this, and this block was the standing exception to it.

---

## Evidence base

Census run 2026-08-10 across `.py`, `.css`, `.html`, `.js`, `.svg`:

| Surface | `refs/heads/main` |
|---|---|
| `rnvizion.github.io` | `8165e875858360476c1cd7f03f4c7fda0219115f` |
| `rnv-color-palette-manager` | `039abc2f8a32ba3ccfd202befe9772234296ba13` |
| `rnv-color-mixer` | `03169428fd21a4516a02443adfdabbc75fabecff` |
| `rnv-color-picker` | `ce27640da9cb61a63ca15a8cbc3ec53a23f8e6ef` |
| `rnv-icon-builder` | `9d5867eec40783e835fd5e2a67851eff3f774463` |
| `rnv-text-transformer` | `c1912ce5f08dc053c6c60e885e08cc738c797011` |
| `rnv-ask-the-corpus` | `c9f2421d4de34984c76e6342f067da3c477b15cd` |
| `rnv-brand` | `c4d479dbf16b95b21fea80016372a03a64f1c450` |

---

*Two golds, three blacks, one white, and everything else is arithmetic.*

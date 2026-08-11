# RNVizion Brand Colors

The register of RNVizion's **permanent** colors. Machine source: `engine/brand.py`
(import from there; never hardcode). This doc is the human-readable explanation.

Last locked: 2026-08-10 (rev 10 — the two-dark rule re-derived from measurement after the
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
| Dark gold | `#b19145` | 177, 145, 69 | **The accent on light surfaces.** Every app's light theme; also gold's shade on dark, where full gold is too loud |

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
| `#f44336`, `#4caf50`, `#ffc107` | Material | App status semantics |
| `#dc3545`, `#28a745` | Bootstrap | Status semantics in picker, icon builder, transformer |
| `#ff6b6b` | Inline error text variant | Palette manager |
| `#4ade80` | Tailwind | Site status indicator |
| `#ff0000`, `#00ff00`, `#0000ff` | RGB primaries | Color math in the picker, mixer, palette manager |

**Two consequences worth stating.** Status colors are outside the brand, so there is no brand
ruling on what red or green means and no light status trio to decide; the surface follows its
platform. And the divergence between the Material and Bootstrap sets across apps is not brand
drift, because neither set was ever the brand's.

**One legibility note, app-level and not a brand matter:** `#ffc107` reads 1.63:1 on white and
is carried unchanged by all five apps. Amber on white is a known trap; worth a look in
whichever app shows warnings on a light surface.

---

## Gold on light, the one usage constraint the brand keeps

Everything else leaves usage to the surface. This one stays because it protects the identity
color from being used where it stops reading.

| Usage | Ratio | Reading |
|---|---|---|
| Black on a `#b19145` fill | 7.01:1 | Strong; gold's best job on light |
| `#b19145` paired with a border or underline | — | Fine; the border carries the signal |
| `#b19145` text on `#ffffff` | 3.00:1 | At the line; acceptable large, bold, or paired |
| `#b19145` text on `#eeeeee` | 2.58:1 | Thin |
| `#b19145` text on `#e0e0e0` | 2.27:1 | Don't |

**On light, gold fills and bounds; it doesn't carry small text alone.** Existing usage mostly
complies already — selected tabs pair gold with an underline, hover buttons with a border,
pressed states use gold as the fill with black on top.

Text on gold is `#000000` on both surfaces: black on `#b19145` is 7.01:1, white is 3.00:1.

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

## Typography (reference)

- Display: Bricolage Grotesque
- Serif (emphasis / italics): Instrument Serif
- Mono (wordmark, labels, footer): JetBrains Mono
- Body: Inter / system stack

Social and OG-card typography is tracked separately.

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

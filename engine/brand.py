"""RNVizion brand tokens — the machine source for color.

Import it, never hardcode. This file is the only place hex literals may
live (besides the tokens.css it emits). Seeded July 5, 2026 from
BRAND_COLORS.md (locked 2026-06-24) and Brand Book v1.2 (§3.1–3.4).
BRAND_COLORS.md stays the human-readable deep-dive; this is the machine.

Place at: engine/brand.py (empty engine/__init__.py beside it).

Usage:
    python engine/brand.py --css web > tokens.css     # website surface
    python engine/brand.py --css app > tokens.css     # desktop surface
    python engine/brand.py --css records > tokens.css # notes, releases, initiatives
    # or, from Python:
    from engine.brand import RNV_BRAND, WEB, APP, RECORDS, STATUS, emit_css

Register discipline (BRAND_COLORS.md rev 8, 2026-08-10). PERMANENT holds the
six values the brand commits to on any medium, print included. Everything else
here is a ramp step, a tint, an alpha, or a platform convenience — real values
that consumers need, but not brand claims. Adding to PERMANENT is a decision;
adding a ramp step is not.

Consumers mirror, they do not import. Each repo carries its own copy of the
values it needs, sourced from here and corrected when drift is detected, so a
program is never one network call away from knowing its own colors. Identifiers
are local by design (BRAND_GOLD in the MCP mirror, GOLD here); the drift check
compares values, never names.
"""

# ---------------------------------------------------------- canonical trio
# HEX VALUES ARE LOWERCASE IN THIS FILE, WITHOUT EXCEPTION. Standardised
# 2026-08-14, after one value arrived in capitals and sat unnoticed among fifty
# that were not. Case is a convention, not a correctness issue -- the same six
# characters name the same colour either way -- but a case-sensitive comparison
# reads them as different, and this file is what other repositories compare
# themselves against.
#
# NO CAPITALISED HEX APPEARS IN THIS COMMENT ON PURPOSE. Writing the wrong form
# in as an example would leave a rule that violates itself, and any audit
# folding case across this file would trip on its own documentation. Same reason
# profile.json's exemption reasons never name the value they permit.
#
# THE ECOSYSTEM IS NOT UNIFORM AND THIS DOES NOT MAKE IT SO. Two apps -- the
# icon builder and the colour picker -- write their status values capitalised.
# Any guard comparing a surface against this file must fold case, or it reports
# drift that is not there.
GOLD = "#d2bc93"         # brand gold (primary) — never varies across surfaces
DARK_GOLD = "#b19145"    # dark gold (light-mode accent)
BRAND_BLACK = "#1a1a1a"  # brand black (charcoal)

# ------------------------------------------------- the rest of the register
# Named because they are permanent, not because a palette happened to use
# them. TRUE_BLACK and WHITE were already in APP and in every light theme as
# bare literals; WEB_BLACK existed only as WEB["bg"] (named bg-0 until 2026-08-13).
TRUE_BLACK = "#000000"   # app window ground; text on gold, on either surface
WHITE = "#ffffff"        # light-surface cards and inputs; the ramp's far anchor
WEB_BLACK = "#0a0a0f"    # rnvizion.dev ground; social and OG base

# The six the brand commits to. Gold on dark, dark gold on light; dark gold is
# additionally gold's shade on dark, where full gold is too loud.
PERMANENT = {
    "gold": GOLD,
    "dark-gold": DARK_GOLD,
    "charcoal": BRAND_BLACK,
    "black": TRUE_BLACK,
    "web-black": WEB_BLACK,
    "white": WHITE,
}

# --------------------------------------------------------------- alpha helper
# Defined here rather than beside the emitter because the RECORDS palette
# derives a value from it. Alpha modulates; it never mints a color.
def _rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


RULE_ALPHA = 0.18      # hairline gold rules at low alpha (Brand Book §3.4)
GOLD_DIM_ALPHA = 0.52  # secondary gold, Records surface

# -------------------------------------------------- desktop / app palette
# The two-dark rule: apps run neutral dark (true-black window, charcoal
# panels); the website runs the blue-tinted ramp. Intentional, not drift.
APP = {
    "window": TRUE_BLACK,
    "panel": BRAND_BLACK,
    "card": "#2a2a2a",
    "border": "#333333",
    "text": "#e0e0e0",
    "text-dim": "#aaaaaa",
    "accent": GOLD,
    "accent-light-mode": DARK_GOLD,
    "text-on-gold": TRUE_BLACK,
}

# ---------------------------------------------- website palette (the ramp)
WEB = {
    # ONE-INDEXED, WITH NO bg-1, because that is what the eleven published
    # pages on rnvizion.dev already call these three colours. Decided
    # 2026-08-13: the source moved to the surface, not the surface to the
    # source. The gap in the sequence is the honest cost of describing a live
    # thing accurately instead of tidily.
    "bg": WEB_BLACK,
    "bg-2": "#11111a",
    "bg-3": "#1a1a26",
    "border": "#25253a",
    "border-soft": "#1e1e2e",
    "text": "#e8e8f0",
    "text-dim": "#9a9ab0",
    "text-faint": "#5a5a72",
    "accent": GOLD,
    "accent-violet": "#b794ff",  # secondary, sparing
    "accent-warm": "#ffd166",    # secondary, sparing
    # ---- signals ---------------------------------------------------------
    # Brand signals: the state of a THING the brand runs. Not STATUS below,
    # which is the result of a user's action in an app. Different job, different
    # lifecycle, different owner -- STATUS moves when a UI framework moves, these
    # move when the brand decides something.
    #
    # THE RING IS NOT IN HERE, AND THAT IS THE DESIGN. Every signal dot is drawn
    # with a 1px `gold` ring, identical in all states, so the ring signals
    # nothing -- it is the component's chrome. It carries the WCAG 1.4.11
    # boundary at 10.68:1 on bg and 3.35:1 at the breathe animation's dim end,
    # which is what frees the FILL to be whatever the brand wants, including
    # values that could never carry it alone. Drop the ring and every value below
    # fails. Measured 2026-08-13; re-measure if the ring or the ground moves.
    #
    # signal-live is 2.56:1 on bg and 2.43:1 on bg-2. DELIBERATELY under the
    # floor, and defensible for two reasons that are now independent: the pill
    # carries the word, and since 2026-08-14 the ring sits on its own element
    # and no longer animates -- it holds 10.68:1 at EVERY frame rather than
    # 3.35:1 at the trough. The 0.5 dip is an aesthetic choice held in common
    # across two surfaces, not a contrast floor. Colour is the third signal.
    #
    # Value changed 2026-08-14 from an earlier wine at hue 351, on the check
    # that mattered rather than on taste: a move toward magenta could have
    # narrowed the gap to STATUS.error and instead widened it -- CIEDE2000 18.22
    # against the error red where the wine was 17.40, and 25.92 against
    # error-text. The error red was always this value's nearest neighbour.
    #
    # signal-offline and signal-down happen to equal text-faint and accent-warm.
    # THE MATCH IS INCIDENTAL AND THE SEAM IS DELIBERATE: text-faint moves for
    # legibility reasons and accent-warm for decorative ones, and neither should
    # drag a signal with it. Do not "de-duplicate" these.
    #
    # Retires #4ade80, the green these replace on rnvizion.dev and rnv-live.
    # Until both surfaces land the change they carry a hex this file no longer
    # defines, and an audit finding that is the work being unfinished, not a bug.
    # signal-live means "RNVizion is on", NOT "a video stream is broadcasting".
    # Widened deliberately 2026-08-13: it carries the availability dot on
    # rnvizion.dev ("open to roles") as well as the broadcast dot on rnv-live.
    # Two different mediums, one recognisable mark -- the adjacent WORD carries
    # the specific meaning on each, the colour carries the presence. That is the
    # same argument that lets the fill sit under the contrast floor: colour is
    # never the only signal here. Keeping the name "live" because it is the
    # brand's own word for this (rnv-live, "RNVizion · live"), not because it is
    # the narrower reading.
    "signal-live": "#a5034e",      # on air / open / present
    "signal-offline": "#5a5a72",   # receding by design; the absent state
    "signal-down": "#ffd166",      # service degraded or unavailable
}

# RESOLVED 2026-08-13. This ramp was named bg-0 / bg-1 / bg-2 while eleven
# published pages called the same three colours --bg / --bg-2 / --bg-3. Values
# identical, nothing rendered wrong -- the collision was that "bg-2" meant
# #11111a to the site and #1a1a26 here, so anyone reading this file and editing
# a page picked the wrong step.
#
# HOW IT SURVIVED, which is the part worth keeping: a checker comparing the SET
# of hexes finds nothing, because every value was canonical. The needle has to
# be the name-to-value BINDING. That is "60" matching a CSS font weight, one
# layer up, and it means a colour guard written against values alone would have
# been armed and blind.
#
# THE RENAME IS NOT FREE AND THE COST IS REAL: emit_css() derives CSS custom
# property names straight from these keys, so rnv-live's generated tokens.css
# renames with them. Its index.astro references --rnv-bg-0 and --rnv-bg-1 by
# name; landing this file without landing that one leaves three var() calls
# resolving to nothing, a page that deploys with no background, and no guard
# anywhere in the path -- rnv-live's own check only asserts hexes stay in
# tokens.css, never that a var() resolves. THE TWO CHANGES SHIP TOGETHER.

WEB_RAMP = (WEB["bg"], WEB["bg-2"], WEB["bg-3"])  # never flatten to charcoal

# ------------------------------------------------------- Records (warm ink)
# Notes, patch notes, updates, newsletters, initiative pages — what RNVizion
# issues and a reader consults later. Same ground and same gold as the site;
# only the ink changes. Established by the AIII page, 2026-08-10.
#
# The cool ramp lifts blue (R = G, B raised); this one warms (R > G > B).
# CONSTRAINT, carried with the value: ink-faint reads 3.77:1 on WEB_BLACK.
# That clears large text and UI components; it does NOT clear the 4.5 floor
# for normal text. Labels only, never body.
RECORDS = {
    "bg": WEB_BLACK,
    "surface": "#13131c",
    "surface-2": "#0f0f17",
    "ink-bright": "#efece2",   # ledes and opening paragraphs
    "ink": "#e7e3d8",          # body, headings, names
    "ink-mute": "#9b978c",     # bylines, definitions, footer links
    "ink-faint": "#6f6c64",    # kickers and small labels ONLY — see above
    "accent": GOLD,
    "gold-dim": _rgba(GOLD, GOLD_DIM_ALPHA),
}

# ---------------------------------------------------------- status (app)
# RULED 2026-08-13. The brand now issues one answer for app status semantics,
# and the answer is BOOTSTRAP'S SET. The previous comment here said the brand
# "neither owns them nor varies them, and issues no ruling on what red means" --
# that sentence is retired, because unifying IS the ruling, and leaving the
# disclaimer beside a decision would have invited the next reader to undo it.
#
# WHY BOOTSTRAP AND NOT MATERIAL: three applications already shipped Bootstrap's
# values in source -- rnv-color-picker (utils/config.py), rnv-icon-builder
# (ui/colors.py), rnv-text-transformer (utils/dialog_styles.py). Choosing the
# set that reality already holds moves one dict in one file and no pixel
# anywhere. Choosing Material would have made three apps wrong on the day it
# landed, each fix in someone else's repository. Warning was never in dispute:
# both systems use #ffc107.
#
# THE COUNT WAS WRONG HERE UNTIL TODAY. This comment said "two apps"; the table
# in BRAND_COLORS.md in this same repository said picker, icon builder and
# transformer, and it was right. Two documents in one repo disagreed and the
# wrong one was the one people read first. Nothing checks prose against prose.
#
# MEASURED CONSTRAINTS, carried with the values rather than assumed:
#   #ffc107  1.63:1 on white  -- dark-tuned. Re-check before any light use.
#   #dc3545  3.84:1 on APP panel, 3.17:1 on APP card. Clears the 3:1 non-text
#            floor for fills, borders and badges; BELOW the 4.5:1 text floor.
#            Material's #f44336 read 4.73:1 on panel and did pass as text, so
#            this ruling is a REGRESSION for that one use. Do not set #dc3545
#            as body text on panel or card -- use it as a fill behind #ffffff,
#            or lighten it for a text variant and record the lift here.
#   #28a745  4.58:1 on APP card -- passes as text, with little margin.
STATUS = {
    "success": "#28a745",
    "warning": "#ffc107",
    "error": "#dc3545",
    # DERIVED, and the steps are published because a consumer that has to guess
    # will guess differently. Same discipline as the two tint censuses in
    # BRAND_COLORS.md: a derived value is publishable without being permanent,
    # and the source emits it so nobody re-derives it by hand.
    #
    #   rule    hold hue and saturation, raise lightness only
    #   target  4.5:1 on the WORST dark ground the value lands on, APP card
    #   walk    L 0.50 #d92637 2.93 · 0.55 #dd3b4b 3.28 · 0.58 #df4857 3.56
    #           L 0.60 #e1515f 3.79 · 0.62 #e25a67 4.03 · 0.65 #e56b77 4.58 <-
    #   taken   the first step that clears, not the first that looks right
    #
    # MEASURED, cross-checked against rnv-color-mcp rather than trusted:
    #   4.58:1 on APP card, 5.55 panel, 6.70 window -- AA normal text passes.
    #   3.13:1 on white -- AA normal text FAILS, which is why `error` above
    #   stays as-is for light mode. This is a dark-theme value, not a
    #   replacement. Same shape as GOLD / DARK_GOLD: one colour, two grounds.
    #   CIEDE2000 26.55 from signal-live, "clearly different" -- the error text
    #   and the live wine cannot be confused, which was the open question when
    #   red was chosen for the live signal.
    #
    # NOT made Records-conformant. Forcing R > G > B swung it to #e56d3c, burnt
    # orange, CIEDE2000 far off the base -- a different colour wearing the right
    # lightness. The tint rules govern the neutral ramps; #dc3545 is a borrowed
    # platform value that never conformed to either register, and a derived
    # variant that conforms while its base does not makes the pair incoherent.
    "error-text": "#e56b77",
}

# ------------------------------------------------------- texture + type
TYPE = {
    "display": "Bricolage Grotesque",
    "mono": "JetBrains Mono",
    "serif-italic": "Instrument Serif",
    "body": "Inter",
}

# ---------------------------------------- resolver contract (rnv-color-mcp)
# The documented MCP interface (BRAND_COLORS.md, "Resolver vocabulary"):
# the color server imports RNV_BRAND; RNV names win over CSS names on
# collision; css:gold forces the universal one.
#
# NOTHING PROPAGATES. Consumers carry their own mirror of this vocabulary and
# are corrected when drift is detected; a change here reaches them only when a
# human lands it there. "One edit updates every consumer" was a claim, never a
# mechanism, and the proof is that "near black" lived in the mirror and not
# here for a month with nobody the wiser.
#
# VOCABULARY NOTE: "near-black" resolves to CHARCOAL, not to the web ground.
# The web ground is "web black". Both readings of "near-black" were in use
# across artifacts; this contract keeps the older one because a live resolver
# is expensive to repoint and a document is cheap to reword.
#
# "white" and "black" shadow CSS names at identical values, so resolution is
# unchanged either way; they are here because the register names them.
RNV_BRAND = {
    "near-black": BRAND_BLACK,
    "near black": BRAND_BLACK,
    "brand black": BRAND_BLACK,
    "rnv black": BRAND_BLACK,
    "charcoal": BRAND_BLACK,
    "gold": GOLD,
    "brand gold": GOLD,
    "rnv gold": GOLD,
    "dark gold": DARK_GOLD,
    "gold dark": DARK_GOLD,
    "light-mode gold": DARK_GOLD,
    "black": TRUE_BLACK,
    "true black": TRUE_BLACK,
    "white": WHITE,
    "brand white": WHITE,
    "web black": WEB_BLACK,
}

# ---------------------------------------------------------------- emitter
def tokens(surface: str = "web") -> dict[str, str]:
    """Flat token map for one surface; the emitter's source of truth."""
    palettes = {"web": WEB, "app": APP, "records": RECORDS}
    if surface not in palettes:
        raise ValueError("surface must be 'web', 'app', or 'records'")
    return {
        "gold": GOLD,
        "gold-dark": DARK_GOLD,
        "black": BRAND_BLACK,
        **palettes[surface],
        "rule": _rgba(GOLD, RULE_ALPHA),
        **{f"status-{name}": value for name, value in STATUS.items()},
        **{f"font-{role}": f'"{family}"' for role, family in TYPE.items()},
    }


def emit_css(surface: str = "web", prefix: str = "rnv") -> str:
    """CSS custom properties for one surface, ready for tokens.css."""
    lines = [":root {"]
    lines += [f"  --{prefix}-{name}: {value};" for name, value in tokens(surface).items()]
    lines.append("}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import sys

    if "--css" in sys.argv:
        i = sys.argv.index("--css")
        surface = sys.argv[i + 1] if len(sys.argv) > i + 1 else "web"
        sys.stdout.write(emit_css(surface))
    else:
        sys.exit("usage: python engine/brand.py --css [web|app|records] > tokens.css")

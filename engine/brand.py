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
GOLD = "#d2bc93"         # brand gold (primary) — never varies across surfaces
DARK_GOLD = "#b19145"    # dark gold (light-mode accent)
BRAND_BLACK = "#1a1a1a"  # brand black (charcoal)

# ------------------------------------------------- the rest of the register
# Named because they are permanent, not because a palette happened to use
# them. TRUE_BLACK and WHITE were already in APP and in every light theme as
# bare literals; WEB_BLACK existed only as WEB["bg-0"].
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
    "bg-0": WEB_BLACK,
    "bg-1": "#11111a",
    "bg-2": "#1a1a26",
    "border": "#25253a",
    "border-soft": "#1e1e2e",
    "text": "#e8e8f0",
    "text-dim": "#9a9ab0",
    "text-faint": "#5a5a72",
    "accent": GOLD,
    "accent-violet": "#b794ff",  # secondary, sparing
    "accent-warm": "#ffd166",    # secondary, sparing
}

WEB_RAMP = (WEB["bg-0"], WEB["bg-1"], WEB["bg-2"])  # never flatten to charcoal

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
# NOT brand colors. Material's semantics, adopted deliberately because they
# fit the platform; the brand neither owns them nor varies them, and issues no
# ruling on what red means. Published here so the apps share one answer.
# Two apps ship Bootstrap's set instead; that is a platform choice, not drift.
# Dark-tuned: #ffc107 reads 1.63:1 on white. Re-check before any light use.
STATUS = {
    "success": "#4caf50",
    "warning": "#ffc107",
    "error": "#f44336",
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

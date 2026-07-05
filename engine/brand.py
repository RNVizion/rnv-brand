"""RNVizion brand tokens — the machine source for color.

Import it, never hardcode. This file is the only place hex literals may
live (besides the tokens.css it emits). Seeded July 5, 2026 from
BRAND_COLORS.md (locked 2026-06-24) and Brand Book v1.2 (§3.1–3.4).
BRAND_COLORS.md stays the human-readable deep-dive; this is the machine.

Place at: engine/brand.py (empty engine/__init__.py beside it).

Usage:
    python engine/brand.py --css web > tokens.css   # website surface
    python engine/brand.py --css app > tokens.css   # desktop surface
    # or, from Python:
    from engine.brand import RNV_BRAND, WEB, APP, STATUS, emit_css
"""

# ---------------------------------------------------------- canonical trio
GOLD = "#d2bc93"         # brand gold (primary) — never varies across surfaces
DARK_GOLD = "#b19145"    # dark gold (light-mode accent)
BRAND_BLACK = "#1a1a1a"  # brand black (charcoal)

# -------------------------------------------------- desktop / app palette
# The two-dark rule: apps run neutral dark (true-black window, charcoal
# panels); the website runs the blue-tinted ramp. Intentional, not drift.
APP = {
    "window": "#000000",
    "panel": BRAND_BLACK,
    "card": "#2a2a2a",
    "border": "#333333",
    "text": "#e0e0e0",
    "text-dim": "#aaaaaa",
    "accent": GOLD,
    "accent-light-mode": DARK_GOLD,
    "text-on-gold": "#000000",
}

# ---------------------------------------------- website palette (the ramp)
WEB = {
    "bg-0": "#0a0a0f",
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

# ---------------------------------------------------------- status (app)
STATUS = {
    "success": "#4caf50",
    "warning": "#ffc107",
    "error": "#f44336",
}

# ------------------------------------------------------- texture + type
RULE_ALPHA = 0.18  # hairline gold rules at low alpha (Brand Book §3.4)

TYPE = {
    "display": "Bricolage Grotesque",
    "mono": "JetBrains Mono",
    "serif-italic": "Instrument Serif",
    "body": "Inter",
}

# ---------------------------------------- resolver contract (rnv-color-mcp)
# The documented MCP interface (BRAND_COLORS.md, "Resolver vocabulary"):
# the color server imports RNV_BRAND; RNV names win over CSS names on
# collision; css:gold forces the universal one. Add a color here, push,
# and every consumer updates from the one edit.
RNV_BRAND = {
    "near-black": BRAND_BLACK,
    "brand black": BRAND_BLACK,
    "rnv black": BRAND_BLACK,
    "gold": GOLD,
    "brand gold": GOLD,
    "rnv gold": GOLD,
    "dark gold": DARK_GOLD,
    "gold dark": DARK_GOLD,
    "light-mode gold": DARK_GOLD,
}

# ---------------------------------------------------------------- emitter
def _rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def tokens(surface: str = "web") -> dict[str, str]:
    """Flat token map for one surface; the emitter's source of truth."""
    palettes = {"web": WEB, "app": APP}
    if surface not in palettes:
        raise ValueError("surface must be 'web' or 'app'")
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
        sys.exit("usage: python engine/brand.py --css [web|app] > tokens.css")

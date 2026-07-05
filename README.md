# rnv-brand

The machine source for RNVizion brand tokens. Import it; never hardcode.

`engine/brand.py` holds the canonical values: the gold, the two darks, both
surface palettes, status colors, type roles, and the `RNV_BRAND` resolver
vocabulary. Every RNV surface (site, apps, MCP servers, OG images) is meant to
consume this file; one edit updates every consumer.

## Usage

    python engine/brand.py --css web > tokens.css   # website surface (the ramp)
    python engine/brand.py --css app > tokens.css   # desktop surface

From Python:

    from engine.brand import RNV_BRAND, WEB, APP, STATUS, emit_css

## The rules

- The gold (`#d2bc93`) never varies across surfaces.
- The two-dark rule is intentional: apps run true black and charcoal; the
  website runs the blue-tinted ramp. Never flatten one into the other.
- Hex literals live here and in the emitted `tokens.css`; nowhere else.
- This repo holds tokens only: never a key, never a secret.

## License

None, deliberately. The source is visible for transparency; no reuse rights
are granted. All rights reserved.

The human-readable deep-dive is `BRAND_COLORS.md`; the identity system is the
RNVizion Brand Book.

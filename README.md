# rnv-brand

The machine source for RNVizion brand tokens. Import it; never hardcode.

`engine/brand.py` holds the values every RNV surface consumes: the two golds, the darks,
the surface palettes, type roles, and the `RNV_BRAND` resolver vocabulary. Every RNV surface
(site, apps, MCP servers, OG images) is meant to consume this file; one edit updates every
consumer.

## Usage

    python engine/brand.py --css web > tokens.css   # website surface (the ramp)
    python engine/brand.py --css app > tokens.css   # desktop surface

From Python:

    from engine.brand import RNV_BRAND, WEB, APP, STATUS, emit_css

## Who owns what

| Artifact | Owns |
|---|---|
| RNVizion Brand Book §3.1 | The summary and the fact that a ruling exists |
| `BRAND_COLORS.md` | The register, the rules, the exclusions, and the reasoning |
| `engine/brand.py` | The values |

A value is stated once, here. `BRAND_COLORS.md` points at it rather than restating it.

## The rules

- **Six values are permanent** — gold `#d2bc93`, dark gold `#b19145`, true black `#000000`,
  charcoal `#1a1a1a`, web near-black `#0a0a0f`, white `#ffffff`. A color is permanent if the
  brand will use it again on any medium, including a printed one.
- **Gold on dark, dark gold on light.** Dark gold is additionally gold's shade on dark, where
  full gold is too loud.
- **The two-dark rule is intentional:** apps run true black and charcoal; the website runs the
  blue-tinted ramp. Never flatten one into the other.
- **Ramps are rules, not lists.** App neutrals are one pure-grey ramp between black and white;
  the website is that ramp with a blue lift; **Records** is that ramp with a warm one. Steps
  are modulations, and a modulation is not a brand color.
- **Alpha modulates, it never mints.** A dark may be thinned; it may not be re-hued.
- **Status colors are outside the brand.** The `STATUS` dict is a shared convenience for the
  apps, not a brand claim; the values are platform semantics and the brand issues no ruling on
  them.
- Hex literals live here and in the emitted `tokens.css`; nowhere else.
- This repo holds tokens only: never a key, never a secret.

## License

None, deliberately. The source is visible for transparency; no reuse rights
are granted. All rights reserved.

The human-readable deep-dive is `BRAND_COLORS.md`, in this repo; the identity system is the
RNVizion Brand Book.
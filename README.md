# rnv-brand

The machine source for RNVizion brand tokens. Import it; never hardcode.

`engine/brand.py` holds the values every RNV surface consumes: the two golds, the darks,
the surface palettes, type roles, and the `RNV_BRAND` resolver vocabulary.

**Consumers mirror; nothing propagates.** Each repo carries its own copy of the values it
needs, sourced from here and corrected when drift is detected, so a program is never one
network call away from knowing its own colors. Identifiers are local by design; the check
compares values, never names.

## Usage

    python engine/brand.py --css web > tokens.css   # website surface (the ramp)
    python engine/brand.py --css app > tokens.css   # desktop surface
    python engine/brand.py --font-faces /fonts/ > fonts.css   # @font-face rules for engine/fonts/, served at /fonts/

From Python:

    from engine.brand import RNV_BRAND, WEB, APP, STATUS, emit_css, fonts_dir, font_faces

The brand's five faces ship in `engine/fonts/`, one `woff2` file for every role, weight and style
`TYPE` names. A consumer serves that folder and passes its URL to `font_faces()`. Why, and what the
guard on the folder does and does not check: `BRAND_TYPE.md`, *The font files*.

## Who owns what

| Artifact | Owns |
|---|---|
| RNVizion Brand Book §3.1 | The summary and the fact that a ruling exists |
| `BRAND_COLORS.md` | The register, the rules, the exclusions, and the reasoning |
| `engine/brand.py` | The values |

A value is stated once, here. `BRAND_COLORS.md` points at it rather than restating it.

## The rules

- **The permanent values are `PERMANENT` in `engine/brand.py`**, and this file does not list or
  count them: it said six until 2026-10-18, when the dict held ten. A color is permanent if the
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

**The font files in `engine/fonts/` are the exception, and they are not ours.** Each face is under
the SIL Open Font License 1.1, whose text sits beside its files and ships with them.

The human-readable deep-dive is `BRAND_COLORS.md`, in this repo; the identity system is the
RNVizion Brand Book.

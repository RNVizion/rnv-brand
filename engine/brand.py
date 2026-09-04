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
program is never one network call away from knowing its own colors. The drift
check still compares values, never names.

IDENTIFIERS ARE NO LONGER LOCAL BY DESIGN -- retired 2026-08-17 (234dca6). That rule let a
mirror name a value whatever suited it, on the grounds that only values were
canonical, and it produced four conventions for one colour across six repos:
BRAND_GOLD_DARK in three apps, _GOLD_BRAND in the mixer, bare literals in the
transformer, and DARK_GOLD here. The names are BRAND_GOLD and BRAND_DARK_GOLD
everywhere now, this file included. A brand system that cannot hold one
identifier across its own repos is not positioned to align anyone else's.
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
# SOURCE AND CONSUMERS NOW AGREE, as of 2026-08-15. The five desktop apps were
# normalised the day after this file was, so for the first time notation is
# common across the ecosystem rather than a convention one file kept alone.
#
# THAT INVERTS THE COMPARATOR CHOICE. While they disagreed, a colour guard had
# to fold case or it would have reported hundreds of findings on its first run
# and been switched off. Against zero findings the reasoning reverses: an exact
# comparison ENFORCES the convention, where a folding one passes on either
# notation and stops catching a regression.
#
# TWO CAVEATS, both of which decide scope before comparator. Roughly fifty
# capitalised values survive OUTSIDE the five colour files -- arbitrary test
# fixtures, plus six instances of a value this file does define, all in test
# files. So a guard scoped to the colour sources can compare exactly and start
# clean; one folded into a whole-repo walk cannot. And the apps are slated to
# move their colour definitions into a single colors.py per repo, so the
# file-to-repo map a guard would enumerate today is temporary.
#
# NOTHING CAUGHT THE DAY THE TWO SIDES DISAGREED. Not a checker failure -- no
# checker was ever pointed at notation. Same shape as type before R2.
# ------------------------------------------------------ how stamps are written
# EVERY DATE IN THIS FILE IS THE CLOCK OF THE COMMIT THAT SHIPPED ITS SUBJECT,
# not the day someone wrote the comment. Where the commit is known it is cited
# beside the date, because a short SHA is checkable and a date is not.
#
# THIS RULE EXISTS BECAUSE THE FILE WAS WRONG TWICE, IN OPPOSITE DIRECTIONS.
# First: an assistant stamped twenty-six artifacts across one session without
# ever calling a clock, inferring each date from context. Then, correcting that,
# it re-dated every 08-17 stamp to "today" -- WITHOUT ASKING GIT EITHER. Three of
# those had been right: the 17th happened, seven commits carry that date, and
# `#8c7337` demonstrably first shipped in 8911f30 on it.
#
# THE SECOND PASS REPEATED THE METHOD OF THE FIRST. Both trusted the narrative
# over the clock, and the clock was one command away:
#
#   git log --format="%h %ad" --date=short -S "<the subject>" -- engine/brand.py
#
# A FABRICATED NARRATIVE DOES NOT FABRICATE THE CLOCK. Shipping stamps a change
# even when the narrator's calendar is wrong, which is exactly why the shipped
# stamps were the recoverable ones. Correct PER STAMP against the commit that
# shipped its subject; "today" is right only for a stamp about today.

# --------------------------------------------------- how figures are written
# EVERY RATIO IN THIS FILE IS TRUNCATED, NOT ROUNDED, AND THE REASON IS THE
# DIRECTION OF THE ERROR. Every contrast check here is a FLOOR -- value must be
# at least T. Truncating can only ever understate a pass; rounding can
# MANUFACTURE one:
#
#   #697f5a on --rnv-bg   true 4.499572...
#     truncated 4.499  -> reads FAIL   correct, and matches the server's flag
#     rounded   4.500  -> reads PASS   a false all-clear from arithmetic alone
#
# A false all-clear is worse than a false failure. This is the same failure that
# retired #b19145: a figure rounded ACROSS the threshold it was authorising.
#
# THE BOUNDARY, WRITTEN DOWN WHILE IT IS IN VIEW. Truncation is conservative for
# a FLOOR and PERMISSIVE for a CEILING. Every check in this system today is a
# floor -- contrast minimums, minimum dE separation from STATUS.error, minimum dE
# between ring states. **But a ceiling already exists in this file**: the claim
# that a derivative "holds hue within a degree" is |dH| <= 1.0.
#
#   BRAND_STILL_GOLD    |dH| 0.952381 from BRAND_GOLD   truncates to 0.9, passes
#   a hypothetical      |dH| 1.040000                   truncates to 1.0, PASSES
#                                                       and should not
#
# It has slack today and would not announce itself when it stops. THE GENERAL
# RULE IS NOT "TRUNCATE" -- it is ROUND IN THE DIRECTION THAT MAKES THE ASSERTION
# HARDER TO SATISFY. Down for a floor, up for a ceiling. Truncation is that rule
# applied to floors, and it silently flips from safe to unsafe the first time a
# ceiling check appears.
#
# Raised by rnv-color-mcp on 2026-08-23, correcting its own earlier note that had
# called the server's truncation a bias. The truncation was right; the rounding
# was the error.

# ---------------------------------------------------------- naming convention
# GOLD SITS IN THE THIRD SLOT. Everything before it modifies it; a fourth word
# marks a DERIVATIVE OR A STATE of the three-word name to its left.
#
#   BRAND_GOLD               the base
#   BRAND_DARK_GOLD          a named gold -- the light-mode one
#   BRAND_STILL_GOLD         a named gold -- stillness, registered
#   BRAND_STANDBY_GOLD       a named gold -- standby, derived by rule
#   BRAND_DARK_GOLD_DEEP     a DERIVATIVE of BRAND_DARK_GOLD
#   BRAND_GOLD_HOVER         a STATE of BRAND_GOLD
#   BRAND_DARK_GOLD_HOVER    the same state, of BRAND_DARK_GOLD
#
# THE TEST IS NOT "IS IT DERIVED", IT IS "DOES IT EXIST WITHOUT ANOTHER GOLD".
# BRAND_STANDBY_GOLD is computed by rule and is still a role the brand names --
# standby is a thing the brand HAS. Hover is not: there is no hover without
# something to hover over, and DEEP has no meaning without the DARK_GOLD it is
# taken from. The fourth word marks dependency.
#
# THIS RULING WAS WRONG WHEN FIRST WRITTEN, ON BOTH HALVES, AND IS CORRECTED
# HERE. As shipped 2026-08-23 (996eade) it listed BRAND_GOLD_HOVER among the
# roles and claimed "it retires nothing in the apps".
#
#   1. IT RETIRED AN IDENTIFIER IN FIVE OF SIX REPOSITORIES -- 43 occurrences of
#      BRAND_GOLD_HOVER and GOLD_HOVER, every one holding #dfc9a0. The claim was
#      made after checking that BRAND_DARK_GOLD_DEEP fits and NOT checking the
#      identifier the same commit was renaming. The check that ran covered the
#      half that was easy; practices doc section 4.
#
#   2. IT LEFT THE LIGHT-MODE COUNTERPART UNSPELLABLE. If hover is a three-word
#      role, its dark-gold sibling is BRAND_DARK_HOVER_GOLD -- four words with
#      gold in the FOURTH slot, which this convention forbids. As a state it is
#      BRAND_DARK_GOLD_HOVER, gold third, and both modes spell symmetrically.
#      A convention tested against one example is a convention tested against
#      the example that suggested it.
#
# The apps' spelling was right and BRAND_COLORS.md's was right. The source was
# the outlier, and reverting costs one file rather than five repositories.
BRAND_GOLD = "#d2bc93"         # brand gold (primary) — never varies across surfaces
# FOR LIGHT-MODE SURFACES. It is darker BECAUSE the ground is lighter -- the name
# describes the colour, this note describes the job, and the two read as
# opposites to anyone meeting the name cold.
#
# VALUE CHANGED 2026-08-17 (8911f30): #b19145 -> #8c7337. THE REASON IS NOT "the old value
# was low", it is that a rounded figure was rounded ACROSS the threshold it was
# being used to authorise. BRAND_COLORS.md recorded gold-on-white as 3.00:1 and
# permitted it "large, bold, or paired" on that basis. The true figure is
# 2.997638:1 -- short of the 3.0 large-text and non-text floors by 0.0024. Every
# permission built on that row was void, and nothing said so because 3.00 is what
# a contrast tool DISPLAYS. rnv-color-mcp returns 3.0 for this pair and flags
# AA_large_text false and AA_ui_components false in the same response. The number
# was read; the flags were not.
#
# WHAT #b19145 ACTUALLY DID, measured against each job's own floor:
#
#   as TEXT on #ffffff          4.5 floor   2.9976 FAIL  ->  4.5429 pass
#   as TEXT on #eeeeee          4.5 floor   2.5837 FAIL  ->  3.9156 FAIL (both)
#   as a BORDER on #ffffff      3.0 floor   2.9976 FAIL  ->  4.5429 pass
#   as a BORDER on #f5f5f5      3.0 floor   2.7495 FAIL  ->  4.1670 pass
#   as a FILL, black on it      4.5 floor   7.0055 pass  ->  4.6226 pass
#   as a FILL, white on it      4.5 floor   2.9976 FAIL  ->  4.5429 pass
#
# One job of six, not one done well and three conditionally. The register's own
# "the border carries the signal" permission fails: a gold border on white is the
# same 2.9976, and on the window ground 2.7495.
#
# THE COST IS REAL AND IS NOT HIDDEN. Black on the fill drops 7.0055 -> 4.6226.
# That is headroom traded on the one job the old value did well, to bring four
# failing jobs across. Text on #eeeeee still fails and is still not permitted.
#
#   rule    hold hue 42.2 and saturation 43.9%, lower lightness until 4.5:1 on #ffffff
#   walk    L 0.482 #b19145 2.9976 -> 0.457 #a88941 3.3230 -> 0.432 #9f823e 3.6606
#           -> 0.407 #957a3a 4.0993 -> 0.382 #8c7337 4.5429
#   taken   the first step that clears, not the first that looks right
#
# TEXT ON GOLD IS STILL BLACK. At the new value black is 4.6226 and white 4.5429,
# so black remains correct and BRAND_COLORS.md's rule survives the change. Three
# apps paint white on the fill against that rule; that is a separate fix and it
# is not what this value change is for.
#
# Cross-checked through rnv-color-mcp rather than trusted to arithmetic.
BRAND_DARK_GOLD = "#8c7337"    # light-mode surfaces -- see above


def lighten(color: str, step: int) -> str:
    """Raise every channel by `step`, clamped to 0-255. Negative darkens.

    A UNIFORM PER-CHANNEL STEP, which holds hue exactly -- #8c7337 and its -14
    derivative both measure 42.4 degrees. It is also the relationship the light
    palettes have always used between accent and hover tint (#b19145 -> #c4a458
    is +19 on every channel), so this is the house method rather than an import.

    Lifted here from rnv-text-transformer, where it was written first. It is in
    the register because three applications derived the same value from the same
    base with the same step, independently -- and nothing anywhere would have
    caught a fourth picking -13.
    """
    c = color.lstrip("#")
    return "#%02x%02x%02x" % tuple(
        max(0, min(255, int(c[i:i + 2], 16) + step)) for i in (0, 2, 4)
    )


# THE DERIVATION RULE, PUBLISHED SO THE STEP STOPS BEING GUESSED.
#
# The brand holds TWO golds per mode and derives the rest. That is the intended
# structure and a third registered gold is the wrong fix. What was missing is the
# RULE: three apps agreeing on -14 is luck, not design. An unpublished derivation
# permits four VALUES for one colour, which is worse than four names -- a wrong
# name is visible in a diff and a wrong value is not.
#
# LIGHT MODE spends its derivative on TEXT. BRAND_DARK_GOLD clears 4.5:1 as text
# on pure white and on nothing else:
#
#   ground     BRAND_DARK_GOLD   -14 derivative
#   #ffffff        4.5429 pass      5.5547 pass
#   #f5f5f5        4.1670 FAIL      5.0949 pass
#   #eeeeee        3.9156 FAIL      4.7875 pass
#   #e8e8e8        3.7078 FAIL      4.5334 pass   <- binding
#   #e0e0e0        3.4414 FAIL      4.2078 FAIL
#
#   rule    uniform per-channel step, which holds hue exactly
#   walk    -13 #7f662a 4.4675 on #e8e8e8 -- fails
#           -14 #7e6529 4.5334 on #e8e8e8 -- clears
#   taken   the smallest step that clears, not the first that looks right
#
# COVERAGE STOPS AT #e8e8e8 and going darker does not extend it: -29 clears
# #d0d0d0 at 4.5054 and then fails black-on-fill at 3.0219, the same exclusion one
# step down. BELOW #e8e8e8, GOLD DOES NOT CARRY TEXT. A ruling, not a gap.
#
# NOT A FILL. Black on the -14 derivative is 3.7806, under the 4.5 text floor.
# BRAND_DARK_GOLD remains the fill; this is the text value only.
#
# DARK MODE spends its derivative on HOVER, +13, and the evidence there was worse
# than for light: the variants existed in every app as hand-written literals and
# NO TWO AGREED ON METHOD. rnv-color-picker held #dcc9a3 (+10/+13/+16) and #b7a480
# (-27/-24/-19), both hue-shifting, because non-uniform steps do not hold hue.
#
# LIGHT PRESSED IS AN ALIAS, NOT A VALUE. No darker pressed shade exists on light
# that still keeps black text: 18% darker measures 3.37 for black-on-gold, which
# would force white text and break the text-on-gold rule. Pressed is the accent.
#
# DARK PRESSED IS OPEN, AND THE TWO APPS DISAGREE. Recorded rather than ruled,
# because it is a design question and not a measurement:
#
#   rnv-text-transformer  GOLD_PRESSED = lighten(BRAND_GOLD, -23) -> #bba57c
#   rnv-color-picker      pressed returns to the accent in both modes
#
# Both are legible as fills -- black reads 8.79 on the derivative and 11.35 on the
# accent -- so this is not a contrast question. It is whether a pressed state
# needs to be visibly distinct, and by how much:
#
#   hover vs accent      1.1449:1 apart
#   accent vs pressed    1.2924:1 apart   (with the -23 derivative)
#
# ARGUMENT FOR THREE STEPS: hover and pressed are different interactions, and a
# pressed control that looks identical to its resting state gives no feedback.
# ARGUMENT FOR TWO: light already collapses pressed into the accent by necessity,
# and a dark-only third step means the two modes stop being described by one rule.
# The register does not rule this yet. Until it does, an app may do either and
# should say which in a comment. WHAT IT MUST NOT DO IS HAND-WRITE THE VALUE --
# if it wants a pressed shade, it derives one with lighten().
# THE DERIVATION'S INPUT, REGISTERED 2026-08-30 BECAUSE IT WAS GOVERNING WITHOUT
# BEING OWNED. #e8e8e8 is the darkest light ground on which the gold family still
# carries text, and BRAND_DARK_GOLD_DEEP is derived to clear IT specifically --
# the walk above marks it "<- binding". It appeared fourteen times in this file's
# comments and in NO dict, so the register published a derivation while leaving
# its input app-owned. That is the unpublished-derivation failure inverted: not a
# step nobody could check, but a CONSTRAINT nobody could mirror.
#
# THE APPS COULD NOT MIRROR WHAT HAD NO KEY. rnv-color-picker holds it as light
# `image_viewer_bg`; rnv-text-transformer as GREY_E8 for two surfaces. They asked
# whether it was a token meant to be added or prose describing a value the
# register deliberately does not own. It was neither -- it was a value doing
# register work with no register entry, which nobody had noticed because the
# comments read as though it had one.
#
# NAMED FOR THE ROLE THAT MAKES IT LOAD-BEARING. It is not a rung of the light
# surface ladder -- that ladder is not ruled, and this does not pre-empt it. A
# boundary and a rung are different things: if the ladder later steps over this
# value, the boundary still holds and still constrains the gold.
# WHICH GOLD, ON A LIGHT GROUND -- ruled 2026-08-31, and it was folk knowledge
# until today. Both values existed and were published; the rule that SELECTS
# between them lived in one comment in one repository:
#
#     'accent_ink': BRAND_DARK_GOLD_DEEP,  # Accent when it carries text
#
# Two applications got it right by copying that key. Three got it wrong across
# seven sites, because the register named the gap in a DERIVATION and never in a
# RULE -- an app reading it learned that a second gold exists without learning
# when the second one is mandatory.
#
#   ON A LIGHT GROUND:
#     gold as TEXT             -> BRAND_DARK_GOLD_DEEP
#     gold as a FILL or EDGE   -> BRAND_DARK_GOLD
#
# NEITHER CAN DO THE OTHER'S JOB, which is why this is a rule and not a
# preference. Measured at the current values:
#
#     job                       BRAND_DARK_GOLD   BRAND_DARK_GOLD_DEEP
#     text on #ffffff           4.5429 pass       5.5546 pass
#     text on #f5f5f5           4.1669 FAIL       5.0949 pass
#     text on #eeeeee           3.9155 FAIL       4.7875 pass
#     text on #e8e8e8           3.7077 FAIL       4.5334 pass
#     border on #ffffff         4.5429 pass       5.5546 pass
#     fill, black on it         4.6225 pass       3.7806 FAIL
#
# BRAND_DARK_GOLD CARRIES TEXT ON PURE WHITE AND NOWHERE ELSE. The reported
# framing -- "it fails exactly one job" -- understates it: it fails as text on
# every light ground except #ffffff, and the apps' own surfaces are mostly not
# #ffffff. BRAND_DARK_GOLD_DEEP fails the fill job in the other direction at
# 3.7806, so the exclusion runs both ways.
#
# IN DARK MODE THE TWO GOLDS ARE THE SAME VALUE, and that is why five separate
# checks missed this. An app asserting `dark["accent_ink"] == dark["accent"]` is
# asserting something true and correct that is STRUCTURALLY INCAPABLE of noticing
# the light case, where they diverge and the divergence is the whole point.
#
#   EVERY CHECK WRITTEN WHERE TWO THINGS COINCIDE IS BLIND TO THE CASE WHERE THEY
#   DO NOT.
#
# THIS REGISTER HAS THE SAME EXPOSURE AND IT IS NAMED RATHER THAN CLOSED.
# _deep_gold_clears_its_floor() guards the coupling between the gold and its
# floor. NOTHING HERE GUARDS WHICH OF THE TWO GOLDS AN APPLICATION PICKS, and
# nothing here can -- the register cannot see an app's stylesheet. That check is
# app-side by construction; publishing the rule is what gives it something to
# check against.
GOLD_TEXT_GROUND_FLOOR = "#e8e8e8"
"""Darkest light ground on which the gold family carries text.

    Below this, gold does not carry text -- a ruling, not a gap. It is the
    binding input to BRAND_DARK_GOLD_DEEP below and is asserted against it at
    import, so the pair cannot drift apart silently.
    """

BRAND_DARK_GOLD_DEEP = lighten(BRAND_DARK_GOLD, -14)   # -> #7e6529, light-mode TEXT
BRAND_GOLD_HOVER = lighten(BRAND_GOLD, 13)             # -> #dfc9a0, dark-mode HOVER

# ---------------------------------------------------------------- stillness
# BRAND_STILL_GOLD IS REGISTERED, NOT DERIVED, AND THAT IS THE WHOLE POINT.
# It means STILLNESS -- not-live, dead, the absence of life in something the
# brand runs. It is the first permanent colour carrying a MEANING rather than a
# role, and it will appear across brand products beyond this first consumer.
#
# THE TEST THAT DECIDED IT IS "WHAT MAKES THE VALUE MOVE":
#   a DERIVATIVE moves when the derivation rule moves
#   a REGISTERED value moves when the brand decides something
# Make stillness a derivative and someone retuning a step -- for hover, for a new
# ground, for any reason -- silently changes what death looks like. The coupling
# would be wrong in DIRECTION, not merely in magnitude.
#
# AND THE METHOD PROVABLY CANNOT REACH IT. Checked all 400 uniform steps: none
# produces #9b907a. Adding a constant to every channel preserves the channel
# SPREAD, and spread is what saturation is -- so lighten() can dim a gold and
# then re-concentrate it, but it cannot DRAIN one:
#
#   step    0  #d2bc93  S 41.2%
#   step  -49  #a18b62  S 25.1%
#   step  -80  #826c43  S 32.0%   <- saturation climbing again
#   step -120  #5a441b  S 53.8%
#   target     #9b907a  S 14.2%   unreachable
#
# The method was constraining the meaning. Registering it is what put a DRAINED
# gold on the table at all; a darkened one reads as gold with the lights off,
# where this reads as gold with the blood out. Same perceptual distance from the
# brand gold -- CIEDE2000 14.56 against the darkened candidate's 14.47 -- and
# opposite stories. No measurement resolves that choice, which is exactly when a
# brand judgement is the right instrument.
#
#   on --rnv-bg      6.267:1   twice the 3:1 UI floor; the offline ring is the
#                              only boundary carrier on that component
#   dE from gold    14.5577   "clearly different" -- a colour, not an artifact
#   dE from fill    30.893    stays distinct from the #5a5a72 it surrounds
#   H 40.0  L 54.3  S 14.2    hue holds within a degree of the brand gold, so it
#                              still reads as gold; saturation is the payload
#
# NEAR-NEIGHBOUR, recorded so it is not "fixed": RECORDS.ink-mute #9b978c sits
# CIEDE2000 5.336 away. Different surfaces, never co-occurring. Same deliberate
# seam as signal-offline equalling text-faint -- one degree less extreme.
BRAND_STILL_GOLD = "#9b907a"   # stillness: not-live, dead, absence of life

# DERIVED. The ring for something RUNNING BUT NOT THE MAIN EVENT, where stillness
# is for something absent. Standby still has gold in it; offline has been drained.
#
#   rule    smallest uniform step whose CIEDE2000 from BRAND_GOLD crosses into
#           "clearly different" -- the instrument's own interpretation band
#   walk    -30 #b49e75  8.4035  perceptible at a glance
#           -35 #af9970  9.9383  perceptible at a glance
#           -36 #ae986f 10.2503  CLEARLY DIFFERENT  <- taken
#           -39 #ab956c 11.1972  clearly different
#           -49 #a18b62 14.4732  clearly different
#   taken   the smallest step that clears, not the first that looks right
#
# ORDERING IS PART OF THE RULING: live 70.0 > standby 55.9 > offline 54.3 in
# lightness. A running-but-not-primary state must not recede FURTHER than an absent
# one -- an earlier -49 candidate did exactly that and was rejected on it.
#
#   on --rnv-bg      7.073:1
#   dE from gold    10.2503   clearly different
#   dE from still    7.0788   perceptible at a glance; the ring is not the only
#                             channel -- fill, motion and the pill word all move
#
# EVERY FIGURE HERE IS rnv-color-mcp's. An earlier hand-computed walk used dE76
# and inflated these by three to four points, which would have put -30 on the
# table as "clearly different" when the instrument calls it perceptible only.
# REGISTERED 2026-09-03, WAS lighten(BRAND_GOLD, -36). The value does not move.
# The formula does, because it pointed the wrong way.
#
# BRAND_GOLD IS THE ACCENT SLOT -- the value a future RNV application replaces
# with a purple or a green when it claims its own accent. Under a formula
# anchored on it, an app choosing purple would drag the standby ring with it.
#
# BUT SIGNALS ARE NOT THE ACCENT. This file rules it forty lines down: signals
# are "the state of a THING the brand runs ... different job, different
# lifecycle, different owner". An application choosing purple is not the brand
# deciding what STANDBY looks like. The formula made a brand-owned signal follow
# an app-owned choice -- the coupling wrong in DIRECTION rather than magnitude,
# which is precisely what BRAND_STILL_GOLD was registered to avoid.
#
# ITS TWO NEIGHBOURS ARE CORRECT AS DERIVED, checked rather than assumed:
#   BRAND_GOLD_HOVER      SHOULD follow an accent swap -- it is a STATE of the accent
#   BRAND_DARK_GOLD_DEEP  SHOULD follow -- no meaning without the gold it is taken from
#   BRAND_STANDBY_GOLD    MUST NOT -- its meaning is brand-owned
# One value on the wrong side of a line this file drew, not a problem with the
# derivations.
#
# THE WALK ABOVE IS UNCHANGED AND BECOMES WHAT IT ALWAYS WAS IN SUBSTANCE:
# provenance. The CIEDE2000 steps, the ordering ruling that rejected -36's
# alternatives, the note that every figure is rnv-color-mcp's -- all stand.
# signal-ring-standby still REFERENCES this constant rather than copying it, and
# registering it does not disturb that.
BRAND_STANDBY_GOLD = "#ae986f"          # the standby ring -- registered, see above

# RENAMED FROM BRAND_DOWN_GOLD ON 2026-08-23, VALUE UNCHANGED. `down` and
# `degraded` both assert that something is WRONG. Standby does not, and the state
# covers a build underway, a stream being prepped, maintenance, AND a partial
# outage -- some of which are good news. Naming the state for the bad half means
# the amber can only ever be a warning, and A SIGNAL THAT CAN ONLY MEAN ONE THING
# GETS USED FOR ONE THING.
#
# The traffic-light reading earns the colour rather than merely tolerating it:
# green go, amber WAIT, dark nothing maps onto live / standby / offline more
# cleanly than onto live / degraded / offline, where amber has to carry a fault it
# may not have.
#
# TWO KINDS OF CHANGE, and which one applies is decided by what is wrong:
#
#   RENAME when the NAME means the wrong thing.
#   KEEP the name and change the WORD when the name is right and only the word
#   collides on a surface.
#
# `down` -> `standby` is the first: the name asserted a fault the state does not
# have. `live` -> label ONLINE is the second: `live` is the brand's own word --
# rnv-live, signal-live -- and stays as the state name; only the displayed word
# moves, because LIVE already appears on that page as the hero kicker directly
# above "Offline right now", and one word in two roles contradicts itself.
#
# Cheap now because rnv-live is the only consumer. A wrong name is visible in a
# diff where a wrong value is not -- so this one is catchable, which is exactly
# why it does not get to wait.
#
# AND THE RENAME WAS SHIPPED HALF-DONE THE FIRST TIME. The identifiers moved by
# regex; four DESCRIPTIONS still called the state "degraded" -- including the one
# line in the naming convention above and the comment on the emitted token. The
# name moved and the meaning did not follow, so the reading this rename exists to
# retire survived in exactly the comments a reader consults to learn what the
# value is for. Caught by rnv-color-mcp, not by me, within the hour.
#
# A RENAME IS NOT COMPLETE WHEN THE IDENTIFIERS MOVE. It is complete when nothing
# still describes the thing by the meaning that was retired. A mechanical pass
# cannot do the second half: prose is where the meaning lives, and a regex cannot
# tell a use of the retired word from a mention of it. The four survivors below
# are mentions, inside this note, and are correct as written -- which is the
# distinction that made the sweep unsafe in the first place.
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
    "gold": BRAND_GOLD,
    "dark-gold": BRAND_DARK_GOLD,
    # SEVENTH PERMANENT COLOUR, added 2026-08-23, and the first carrying a
    # MEANING rather than a role. See BRAND_STILL_GOLD above for why it is
    # registered and not derived.
    "still-gold": BRAND_STILL_GOLD,
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
    # THE DARK SURFACE LADDER, ruled 2026-08-29. Four rungs on a permanent anchor:
    #
    #   BRAND_BLACK + n * 0x10,  n in -1..+2
    #     n = -1   #0a0a0a   canvas, image-viewer ground
    #     n =  0   #1a1a1a   panel        <- BRAND_BLACK
    #     n = +1   #2a2a2a   card
    #     n = +2   #3a3a3a   panel hover
    #
    # ALL FOUR ARE NOW REGISTERED. The two ends were app-owned. A brand that
    # publishes the middle of a ladder and leaves the edges to applications is
    # publishing a derivation nobody can check -- the unpublished-step failure,
    # arriving in a ramp instead of a colour.
    #
    # BORDER IS NOT A RUNG AND ITS ABSENCE WAS NEVER A GAP. An earlier reading
    # from this side called this ladder "two-thirds specified" because
    # APP["border"] #333333 is not #3a3a3a. #333333 is grey(3) EXACTLY on the ink
    # grid, and that grid governs inks AND EDGES. A border is an edge. It was
    # measured against the wrong family and reported as a hole in this one.
    #
    # #0a0a0a IS NOT WEB_BLACK, AND THE SEAM IS DELIBERATE. The web canvas is
    # #0a0a0f -- same lightness, blue channel lifted. This register already rules
    # it: app neutrals are pure grey, R = G = B, without exception, and the web
    # ground carries a tint the apps do not. Two canvases one byte apart is not
    # drift -- and that near-miss is exactly what made an inversion anchor look
    # convincing on the light side when it was not.
    "canvas": "#0a0a0a",
    "panel": BRAND_BLACK,
    "card": "#2a2a2a",
    "panel-hover": "#3a3a3a",
    "border": "#333333",   # grey(3) on the INK grid: an edge, not a surface
    # THE INK GRID, ruled 2026-08-28 together with this value, because the value
    # moved only to satisfy it and neither is defensible alone.
    #
    #   grey(n) = n * 0x11, n in 0..15.  TRUE_BLACK -> WHITE in fifteen steps.
    #
    # IT GOVERNS INKS AND EDGES. IT DOES NOT GOVERN SURFACES AND IT NEVER CAN --
    # `panel` is BRAND_BLACK #1a1a1a at n = 1.53 and `card` is #2a2a2a at n = 2.47.
    # BRAND_BLACK is a permanent brand colour and will not move to fit a ladder.
    # THE SCOPE IS WRITTEN INTO THE RULE rather than discovered by whoever extends
    # the grid to surfaces and finds a permanent in the way.
    #
    #   ink   text      grey(13)  #dddddd    was #e0e0e0 at n = 13.18
    #   ink   text-dim  grey(10)  #aaaaaa
    #   edge  border    grey(3)   #333333
    #
    # WHY THE VALUE MOVED. #e0e0e0 was ONE HEX DOING TWO UNRELATED JOBS: ink in
    # dark mode, and a light SURFACE in the apps' light palettes and in this
    # register's own contrast tables. It refused to sit on the grid because the
    # grid governs inks and half its uses were not ink. Split the roles and both
    # halves land -- the ink half moves to grey(13); the surface half keeps
    # #e0e0e0 and does not move, so BRAND_COLORS.md's two contrast rows stand.
    #
    # PRIMARY TEXT IS ONE ROLE WITH TWO MODE VALUES: dark is a grey on the ink
    # grid, light is TRUE_BLACK. Already true in all five apps with no exceptions;
    # unwritten is why it looked like a question.
    #
    # COST, measured on every ground it is drawn on. Contrast falls 0.20 to 0.44
    # and the floor afterwards is 7.17 on the pressed plate #444444, the darkest
    # ground it touches:
    #
    #   #444444  7.37 -> 7.17     #2a2a2a  10.87 -> 10.56
    #   #3a3a3a  8.61 -> 8.37     #1a1a1a  13.18 -> 12.81
    #   #333333  9.57 -> 9.30     #000000  15.90 -> 15.46
    #
    # SAFE TO MOVE, checked rather than assumed: nothing in this file derives from
    # it, profile.json does not carry it, and rnv-live emits from --css web and
    # reads WEB["text"] #e8e8f0, not this one. All six existing uses of #dddddd
    # across the five apps sit under LIGHT palettes, so it collides with nothing
    # it could render against.
    "text": "#dddddd",   # grey(13)

    # COINCIDENCE IS PERMITTED AND MUST BE NAMED, ruled 2026-08-28.
    #
    # Publishing the grid created a class this register had only ever met once
    # before: an app-owned ramp step landing on a REGISTERED value while doing a
    # different job. rnv-text-transformer's light `border_light` is grey(13), and
    # so is this ink. They are not the same value and must not be collapsed --
    # IF THIS INK EVER MOVES OFF grey(13), THAT BORDER MUST NOT FOLLOW IT.
    #
    # THE SEAM ALREADY HAS A NAME HERE. signal-offline equals text-faint exactly,
    # and the rule twenty lines into WEB reads "do not de-duplicate these": one
    # moves for legibility, the other for the type ramp, and a shared hex is not
    # shared ownership. This is that rule meeting an app ramp instead of two
    # register families.
    #
    # THE APPS' `COINCIDENT` TABLE IS THE MACHINE-READABLE FORM OF IT AND IS
    # ADOPTED AS THE RECORDING FORM. Name, the register entry it shares a value
    # with, and why it is not the same role -- asserted in four directions so it
    # cannot rot: a coincidence that stops coinciding fails, one whose register
    # entry changed identity fails, one naming a `register`-classified constant
    # fails, and one with no written reason fails.
    #
    # THE ALTERNATIVE WAS CONSIDERED AND REJECTED. Telling apps to avoid grid
    # positions the register occupies would put holes at arbitrary indices in
    # every app ramp, and a ramp with holes is worse than a coincidence with a
    # reason -- the holes carry no explanation and the next author closes them.
    "text-dim": "#aaaaaa",   # grey(10)

    # THE LIGHT HOVER PLATE. #eeeeee, corrected 2026-08-30 from a ruling made the
    # day before, and the correction is worth more than the value.
    #
    # THE FIRST RULING PUT IT ON #e8e8e8 AND SAID "the arithmetic does not leave a
    # choice". It argued: the plate must be dark enough to read against the
    # #ffffff base and light enough that BRAND_DARK_GOLD_DEEP clears 4.5 as its
    # label; the band is #e8e8e8 and lighter; #e8e8e8 is its dark edge and so
    # maximises separation from the base; every lighter option is dominated.
    #
    # IT MEASURED ONE AXIS AND CALLED THE RESULT DOMINANCE. The axis it did not
    # measure is margin on the binding constraint:
    #
    #     plate      gold      margin     error-red   margin
    #     #e8e8e8    4.5334    +0.0334    4.6100      +0.1100
    #     #eeeeee    4.7875    +0.2875    4.8684      +0.3684
    #
    # A BOUNDARY IS NOT A PLATE. #e8e8e8 is the value at which the next step down
    # FAILS. It is also the ground this file's own gold derivation is calibrated
    # against -- marked "<- binding" above. Putting every hover in every
    # application on it couples plate to gold so tightly that one rounding fails
    # them together: -13 instead of -14 gives 4.4675 and both go at once.
    #
    # AND THE APPLICATIONS HAD ALREADY ANSWERED IT. Eleven hover keys across four
    # apps hold #eeeeee; ZERO hold #e8e8e8. Every use #e8e8e8 has is a static
    # surface. The convergence was there to be read and the ruling did not read
    # it -- it reasoned from a contrast table about a question the shipped code
    # had already settled.
    #
    # #e8e8e8 IS NOT RETIRED AND NOT WEAKENED. It stays registered, stays the
    # published gold-as-text coverage boundary, and keeps its three surface uses
    # and its role as the binding ground in the derivation. It is doing real work.
    # It is simply not the hover: A WORKING STATE SHOULD NOT SIT ON THE LAST VALUE
    # THAT WORKS.
    #
    # A CLAIM WITHDRAWN IN THE SAME CHANGE, because it was load-bearing for a
    # separate ruling and would not have held it up. This file argued that the
    # apps walking UP from a failing plate and this register walking DOWN from a
    # failing text colour and both stopping at #e8e8e8 was "a boundary two
    # independent walks land on".
    #
    # THE WALKS WERE NEVER INDEPENDENT. It is one equation -- cr(gold, ground) >=
    # 4.5 -- solved for two unknowns. The register fixed a set of grounds and took
    # the SMALLEST step clearing its darkest one, which calibrates the gold TO
    # that ground. Asking afterwards which ground the gold clears returns the
    # ground you fed it. Demonstrated by varying it:
    #
    #     darkest ground fed    step chosen    crossing then lands at
    #     #eeeeee               -10            #eeeeee
    #     #e8e8e8               -14            #e8e8e8
    #     #e0e0e0               -19            #e0e0e0
    #     #dddddd               -21            #dddddd
    #
    # Every time. That is arithmetic, not corroboration. THE GOLD-AS-TEXT RULING
    # STANDS ON THE SIX-JOB TABLE ABOVE -- one value passing one job of six
    # against another passing five -- which is real independent evidence. Raised
    # by the app side, which was right to refuse unsafe support for a ruling it
    # agrees with.
    #
    # DARK NEEDS NOTHING: BRAND_GOLD on the panel-hover rung reads 6.1503.
    # THE LIGHT SURFACE LADDER, ruled 2026-09-01. Four rungs, and the derivation
    # is a PROPORTION rather than a step, because light has less room than dark.
    #
    #   LIGHT'S RUNGS TAKE THE SAME SHARE OF LIGHT'S SPAN THAT DARK'S RUNGS TAKE
    #   OF DARK'S SPAN, MEASURED IN CONTRAST.
    #
    # Shares are logarithmic -- contrast ratios compose multiplicatively, so equal
    # shares in log space are equal perceptual steps. Dark runs #0a0a0a -> #3a3a3a
    # across 1.7405 and divides it 0.233 / 0.348 / 0.420. Light runs #ffffff ->
    # #eeeeee across 1.1602 and divides it 0.230 / 0.351 / 0.419.
    #
    #   #    dark       light      share d -> l    job
    #   1    #0a0a0a    #ffffff    --             card, list row, button face
    #   2    #1a1a1a    #fbfbfb    0.233 -> 0.230  alternating rows, second tier
    #   3    #2a2a2a    #f5f5f5    0.348 -> 0.351  panel, window, statusbar
    #   4    #3a3a3a    #eeeeee    0.420 -> 0.419  the hover plate
    #   --   #333333    #e0e0e0    OFF THE LADDER  pressed, tab, scrollbar trough
    #
    # PRESSED COMES FROM THE EDGE FAMILY, NOT THE LADDER, and light mirrors that.
    # Dark's pressed is #333333, which is grey(3), which is APP["border"]. An
    # earlier proposal made #e0e0e0 the bottom rung; dark does not put an
    # interaction state in its surface ladder and neither does light.
    #
    # THE HOVER -> PRESSED STEP IS THE ONE THAT HAD TO MATCH, because it is the
    # one a user sees fire under the cursor: 1.1377 in light against 1.1107 in
    # dark. It does.
    #
    # WHY PROPORTIONS AND NOT STEP SIZES. Copying dark's step sizes down from
    # white gives #ffffff -> #f0f0f0 -> #dbdbdb -> #c4c4c4. The bottom two land on
    # the ink and edge families -- #dbdbdb is one byte from APP["text"] #dddddd,
    # and #c4c4c4 is in the light border's neighbourhood. LIGHT HAS LESS ROOM
    # ABOVE THE INK THAN DARK HAS BELOW IT, and that is a property of sRGB rather
    # than a choice: near white, equal contrast steps need growing byte steps.
    # Light's are 4, 6, 7; dark's are a flat 0x10.
    #
    # THE CONFIRMATION NOBODY PLANTED. #f5f5f5 already carried fifteen keys across
    # the five applications before this rule existed, and it lands on rung 3 at
    # luminance 0.91310 against an ideal of 0.91324 -- 0.00014 out, where the byte
    # grid puts a candidate every 0.0084. That is 1/57th of a step. The ladder was
    # two-thirds built at the correct positions and only the missing rung had to
    # be found.
    #
    # #fbfbfb IS THE ONLY NEW VALUE and it is what the rule returns, not a
    # compromise between the strays already in use. Worst deviation from dark's
    # shares: #fdfdfd 0.119, #fcfcfc 0.061, #fbfbfb 0.003, #fafafa 0.056,
    # #f8f8f8 0.172. Two strays sit either side of it.
    #
    # GOLD PASSES ON EVERY RUNG -- 5.5546 / 5.3678 / 5.0949 / 4.7875 for
    # BRAND_DARK_GOLD_DEEP. #e0e0e0 reads 4.2078 and is the one light surface gold
    # can never sit on, which is survivable because it is a pressed state rather
    # than a plate.
    "surface-light": WHITE,
    "surface-light-2": "#fbfbfb",
    "surface-light-3": "#f5f5f5",
    "hover-light": "#eeeeee",   # grey(14), rung 4
    "pressed-light": "#e0e0e0",   # a STATE, not a rung -- see above
    "accent": BRAND_GOLD,
    "accent-light-mode": BRAND_DARK_GOLD,
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
    "accent": BRAND_GOLD,
    "accent-violet": "#b794ff",  # secondary, sparing
    "accent-warm": "#ffd166",    # secondary, sparing
    # ---- signals ---------------------------------------------------------
    # Brand signals: the state of a THING the brand runs. Not STATUS below,
    # which is the result of a user's action in an app. Different job, different
    # lifecycle, different owner -- STATUS moves when a UI framework moves, these
    # move when the brand decides something.
    #
    # THE RING IS NOT IN HERE, AND THAT IS THE DESIGN. Every signal dot is drawn
    # with a `gold` ring, identical in all states, so the ring signals nothing --
    # it is the component's chrome. It carries the WCAG 1.4.11 boundary, which is
    # what frees the FILL to be whatever the brand wants, including values that
    # could never carry it alone. Drop the ring and every value below fails.
    #
    # THE RING IS 0.75px ON BOTH SURFACES as of 2026-08-14, down from 1px. Sub-
    # pixel, so a 1x display antialiases it and the effective colour is roughly
    # 75% gold over the ground: ~6.1:1 on the site's bg-2, ~6.3:1 on rnv-live's
    # bg, both at 1x. Both still about 2x the 3:1 floor, down from 3.4x. On 2x
    # and 3x screens it renders nearer the solid value.
    #
    # ONE DECIMAL IS DELIBERATE. Two projects measured this ring independently
    # and got 6.09/6.27 and 6.12/6.33 -- the same sRGB compositing model,
    # differing only on whether the blend was rounded to a hex before measuring.
    # That gap is smaller than the model's own uncertainty, because rendered
    # coverage depends on the rasterizer, the device pixel ratio and subpixel
    # positioning. Two files held the figure to two decimals and disagreed in the
    # second one; neither was wrong by its own method, which is why the digit was
    # dropped rather than arbitrated.
    #
    # **0.75px is unverified below 3x** and is carried as an open confirm in
    # BRAND_COLORS.md rev 15; if it reads absent rather than finer, both surfaces
    # revert in one pass.
    #
    # No dim-end figure here any more -- see below, the ring stopped animating.
    # Measured 2026-08-14. RE-MEASURE IF THE RING OR THE GROUND MOVES: that
    # sentence was written on the 13th and the ring moved on the 14th, which is
    # the only reason this block is correct rather than quietly wrong.
    #
    # signal-live is 2.56:1 on bg and 2.43:1 on bg-2. DELIBERATELY under the
    # floor, and defensible for two reasons that are now independent: the pill
    # carries the word, and since 2026-08-14 the ring sits on its own element and
    # no longer animates, so it holds its full value at EVERY frame -- see the
    # figures above. The 0.5 dip is an aesthetic choice held in common across two
    # surfaces, not a contrast floor. Colour is the third signal.
    #
    # WHY THE SPLIT MATTERED, kept because the argument outlives the numbers:
    # when ring and fill shared one element, the ring dimmed with the animation
    # and fell to 3.35:1 at the trough against 10.68:1 at rest. The fix was
    # structural, not numeric -- decouple the thing carrying the boundary from
    # the thing that moves, rather than tuning the keyframe until the boundary
    # survives it. Those two figures describe the retired 1px design and are
    # history, not current measurements.
    #
    # Value changed 2026-08-14 from an earlier wine at hue 350.5, on the check
    # that mattered rather than on taste: a move toward magenta could have
    # narrowed the gap to STATUS.error and instead widened it. Hue measured
    # 350.5 -> 332.2; published as 333 in one handoff and corrected to 332.
    # TWO CROSS-FAMILY DISTANCES, recorded 2026-09-03 because the register held
    # one and read as though it held all of them.
    #
    # THE 18.22 BELOW IS STALE FOR THE MEMBER, not the family. It says "the error
    # red was always this value's nearest neighbour" -- true of STATUS.error when
    # written, and error-text-light #c82131 was published on 2026-08-24 at
    # CIEDE2000 16.19. Closer. A note recording one distance reads as though all
    # of them were checked, which is this file's own four-channel failure:
    # A TABLE THAT OMITS A CHANNEL DOES NOT LOOK INCOMPLETE, IT LOOKS SETTLED.
    #
    # AND THE CLOSEST CROSS-FAMILY PAIR IN THE WHOLE MATRIX WAS NEVER RECORDED:
    # signal-standby #ffd166 against the old STATUS.warning #ffc107 read
    # CIEDE2000 6.83 -- BELOW this register's own threshold for a distinguishable
    # colour, since BRAND_STANDBY_GOLD's published walk calls 8.40 "perceptible at
    # a glance" and would not take it. Two ambers, one meaning "running but not
    # the main event" and one meaning "warning".
    #
    # THE RNV STATUS FAMILY CLOSES IT. The new warning #a2703c sits far from
    # signal-standby, so the pair that was 6.83 is no longer a pair. It is
    # recorded anyway, because the reason the amber moved was measured twice --
    # once as a light-ground fill failure and once as this collision -- and a
    # value with two independent reasons to move should not read as though it had
    # one.
    # CIEDE2000 18.22
    # against the error red where the wine was 17.40, and 25.92 against
    # error-text. The error red was always this value's nearest neighbour.
    #
    # signal-offline and signal-standby happen to equal text-faint and accent-warm.
    # THE MATCH IS INCIDENTAL AND THE SEAM IS DELIBERATE: text-faint moves for
    # legibility reasons and accent-warm for decorative ones, and neither should
    # drag a signal with it. Do not "de-duplicate" these.
    #
    # Retires #4ade80, the green these replace on rnvizion.dev and rnv-live.
    # Both surfaces landed on 2026-08-14 and no repo holds an instance. THE
    # MEANING OF A SIGHTING HAS THEREFORE INVERTED: until the 14th it meant the
    # work was unfinished; from now on it means a regression or a stale base.
    # An expired note that still reads as current is worse than no note.
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
    # THE RING IS NOW A SIGNAL CHANNEL, not unconditional chrome. It was gold in
    # every state; on rnv-live it becomes stateful so every channel agrees with
    # the label instead of the fill carrying it alone.
    #
    # FOUR CHANNELS, NOT THREE. An earlier version of this table folded the halo
    # into live's motion cell and said "still" for the other two -- which reads as
    # a statement about motion and says nothing about glow. A TABLE THAT OMITS A
    # CHANNEL DOES NOT LOOK INCOMPLETE, IT LOOKS SETTLED, and the next reader
    # reasons from three columns as though three is all there is. Same shape as
    # the bg-2 collision: nothing renders wrong, every value is canonical, and the
    # failure is in what the structure implies rather than what it states.
    #
    #   state    ring                  fill             halo        breath
    #   live     signal-ring-live      signal-live      12px full   3s,  0.5 trough
    #   standby  signal-ring-standby   signal-standby   8px  55%    5s,  0.7 trough
    #   offline  signal-ring-still     signal-offline   none        still
    #
    # THREE OF THE FOUR CHANNELS ORDER, and the fourth cannot:
    #   ring     10.679 > 7.073 > 6.267     orders
    #   halo     12px   > 8px   > none      orders
    #   breath   3s/0.5 > 5s/0.7 > still    orders
    #   fill      2.560 < 13.698 > 2.953    DOES NOT ORDER, and must not be
    #                                       described as though it does
    # The fill carries HUE IDENTITY, not intensity -- live is a deep wine and
    # standby a bright amber, so live's fill is the dimmest of the three. The
    # ranking a reader gets comes from ring, halo and breath. Claiming "every
    # channel steps down" would be a claim the table then inherits.
    #
    # STANDBY BREATHES, SLOWER AND SHALLOWER THAN LIVE. Offline means nothing is
    # running; standby means something is running but is not the main event.
    # Motion reads as life, so making it a GRADIENT rather than a binary is what
    # makes standby a genuine middle state instead of offline in another colour.
    # Less life, not no life. The fill reads 13.698 at full and 6.953 at its 0.7
    # trough; the ring does not animate, so the boundary holds at 7.073 at every
    # frame -- the 2026-08-14 ring/fill split still doing its job.
    #
    # THE HALO IS DIMMED ON STANDBY AND THAT IS NOT TASTE. signal-standby carries
    # 5.35x the luminance contrast of signal-live -- 13.698 against 2.560 -- so a
    # 12px halo of it at full strength reads LOUDER than live's, inverting the
    # ordering the states exist to express. Hence 8px at 55%, cut on both axes.
    #
    # [confirm/fill] LIVE AND STANDBY HAVE NEVER BEEN RENDERED. rnv-live's pill is
    # a static element with OFFLINE hardcoded, so those two states are applied by
    # hand-editing markup. Every figure above is measured; halo radius and alpha,
    # breath rate and trough depth are EYE CALLS NO EYE HAS MADE ON THE REAL
    # SURFACE. A state toggle on that page turns an unverifiable design into a
    # checkable one, which is worth more than any single value here: a three-state
    # system exists today where two states have never rendered, and nothing in
    # either repository would report that.
    #
    # THESE REFERENCE THE CONSTANTS RATHER THAN COPYING THEM, and that is the
    # OPPOSITE of the signal-offline / text-faint seam noted above. There the
    # match is incidental and the two must move independently. Here the ring IS
    # the stillness colour -- if BRAND_STILL_GOLD moves, this moves with it,
    # because it is the same decision. Do not split them.
    "signal-ring-live": BRAND_GOLD,
    "signal-ring-standby": BRAND_STANDBY_GOLD,
    "signal-ring-still": BRAND_STILL_GOLD,
    "signal-standby": "#ffd166",      # running, but not the main event
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
    "accent": BRAND_GOLD,
    "gold-dim": _rgba(BRAND_GOLD, GOLD_DIM_ALPHA),
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
    # ================================================================
    # THE RNV STATUS FAMILY, ruled 2026-09-03. Chris chose the three sources;
    # everything else here is measurement.
    #
    # WHAT IT REPLACES AND WHY. The old values were Bootstrap 4 defaults --
    # borrowed, not chosen. This file half-said so already of the red: "a
    # borrowed platform value that never conformed to either register." Two
    # measurements made keeping them indefensible:
    #
    #   THE AMBER COULD NOT LEGALLY CARRY A BOUNDARY ON A LIGHT GROUND.
    #   #ffc107 reads 1.63 on #ffffff and 1.49 on #f5f5f5 against a 3:1 fill
    #   floor. Not taste -- arithmetic. The green failed too, at 2.87 on #f5f5f5.
    #
    #   SUCCESS AND ERROR WERE THE SAME COLOUR TO A DEUTERANOPE. #28a745 and
    #   #dc3545 sit CIEDE2000 74 apart in normal vision and about 4 apart
    #   simulated -- both collapse to one olive, because deuteranopia flattens
    #   red and green onto one axis and what survives is lightness, of which
    #   those two have almost none between them. Roughly 8% of men. Success and
    #   error are the two most consequential colours in any interface.
    #
    # A SEARCH OF THE RECOGNISABLE STATUS HUE BANDS -- green 138-160, amber
    # 26-46, red 350-10 -- found NO triple that both separates under
    # deuteranopia and clears 3:1 on all four grounds. That was true, and the
    # constraint was the problem: it assumed green/amber/red. LEAVING THE
    # RED-GREEN AXIS DISSOLVES A PROBLEM THAT CANNOT BE SOLVED INSIDE IT.
    #
    # THE DERIVATION, published so nobody re-derives it by hand and gets a
    # fourth value:
    #
    #     50% toward BRAND_DARK_GOLD #8c7337, interpolated in OKLab
    #
    #   role      source     ->  fill
    #   success   #9b59cc        #926c89
    #   warning   #b76c40        #a2703c
    #   error     #fe0f8a        #c75b64   <- corrected 2026-09-04, see below
    #
    # OKLab and not sRGB because the ramp must stay perceptually even; an sRGB
    # blend goes muddy through the middle and the midpoint would not be one.
    # 50% is the DEEPEST mix that passes every bar -- at 60% the worst
    # colour-blind pair drops to 6.8 and the nearest registered value to 7.4,
    # both under the register's own "clearly different" threshold. It passes by
    # 0.3 on one bar and 0.7 on the other, and that thinness is deliberate: the
    # gold has to read in all three.
    #
    # THE MIX IS PROVENANCE, NOT A LIVE FORMULA, and the difference matters.
    # Held as a rule, the ratio becomes an edit anyone can make, and retuning it
    # would silently change what ERROR looks like -- the same argument that
    # registered BRAND_STILL_GOLD rather than deriving it. So the derivation is
    # published to make the choice auditable, and the values are then written
    # down. #926c89 is #926c89.
    #
    # THE GAMUT CORRECTION, CLOSED 2026-09-04. The error source was published as
    # #ff008f, dialled at CIELCh L 55.3 / C 90 / h 359. That coordinate is
    # OUTSIDE sRGB and the value shipped was what a naive per-channel clip
    # produced.
    #
    # THE CLIP MOVED THE HUE, WHICH IS THE PART WORTH KNOWING. Measured, #ff008f
    # sits at h 357.2, not the 359 that was dialled -- clipping channels does not
    # preserve hue, so the published "source" was a different colour at a
    # different angle, and its R sat on 255 and its G on 0. Two rails is what a
    # clipped value looks like.
    #
    # PROPER GAMUT MAPPING HOLDS L AND h AND REDUCES C ONLY, which is the CSSWG's
    # own recommendation. At L 55.3 / h 359 the sRGB boundary is C 84.99:
    #
    #     C 90    outside          the dialled coordinate
    #     C 85.8  outside          what was published as the source's chroma
    #     C 85    outside
    #     C 84    INSIDE  #fe0f8a  zero channels on a rail   <- taken
    #
    # C 84 IS TAKEN RATHER THAN THE BOUNDARY 84.99. A value sitting exactly on
    # the gamut edge still resolves differently in a wider gamut, because "the
    # most chroma available" is relative to the gamut asking. #fe0f8a is
    # INTERIOR -- no channel at 0 or 255 -- so the coordinate is absolute and
    # resolves identically in sRGB, P3 and print.
    #
    # THE COST IS ONE BYTE IN THE FILL: #c85b67 -> #c75b64. Every floor still
    # clears and two improve, because the corrected hue is marginally warmer:
    #
    #     ground     new    was
    #     #1a1a1a    4.23   4.26
    #     #2a2a2a    3.49   3.51
    #     #ffffff    4.11   4.07
    #     #f5f5f5    3.77   3.74
    #
    # Ink stays TRUE_BLACK at 5.10 against white's 4.11. The two error text
    # variants were re-derived from the corrected fill by the same rule rather
    # than kept: #e0707b -> #dd6f77 and #b64b58 -> #b84e58. A text variant is
    # derived from its fill, so a fill correction that left them alone would
    # orphan them one week after the last orphan was cleaned up.
    #
    # FILL FLOOR, 3:1 on the four grounds the fleet paints:
    #             #1a1a1a  #2a2a2a  #ffffff  #f5f5f5   worst
    #   success      3.91     3.23     4.44     4.07    3.23
    #   warning      4.07     3.36     4.26     3.91    3.36
    #   error        4.26     3.51     4.07     3.74    3.51
    # All three clear on all four, which Bootstrap's green and amber did not.
    #
    # INK IS TRUE_BLACK on all three -- 4.72 / 4.91 / 5.14 against white's
    # 4.44 / 4.26 / 4.07 -- which agrees with the ink rule.
    "success": "#926c89",
    "warning": "#a2703c",
    "error": "#c75b64",

    # THE SIX TEXT VARIANTS ARE GENUINELY DERIVED, and are the opposite case to
    # the fills above: one deterministic rule, no judgement in it, recomputed
    # rather than re-decided if a fill ever moves.
    #
    # NONE OF THE THREE FILLS CLEARS 4.5 AS TEXT ON ANY GROUND, and that is not
    # a fault in the choice -- it is the fill band. Anything working as a fill on
    # BOTH a dark and a light ground sits at L* 48-59 by arithmetic, and a
    # mid-tone cannot carry text on either side. This file already knew it for
    # red and spent error-text / error-text-light on it; the other two had no
    # light sibling only because #28a745 and #ffc107 had nowhere to go.
    #
    # RULE: hold hue and chroma, move lightness only, take the first step that
    # clears 4.5 on the worst ground -- APP card #2a2a2a for dark, #f5f5f5 for
    # light. Same walk that produced error-text.
    # THE TWO EXISTING error-text KEYS MOVE WITH THEIR BASE. #e56b77 and #c82131
    # were derived from Bootstrap's #dc3545. With the base retired they are
    # ORPHANS -- values derived from something no longer in the palette, which is
    # exactly the #c4a458 failure this programme has already paid for once. They
    # are replaced, not kept alongside.
    #
    #   error-text        #e56b77 -> #e0707b   (was from #dc3545)
    #   error-text-light  #c82131 -> #b64b58   (was from #dc3545)
    #
    # THIS MOVES VALUES FIVE APPLICATIONS MIRROR. That is the cost of moving a
    # base, and it is the correct cost: the alternative is a text colour that no
    # longer belongs to its fill.
    "success-text": "#ad85a3",          # card 4.55
    "warning-text": "#bc8752",          # card 4.59
    "success-text-light": "#8a6581",    # f5f5f5 4.52
    "warning-text-light": "#976633",
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
    #   replacement. Same shape as BRAND_GOLD / BRAND_DARK_GOLD: one colour, two grounds.
    #   CIEDE2000 25.92 from signal-live, "clearly different" -- the error text
    #   and the live wine cannot be confused, which was the open question when
    #   red was chosen for the live signal.
    #
    # NOT made Records-conformant. Forcing R > G > B swung it to #e56d3c, burnt
    # orange, CIEDE2000 far off the base -- a different colour wearing the right
    # lightness. The tint rules govern the neutral ramps; #dc3545 is a borrowed
    # platform value that never conformed to either register, and a derived
    # variant that conforms while its base does not makes the pair incoherent.
    "error-text": "#dd6f77",         # card 4.52
    # LIGHT-MODE ERROR TEXT, published 2026-08-24 because three applications had
    # already derived it independently under TWO identifiers -- STATUS_ERROR_LIGHT
    # in the picker and the transformer, STATUS_ERROR_TEXT_LIGHT in the palette
    # manager. That is the condition publishing BRAND_DARK_GOLD_DEEP was meant to
    # end, recurring in a different family: an unpublished derivation permits four
    # VALUES for one colour, and here it also produced two NAMES.
    #
    # THE REGISTER SAID THIS COLOUR DID NOT EXIST WHILE THE BRAND BOOK SAID IT WAS
    # RULED AND APPLIED. BRAND_COLORS.md rev 18 carried a heading "There is no
    # light-mode error text"; Book v1.49 section 9 carried #c82131 as ruled. The
    # apps followed the Book. Three sources, three answers -- practices doc
    # section 5.5.0, and the measurement settles it.
    #
    #   error #dc3545 as TEXT on #f5f5f5   4.1528  FAIL, it is a fill colour
    #   error-text #e56b77 on #f5f5f5      2.8745  FAIL, it is a DARK-theme value
    #   this value on #f5f5f5              5.1810  pass
    #                on #ffffff            5.6485  pass
    #                on #eeeeee            4.8684  pass
    #                on #e8e8e8            4.6100  pass
    #
    # Same uniform per-channel step as every other derivation here, holding hue.
    # Named error-text-light rather than a fourth spelling: it is the light-mode
    # sibling of error-text above, and the pair should read as a pair.
    "error-text-light": "#b84e58",   # f5f5f5 4.51; re-derived from the corrected fill
}

# ------------------------------------------------------- texture + type
# ROLE -> {family, weights, ...}. Reshaped 2026-08-15 from role -> family.
#
# WHY THE SHAPE CHANGED: BRAND_TYPE.md rules a weight for every role -- the mark
# is Montserrat *Black*, not Montserrat -- and F8 rules one weight-axis standard
# per face, "request the weights actually drawn and nothing synthesised". A map
# of role to family string cannot express either, so both rulings were
# unenforceable at the source no matter how carefully they were written down.
#
# `weights` is a tuple of the weights that should be REQUESTED. For a variable
# face it holds the two endpoints of the range and `variable` is True; consumers
# read `variable` before reading the tuple. `italic` and `opsz` are carried where
# the face has them, because a font link that omits an axis silently synthesises
# it, which F8 forbids.
#
# THE MARK ROLE IS NEW AND IT CLOSES R1. tokens() builds font tokens by
# comprehension over this dict, so before today the emitter could produce exactly
# four font tokens while twelve pages consumed five. `--rnv-font-mark` was not
# missing from a list, it was unemittable, and any consumer adopting emit_css()
# lost the mark. Adding a role is additive: no existing token name or value
# moves, so no consumer breaks.
#
# THE SERIF ROLE IS NAMED `serif`, NOT `serif-italic`, AND THAT IS A CORRECTION.
# The old key emitted --rnv-font-serif-italic while forty-four references across
# twelve site files said --font-serif, so one value carried two names and no
# check compares a name-to-value binding. The source moved, not the site: same
# call as the ground ramp, and for the same reason once the evidence was read.
#
# THE EVIDENCE REVERSED THE ARGUMENT I HAD FOR KEEPING `serif-italic`. That name
# was defended on the grounds that the face is only ever drawn italic, so the
# name carried a ruling `serif` would lose. It is drawn BOTH ways: twenty-four
# rules set it with font-style italic, and eight draw the blog drop cap
# `article p:first-of-type::first-letter` in roman with no italic anywhere in
# the rule or its parents. `serif-italic` misdescribed a third of its own uses.
# `ital: (0, 1)` records both axes, which is also why the font link's `ital@0;1`
# is correct rather than an over-request.
#
# TWO CONFLICTS WITH THE REGISTER, encoded as measured rather than as ruled, and
# routed rather than silently resolved. BRAND_TYPE.md's mono row says 400/500/600;
# the canonical font link requests 400;500;600;700 and site rules that use
# --font-mono draw 500 and 700. The register understates by a weight that ships.
# And in the other direction, no site rule draws mono 400 or 600 explicitly --
# they may be inherited, or they may be two weights requested and never used,
# which is the same F8 violation from the other side. The values below match the
# shipped link; the register is the thing that needs the ruling.
TYPE = {
    "mark":         {"family": "Montserrat",          "weights": (900,)},
    "display":      {"family": "Bricolage Grotesque", "weights": (300, 800),
                     "variable": True, "opsz": (12, 96)},
    "serif":        {"family": "Instrument Serif",    "weights": (400,), "ital": (0, 1)},
    "mono":         {"family": "JetBrains Mono",      "weights": (400, 500, 600, 700)},
    "body":         {"family": "Inter",               "weights": (400, 500, 600)},
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
    "gold": BRAND_GOLD,
    "brand gold": BRAND_GOLD,
    "rnv gold": BRAND_GOLD,
    "dark gold": BRAND_DARK_GOLD,
    "gold dark": BRAND_DARK_GOLD,
    "light-mode gold": BRAND_DARK_GOLD,
    # THE SEVENTH PERMANENT WAS UNRESOLVABLE FOR A DAY. still-gold entered
    # PERMANENT on 2026-08-23 and no key here reached it, so the brand's own name
    # resolver refused a permanent brand colour. PERMANENT and RNV_BRAND are two
    # lists of the same thing, one gained a member and the other did not, and
    # NOTHING COMPARED THEM -- the construct-with-no-consumer failure between two
    # constructs that both have consumers.
    #
    # Guarded below by _resolver_covers_permanent(), which is the completeness
    # check that should have existed before the gap did.
    "still gold": BRAND_STILL_GOLD,
    "still-gold": BRAND_STILL_GOLD,
    "stillness": BRAND_STILL_GOLD,
    "standby gold": BRAND_STANDBY_GOLD,
    "standby-gold": BRAND_STANDBY_GOLD,
    "black": TRUE_BLACK,
    "true black": TRUE_BLACK,
    "white": WHITE,
    "brand white": WHITE,
    "web black": WEB_BLACK,
}

# ---------------------------------------------------------------- emitter

def _light_ladder_matches_dark_shares():
    """The light rungs must divide light's span as dark divides dark's.

    THE LADDER IS A DERIVATION, SO IT IS CHECKED RATHER THAN TRANSCRIBED. Both
    ladders are anchored on values that can move -- dark on BRAND_BLACK, light on
    a hover plate that has already moved once -- and if either end shifts the
    shares stop matching with nothing to say so. Tolerance 0.02, which is well
    inside the byte grid's own resolution near white.
    """
    import math

    def _lum(hexv):
        c = [int(hexv.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

    def _cr(a, b):
        la, lb = _lum(a), _lum(b)
        hi, lo = max(la, lb), min(la, lb)
        return (hi + 0.05) / (lo + 0.05)

    def _shares(rungs):
        total = math.log(_cr(rungs[0], rungs[-1]))
        return [math.log(_cr(rungs[i], rungs[i + 1])) / total
                for i in range(len(rungs) - 1)]

    dark = [APP["canvas"], APP["panel"], APP["card"], APP["panel-hover"]]
    light = [APP["surface-light"], APP["surface-light-2"],
             APP["surface-light-3"], APP["hover-light"]]
    for i, (d, l) in enumerate(zip(_shares(dark), _shares(light)), start=1):
        if abs(d - l) > 0.02:
            raise AssertionError(
                f"light ladder step {i} takes share {l:.3f} of light's span "
                f"where dark takes {d:.3f} of dark's -- off by {abs(d - l):.3f}. "
                f"One of the four anchors moved without the ladder being "
                f"re-derived. The rule is that light mirrors dark's PROPORTIONS, "
                f"not its step sizes; re-derive rather than nudging a rung."
            )


_light_ladder_matches_dark_shares()


def _deep_gold_clears_its_floor():
    """BRAND_DARK_GOLD_DEEP must clear 4.5:1 on GOLD_TEXT_GROUND_FLOOR.

    THE COUPLING THIS ENFORCES WAS DOCUMENTED AND UNCHECKED FOR A WEEK. The
    derivative is chosen as the smallest step clearing that ground; the ground is
    published as the boundary below which gold carries no text. Each is written in
    terms of the other, and until 2026-08-30 the ground was not even a key -- so a
    change to either would have left prose describing a relationship that no
    longer held, with nothing to say so.

    -13 gives 4.4675 here and fails. The margin is 0.0334, which is why this is a
    check and not a comment: a coupling that tight cannot be maintained by anyone
    remembering it.
    """
    def _lum(hexv):
        c = [int(hexv.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

    a, b = _lum(BRAND_DARK_GOLD_DEEP), _lum(GOLD_TEXT_GROUND_FLOOR)
    hi, lo = max(a, b), min(a, b)
    ratio = (hi + 0.05) / (lo + 0.05)
    if ratio < 4.5:
        raise AssertionError(
            f"BRAND_DARK_GOLD_DEEP {BRAND_DARK_GOLD_DEEP} reads {ratio:.4f} on "
            f"GOLD_TEXT_GROUND_FLOOR {GOLD_TEXT_GROUND_FLOOR}, under the 4.5 "
            f"floor. One of the two moved without the other -- the derivative is "
            f"defined as the smallest step that clears this ground, so if the "
            f"ground moved, re-derive; if the step moved, say why here."
        )


_deep_gold_clears_its_floor()


def _resolver_covers_permanent():
    """Every PERMANENT colour must be reachable by at least one resolver name.

    THE GAP THIS CLOSES EXISTED FOR A DAY AND NOTHING REPORTED IT. `still-gold`
    entered PERMANENT and no RNV_BRAND key reached it, so the brand's own name
    resolver refused a permanent brand colour. PERMANENT and RNV_BRAND are two
    lists of the same thing; one gained a member, the other did not, and nothing
    compared them.

    RUNS AT IMPORT, so a consumer mirroring this module fails on the mirror rather
    than discovering it when someone asks for the colour out loud. That is the
    difference between a check and a note: a note about this would have been true
    and unread.
    """
    reachable = set(RNV_BRAND.values())
    missing = {k: v for k, v in PERMANENT.items()
               if not k.startswith("_") and v not in reachable}
    if missing:
        raise AssertionError(
            "PERMANENT colours unreachable through RNV_BRAND: "
            + ", ".join(f"{k}={v}" for k, v in sorted(missing.items()))
            + " -- add a resolver key in the same change that adds the colour"
        )


_resolver_covers_permanent()


def tokens(surface: str = "web") -> dict[str, str]:
    """Flat token map for one surface; the emitter's source of truth."""
    palettes = {"web": WEB, "app": APP, "records": RECORDS}
    if surface not in palettes:
        raise ValueError("surface must be 'web', 'app', or 'records'")
    return {
        "gold": BRAND_GOLD,
        # `dark-gold`, matching PERMANENT and the constant. This file carried
        # THREE word orders for one colour until 2026-08-17 (234dca6) -- DARK_GOLD the
        # constant, "dark-gold" in PERMANENT, "gold-dark" emitted. Safe to move:
        # rnv-live consumed --rnv-gold-dark zero times, verified before landing,
        # and nothing else reads this namespace. verify_tokens catches it if that
        # ever stops being true.
        "dark-gold": BRAND_DARK_GOLD,
        "black": BRAND_BLACK,
        **palettes[surface],
        "rule": _rgba(BRAND_GOLD, RULE_ALPHA),
        **{f"status-{name}": value for name, value in STATUS.items()},
        # Reads spec["family"], not the value, since TYPE became a dict of dicts
        # on 2026-08-15. The emitted token name and string are unchanged for the
        # four roles that already existed; `mark` is new.
        **{f"font-{role}": f'"{spec["family"]}"' for role, spec in TYPE.items()},
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
# NVT Congratulation Poster — Design System (v1.0, derived from Era 4 / latest)

All values measured directly from pixels in `reference_crops/` and the NVT logo
masters at `~/Desktop/Nvt logo/`. See `design_system.json` for the machine-readable
version consumed by the skill's build script.

## Canvas
- **Primary: 1440×1800 px (4:5 portrait)** — the live Era-4 standard (Instagram
  in-feed crop). Some recent posts use 1638×2048 (identical 0.8 ratio, just
  higher-res) — treat as the same template at a different export size.
- **1:1 (1440×1440)** — for IG grid/profile-friendly reposts. Same template,
  recentre the photo block and shrink the footer bar proportionally.
- **9:16 (1080×1920)** — for Stories/Reels covers. Stack the same blocks with
  more vertical breathing room above/below the photo.
- Square (1080×1080) is the OLD (Era 2–3) standard — do not use for new work.

## Grid, margins, safe zones
- Outer margin: **80px at 1440 width (5.5%)** on all sides for text blocks;
  photo block may run wider (10% side margin) than text.
- Logo clear space: diameter of the microphone emblem on all sides (do not
  crop or let other elements enter this zone).
- Keep the bottom **8%** of the canvas reserved for the footer bar — never let
  body text or the photo frame encroach on it.
- Bottom-of-photo badge (medallion/ribbon) is allowed to overlap the photo's
  own corner but never the footer bar.

## Colour palette — confirmed & corrected
Your brief's recorded values (NVT Blue #1818F0, NVT Red #F01800) are
**confirmed** — direct pixel sampling of the "CONGRATULATIONS" script, the
achievement headline and the category pill across 6 Era-4 posters clustered
tightly around these two hexes (samples ranged #06047E–#212C99 for blue and
#E50F0E–#F70102 for red; the spread is anti-aliasing/compression noise around
a single source colour).

**NVT Amber #F0A830 is corrected.** Every Era-2 through Era-4 accent-yellow
sample (the footer bar, "RANK" word, medal ribbons) read as a bright lemon
yellow, not an orange-amber — measured #F9E41B, #FBEC5A, #EFD324. The system
token is now **NVT Yellow #FFE600**.

| Role | Token | Hex | Where it's used |
|---|---|---|---|
| Headline / script / name | NVT Blue | `#1818F0` | "CONGRATULATIONS" script, bold names, AIR numbers |
| Achievement / alert | NVT Red | `#F01800` | category pills, achievement line, JNV+state line |
| Accent / footer | NVT Yellow | `#FFE600` | footer bar, medal ribbons, sparkle accents |
| Body ink | Ink | `#111111` | all running body copy |
| Background (paper) | Paper | `#F8F6F1` | Template A/C background base, before grain texture |
| Background (dark) | Ink-Black | `#0A0A0A` | Template B background, Template C lower half |
| Neutral / secondary | Grey | `#6B7280` | captions, credit lines, de-emphasised text |
| White | White | `#FFFFFF` | text on dark backgrounds, card fills |

Rule: **1 headline colour (Blue) + 1 alert colour (Red) + 1 accent (Yellow) +
Ink**, per poster — never introduce a fifth hue. Keyword-highlighting inside
body paragraphs pulls from this same 3-colour set, never a new one.

The NVT logo itself is multi-coloured (orange→pink mic badge, blue wordmark,
red "Talk", green feather) and is **never** restricted to this palette — it is
reproduced exactly as supplied, at any size, on any approved background.

**Two palettes now coexist by design** (per your "offer both as separate
templates" call): Templates A/B/C use the richer Blue/Red/Yellow palette above
(measured from actual published posts). **Template D** uses the official
Brand Kit v2.0 palette strictly: Navodaya Blue `#2E35E8` (main) + Talk Red
`#F13B19` (accent) only — the kit's other named colours (Voice Orange
`#FF9F2D`, Mic Pink `#FF5FA2`, Mic Sky `#65C8EE`, Feather Green `#7ED957`) are
documented in the kit for *other* creative families (quote posts, educational
carousels, etc.), not for achievement creatives, so Template D doesn't use
them either.

## Typography
All fonts bundled in `assets/fonts/`.
- **Devanagari body & headlines:** Noto Sans Devanagari (bundled
  `NotoSansDevanagari.ttf`, variable weight 400–800). Use Tiro Devanagari Hindi
  only if a serif-leaning historic look is explicitly requested — Noto is the
  default for everything new.
- **Latin headlines / "CONGRATULATIONS":** a bold, rounded, slightly
  hand-drawn display face for the script treatment (Template A) — rendered as
  an SVG path (`assets/decor/congratulations_script.svg`) rather than a live
  font, since no exact match to the original hand-lettering exists locally;
  for Template B/C's bold caps "CONGRATULATIONS", use **Montserrat ExtraBold**
  (bundled) tracked +2%.
- **Latin body / names / UI:** Manrope (bundled, weight 500–800).
- Sizes at 1440px canvas width (scale proportionally for other sizes):
  - CONGRATULATIONS script: 90–110px cap-height
  - Achievement/category headline: 56–64px, weight 800
  - Name line: 48–54px, weight 800
  - Body paragraph: 34–40px, weight 500, line-height 1.35
  - Footer wordmark: 28px, weight 700
- Never go below **28px** body size even under long-text auto-fit (see rules
  below) — shrink the photo block or add a line instead.

## Photo rules
- Crop to include head + shoulders to roughly waist, centred, eyes in the
  upper third of the photo block. Never crop into the top of the head or
  through the chin.
- No background removal/cutout in the latest era — rectangular photo, light
  colour-correction only (level balance, no filters, no heavy saturation).
- Frame: rounded-rect, radius ~2% of photo width, border either a crisp 4–6px
  black/brand-colour line (Template A, formal subjects) or a hand-drawn
  yellow marker stroke (Template A, warmer/personal subjects) — see
  `assets/decor/marker_frame.svg`.
- Template B/C: no separate frame — photo bleeds to canvas edges and is
  blended into the background via a gradient scrim (cream→black or white→black
  per the template).
- If supplied photo is under 800px on its short side, gently upscale (Lanczos,
  max 1.5×) and warn the user the source is low-resolution.
- Never alter facial features. Never add filters that change skin tone.

## Logo rules
- Source master: `assets/logo/nvt_logo_light.png` (transparent, for light/
  paper backgrounds) and `assets/logo/nvt_logo_dark_halo.png` (pre-built soft
  white halo, for Template B/C dark backgrounds).
- Never recolour, restretch (always preserve aspect ratio), or redraw the
  logo. Never merge it with the NVS/JNV Samiti emblem — if a JNV emblem is
  also required (Template A appointment variant), place it as its own element,
  never combined into one mark.
- Clear space: the logo's own height on every side.
- Placement: centred top (Template A, large lockup, 18–20% of canvas width) OR
  small top-left corner (Template A compact, 10–12% of canvas width;
  Templates B/C always use this small corner placement, since the full-bleed
  photo needs headroom).

## Layout templates (measured from Era 4 / latest)

### Template A — Portrait & Statement (default; exam ranks, appointments, honours)
Canvas 1440×1800.
| Block | x | y | notes |
|---|---|---|---|
| Logo | 41–59% | 4–13% | centred lockup |
| "CONGRATULATIONS" script | 22–78% | 14–22% | sparkle flourish + double underline |
| Category pill (optional) | 30–70% | 24–30% | red fill, white bold text, e.g. "UPSC CSE 2025" |
| Fact sentence (2–3 lines) | 9–91% | 31–43% | mixed Blue/Red/Ink spans |
| Photo frame | 10–90% | 45–82% | black or yellow-marker rounded border |
| Rank medallion (optional) | 75–93% | 70–82% | gold ribbon badge, overlaps photo corner |
| JNV + state line | 9–91% | 83–89% | Red (JNV name) + Ink (state line) |
| Footer bar | 0–100% | 92–100% | solid Yellow, icons + wordmark centred |

### Template B — Editorial Honor (ceremony/group photos, no clean portrait)
Canvas 1638×2048.
| Block | x | y | notes |
|---|---|---|---|
| Photo (full-bleed) | 0–100% | 0–62% | gradient scrim to black at bottom |
| Logo | 22–32% | 58–66% | overlaid on photo near the scrim seam |
| "CONGRATULATIONS" | 0–100% | 60–68% | bold Yellow caps, straddles photo/text seam |
| Citation paragraph | 6–94% | 70–84% | dashed white border box, keyword highlights |
| Footer info bar (3-col) | 0–100% | 88–96% | name+role / medal icon / award+reason |
| Icon row | 0–100% | 96–100% | on black, no bar |

### Template C — Achievement Spotlight (sports/physical achievement)
Canvas 1638×2048.
| Block | x | y | notes |
|---|---|---|---|
| Logo | 2–10% | 2–7% | small, top-left |
| Photo | 0–100% | 0–68% | cream→black gradient scrim, ghosted watermark right |
| Event-name pill | 15–85% | 56–63% | dashed pill, drop shadow |
| Medal sub-headline | 25–75% | 64–68% | bold Yellow |
| Name plate | 15–70% | 70–75% | torn-paper/brush-stroke rect behind bold name |
| Body paragraph | 6–94% | 82–94% | white text, Yellow/Red keyword highlights, on black |
| Icon row | 0–100% | 96–100% | plain, on black |

### Template D — Official Brand Kit (Achievement Creative, per Brand Kit v2.0 p.12)
Canvas 1080×1350 (the kit's own Instagram-post size, p.8), 90px safe margin.
This is the **official written spec**, distinct from Templates A/B/C (which
follow what the Instagram account has actually been publishing). Use D when a
clean, restrained, strictly-on-brand-kit creative is wanted instead of the
richer Instagram house style.
| Block | notes |
|---|---|
| Headline | top-left, Talk Red `#F13B19`, bold, left-aligned — "CONGRATULATIONS" or a short specific headline |
| Photo | plain rectangle, 1px light-grey border, no frame/badge/decoration |
| Name | Navodaya Blue `#2E35E8`, bold |
| Role line | "Rank / Exam / role" — one plain Ink line |
| JNV + state line | one plain Ink line |
| Batch line (optional) | one plain Ink line |
| Source/verification note (optional) | small, grey, italic |
| Logo | small (4–5% of canvas width), bottom-right corner only |

Brand-kit colour discipline for this template: **one main colour (Blue) + one
accent (Red) only** — never introduce Yellow/Orange/Pink/Green here. No
gradients, no shadows, no glow, one font family per language (Manrope +
Noto Sans Devanagari) — the kit's Don'ts (p.13) are hard rules for Template D,
not just guidance.

## Rules for edge cases
- **Long names** (>22 characters): drop to the next size step (−10%) once;
  if still overflowing, wrap to a second line within the name block — never
  shrink below the 48px floor or truncate.
- **Long achievement lines**: prefer rewording/wrapping over shrinking;
  category pill text wraps to 2 lines centre-aligned before its font shrinks.
- **Two-line headlines**: keep the hand-drawn underline under the full two-line
  block, not just line 1; increase line-height to 1.2 for the script face to
  avoid ascender/descender collisions.
- If after one size-step-down and one wrap attempt text still overflows its
  block, stop and flag it to the user rather than silently shrinking further
  or letting it bleed outside the safe margin.

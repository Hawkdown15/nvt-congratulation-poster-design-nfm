---
name: nvt-congratulation-poster-design-nfm
description: Design a Navodayans Talk (NVT) congratulation poster from a person's photo and achievement facts, in NVT's latest brand style. Triggers on "congratulation poster", "badhai poster", "NVT poster", "बधाई पोस्टर", a photo plus achievement text, or a request to congratulate a JNV alumnus on Navodayans Talk.
---

# NVT Congratulation Poster

Builds a poster in Navodayans Talk's current (2026) house style, derived from
156 real NVT posters spanning 2022-2026 — see `evolution.md` for the research
and `design_system.md` / `design_system.json` for the exact measured values
(colours, type scale, layout grids) this skill enforces.

## What this skill will never do
- Invent a rank, post, exam name, JNV name, batch year, or any other fact not
  given by the user. If a fact is missing, ask for it — never guess, never
  pull a plausible-sounding number.
- Alter the person's face or features (no face-swap, no reshaping, no
  skin-tone changes — see `design_system.md` Photo rules).
- Recolour, redraw, restretch, or merge the NVT logo with anything else.
- Silently shrink text past the floor in `design_system.json`
  (`overflow_rules.never`) or let it bleed outside the safe margins — it stops
  and flags instead (see Step 4).

## Step 1 — Collect inputs
You need: a photo, and the person's name + achievement. From the text the
user gives, extract whatever of these fields are present:
- `person_name`
- `achievement` (exam/rank/post/medal/honour — whatever applies)
- `category` (exam name + year, e.g. "UPSC CSE 2025" — optional, maps to the
  category pill)
- `jnv_name` (which JNV, e.g. "जवाहर नवोदय विद्यालय, कुशीनगर")
- `state_or_context` (state, or an appointment/award detail line)
- `photo`

Ask for whatever is missing, **in one round, in Hinglish**, e.g.:
"Bas ek cheez chahiye — kaunsa JNV aur kaunsa state the?" Don't ask about
template choice or size unless the user's phrasing suggests they want to pick
(then offer Template A/B/C — see `design_system.md` for which fits which photo
type — and canvas: primary 4:5 / square 1:1 / story 9:16).

## Step 2 — Pick a template and write the Hindi message
Two families exist (ask the user if it's not obvious which they want — this
is a real fork, not a default to guess past):
- **A / B / C — Instagram house style.** Richer, matches what NVT has
  actually been publishing (paper texture, ribbon badges, handwritten
  headline). Pick by photo type (see `design_system.md` → Layout templates):
  - Clean single-subject photo + a rank/exam/appointment/honour →
    **Template A** (`templates/template_a.html`) — the default within this
    family.
  - Ceremony/news photo with multiple people, no clean solo portrait →
    **Template B** (`templates/template_b.html`).
  - Sports/physical-achievement action or medal photo → **Template C**
    (`templates/template_c.html`).
- **D — Official Brand Kit.** Strictly follows Brand Kit v2.0 p.12: plain
  card, one main colour (Blue) + one accent (Red) only, small corner logo, no
  gradients/shadows/decorative fonts (`templates/template_d.html`). Use this
  when the user wants the clean/official look, or for any context where strict
  brand-kit compliance matters more than matching the Instagram archive.

Use the name, achievement and other facts **exactly as given**. If the user
gave only bare facts (no ready sentence), write the congratulations message
yourself in Hindi, in the tone of the reference posters (`examples/` and
`evolution.md`) — formal-warm, third-person, ending in "...हार्दिक बधाई एवं
शुभकामनाएँ।" — and **show it to the user for approval before rendering**.

## Step 3 — Prepare the photo
```
python3 scripts/prepare_photo.py --in <raw_photo> --out <prepared_photo.jpg>
```
This detects the face (YuNet), crops to head+shoulders with eyes in the upper
third, applies light CLAHE levelling only, and upscales gently (max 1.5x) if
the source is under 800px on its short side — it will print a WARNING if it
had to upscale; pass that warning on to the user rather than silently
proceeding. If no face is detected it falls back to the full photo and warns —
check the framing yourself before rendering. Pass `--no-crop` if the user
already supplies a pre-cropped/pre-framed photo.

## Step 4 — Build the poster
Write a JSON data file (see each template's field list in
`scripts/build_poster.py`'s docstring, and the worked examples in
`tests/` from this skill's own build) and render:
```
python3 scripts/build_poster.py --data poster.json --template A --out out/poster.png
```
This applies the `overflow_rules` from `design_system.json` automatically
(shrinks once, then — if still over the hard character limit — prints a
WARNING instead of shrinking further). **If you see that warning, stop and
tell the user to shorten the line; don't re-render hoping it fits.**

## Step 5 — QA
```
python3 scripts/qa_check.py --png out/poster.png --data poster.json --canvas primary
```
This is a mechanical safety net (canvas size, logo not blank, OCR can find the
name/JNV text you supplied) — **not** a substitute for actually looking at the
rendered PNG yourself. Read the poster: check Hindi matras/conjuncts rendered
correctly, the name spelling matches the user's input exactly, the logo
position/size, safe margins, the face isn't cropped oddly, and contrast is
readable. Compare side-by-side against a latest-era example in `examples/` if
anything looks off.

## Step 6 — Output
Save to `~/Desktop/NVT Posters/<YYYY-MM-DD>_<Name>/`:
- `poster.png` (full resolution)
- `poster.jpg` (for upload — `build_poster.py` writes this automatically)
- any other size variant asked for (re-run `build_poster.py` with a different
  `canvas` value: `primary` 4:5, `square` 1:1, `story` 9:16)

Show the user the poster and offer: change text / change photo crop / try
another template.

## Reference material in this skill
- `evolution.md` — the 5-era history and what's constant vs. what changed.
- `design_system.md` / `design_system.json` — exact colours, type, grid,
  photo/logo rules, and the 3 layout templates' measured block positions.
- `examples/` — 4 real latest-era reference posters to compare against.
- `assets/logo/` — `nvt_logo_light.png` (transparent, light backgrounds),
  `nvt_logo_dark_halo.png` (transparent with built-in soft white halo, dark
  backgrounds) — never redraw or recolour these — and `brand_kit_v2.pdf`, the
  official Navodayans Talk Brand Kit v2.0 (16pp) that Template D follows
  exactly; re-read it if you need the rules for a creative type this skill
  doesn't cover (quote posts, reels covers, carousels, etc.).
- `assets/fonts/` — Noto Sans Devanagari, Tiro Devanagari Hindi, Manrope,
  Montserrat, Anton, Permanent Marker (all bundled, no network needed to
  render).
- `assets/decor/` — paper texture, hand-drawn marker-frame overlays, sparkle
  flourish, dot-grid — generated by `scripts/make_decor_assets.py` (re-run
  only if you want to regenerate/vary them; the current files are already in
  place).

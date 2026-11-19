# Navodayans Talk — Congratulation Poster Evolution

Source: 1,389 scraped Instagram posts from `@navodayanstalk` (no curated reference
folder existed — see note at the end). OCR + manual visual triage found **156
genuine congratulation posters** spanning March 2022 to September 2026, after
excluding festival/occasion graphics (Republic Day, Rakhi, Janmashtami, etc.)
that share the same brand but aren't congratulation posters. Full list:
`poster_analysis.csv`. Contact sheets per era: `era_contact_sheets/`.

## Era 1 — Card Experimental (Mar–Oct 2022, 9 posts)
Inconsistent: most 2022 posts are book-cover reveals or newspaper-clipping
collages, not a settled congratulations format. The one clean example
(`era1_card_SubharshSingh.png`) already shows the DNA that survives today: a
centred full-colour logo, a bordered box holding the key fact, and the brand
yellow. But there's no repeatable template yet — layout, photo treatment and
colour all vary post to post.

## Era 2 — Black-Frame Rank Cascade (Jan 2023–Mar 2025, 97 posts — the workhorse)
The format that defined NVT for two years. Square canvas, solid black
background with a thin white outline frame, the subject's photo bled full-width
with a soft vignette fade, and oversized cascading rank numerals (white →
yellow → red, one word per line: `239 / th`, `RANK`, `UPSC`) overlapping the
photo's top-left. Bold yellow "CONGRATULATIONS" in condensed caps. A 3-line
justified Hindi paragraph in white, with the person's name, home district and
exam detail each picked out in a different highlight colour. This is where
**colour-coded keyword highlighting inside the body text** was born — it's the
single most persistent device in NVT's whole history.

## Era 3 — Gradient Transition (Apr–Aug 2025, 16 posts)
A short-lived redesign, visibly where Nav Fusion Media's hand first shows.
Dropped the black background and white frame; the photo now alpha-fades
directly into a flat white canvas. Typography switched to a bold condensed
display face (Anton/Bebas-style) in place of the old sign-painter caps.
First appearance of a YouTube "SUBSCRIBE" call-to-action pill in the footer.
Kept the oversized rank-numeral motif but simplified its colour to one flat
red/navy pair instead of three cascading colours.

## Era 4 — Paper & Premium Editorial (Sep 2025–present, 34 posts) — **LATEST**
The current, most accomplished era, and the base for the skill. Canvas moved
from square to 4:5 portrait. Three distinct layout templates now coexist,
chosen by content type rather than one-size-fits-all:

- **Template A — Portrait & Statement.** Cream paper-grain background (with a
  faint diagonal repeat of the wordmark as a watermark), a single rectangular
  portrait photo in either a crisp black rounded border or a hand-drawn yellow
  marker-stroke border, a handwritten-script blue "CONGRATULATIONS" with a
  sparkle flourish and double underline, a red achievement headline, a 3-line
  fact block, and a solid yellow footer bar with flat social icons. A gold
  ribbon medallion badge for the rank number is pinned over the photo's corner
  on exam-result posts. This is the most common latest-era layout — used for
  exam ranks, appointments and honours alike.
- **Template B — Editorial Honor.** For ceremony/news photos (multiple people,
  no clean single portrait available). Full-bleed photo fading to black via a
  gradient scrim, bold yellow caps "CONGRATULATIONS" straddling the photo/text
  seam, a dashed-border citation paragraph with inline colour-keyword
  highlights, and a 3-column dark footer bar (name+role / medal icon /
  award name+reason).
- **Template C — Achievement Spotlight.** For sports and physical
  achievements. Portrait photo gradient-fading cream-to-black with a ghosted
  sport-silhouette watermark, a dashed-pill event-name headline, a torn-paper
  brush-stroke name plate, and a highlighted-keyword body paragraph on black.

## What got better over time
- Canvas: square → 4:5 portrait (matches how Instagram now crops in-feed).
- Photo treatment: hard black-bg cutout-less bleed → soft paper-texture
  background with a proper photo frame — reads calmer and more premium.
- Typography: a single bold-caps mood (Era 2–3) → a mixed register (Era 4)
  that pairs a handwritten "human" headline with a disciplined bold-sans fact
  block — friendlier without losing clarity.
- Information hierarchy: Era 2's 3-line paragraph crammed name+place+exam
  together; Era 4 separates WHO / WHAT / WHERE into distinct visual blocks.
- Content-specific templates (A/B/C) replaced one rigid format, so a ceremony
  photo or a sports photo no longer gets forced into an exam-result frame.

## What got dropped
- Newspaper/collage layouts (Era 1) — too inconsistent to repeat.
- Hard black canvas + white outline frame (Era 2) — replaced by the paper
  texture, which photographs better on mobile screens and in print.
- Bare, un-boxed footer icons with no bar (Era 1 and 3) — Era 4 always frames
  the footer, either as a solid bar (Template A) or a dark info strip
  (Template B).
- The YouTube "SUBSCRIBE" CTA pill (Era 3) — not carried into Era 4; the brief
  stays focused on the congratulations message.

## What has stayed constant across all 5 years (the core NVT identity)
1. **The NVT logo** — never recoloured, never redrawn, always on a light or
   neutral ground, always present.
2. **"CONGRATULATIONS" in English** as the universal headline word, even
   though every surrounding sentence is in Hindi.
3. **A fixed WHO + WHAT + WHERE structure** — name, achievement/rank/post, and
   JNV name + state, always present, always in that order.
4. **Colour-coded keyword highlighting** inside the Hindi body paragraph —
   present since Era 2, still present in Era 4.
5. **A social-icon + "Navodayans Talk" wordmark footer** on every single
   poster, in every era.
6. **Single-subject portrait photography** (never a multi-person collage as
   the hero image) from Era 2 onward.

## Note on the reference set
The brief expected a pre-curated folder with `index.csv` and date-prefixed
filenames; what existed on disk instead was a raw, undeduplicated Instagram
scrape (`_work/all_posts/instagram/`) covering ~20 accounts. There was no
curated congratulations-only set. Per your direction, I built one myself:
Hindi+English OCR over all 1,389 `navodayanstalk` posts flagged 175
candidates, which I then visually triaged (era contact sheets in this folder)
down to the 156 genuine congratulation posters catalogued here.

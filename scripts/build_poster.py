"""Render a congratulation poster from structured JSON data + a Jinja2/HTML
template, via headless Chromium (Playwright). No network access needed.

Usage:
    python3 build_poster.py --data poster.json --template A --out out/poster.png

poster.json fields (template A):
  congrats_word (default "CONGRATULATIONS")
  category_label (optional)
  fact_html   - pre-built HTML string with <span class="name">/<span class="achieve"> wraps
  photo_path  - absolute path to the prepared (cropped) photo
  frame_style - "black" | "yellow"
  medallion_text (optional, e.g. "AIR 371")
  jnv_name, state_line
  logo_mode   - "centered" | "corner"
  canvas      - "primary" | "square" | "story"  (default "primary")

poster.json fields (template D — official Brand Kit v2.0 p.12 "Achievement
Creatives" layout: plain card, one main + one accent colour, small corner
logo, no gradients/shadows/decorative fonts):
  achievement_headline  - e.g. "CONGRATULATIONS" (Talk Red, left-aligned)
  photo_path
  person_name            (Navodaya Blue, bold) — set name_is_devanagari:true if Hindi
  role_line               - "Rank / Exam / role" one line (kit hierarchy item 3)
  jnv_state_line          - JNV name + state (kit hierarchy item 4)
  batch_line (optional)   - batch/year (kit hierarchy item 5)
  source_note (optional)  - verification note, small grey italic (kit hierarchy item 6)
  canvas      - default "kit_post" (1080x1350, the kit's own IG-post size)
"""
import argparse, json, os, re, sys
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
from PIL import Image

NAME_CHAR_THRESHOLD = 22   # design_system.json overflow_rules.long_name_chars_threshold
FACT_CHAR_SOFT_LIMIT = 140  # ~3 lines at default size on a 1440-wide canvas
FACT_CHAR_HARD_LIMIT = 220  # beyond this, stop shrinking and flag instead


def _plain(html):
    return re.sub("<[^>]+>", "", html or "")


def apply_overflow_rules(data):
    """Mutates data in place: adds a fact_scale (CSS %) and jnv_scale, plus a
    'warnings' list the caller should surface to the user instead of silently
    shrinking further (design_system.json overflow_rules)."""
    warnings = []

    fact_len = len(_plain(data.get("fact_html", "")))
    if fact_len > FACT_CHAR_HARD_LIMIT:
        warnings.append(
            f"fact_html is {fact_len} chars (hard limit {FACT_CHAR_HARD_LIMIT}) — "
            "reword/shorten it rather than relying on auto-shrink, or text will crowd the photo block."
        )
        data["fact_scale"] = 80
    elif fact_len > FACT_CHAR_SOFT_LIMIT:
        data["fact_scale"] = 88
    else:
        data["fact_scale"] = 100

    name_len = len(_plain(data.get("jnv_name", "")))
    if name_len > NAME_CHAR_THRESHOLD:
        data["jnv_scale"] = 85
    else:
        data["jnv_scale"] = 100

    data["_overflow_warnings"] = warnings
    return warnings

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(SKILL_DIR, "templates")
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
DECOR_DIR = os.path.join(ASSETS_DIR, "decor")
LOGO_DIR = os.path.join(ASSETS_DIR, "logo")

CANVAS_SIZES = {
    "primary": (1440, 1800),
    "square": (1440, 1440),
    "story": (1080, 1920),
    "kit_post": (1080, 1350),   # Brand Kit v2.0 p.8 Instagram-post size, for Template D
}

TEMPLATE_FILES = {
    "A": "template_a.html",
    "B": "template_b.html",
    "C": "template_c.html",
    "D": "template_d.html",
}


def render(data, template_key, out_png):
    canvas_key = data.get("canvas", "kit_post" if template_key == "D" else "primary")
    w, h = CANVAS_SIZES[canvas_key]

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    tpl = env.get_template(TEMPLATE_FILES[template_key])

    logo_default = "nvt_logo_dark_halo.png" if template_key in ("B", "C") else "nvt_logo_light.png"
    ctx = dict(data)
    ctx.setdefault("fonts_dir", FONTS_DIR)
    ctx.setdefault("decor_dir", DECOR_DIR)
    ctx.setdefault("logo_path", os.path.join(LOGO_DIR, data.get("logo_file", logo_default)))
    ctx.setdefault("canvas_w", w)
    ctx.setdefault("canvas_h", h)
    ctx.setdefault("congrats_word", "CONGRATULATIONS")
    ctx.setdefault("logo_mode", "centered")
    if template_key == "D":
        # Brand Kit v2.0 p.8: 90px safe margin @ 1080 wide; scale proportionally for other widths
        ctx.setdefault("margin_px", round(90 * w / 1080))
        ctx.setdefault("logo_height_px", round(42 * w / 1080))

    warnings = apply_overflow_rules(ctx) if template_key == "A" else []

    html = tpl.render(**ctx)
    tmp_html = out_png + ".tmp.html"
    with open(tmp_html, "w") as f:
        f.write(html)

    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(250)
        page.screenshot(path=out_png)
        browser.close()
    os.remove(tmp_html)

    # JPG companion for upload
    jpg_path = os.path.splitext(out_png)[0] + ".jpg"
    Image.open(out_png).convert("RGB").save(jpg_path, quality=92)
    return out_png, jpg_path, warnings


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="path to poster JSON")
    ap.add_argument("--template", required=True, choices=["A", "B", "C", "D"])
    ap.add_argument("--out", required=True, help="output PNG path")
    args = ap.parse_args()

    with open(args.data) as f:
        data = json.load(f)

    png, jpg, warnings = render(data, args.template, args.out)
    print("PNG:", png)
    print("JPG:", jpg)
    for w in warnings:
        print("WARNING:", w)

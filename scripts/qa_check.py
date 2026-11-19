"""Automated self-check for a rendered poster, run right after build_poster.py.
Not a substitute for looking at the image — just catches the common failure
modes: wrong canvas size, missing/blank logo, and text that didn't actually
render (OCR round-trip on the name + JNV fields you supplied).

Usage:
    python3 qa_check.py --png out/poster.png --data poster.json [--canvas primary]
"""
import argparse, json, subprocess, sys
from PIL import Image

CANVAS_SIZES = {"primary": (1440, 1800), "square": (1440, 1440), "story": (1080, 1920),
                 "kit_post": (1080, 1350)}


def ocr_text(path):
    out = subprocess.run(["tesseract", path, "stdout", "-l", "hin+eng", "--psm", "11"],
                          capture_output=True, text=True, timeout=30)
    return out.stdout


def check(png_path, data, canvas_key):
    issues = []
    im = Image.open(png_path)
    expected_w, expected_h = CANVAS_SIZES[canvas_key]
    # screenshot may be 2x (device_scale_factor) — accept exact or 2x
    ok_size = (im.size in [(expected_w, expected_h), (expected_w * 2, expected_h * 2)])
    if not ok_size:
        issues.append(f"canvas size {im.size} does not match expected {expected_w}x{expected_h} (or 2x)")

    # logo sanity: sample a few points near top where logo should be (template A default)
    arr = im.convert("RGB")
    w, h = arr.size
    sample_pts = [(int(w * 0.5), int(h * 0.08)), (int(w * 0.06), int(h * 0.05))]
    bg_like = [c for c in [arr.getpixel(p) for p in sample_pts]
               if sum(abs(v - 248) for v in c) < 25]  # close to paper colour on all points = suspicious
    if len(bg_like) == len(sample_pts):
        issues.append("logo area looks blank at both expected positions (centered + corner) — check logo_path")

    text = ocr_text(png_path)
    name_fields = []
    for key in ("person_name", "jnv_name", "name"):
        if key in data and data[key]:
            name_fields.append(data[key])
    # fact_html / citation_html / body_html may embed the name instead of a dedicated field
    for key in ("fact_html", "citation_html", "body_html"):
        if key in data and data[key]:
            name_fields.append(data[key])

    missing = []
    for field in name_fields:
        # strip simple html tags for a rough substring check
        import re
        plain = re.sub("<[^>]+>", "", field)
        # check the first 6 chars of each word >=3 chars long survive in OCR text
        words = [wd for wd in plain.split() if len(wd) >= 3]
        found_any = any(wd[:4] in text for wd in words[:3]) if words else True
        if not found_any:
            missing.append(plain[:40])
    if missing:
        issues.append(f"OCR could not confirm these fields rendered: {missing}")

    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--canvas", default="primary", choices=list(CANVAS_SIZES))
    args = ap.parse_args()

    with open(args.data) as f:
        data = json.load(f)

    issues = check(args.png, data, args.canvas)
    if issues:
        print("QA: ISSUES FOUND")
        for i in issues:
            print(" -", i)
        sys.exit(1)
    else:
        print("QA: OK (size, logo, text all present — still look at the image yourself)")

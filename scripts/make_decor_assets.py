"""One-time generator for the skill's decorative assets (paper texture, hand-drawn
frame overlay, sparkle flourish). Run once; outputs land in assets/decor/."""
import os, random, math
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECOR = os.path.join(HERE, "assets", "decor")
os.makedirs(DECOR, exist_ok=True)


def make_paper_texture(path, size=512, base=(248, 246, 241), seed=7):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 1, (size, size))
    # smooth it a little (cheap box blur) for a paper-grain (not static) look
    k = 3
    pad = np.pad(noise, k, mode="wrap")
    smooth = np.zeros_like(noise)
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            smooth += pad[k + dy:k + dy + size, k + dx:k + dx + size]
    smooth /= (2 * k + 1) ** 2
    smooth = (smooth - smooth.min()) / (smooth.max() - smooth.min())
    arr = np.zeros((size, size, 4), dtype=np.uint8)
    for c in range(3):
        arr[:, :, c] = np.clip(base[c] + (smooth - 0.5) * 22, 0, 255).astype(np.uint8)
    arr[:, :, 3] = 255
    Image.fromarray(arr, "RGBA").save(path)
    print("wrote", path)


def wobble_rounded_rect_path(w, h, r, wobble=2.0, seed=1):
    rng = random.Random(seed)
    pts = []
    n = 40
    for i in range(n):
        t = i / n
        # parametrize a rounded rect perimeter roughly, then jitter
        ang = t * 2 * math.pi
        # superellipse-ish blend toward rect
        x = w / 2 * math.copysign(abs(math.cos(ang)) ** 0.35, math.cos(ang))
        y = h / 2 * math.copysign(abs(math.sin(ang)) ** 0.35, math.sin(ang))
        x += w / 2 + rng.uniform(-wobble, wobble)
        y += h / 2 + rng.uniform(-wobble, wobble)
        pts.append((x, y))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} "
    for p in pts[1:]:
        d += f"L {p[0]:.1f},{p[1]:.1f} "
    d += "Z"
    return d


def make_marker_frame(path, w=600, h=760, stroke="#FFE600", sw=16):
    d = wobble_rounded_rect_path(w - sw, h - sw, 40, wobble=3.5, seed=3)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <g transform="translate({sw/2},{sw/2})">
    <path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"
          stroke-linejoin="round" stroke-linecap="round" opacity="0.95"/>
  </g>
</svg>'''
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", path)


def make_marker_frame_dark(path, w=600, h=760, stroke="#111111", sw=10):
    d = wobble_rounded_rect_path(w - sw, h - sw, 28, wobble=1.5, seed=9)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <g transform="translate({sw/2},{sw/2})">
    <path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"
          stroke-linejoin="round" stroke-linecap="round"/>
  </g>
</svg>'''
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", path)


def make_sparkle(path, color="#1818F0"):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 90" width="220" height="90">
  <g stroke="{color}" stroke-width="3" fill="none" stroke-linecap="round">
    <path d="M10,45 C 40,15 70,15 100,30" stroke-dasharray="1 10"/>
    <path d="M100,30 C 115,38 130,10 150,45" stroke-dasharray="1 10" opacity="0.6"/>
  </g>
  <g fill="{color}">
    <circle cx="8" cy="46" r="3"/>
    <circle cx="190" cy="20" r="2.5"/>
    <path d="M200,55 l3,8 l8,3 l-8,3 l-3,8 l-3,-8 l-8,-3 l8,-3 Z"/>
  </g>
</svg>'''
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", path)


def make_dot_grid(path, color="#FFFFFF"):
    dots = ""
    for yy in range(6):
        for xx in range(6):
            dots += f'<circle cx="{10+xx*16}" cy="{10+yy*16}" r="2" fill="{color}" opacity="0.5"/>'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">{dots}</svg>'
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", path)


if __name__ == "__main__":
    make_paper_texture(os.path.join(DECOR, "paper_texture.png"))
    make_marker_frame(os.path.join(DECOR, "marker_frame_yellow.svg"))
    make_marker_frame_dark(os.path.join(DECOR, "marker_frame_black.svg"))
    make_sparkle(os.path.join(DECOR, "sparkle_blue.svg"), "#1818F0")
    make_dot_grid(os.path.join(DECOR, "dot_grid_white.svg"), "#FFFFFF")

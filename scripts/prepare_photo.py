"""Prepare a raw user photo for a congratulation poster: detect the face,
crop to head+shoulders with eyes in the upper third, light auto-levels colour
correction, and gentle upscaling if the source is small. Never touches facial
features. No background removal (latest era uses rectangular photos, not cutouts).

Usage:
    python3 prepare_photo.py --in photo.jpg --out prepared.jpg [--target-ratio 0.75]
"""
import argparse, os, sys
import cv2
import numpy as np
from PIL import Image

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "assets", "models", "face_detection_yunet_2023mar.onnx")
MIN_SOURCE_PX = 800
MAX_UPSCALE = 1.5


def detect_face(img_bgr):
    h, w = img_bgr.shape[:2]
    detector = cv2.FaceDetectorYN_create(MODEL_PATH, "", (w, h), score_threshold=0.7)
    _, faces = detector.detect(img_bgr)
    if faces is None or len(faces) == 0:
        return None
    # largest face = main subject
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    x, y, fw, fh = faces[0][:4]
    return int(x), int(y), int(fw), int(fh)


def auto_levels(img_bgr):
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    l2 = clahe.apply(l)
    merged = cv2.merge((l2, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def crop_head_shoulders(img_bgr, face, target_ratio, zoom=3.0):
    x, y, w, h = face
    cx = x + w / 2
    eye_y = y + h * 0.4  # approx eye line within detected face box

    # Head+shoulders box: ~zoom x face width wide, eyes sit at ~33% from top
    box_w = w * zoom
    box_h = box_w / target_ratio
    top = eye_y - box_h * 0.33
    left = cx - box_w / 2

    H, W = img_bgr.shape[:2]
    left = max(0, min(left, W - box_w))
    top = max(0, min(top, H - box_h))
    box_w = min(box_w, W - left)
    box_h = min(box_h, H - top)

    l, t, r, b = int(left), int(top), int(left + box_w), int(top + box_h)
    return img_bgr[t:b, l:r]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--target-ratio", type=float, default=0.78,
                     help="crop width/height ratio (default ~4:5 portrait box)")
    ap.add_argument("--zoom", type=float, default=3.0,
                     help="crop width as a multiple of detected face width — lower = tighter on face+shoulders, less background (default 3.0)")
    ap.add_argument("--no-crop", action="store_true",
                     help="skip face-crop, only colour-correct/upscale (use when photo is pre-cropped)")
    args = ap.parse_args()

    img = cv2.imread(args.inp)
    if img is None:
        print(f"ERROR: could not read {args.inp}", file=sys.stderr)
        sys.exit(1)

    short_side = min(img.shape[0], img.shape[1])
    warn = None
    if short_side < MIN_SOURCE_PX:
        scale = min(MAX_UPSCALE, MIN_SOURCE_PX / short_side)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)
        warn = f"source photo short side was {short_side}px (<{MIN_SOURCE_PX}); upscaled {scale:.2f}x — quality may be soft"

    if not args.no_crop:
        face = detect_face(img)
        if face is not None:
            img = crop_head_shoulders(img, face, args.target_ratio, zoom=args.zoom)
        else:
            print("WARNING: no face detected — using full photo uncropped, check framing manually", file=sys.stderr)

    img = auto_levels(img)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    cv2.imwrite(args.out, img, [cv2.IMWRITE_JPEG_QUALITY, 95])

    if warn:
        print("WARNING:", warn, file=sys.stderr)
    print("OK:", args.out)


if __name__ == "__main__":
    main()

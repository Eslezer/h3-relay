#!/usr/bin/env python3
"""Expression sheets through the H3 relay: pad the portrait, queue the clips, then crop the held frames.

    python sheet.py prep portrait.png                 # -> work/frame.png (padded to the canvas)
    python sheet.py prompts                           # write work/prompts/clipNN.txt to review
    python sheet.py submit --only 7                   # queue one test clip
    python sheet.py submit                            # queue every clip not queued yet
    python sheet.py crop                              # fetch finished clips, write work/out/NN-name.png

Needs h3relay.py (next to this file, at the repo root, or pass --client) plus Pillow, numpy and ffmpeg.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from expressions import CLIPS, ORDER, SECONDS, WINDOWS, prompt_for  # noqa: E402

FPS = 24


def load_client(path: str | None):
    here = Path(__file__).resolve().parent
    for p in filter(None, [path and Path(path), here / "h3relay.py", here.parents[1] / "h3relay.py",
                           Path.cwd() / "h3relay.py"]):
        if p.is_file():
            spec = importlib.util.spec_from_file_location("h3relay", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    sys.exit("error: can't find h3relay.py; pass --client path/to/h3relay.py")


def canvas(size: str):
    w, h = (int(v) for v in size.lower().split("x"))
    return w, h


def square_box(w: int, h: int):
    """Where the square portrait sits on the canvas (centered, full height)."""
    side = min(w, h)
    x, y = (w - side) // 2, (h - side) // 2
    return x, y, x + side, y + side


def cmd_prep(a):
    w, h = canvas(a.size)
    src = Image.open(a.image).convert("RGBA")
    bg = Image.new("RGBA", src.size, (255, 255, 255, 255))
    src = Image.alpha_composite(bg, src).convert("RGB")
    x0, y0, x1, y1 = square_box(w, h)
    src = src.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    out = Image.new("RGB", (w, h), (255, 255, 255))
    out.paste(src, (x0, y0))
    a.work.mkdir(parents=True, exist_ok=True)
    dest = a.work / "frame.png"
    out.save(dest)
    (a.work / "plan.json").write_text(json.dumps({"size": a.size, "box": [x0, y0, x1, y1]}, indent=2))
    print(dest)


def cmd_prompts(a):
    d = a.work / "prompts"
    d.mkdir(parents=True, exist_ok=True)
    for i, clip in enumerate(CLIPS, 1):
        (d / f"clip{i:02d}.txt").write_text(prompt_for(clip) + "\n", encoding="utf-8")
    print(f"wrote {len(CLIPS)} prompts to {d}")


def load_manifest(work: Path) -> dict:
    p = work / "manifest.json"
    return json.loads(p.read_text()) if p.exists() else {}


def cmd_submit(a):
    h3 = load_client(a.client)
    plan = json.loads((a.work / "plan.json").read_text())
    frame = a.work / "frame.png"
    manifest = load_manifest(a.work)
    relay = h3.Relay(h3.load_repo(a), h3.find_token())
    picks = a.only or range(1, len(CLIPS) + 1)
    for i in picks:
        key = f"{i:02d}"
        if key in manifest and not a.again:
            print(f"clip {key} already queued as {manifest[key]['id']} (use --again to resubmit)")
            continue
        job = h3.submit_job(relay, prompt_for(CLIPS[i - 1]), first=str(frame), seconds=SECONDS,
                            size=plan["size"], steps=a.steps, seed=a.seed)
        manifest[key] = {"id": job["id"], "expressions": CLIPS[i - 1], "seed": job["seed"]}
        (a.work / "manifest.json").write_text(json.dumps(manifest, indent=2))
        print(f"clip {key}: {job['id']}  ({', '.join(CLIPS[i - 1])})")


def read_frames(video: Path, w: int, h: int) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def stillest(frames: np.ndarray, lo: int, hi: int, box) -> int:
    """Frame with the least motion in the second part of the window (after the change has landed)."""
    x0, y0, x1, y1 = box
    roi = frames[:, y0:y1, x0:x1].astype(np.int16)[:, ::4, ::4]
    lo = lo + (hi - lo) * 2 // 5
    best, best_i = None, (lo + hi) // 2
    for i in range(max(lo, 1), min(hi, len(frames) - 1)):
        motion = np.abs(roi[i] - roi[i - 1]).mean() + np.abs(roi[i + 1] - roi[i]).mean()
        if best is None or motion < best:
            best, best_i = motion, i
    return best_i


def cmd_crop(a):
    h3 = load_client(a.client)
    plan = json.loads((a.work / "plan.json").read_text())
    w, h = canvas(plan["size"])
    box = plan["box"]
    manifest = load_manifest(a.work)
    relay = h3.Relay(h3.load_repo(a), h3.find_token())
    out, vids, full = a.work / "out", a.work / "videos", a.work / "out" / "full"
    full.mkdir(parents=True, exist_ok=True)
    tiles = []
    for key, entry in sorted(manifest.items()):
        st, _ = relay.read_json(f"status/{entry['id']}.json")
        state = (st or {}).get("state", "queued")
        if state != "done":
            print(f"clip {key} ({entry['id']}): {state}, skipping")
            continue
        video = vids / st["output"]
        if not video.exists():
            relay.download("outputs", st["output"], video)
        frames = read_frames(video, w, h)
        for (start, end), name in zip(WINDOWS, entry["expressions"]):
            lo, hi = int(start * FPS), min(int(end * FPS), len(frames))
            i = stillest(frames, lo, hi, box)
            img = Image.fromarray(frames[i])
            stem = f"{ORDER.index(name) + 1:02d}-{name.replace(' ', '-')}"
            img.save(full / f"{stem}.png")
            sq = img.crop(box)
            sq.save(out / f"{stem}.png")
            tiles.append((stem, sq))
            print(f"clip {key}  {stem:<32} frame {i} ({i / FPS:.2f}s)")
    if tiles:
        tiles.sort()
        cols, t = 8, 192
        sheet = Image.new("RGB", (cols * t, -(-len(tiles) // cols) * t), "white")
        for n, (_, sq) in enumerate(tiles):
            sheet.paste(sq.resize((t, t), Image.LANCZOS), ((n % cols) * t, (n // cols) * t))
        sheet.save(out / "contact-sheet.png")
        print(out / "contact-sheet.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--work", type=Path, default=Path("work"), help="working folder (default ./work)")
    ap.add_argument("--repo", help="relay repo owner/name (default: h3relay's .h3relay.json / H3RELAY_REPO)")
    ap.add_argument("--client", help="path to h3relay.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep")
    p.add_argument("image")
    p.add_argument("--size", default="1344x768", help="canvas, e.g. 1344x768 (detail) or 960x544 (fast)")
    p.set_defaults(fn=cmd_prep)
    sub.add_parser("prompts").set_defaults(fn=cmd_prompts)
    p = sub.add_parser("submit")
    p.add_argument("--only", type=int, action="append", help="clip number 1-12; repeat for several")
    p.add_argument("--again", action="store_true", help="resubmit clips already in the manifest")
    p.add_argument("--steps", type=int, default=50)
    p.add_argument("--seed", type=int)
    p.set_defaults(fn=cmd_submit)
    sub.add_parser("crop").set_defaults(fn=cmd_crop)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

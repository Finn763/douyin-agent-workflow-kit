#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render support cards for a batch plan.

Requires Pillow. This script renders card 2 and card 3 only. Main covers should
be generated directly by an image model/tool according to the skill rules.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


W, H = 1080, 1440


def font_path() -> Path | None:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


FONT_PATH = font_path()


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if FONT_PATH:
        return ImageFont.truetype(str(FONT_PATH), size)
    return ImageFont.load_default()


def wrapped_lines(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    line = ""
    for ch in text:
        cand = line + ch
        if draw.textlength(cand, font=fnt) <= max_width:
            line = cand
        else:
            if line:
                lines.append(line)
            line = ch
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], fnt: ImageFont.ImageFont, fill: tuple[int, int, int], max_width: int, line_gap: int = 10) -> int:
    x, y = xy
    size = getattr(fnt, "size", 36)
    for line in wrapped_lines(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += size + line_gap
    return y


def render_card(hotspot: str, title: str, bullets: list[str], footer: str, out: Path, variant: int) -> None:
    palettes = [
        ((248, 250, 252), (15, 23, 42), (37, 99, 235), (219, 234, 254)),
        ((255, 247, 237), (124, 45, 18), (234, 88, 12), (255, 237, 213)),
        ((240, 253, 244), (20, 83, 45), (22, 163, 74), (220, 252, 231)),
        ((250, 245, 255), (88, 28, 135), (147, 51, 234), (243, 232, 255)),
    ]
    bg, fg, accent, soft = palettes[variant % len(palettes)]
    im = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle((58, 62, 1022, 248), radius=28, fill=soft)
    draw.text((92, 92), hotspot[:32], font=font(32), fill=accent)
    y = draw_wrapped(draw, title, (92, 146), font(50), fg, 880, 8)
    draw.line((92, max(254, y + 18), 988, max(254, y + 18)), fill=accent, width=5)

    y = 322
    for idx, bullet in enumerate(bullets[:5], 1):
        card_h = 164
        draw.rounded_rectangle((76, y, 1004, y + card_h), radius=28, fill=(255, 255, 255), outline=accent, width=3)
        draw.ellipse((116, y + 45, 186, y + 115), fill=accent)
        draw.text((139, y + 57), str(idx), font=font(34), fill=(255, 255, 255))
        draw_wrapped(draw, bullet, (222, y + 43), font(42), fg, 710, 8)
        y += card_h + 28

    draw.rounded_rectangle((76, 1134, 1004, 1332), radius=30, fill=fg)
    draw_wrapped(draw, footer, (116, 1188), font(36), (255, 255, 255), 850, 12)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=94)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    footer = "把热点变成可执行流程，而不是只追热点本身"
    for index, post in enumerate(plan.get("posts", [])):
        post_id = post.get("post_id") or f"post-{index + 1:02d}"
        hotspot = post.get("hotspot", "")
        card1 = post.get("support_card_1") or {}
        card2 = post.get("support_card_2") or {}
        render_card(hotspot, card1.get("title", "热点怎么理解"), card1.get("bullets", []), footer, args.outdir / post_id / "02-steps.png", index)
        render_card(hotspot, card2.get("title", "行业怎么接上"), card2.get("bullets", []), footer, args.outdir / post_id / "03-workflow.png", index + 1)
    print(f"rendered support cards for {len(plan.get('posts', []))} posts")


if __name__ == "__main__":
    try:
        main()
    except ImportError as exc:
        raise SystemExit("Pillow is required: pip install pillow") from exc

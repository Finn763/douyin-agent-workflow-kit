#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cross-platform publishing wrapper template for social-auto-upload.

Environment variables:
- SAU_ROOT: path to a social-auto-upload checkout.
- DOUYIN_ACCOUNT: account alias inside social-auto-upload cookies.
- SAU_BATCH_START_INDEX / SAU_BATCH_END_INDEX: optional resume range.

The batch plan must have final image paths in each post's `images` list.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def env_for_post(post: dict[str, Any]) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "SAU_DOUYIN_AUTO_MUSIC": "1",
            "SAU_DOUYIN_FAST_HOTSPOT": "1",
            "SAU_DOUYIN_HOTSPOT_SCROLLS": "5",
            "SAU_DOUYIN_HOTSPOT_LIMIT": "36",
            "SAU_DOUYIN_HOTSPOT_READY_MS": "700",
            "SAU_DOUYIN_HOTSPOT_SCROLL_WAIT_MS": "350",
            "SAU_DOUYIN_HOTSPOT_SEARCH_WAIT_MS": "1500",
            "SAU_DOUYIN_OPTIMIZE_IMAGES": "1",
            "SAU_DOUYIN_HOTSPOT_SEARCH_KEYWORD": str(post.get("hotspot_search_keyword") or post.get("hotspot") or ""),
        }
    )
    return env


def run_post(sau_root: Path, account: str, post: dict[str, Any], log_dir: Path) -> int:
    images = [str(Path(p)) for p in post.get("images", [])]
    if not images:
        raise RuntimeError(f"post {post.get('post_id')} has no images")

    cmd = [
        sys.executable,
        "sau_cli.py",
        "douyin",
        "upload-note",
        "--account",
        account,
        "--images",
        *images,
        "--title",
        str(post.get("title", "")),
        "--note",
        str(post.get("body", "")),
        "--tags",
        ",".join(post.get("tags", [])),
        "--hotspot",
        str(post.get("hotspot", "")),
        "--headed",
    ]
    post_id = str(post.get("post_id") or datetime.now().strftime("%H%M%S"))
    log_path = log_dir / f"{post_id}.log"
    result = subprocess.run(
        cmd,
        cwd=sau_root,
        env=env_for_post(post),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    log_path.write_text(result.stdout, encoding="utf-8")
    return result.returncode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--log-dir", required=True, type=Path)
    args = parser.parse_args()

    sau_root = Path(os.environ.get("SAU_ROOT", "")).expanduser()
    account = os.environ.get("DOUYIN_ACCOUNT", "")
    if not sau_root.exists():
        raise SystemExit("Set SAU_ROOT to your social-auto-upload folder")
    if not account:
        raise SystemExit("Set DOUYIN_ACCOUNT to your account alias")

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    posts = list(plan.get("posts", []))
    start = int(os.environ.get("SAU_BATCH_START_INDEX", "0") or "0")
    end_raw = os.environ.get("SAU_BATCH_END_INDEX", "")
    end = int(end_raw) if end_raw.strip() else len(posts)
    selected = posts[start:end]

    args.log_dir.mkdir(parents=True, exist_ok=True)
    failed = 0
    for post in selected:
        rc = run_post(sau_root, account, post, args.log_dir)
        print(f"{post.get('post_id')} rc={rc}", flush=True)
        if rc != 0:
            failed += 1
    print(f"summary total={len(selected)} failed={failed} logs={args.log_dir}")
    if failed:
        raise SystemExit(failed)


if __name__ == "__main__":
    main()

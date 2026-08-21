#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a cross-platform Douyin batch plan from a profile and searched hotspots.

This script does not call Douyin or generate images. It prepares a deterministic
JSON plan that an agent can fill with final copy and cover prompts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def distribute(total: int, topics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not topics:
        return []
    base, extra = divmod(total, len(topics))
    rows: list[dict[str, Any]] = []
    for index, topic in enumerate(topics):
        count = base + (1 if index < extra else 0)
        for variant in range(1, count + 1):
            rows.append(
                {
                    "post_id": f"post-{index + 1:02d}-{variant:02d}",
                    "hotspot": topic["title"],
                    "hotspot_search_keyword": topic.get("keyword") or topic["title"],
                    "hotspot_heat": topic.get("heat", ""),
                    "variant": variant,
                    "title": "",
                    "body": "",
                    "tags": [],
                    "cover_prompt": "",
                    "support_card_1": {"title": "", "bullets": []},
                    "support_card_2": {"title": "", "bullets": []},
                    "images": [],
                }
            )
    return rows


def choose_topics(profile: dict[str, Any], hotspots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    target = int(profile.get("topics_target") or 1)
    seen: set[str] = set()
    chosen: list[dict[str, Any]] = []
    for item in hotspots:
        title = str(item.get("title", "")).strip()
        if not title or title in seen:
            continue
        seen.add(title)
        chosen.append(
            {
                "title": title,
                "heat": str(item.get("heat", "")).strip(),
                "keyword": str(item.get("keyword", "")).strip() or title,
            }
        )
        if len(chosen) >= target:
            break
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--hotspots", required=True, type=Path, help="JSON list from hotspot search")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    profile = load_json(args.profile)
    hotspots = load_json(args.hotspots)
    if not isinstance(hotspots, list):
        raise SystemExit("--hotspots must be a JSON list")

    chosen = choose_topics(profile, hotspots)
    posts = distribute(int(profile.get("post_count") or 1), chosen)
    plan = {
        "profile": profile,
        "selected_topics": chosen,
        "posts": posts,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.out} with {len(posts)} posts and {len(chosen)} topics")


if __name__ == "__main__":
    main()

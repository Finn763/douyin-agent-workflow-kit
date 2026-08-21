from __future__ import annotations

import argparse
from pathlib import Path

from workflow_utils import find_plan_row, image_size, project_path, read_plan, split_assets, split_tags


def check_row(project: Path, row: dict[str, str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    assets = split_assets(row, project)
    tags = split_tags(row)

    if not row.get("id"):
        errors.append("missing id")
    if not row.get("account"):
        errors.append("missing account")
    if row.get("type") not in {"note", "video"}:
        errors.append("type must be note or video")
    if not row.get("title"):
        errors.append("missing title")
    if not row.get("body"):
        errors.append("missing body")
    if not tags:
        warnings.append("missing tags")
    if row.get("title") and len(row["title"]) > 30:
        warnings.append("title is longer than 30 chars")
    if not assets:
        errors.append("missing assets")

    for asset in assets:
        if not asset.exists():
            errors.append(f"asset not found: {asset}")

    if row.get("type") == "note":
        if len(assets) != 3:
            warnings.append(f"note should usually have 3 images, found {len(assets)}")
        if not row.get("hotspot"):
            warnings.append("missing hotspot")
        for asset in assets:
            if not asset.exists():
                continue
            size = image_size(asset)
            if size is None:
                warnings.append(f"cannot read image size: {asset}")
                continue
            if size != (1080, 1440):
                warnings.append(f"image is not 1080x1440: {asset} ({size[0]}x{size[1]})")

    if row.get("type") == "video" and len(assets) != 1:
        warnings.append(f"video should usually have 1 asset, found {len(assets)}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether plan rows are ready to publish.")
    parser.add_argument("--project", required=True, help="Project directory.")
    parser.add_argument("--id", default="", help="Plan row id. If omitted, checks draft and pending rows.")
    parser.add_argument("--plan", default="schedules/publish_plan.csv", help="Plan CSV path relative to project.")
    args = parser.parse_args()

    project = project_path(args.project)
    rows = [find_plan_row(project, args.id, args.plan)] if args.id else [
        row for row in read_plan(project, args.plan) if row.get("status") in {"draft", "pending"}
    ]

    failed = False
    for row in rows:
        errors, warnings = check_row(project, row)
        label = row.get("id", "(no id)")
        title = row.get("title", "")
        if errors:
            failed = True
            print(f"[FAIL] {label} {title}")
            for item in errors:
                print(f"  ERROR: {item}")
        else:
            print(f"[OK] {label} {title}")
        for item in warnings:
            print(f"  WARN: {item}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())


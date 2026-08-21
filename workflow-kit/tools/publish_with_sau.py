from __future__ import annotations

import argparse
import csv
import os
import subprocess
from datetime import datetime
from pathlib import Path

from build_sau_command import build_args, default_python_for_social_root
from check_note_ready import check_row
from workflow_utils import find_plan_row, project_path


def append_log(project: Path, row: dict[str, str], status: str, message: str) -> None:
    log_path = project / "logs" / "publish_log.csv"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with log_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["time", "id", "account", "type", "title", "status", "message"])
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "time": datetime.now().isoformat(timespec="seconds"),
                "id": row.get("id", ""),
                "account": row.get("account", ""),
                "type": row.get("type", ""),
                "title": row.get("title", ""),
                "status": status,
                "message": message,
            }
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish one plan row with social-auto-upload.")
    parser.add_argument("--project", required=True, help="Project directory.")
    parser.add_argument("--id", required=True, help="Plan row id.")
    parser.add_argument("--social-root", required=True, help="social-auto-upload root directory.")
    parser.add_argument("--plan", default="schedules/publish_plan.csv", help="Plan CSV path relative to project.")
    parser.add_argument("--no-music", action="store_true", help="Do not request automatic music selection.")
    parser.add_argument("--dry-run-screenshot", default="", help="Ask compatible publisher to stop before publish and save screenshot.")
    args = parser.parse_args()

    project = project_path(args.project)
    social_root = project_path(args.social_root)
    row = find_plan_row(project, args.id, args.plan)

    errors, warnings = check_row(project, row)
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        append_log(project, row, "failed", "validation failed")
        return 1

    python_cmd = default_python_for_social_root(social_root)
    command = [python_cmd, *build_args(project, row)]

    env = os.environ.copy()
    if not args.no_music:
        env["SAU_DOUYIN_AUTO_MUSIC"] = "1"
    env["SAU_DOUYIN_HOTSPOT_LIMIT"] = "50"
    env["SAU_DOUYIN_HOTSPOT_SCROLLS"] = "6"

    failed_dir = project / "failed"
    failed_dir.mkdir(parents=True, exist_ok=True)
    env["SAU_PUBLISH_FAIL_SCREENSHOT"] = str(failed_dir / f"{row.get('id', 'unknown')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png")
    if args.dry_run_screenshot:
        env["SAU_DRY_RUN_SCREENSHOT"] = str((project / args.dry_run_screenshot).resolve())

    print("Running publisher...")
    result = subprocess.run(command, cwd=social_root, env=env, text=True)
    if result.returncode == 0:
        append_log(project, row, "published", "published successfully")
        return 0

    append_log(project, row, "failed", f"publisher exit code {result.returncode}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())


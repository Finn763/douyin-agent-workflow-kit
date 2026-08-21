from __future__ import annotations

import argparse
from pathlib import Path

from workflow_utils import find_plan_row, powershell_command, project_path, quote_command, split_assets


def default_python_for_social_root(social_root: Path) -> str:
    windows_python = social_root / ".venv" / "Scripts" / "python.exe"
    posix_python = social_root / ".venv" / "bin" / "python"
    if windows_python.exists():
        return str(windows_python)
    if posix_python.exists():
        return str(posix_python)
    return "python"


def build_args(project: Path, row: dict[str, str]) -> list[str]:
    assets = [str(path) for path in split_assets(row, project)]
    content_type = row.get("type", "")
    if content_type == "note":
        args = [
            "sau_cli.py",
            "douyin",
            "upload-note",
            "--account",
            row.get("account", ""),
            "--images",
            *assets,
            "--title",
            row.get("title", ""),
            "--note",
            row.get("body", ""),
            "--tags",
            row.get("tags", ""),
        ]
        if row.get("hotspot"):
            args += ["--hotspot", row["hotspot"]]
        if row.get("schedule"):
            args += ["--schedule", row["schedule"]]
        args += ["--headed"]
        return args

    if content_type == "video":
        if not assets:
            raise ValueError("video row has no asset")
        args = [
            "sau_cli.py",
            "douyin",
            "upload-video",
            "--account",
            row.get("account", ""),
            "--file",
            assets[0],
            "--title",
            row.get("title", ""),
            "--desc",
            row.get("body", ""),
            "--tags",
            row.get("tags", ""),
            "--headed",
        ]
        if row.get("schedule"):
            args += ["--schedule", row["schedule"]]
        return args

    raise ValueError(f"Unsupported type: {content_type}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a social-auto-upload command for a plan row.")
    parser.add_argument("--project", required=True, help="Project directory.")
    parser.add_argument("--id", required=True, help="Plan row id.")
    parser.add_argument("--social-root", required=True, help="social-auto-upload root directory.")
    parser.add_argument("--plan", default="schedules/publish_plan.csv", help="Plan CSV path relative to project.")
    args = parser.parse_args()

    project = project_path(args.project)
    social_root = project_path(args.social_root)
    row = find_plan_row(project, args.id, args.plan)
    python_cmd = default_python_for_social_root(social_root)
    cli_args = build_args(project, row)

    print("Run from:")
    print(str(social_root))
    print("")
    print("Recommended environment:")
    print("SAU_DOUYIN_AUTO_MUSIC=1")
    print("SAU_DOUYIN_HOTSPOT_LIMIT=50")
    print("SAU_DOUYIN_HOTSPOT_SCROLLS=6")
    print("")
    print("PowerShell command:")
    print(powershell_command([python_cmd, *cli_args]))
    print("")
    print("Portable command:")
    print(quote_command([python_cmd, *cli_args]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

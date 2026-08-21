from __future__ import annotations

import csv
import imghdr
import shlex
import struct
from pathlib import Path


PLAN_FIELDS = [
    "id",
    "account",
    "type",
    "asset_paths",
    "title",
    "body",
    "tags",
    "hotspot",
    "schedule",
    "status",
    "result",
]


def project_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def read_plan(project: Path, plan_path: str = "schedules/publish_plan.csv") -> list[dict[str, str]]:
    path = project / plan_path
    if not path.exists():
        raise FileNotFoundError(f"Plan file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def find_plan_row(project: Path, plan_id: str, plan_path: str = "schedules/publish_plan.csv") -> dict[str, str]:
    rows = [row for row in read_plan(project, plan_path) if row.get("id") == plan_id]
    if len(rows) != 1:
        raise ValueError(f"Expected one plan row for id={plan_id}, found {len(rows)}")
    return rows[0]


def split_assets(row: dict[str, str], project: Path) -> list[Path]:
    raw = row.get("asset_paths", "")
    paths = [part.strip() for part in raw.split("|") if part.strip()]
    resolved = []
    for item in paths:
        path = Path(item)
        if not path.is_absolute():
            path = project / path
        resolved.append(path.resolve())
    return resolved


def split_tags(row: dict[str, str]) -> list[str]:
    return [part.strip() for part in row.get("tags", "").split(",") if part.strip()]


def quote_command(args: list[str]) -> str:
    return " ".join(shlex.quote(str(arg)) for arg in args)


def powershell_quote(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def powershell_command(args: list[str]) -> str:
    if not args:
        return ""
    return "& " + " ".join(powershell_quote(str(arg)) for arg in args)


def image_size(path: Path) -> tuple[int, int] | None:
    kind = imghdr.what(path)
    if kind == "png":
        with path.open("rb") as handle:
            header = handle.read(24)
        if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        width, height = struct.unpack(">II", header[16:24])
        return int(width), int(height)

    if kind == "jpeg":
        return jpeg_size(path)

    return None


def jpeg_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        data = handle.read()

    index = 2
    while index < len(data):
        if data[index] != 0xFF:
            index += 1
            continue

        marker = data[index + 1]
        index += 2
        if marker in (0xD8, 0xD9):
            continue
        if index + 2 > len(data):
            return None
        length = struct.unpack(">H", data[index:index + 2])[0]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            if index + 7 > len(data):
                return None
            height, width = struct.unpack(">HH", data[index + 3:index + 7])
            return int(width), int(height)
        index += length

    return None

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_tree(src: Path, dst: Path, force: bool) -> None:
    for item in src.rglob("*"):
        relative = item.relative_to(src)
        target = dst / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Douyin AI workflow project.")
    parser.add_argument("--target", required=True, help="Target project directory.")
    parser.add_argument("--account-alias", default="your-account-alias", help="Publisher account alias.")
    parser.add_argument("--display-name", default="", help="Douyin display name.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing template files.")
    args = parser.parse_args()

    kit_root = Path(__file__).resolve().parents[1]
    template = kit_root / "templates" / "project"
    target = Path(args.target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    copy_tree(template, target, args.force)

    account_file = target / "accounts" / f"{args.account_alias}.md"
    if args.force or not account_file.exists():
        account_file.write_text(
            "\n".join(
                [
                    f"# Account: {args.display_name or args.account_alias}",
                    "",
                    f"account_alias: `{args.account_alias}`",
                    "platform: douyin",
                    "",
                    "Do not store passwords, verification codes, or QR login data here.",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    account_yaml = target / "configs" / "account.yaml"
    account_yaml.write_text(
        "\n".join(
            [
                f'display_name: "{args.display_name}"',
                f'account_alias: "{args.account_alias}"',
                "platform: douyin",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Initialized project: {target}")
    print(f"Account alias: {args.account_alias}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


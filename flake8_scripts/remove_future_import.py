from __future__ import annotations

import argparse

from .utils.resolve import resolve_globs

future_import_count = 0


def fix_file(file_path: str, fix: bool = False):
    global future_import_count
    with open(file_path, "r") as f:
        lines = f.readlines()

    new_lines: list[str] = []
    for lineno, line in enumerate(lines, 1):
        if line.startswith("from __future__ import"):
            print(f"Found __future__ import in {file_path}:{lineno}")
            future_import_count += 1
            continue
        new_lines.append(line)

    if fix:
        with open(file_path, "w") as f:
            f.writelines(new_lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("globs", help="Path glob to check", nargs="+")
    parser.add_argument("--fix", help="Auto fix the wrongs", action="store_true")
    parser.add_argument("--ignore-globs", help="Path glob to ignore, comma separated", type=str, default="")

    args = parser.parse_args()
    path_list = resolve_globs(args.globs, args.ignore_globs.split(","))

    for path in path_list:
        fix_file(path, args.fix)

    print(f"Found {future_import_count} __future__ imports")


if __name__ == "__main__":
    main()

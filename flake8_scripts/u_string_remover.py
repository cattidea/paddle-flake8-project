from __future__ import annotations

import argparse
import ast

from .utils.replace import Location, ReplacementInfo, replace_with_location
from .utils.resolve import resolve_globs

EMPTY_NODE = ast.Name("")


class ReWriter(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.to_replace: list[ReplacementInfo] = []

    def generic_visit(self, node: ast.AST):
        ast.NodeVisitor.generic_visit(self, node)

    def add_to_replace(self, node: ast.AST, replacement: ast.AST):
        self.to_replace.append(
            ReplacementInfo(
                start=Location(lineno=node.lineno, col_offset=node.col_offset),
                end=Location(lineno=node.end_lineno, col_offset=node.end_col_offset),  # type: ignore
                replacement=ast.unparse(replacement),
            )
        )


class UStringRemover(ReWriter):
    def visit_Constant(self, node: ast.Constant):
        if node.kind == "u":
            self.add_to_replace(node, ast.Constant(node.value, kind=None))
        else:
            ast.NodeVisitor.generic_visit(self, node)


def remove_u_string_from_text(text: str, filepath: str = "<unknown>") -> str:
    passes: list[type[ReWriter]] = [
        UStringRemover,
    ]

    for pass_cls in passes:
        tree = ast.parse(text, filepath)
        pass_ = pass_cls()
        pass_.visit(tree)
        text = replace_with_location(text, pass_.to_replace)

    return text


def fix_file(file_path: str, fix: bool = False):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = remove_u_string_from_text(text, file_path)

    if fix:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("globs", help="Path glob to check", nargs="+")
    parser.add_argument("--fix", help="Auto fix the wrongs", action="store_true")
    parser.add_argument("--ignore-globs", help="Path glob to ignore, comma separated", type=str, default="")

    args = parser.parse_args()
    path_list = resolve_globs(args.globs, args.ignore_globs.split(","))

    for path in path_list:
        fix_file(path, args.fix)

    # print(f"Found {future_import_count} __future__ imports")


if __name__ == "__main__":
    main()

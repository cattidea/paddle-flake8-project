from __future__ import annotations

import argparse
import ast
from typing import Optional

from .utils.replace import Location, ReplacementInfo, replace_with_location
from .utils.resolve import resolve_globs


class SixRemover(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.to_replace: list[ReplacementInfo] = []

    def generic_visit(self, node: ast.AST):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node: ast.Call):
        transformed_node = node
        match node:
            # six.moves.xrange
            case ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id="six"),
                        attr="moves",
                    )
                    | ast.Name(id="moves"),
                    attr="xrange",
                ),
                args=args,
                keywords=keywords,
            ):
                transformed_node = ast.Call(
                    func=ast.Name(id="range"),
                    args=args,
                    keywords=keywords,
                )
            # six.iteritems
            case ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="six"),
                    attr="iteritems",
                ),
                args=[dictionary],
            ):
                transformed_node = ast.Call(
                    func=ast.Attribute(
                        value=dictionary,
                        attr="items",
                    ),
                    args=[],
                    keywords=[],
                )
            # six.binary_type
            case _:
                ...

        if transformed_node is not node:
            self.to_replace.append(
                ReplacementInfo(
                    start=Location(lineno=node.lineno, col_offset=node.col_offset),
                    end=Location(lineno=node.end_lineno, col_offset=node.end_col_offset),  # type: ignore
                    replacement=ast.unparse(transformed_node),
                )
            )


def remove_six_from_text(text: str) -> Optional[str]:
    tree = ast.parse(text)
    trans = SixRemover()
    trans.visit(tree)
    to_replace = trans.to_replace
    if not to_replace:
        return None

    return replace_with_location(text, to_replace)


def fix_file(file_path: str, fix: bool = False):
    with open(file_path, "r") as f:
        text = f.read()

    tree = ast.parse(text)
    trans = SixRemover()
    trans.visit(tree)
    to_replace = trans.to_replace
    if not to_replace:
        return

    text = replace_with_location(text, to_replace)

    if fix:
        with open(file_path, "w") as f:
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

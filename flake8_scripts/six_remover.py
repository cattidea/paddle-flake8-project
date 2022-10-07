from __future__ import annotations

import argparse
import ast
from typing import Optional

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


class SixRemover(ReWriter):
    def visit_Attribute(self, node: ast.Attribute):
        transformed_node = node
        attr_map = {
            "string_types": "str,",
            "integer_types": "int,",
            "class_types": "type,",
            "text_type": "str",
            "binary_type": "bytes",
        }
        match node:
            case ast.Attribute(
                value=ast.Name(
                    id="six",
                ),
                attr="string_types" | "integer_types" | "class_types" | "text_type" | "binary_type" as attr,
            ):

                transformed_node = ast.parse(attr_map[attr])
            case _:
                ...
        if transformed_node is not node:
            self.add_to_replace(node, transformed_node)
        else:
            ast.NodeVisitor.generic_visit(self, node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        transformed_node = node
        match node:
            # from six.moves.queue import Queue -> from queue import Queue
            case ast.ImportFrom(
                module="six.moves.queue",
                names=[ast.alias(name="Queue")],
                level=0,
            ):
                transformed_node = ast.ImportFrom(
                    module="queue",
                    names=[ast.alias(name="Queue")],
                    level=0,
                )
            # from six.moves import move_alias
            case ast.ImportFrom(
                module="six.moves",
                names=[move_node],
                level=0,
            ):
                match move_node:
                    # from six.moves import zip_longest -> from itertools import zip_longest
                    case ast.alias(name="zip_longest"):
                        transformed_node = ast.ImportFrom(
                            module="itertools",
                            names=[ast.alias(name="zip_longest")],
                            level=0,
                        )
                    # from six.moves import zip -> EMPTY_NODE
                    case ast.alias(name="zip"):
                        transformed_node = EMPTY_NODE
                    case ast.alias(name="map"):
                        transformed_node = EMPTY_NODE
                    case _:
                        ...
            case _:
                ...
        if transformed_node is not node:
            self.add_to_replace(node, transformed_node)
        else:
            ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node: ast.Call):
        transformed_node = node
        match node:
            # six.moves.xrange(*args) / six.moves.range(*args) -> range(*args)
            case ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id="six"),
                        attr="moves",
                    )
                    | ast.Name(id="moves"),
                    attr="xrange" | "range",
                ),
                args=args,
                keywords=keywords,
            ):
                transformed_node = ast.Call(
                    func=ast.Name(id="range"),
                    args=args,
                    keywords=keywords,
                )
            # six.moves.zip(*args) -> zip(*args)
            case ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id="six"),
                        attr="moves",
                    )
                    | ast.Name(id="moves"),
                    attr="zip",
                ),
                args=args,
                keywords=keywords,
            ):
                transformed_node = ast.Call(
                    func=ast.Name(id="zip"),
                    args=args,
                    keywords=keywords,
                )
            # six.iteritems(d) -> d.items()
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
            # six.b(s)
            case ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="six"),
                    attr="b",
                ),
                args=[s],
                keywords=[],
            ):
                match s:
                    # six.b('literal_string') -> b'literal_string'
                    case ast.Constant(value=literal_string):
                        transformed_node = ast.Constant(value=literal_string.encode())
                    # six.b(s) -> s.encode("latin-1")
                    case expr:
                        transformed_node = ast.Call(
                            func=ast.Attribute(value=expr, attr="encode"),
                            args=[ast.Constant(value="latin-1")],
                            keywords=[],
                        )
            # six.u(s) -> s
            case ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="six"),
                    attr="u",
                ),
                args=[s],
                keywords=[],
            ):
                transformed_node = s
            case _:
                ...

        if transformed_node is not node:
            self.add_to_replace(node, transformed_node)
        else:
            ast.NodeVisitor.generic_visit(self, node)


class IsInstanceCleaner(ReWriter):
    def visit_Call(self, node: ast.Call):
        transformed_node = node
        match node:
            case ast.Call(
                func=ast.Name(id="isinstance"),
                args=[
                    obj,  # type: ignore
                    ast.Tuple(
                        elts=[tp],
                    ),
                ],
                keywords=[],
            ):
                transformed_node = ast.Call(
                    func=ast.Name(id="isinstance"),
                    args=[
                        obj,
                        tp,
                    ],
                    keywords=[],
                )
            case _:
                ...
        if transformed_node is not node:
            self.add_to_replace(node, transformed_node)
        else:
            ast.NodeVisitor.generic_visit(self, node)


def remove_six_from_text(text: str, filepath: str = "<unknown>") -> str:
    passes: list[type[ReWriter]] = [
        SixRemover,
        IsInstanceCleaner,
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

    text = remove_six_from_text(text, file_path)

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

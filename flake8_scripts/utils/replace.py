from __future__ import annotations

from typing import TypedDict


class Location(TypedDict):
    lineno: int
    col_offset: int


class ReplacementInfo(TypedDict):
    start: Location
    end: Location
    replacement: str


def replace_with_location(text: str, to_replace: list[ReplacementInfo]) -> str:
    lines_length = [len(line) + 1 for line in text.splitlines()]
    out = ""

    index = 0

    for to_replace_info in to_replace:
        start_index = (
            sum(lines_length[: to_replace_info["start"]["lineno"] - 1]) + to_replace_info["start"]["col_offset"]
        )
        end_index = sum(lines_length[: to_replace_info["end"]["lineno"] - 1]) + to_replace_info["end"]["col_offset"]
        out += text[index:start_index] + to_replace_info["replacement"]
        index = end_index

    out += text[index:]
    return out

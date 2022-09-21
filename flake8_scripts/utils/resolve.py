from __future__ import annotations

import glob


def resolve_globs(globs: list[str], ignore_globs: list[str]) -> list[str]:
    ignore_paths_list = [glob.glob(ignore_glob, recursive=True) for ignore_glob in ignore_globs]
    ignore_paths = [path for ignore_paths in ignore_paths_list for path in ignore_paths]

    paths_list = [glob.glob(glob_, recursive=True) for glob_ in globs]
    paths = [path for paths in paths_list for path in paths if path not in ignore_paths]
    return paths

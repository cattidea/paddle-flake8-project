from __future__ import annotations

import argparse

from flake8_scripts import __version__


def main() -> None:
    parser = argparse.ArgumentParser(prog="flake8_scripts", description="A moe moe project")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()  # type: ignore


if __name__ == "__main__":
    main()

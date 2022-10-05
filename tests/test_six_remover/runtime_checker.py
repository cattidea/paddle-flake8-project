from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO


def run_code(code: str):
    """A solution to execute code and return the output.

    ref: https://stackoverflow.com/a/3906390/17656881
    """
    f = StringIO()
    with redirect_stdout(f):
        exec(code)
    return f.getvalue()

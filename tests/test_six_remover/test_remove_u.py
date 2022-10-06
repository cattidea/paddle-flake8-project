from __future__ import annotations

import inspect

from flake8_scripts.six_remover import remove_six_from_text

from .runtime_checker import run_code


def test_remove_u():
    source = """
    import six

    a = six.u("blabla") # keep this comment
    b = six.u("lablab") # keep this comment too
    c = a.encode() + b.encode()
    print(a, b, c)
    """

    expected = """
    import six

    a = 'blabla' # keep this comment
    b = 'lablab' # keep this comment too
    c = a.encode() + b.encode()
    print(a, b, c)
    """

    assert remove_six_from_text(inspect.cleandoc(source)) == inspect.cleandoc(expected)
    assert run_code(inspect.cleandoc(source)) == run_code(inspect.cleandoc(expected))

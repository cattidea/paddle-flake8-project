from __future__ import annotations

import inspect

from flake8_scripts.six_remover import remove_six_from_text

from .runtime_checker import run_code


def test_remove_b():
    source = """
    import six

    a = six.b("blabla") # keep this comment
    b = six.b("lablab") # keep this comment too
    c = a.decode() + b.decode()
    print(a, b, c)
    """

    expected = """
    import six

    a = b'blabla' # keep this comment
    b = b'lablab' # keep this comment too
    c = a.decode() + b.decode()
    print(a, b, c)
    """

    assert remove_six_from_text(inspect.cleandoc(source)) == inspect.cleandoc(expected)
    assert run_code(inspect.cleandoc(source)) == run_code(inspect.cleandoc(expected))

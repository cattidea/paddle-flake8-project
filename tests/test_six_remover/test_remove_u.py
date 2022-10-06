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

    expect = """
    import six

    a = 'blabla' # keep this comment
    b = 'lablab' # keep this comment too
    c = a.encode() + b.encode()
    print(a, b, c)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)

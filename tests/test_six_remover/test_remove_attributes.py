from __future__ import annotations

import inspect

from flake8_scripts.six_remover import remove_six_from_text

from .runtime_checker import run_code


def test_remove_string_types():
    source = """
    import six

    if isinstance("abc", six.string_types):
        print(1)
    """

    expect = """
    import six

    if isinstance('abc', str):
        print(1)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)


def test_remove_integer_types():
    source = """
    import six

    if isinstance(1, six.integer_types):
        print(1)
    """

    expect = """
    import six

    if isinstance(1, int):
        print(1)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)

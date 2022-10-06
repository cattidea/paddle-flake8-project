from __future__ import annotations

import inspect

from flake8_scripts.six_remover import remove_six_from_text

from .runtime_checker import run_code


def test_remove_zip():
    source = """
    import six
    from six import moves

    numbers = [5, 4, 3, 2, 1]
    values = ["foo", "bar", "baz", "qux", "quux"]
    for number, value in six.moves.zip(numbers, values):
        print(number ** 2, value)
    """

    expected = """
    import six
    from six import moves

    numbers = [5, 4, 3, 2, 1]
    values = ["foo", "bar", "baz", "qux", "quux"]
    for number, value in zip(numbers, values):
        print(number ** 2, value)
    """

    assert remove_six_from_text(inspect.cleandoc(source)) == inspect.cleandoc(expected)
    assert run_code(inspect.cleandoc(source)) == run_code(inspect.cleandoc(expected))


def test_remove_moves_zip():
    source = """
    import six
    from six import moves

    numbers = [5, 4, 3, 2, 1]
    values = ["foo", "bar", "baz", "qux", "quux"]
    for number, value in moves.zip(numbers, values): # comment
        print(number ** 2, value)
    """

    expected = """
    import six
    from six import moves

    numbers = [5, 4, 3, 2, 1]
    values = ["foo", "bar", "baz", "qux", "quux"]
    for number, value in zip(numbers, values): # comment
        print(number ** 2, value)
    """

    assert remove_six_from_text(inspect.cleandoc(source)) == inspect.cleandoc(expected)
    assert run_code(inspect.cleandoc(source)) == run_code(inspect.cleandoc(expected))

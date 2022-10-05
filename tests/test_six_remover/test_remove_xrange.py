from __future__ import annotations

import inspect

from flake8_scripts.six_remover import remove_six_from_text

from .runtime_checker import run_code


def test_remove_xrange():
    source = """
    import six
    from six import moves

    numbers = [5, 4, 3, 2, 1]
    for i in six.moves.xrange(1, len(numbers), 2):
        print(numbers[i])
    """

    expected = """
    import six
    from six import moves

    numbers = [5, 4, 3, 2, 1]
    for i in range(1, len(numbers), 2):
        print(numbers[i])
    """

    assert remove_six_from_text(inspect.cleandoc(source)) == inspect.cleandoc(expected)
    assert run_code(inspect.cleandoc(source)) == run_code(inspect.cleandoc(expected))


def test_remove_moves_xrange():
    source = """
    import six
    from six import moves

    for i in moves.xrange(1000, 9, -1):
        print(i)
    """

    expected = """
    import six
    from six import moves

    for i in range(1000, 9, -1):
        print(i)
    """

    assert remove_six_from_text(inspect.cleandoc(source)) == inspect.cleandoc(expected)
    assert run_code(inspect.cleandoc(source)) == run_code(inspect.cleandoc(expected))

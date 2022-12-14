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

    expect = """
    import six
    from six import moves

    numbers = [5, 4, 3, 2, 1]
    for i in range(1, len(numbers), 2):
        print(numbers[i])
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(inspect.cleandoc(source))

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)


def test_remove_moves_xrange():
    source = """
    import six
    from six import moves

    for i in moves.xrange(1000, 9, -1):
        print(i)
    """

    expect = """
    import six
    from six import moves

    for i in range(1000, 9, -1):
        print(i)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(inspect.cleandoc(source))

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)


def test_remove_range():
    source = """
    import six
    from six import moves

    numbers = [2, 3, 3, 3, 3]
    for i in six.moves.range(1, len(numbers), 2):
        print(numbers[i])
    """

    expect = """
    import six
    from six import moves

    numbers = [2, 3, 3, 3, 3]
    for i in range(1, len(numbers), 2):
        print(numbers[i])
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(inspect.cleandoc(source))

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)


def test_remove_moves_range():
    source = """
    import six
    from six import moves

    for i in moves.range(1000, 9, -1):
        print(i)
    """

    expect = """
    import six
    from six import moves

    for i in range(1000, 9, -1):
        print(i)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)

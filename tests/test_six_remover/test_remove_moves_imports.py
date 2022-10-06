from __future__ import annotations

import inspect

from flake8_scripts.six_remover import remove_six_from_text

from .runtime_checker import run_code


def test_remove_iteritems():
    source = """
    from six.moves.queue import Queue

    q = Queue()
    for i in range(100):
        q.put(i ** 2)

    while not q.empty():
        print(q.get())
    """

    expect = """
    from queue import Queue

    q = Queue()
    for i in range(100):
        q.put(i ** 2)

    while not q.empty():
        print(q.get())
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)


def test_remove_zip_longest():
    source = """
    from six.moves import zip_longest

    a = [1, 2, 3]
    b = [4, 5, 6, 7]
    for i, j in zip_longest(a, b):
        print(i, j)
    """

    expect = """
    from itertools import zip_longest

    a = [1, 2, 3]
    b = [4, 5, 6, 7]
    for i, j in zip_longest(a, b):
        print(i, j)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)


def test_remove_zip():
    source = """
    import six
    from six.moves import zip

    a = [1, 2, 3]
    b = [4, 5, 6]
    for i, j in zip(a, b):
        print(i, j)
    """

    expect = """
    import six


    a = [1, 2, 3]
    b = [4, 5, 6]
    for i, j in zip(a, b):
        print(i, j)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)


def test_remove_map():
    source = """
    import six
    from six.moves import map

    a = [1, 2, 3]
    for i in map(lambda x: x ** 2, a):
        print(i)
    """

    expect = """
    import six


    a = [1, 2, 3]
    for i in map(lambda x: x ** 2, a):
        print(i)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_six_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)

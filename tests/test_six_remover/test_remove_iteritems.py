from __future__ import annotations

import inspect

from flake8_scripts.six_remover import remove_six_from_text

from .runtime_checker import run_code


def test_remove_iteritems():
    source = """
    import six
    from six import moves

    d = {
        "foo": "xxx",
        "bar": "yyy",
    }
    count = {}
    for key, value in six.iteritems(d):
        if value not in count:
            count[key] = 0
        count[key] += 1
        print(key, value)
    print(count)
    """

    expected = """
    import six
    from six import moves

    d = {
        "foo": "xxx",
        "bar": "yyy",
    }
    count = {}
    for key, value in d.items():
        if value not in count:
            count[key] = 0
        count[key] += 1
        print(key, value)
    print(count)
    """

    assert remove_six_from_text(inspect.cleandoc(source)) == inspect.cleandoc(expected)
    assert run_code(inspect.cleandoc(source)) == run_code(inspect.cleandoc(expected))

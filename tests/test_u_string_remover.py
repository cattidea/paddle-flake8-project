from __future__ import annotations

import os
import sys

sys.path.append(os.path.dirname(__file__))

import inspect

from test_six_remover.runtime_checker import run_code

from flake8_scripts.u_string_remover import remove_u_string_from_text


def test_replace_u_string_with_its_own_literal():
    source = """
    import six

    a = u"blabla" # keep this comment
    b = u"lablab" # keep this comment too
    c = a.encode() + b.encode()
    print(a, b, c)

    # TODO
    # d = u'''
    # 中文
    # 且
    # 多行
    # '''
    # for line in d.splitlines():
    #     print(line)
    """

    expect = """
    import six

    a = 'blabla' # keep this comment
    b = 'lablab' # keep this comment too
    c = a.encode() + b.encode()
    print(a, b, c)

    # TODO
    # d = u'''
    # 中文
    # 且
    # 多行
    # '''
    # for line in d.splitlines():
    #     print(line)
    """

    source = inspect.cleandoc(source)
    expect = inspect.cleandoc(expect)
    actual = remove_u_string_from_text(source)

    assert actual is not None
    assert actual == expect
    assert run_code(source) == run_code(expect)

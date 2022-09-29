# PaddlePaddle Flake8 引入计划

## 我们要做什么？

由于目前 Paddle 并没有在 Python 端使用 Linter，因此存在很多格式上的问题，因此本计划即是在 Paddle 中引入 Flake8 ～

那么引入 Flake8 都需要做些什么呢？引入一个新的工具无非有两件主要要做的事情：存量修复 + 增量阻止。想要阻止增量很简单，直接在 pre-commit 中引入 Flake8 hook 即可，而存量的修复则是一件非常麻烦的事情，往往需要针对不同问题选择不同的解决方案。Flake8 的引入也是这样的，由于 Flake8 存在多达 132 个错误码，因此每一个错误码可能都需要考虑一种或者多种修复方案来进行修复。

::: details 错误码统计（点击展开）

如下是在修复 trailing whitespace 后统计的现存错误码：

```text
Type: E (26468)
E101    11
E121    8
E122    81
E123    12
E125    168
E126    723
E127    140
E128    207
E129    9
E131    45
E201    29
E202    11
E203    32
E225    61
E226    93
E228    3
E231    60
E241    2
E251    109
E261    11
E262    238
E265    925
E266    116
E271    4
E272    1
E301    7
E302    3
E303    7
E305    2
E306    1
E401    19
E402    2666
E501    19252
E502    400
E701    108
E711    166
E712    340
E713    22
E714    4
E721    8
E722    149
E731    62
E741    153

Type: F (9895)
F401    6750
F402    1
F403    57
F405    556
F522    1
F524    1
F541    33
F601    7
F631    2
F632    18
F811    177
F821    88
F841    2204

Type: W (1414)
W191    11
W503    279
W504    949
W601    3
W605    172
```

-  E、W 错误码详情见：[pycodestyle Error Code](https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes)
-  F 错误码详情见：[Flake8 Error Code](https://flake8.pycqa.org/en/latest/user/error-codes.html)

:::

## 具体怎么做？

在 [#45943](https://github.com/PaddlePaddle/Paddle/pull/45943) 已经添加了 Flake8 并将现存错误码禁用掉了，这样可以保证当前配置下直接运行 flake8 不会报错。之后我们可以每修复一个错误码就从配置文件中移除错误码，使其成为 flake8 的检测项目，避免增量的出现。

如在修复全部 tabs 相关问题后，[#46290](https://github.com/PaddlePaddle/Paddle/pull/46290) 将 E101 和 W191 从配置文件中移除了。

整体来说就是这么简单啦，接下来是一些具体的操作流程～

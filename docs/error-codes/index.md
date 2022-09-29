# Flake8 错误码

Flake8 默认启用的三个工具（pycodestyle、pyflakes、mccabe）共有 132 个错误码（C、E、F、W），其中 [E、W 错误码](https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes)为 pycodestyle 报告的错误码，主要是一些 [PEP 8](https://peps.python.org/pep-0008/) 中描述的格式问题，[F 错误码](https://flake8.pycqa.org/en/latest/user/error-codes.html)则是 pyflakes 报告的通过语法分析发现的潜在逻辑错误。

由于目前计划引入 black 作为新的 Formatter，black 可以解决大多数 E 错误码，因此 E 错误码暂缓修复，优先修复 F 错误码。

一些错误码的具体修复计划如下

-  [F401](./F401.md)
-  TODO... 将在之后逐步完成

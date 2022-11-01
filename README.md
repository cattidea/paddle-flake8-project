# PaddlePaddle flake8 project

PaddlePaddle Flake8 引入计划 repo，用于存放一些可能会使用的脚本，以及利用 Project 来追踪各个子任务的完成情况。

## Projects

[Flake8 错误码修复](https://github.com/orgs/cattidea/projects/4/views/2)

## Scripts

### Installation

```bash
git clone https://github.com/cattidea/paddle-flake8-project.git
cd paddle-flake8-project
# Need python >= 3.10
pip install .
```

### Usage

> 虽然是针对 Flake8 建的 repo，结果目前所有脚本都跟 Flake8 错误码无关 :joy:

#### remove-future-import

```bash
remove-future-import <path-globs> --fix
```

#### six-remover

```bash
six-remover <path-globs> --fix
```

#### u-string-remover

```bash
u-string-remover <path-globs> --fix
```

### Development

```bash
# Clone this repo
git clone https://github.com/cattidea/paddle-flake8-project.git
cd paddle-flake8-project
# Install poetry, see https://python-poetry.org/
# Install dependencies
poetry install
# Run tests
poetry run pytest
```

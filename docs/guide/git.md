# git 常用命令

:::tip

这里主要补充在引入 flake8 过程中常用的命令，commit、push 等基础命令不再赘述。

:::

## revert 部分修改过的文件

即，将修改的文件回撤回 develop 时的状态

```bash
# 建议操作之前先 merge 下 upstream/develop
git checkout develop -- <filepath>
```

## TODO...

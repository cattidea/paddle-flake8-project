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

## 同步上游修改 / 处理冲突

这里以上游 repo [PaddlePaddle/Paddle](https://github.com/PaddlePaddle/Paddle.git) 和 fork 后的 repo [cattidea/Paddle](https://github.com/cattidea/Paddle.git) 为例

如果一些微小的冲突，可以直接在网页上直接编辑以解决，如果不太方便在网页上解决则需要在本地进行一些操作……

```bash
# 首先需要确定设置了远程上游 repo，并将其命名为 upstream
git remote add upstream https://github.com/PaddlePaddle/Paddle.git
# 确定切回到 develop
git switch develop
# 然后 fetch 上游 repo 的 develop 分支
git fetch upstream develop
# 将上游 develop 最新更改应用到本地 develop 分支
git merge upstream/develop
# 此时本地 develop 分支已经同步上游 develop 分支，已经是最新的了
# 此时可选将本地 develop 分支 push 到自己的 fork repo，如果是在 cattidea 可以不用这一步
git push
# 然后切回自己的分支
git switch <branch_name>
# 将本地 develop 分支合并到自己的分支
git merge develop
# 此时如果出现无法自动解决的冲突需要手动解决冲突
# 手动解决冲突之后
git merge --continue
# 此时应该会提示添加 commit message，建议保持默认即可，如果 merge 时添加 `--no-edit` 参数（`git merge develop --no-edit` ），即为保持默认参数
# 此时自己的分支也是最新的了，push 上去就可以发现冲突解决了
```

## TODO...

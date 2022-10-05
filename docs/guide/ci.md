# CI 常见问题

:::tip

这里主要补充在引入 flake8 过程中一些建议的技巧做法，主要是 [Paddle CI 测试详解](https://www.paddlepaddle.org.cn/documentation/docs/zh/develop/dev_guides/git_guides/paddle_ci_manual_cn.html)的一个补充。

:::

## 为什么鼓励修复 PR 和配置 PR 分离？

由于多人协作时候经常会出现多个 PR 同时修改同一个文件的情况，在 git 无法自动解决冲突时，必须要手动解决冲突，在发生这种情况时，新提交的 commit 会使所有已有的 approval 都将作废，需要重新过 CI 并找人 approve，然而找人 approve 一般都非常花时间，有时可能要等好几天。

flake8 小组最可能发生冲突的就是配置文件，在多人协作的过程中可能要经常修改配置文件（删除错误码）以避免增量，如果因为配置文件的冲突重新找 approve 就得不偿失了，会极大影响小组协作的效率。

因此建议将配置文件分离出去单独做一个 PR，不过同时鼓励一个配置文件的 PR 对应多个修复 PR。

另外，配置文件的修改可以通过使用 `test=document_fix` 后缀来仅触发文档相关构建 CI（含 CodeStyle Check），即便发生冲突，解决冲突 + 重新触发 CI 也不过几分钟，对 merge 流程影响很小～

::: tip 小技巧

`test=document_fix` 需要在 PR 的**最新一次** commit message 里才是有效的，PR 标题是无效的，中间任何一次 commit message 里包含 `test=document_fix` 也是无效的。

如果上一个 commit message 忘记加 `test=document_fix` 也没关系，提交一个空 commit 来触发 document_fix 即可

```bash
git commit --allow-empty -m 'empty commit, test=document_fix'
```

:::

## 应当主要关注哪些 CI 流水线？

所有 `required` 的流水线都需要关注，不过一些流水线需要根据情况判断是否需要关注。

-  `PR-CI-Py3` 里会运行大量单测，也是最主要需要关注的 CI
-  `PR-CI-Codestyle-Check` 里会运行 pre-commit，如果修改了 pre-commit 相关脚本、配置文件，需要重点关注
-  `PR-CI-Static-Check` 里会运行编译 + docstring 示例代码运行、Approval 检查等，所有修改都应该重点关注此流水线，需根据情况处理
   -  docstring 示例代码失败：看是否是因为自己修改导致的，根据情况处理
   -  Approval 检查失败：看具体情况，如果是避不开的 Approval 需要等 approve
   -  编译失败：按理说除去修改 yaml codegen 脚本之外，修改 Python 代码应该不会导致编译失败，此时优先尝试 re-run
-  `PR-CI-APPROVAL` 里会检查 Approval，同上

近期不太稳定的流水线（10.5 updated）：

-  `PR-CI-NPU` 10.1 左右会在 git pull 时因网络问题失败，需要 re-run
-  `PR-CI-Windows` 近期持续排队中，需要等工作日修复后 re-run
-  `PR-CI-Windows-Inference` 同 `PR-CI-Windows`
-  `PR-CI-Coverage`
   -  近期偶尔会发生 build 失败问题，在这种情况下需要 re-run
   -  如果是后续单测失败，需要查看问题原因
   -  如果是覆盖率不够导致失败，需要查看是否是自己修改导致的覆盖率不够，如果不是，等工作日问是否可以豁免

## TODO...

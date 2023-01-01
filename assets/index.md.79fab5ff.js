import{_ as s,c as a,o as n,a as l}from"./app.7df73375.js";const D=JSON.parse('{"title":"PaddlePaddle Flake8 引入计划","description":"","frontmatter":{},"headers":[{"level":2,"title":"我们要做什么？","slug":"我们要做什么","link":"#我们要做什么","children":[]},{"level":2,"title":"具体怎么做？","slug":"具体怎么做","link":"#具体怎么做","children":[]}],"relativePath":"index.md"}'),p={name:"index.md"},e=l(`<h1 id="paddlepaddle-flake8-引入计划" tabindex="-1">PaddlePaddle Flake8 引入计划 <a class="header-anchor" href="#paddlepaddle-flake8-引入计划" aria-hidden="true">#</a></h1><h2 id="我们要做什么" tabindex="-1">我们要做什么？ <a class="header-anchor" href="#我们要做什么" aria-hidden="true">#</a></h2><p>由于目前 Paddle 并没有在 Python 端使用 Linter，因此存在很多格式上的问题，因此本计划即是在 Paddle 中引入 Flake8 ～</p><details class="details custom-block"><summary>Paddle 貌似使用了 Pylint？</summary><p>虽然确实目前使用了 Pylint，但是只是禁用了所有默认功能，单独启用了一个自定义的 docstring checker 而已，而且目前拥有若干问题（如 <a href="https://github.com/PaddlePaddle/Paddle/pull/46102#issuecomment-1248535300" target="_blank" rel="noreferrer">#46102 (comment)</a> 中描述的 CI 问题，貌似还有其他问题），感觉是个大坑，因此暂缓修复，将来有机会的话和文档方向一起整。</p></details><p>那么引入 Flake8 都需要做些什么呢？引入一个新的工具无非有两件主要要做的事情：存量修复 + 增量控制。</p><p>想要控制增量很简单，直接在 pre-commit 中引入 Flake8 hook 即可，这样就可以同时在 pre-commit 阶段和 CI 阶段都对 Python 的 CodeStyle 进行检查，保证每个 PR 都是满足 Flake8 要求的。</p><p>而存量的修复则是一件非常麻烦的事情，往往需要针对不同问题选择不同的解决方案。Flake8 的引入也是这样的，由于 Flake8 存在多达 132 个错误码，因此每一个错误码可能都需要考虑一种或者多种修复方案来进行修复。</p><details class="details custom-block"><summary>错误码统计（点击展开）</summary><p>如下是在修复 trailing whitespace 后统计的现存错误码：</p><div class="language-text"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki material-palenight"><code><span class="line"><span style="color:#A6ACCD;">Type: E (26468)</span></span>
<span class="line"><span style="color:#A6ACCD;">E101    11</span></span>
<span class="line"><span style="color:#A6ACCD;">E121    8</span></span>
<span class="line"><span style="color:#A6ACCD;">E122    81</span></span>
<span class="line"><span style="color:#A6ACCD;">E123    12</span></span>
<span class="line"><span style="color:#A6ACCD;">E125    168</span></span>
<span class="line"><span style="color:#A6ACCD;">E126    723</span></span>
<span class="line"><span style="color:#A6ACCD;">E127    140</span></span>
<span class="line"><span style="color:#A6ACCD;">E128    207</span></span>
<span class="line"><span style="color:#A6ACCD;">E129    9</span></span>
<span class="line"><span style="color:#A6ACCD;">E131    45</span></span>
<span class="line"><span style="color:#A6ACCD;">E201    29</span></span>
<span class="line"><span style="color:#A6ACCD;">E202    11</span></span>
<span class="line"><span style="color:#A6ACCD;">E203    32</span></span>
<span class="line"><span style="color:#A6ACCD;">E225    61</span></span>
<span class="line"><span style="color:#A6ACCD;">E226    93</span></span>
<span class="line"><span style="color:#A6ACCD;">E228    3</span></span>
<span class="line"><span style="color:#A6ACCD;">E231    60</span></span>
<span class="line"><span style="color:#A6ACCD;">E241    2</span></span>
<span class="line"><span style="color:#A6ACCD;">E251    109</span></span>
<span class="line"><span style="color:#A6ACCD;">E261    11</span></span>
<span class="line"><span style="color:#A6ACCD;">E262    238</span></span>
<span class="line"><span style="color:#A6ACCD;">E265    925</span></span>
<span class="line"><span style="color:#A6ACCD;">E266    116</span></span>
<span class="line"><span style="color:#A6ACCD;">E271    4</span></span>
<span class="line"><span style="color:#A6ACCD;">E272    1</span></span>
<span class="line"><span style="color:#A6ACCD;">E301    7</span></span>
<span class="line"><span style="color:#A6ACCD;">E302    3</span></span>
<span class="line"><span style="color:#A6ACCD;">E303    7</span></span>
<span class="line"><span style="color:#A6ACCD;">E305    2</span></span>
<span class="line"><span style="color:#A6ACCD;">E306    1</span></span>
<span class="line"><span style="color:#A6ACCD;">E401    19</span></span>
<span class="line"><span style="color:#A6ACCD;">E402    2666</span></span>
<span class="line"><span style="color:#A6ACCD;">E501    19252</span></span>
<span class="line"><span style="color:#A6ACCD;">E502    400</span></span>
<span class="line"><span style="color:#A6ACCD;">E701    108</span></span>
<span class="line"><span style="color:#A6ACCD;">E711    166</span></span>
<span class="line"><span style="color:#A6ACCD;">E712    340</span></span>
<span class="line"><span style="color:#A6ACCD;">E713    22</span></span>
<span class="line"><span style="color:#A6ACCD;">E714    4</span></span>
<span class="line"><span style="color:#A6ACCD;">E721    8</span></span>
<span class="line"><span style="color:#A6ACCD;">E722    149</span></span>
<span class="line"><span style="color:#A6ACCD;">E731    62</span></span>
<span class="line"><span style="color:#A6ACCD;">E741    153</span></span>
<span class="line"><span style="color:#A6ACCD;"></span></span>
<span class="line"><span style="color:#A6ACCD;">Type: F (9895)</span></span>
<span class="line"><span style="color:#A6ACCD;">F401    6750</span></span>
<span class="line"><span style="color:#A6ACCD;">F402    1</span></span>
<span class="line"><span style="color:#A6ACCD;">F403    57</span></span>
<span class="line"><span style="color:#A6ACCD;">F405    556</span></span>
<span class="line"><span style="color:#A6ACCD;">F522    1</span></span>
<span class="line"><span style="color:#A6ACCD;">F524    1</span></span>
<span class="line"><span style="color:#A6ACCD;">F541    33</span></span>
<span class="line"><span style="color:#A6ACCD;">F601    7</span></span>
<span class="line"><span style="color:#A6ACCD;">F631    2</span></span>
<span class="line"><span style="color:#A6ACCD;">F632    18</span></span>
<span class="line"><span style="color:#A6ACCD;">F811    177</span></span>
<span class="line"><span style="color:#A6ACCD;">F821    88</span></span>
<span class="line"><span style="color:#A6ACCD;">F841    2204</span></span>
<span class="line"><span style="color:#A6ACCD;"></span></span>
<span class="line"><span style="color:#A6ACCD;">Type: W (1414)</span></span>
<span class="line"><span style="color:#A6ACCD;">W191    11</span></span>
<span class="line"><span style="color:#A6ACCD;">W503    279</span></span>
<span class="line"><span style="color:#A6ACCD;">W504    949</span></span>
<span class="line"><span style="color:#A6ACCD;">W601    3</span></span>
<span class="line"><span style="color:#A6ACCD;">W605    172</span></span>
<span class="line"><span style="color:#A6ACCD;"></span></span></code></pre></div><ul><li>E、W 错误码详情见：<a href="https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes" target="_blank" rel="noreferrer">pycodestyle Error Code</a></li><li>F 错误码详情见：<a href="https://flake8.pycqa.org/en/latest/user/error-codes.html" target="_blank" rel="noreferrer">Flake8 Error Code</a></li></ul></details><h2 id="具体怎么做" tabindex="-1">具体怎么做？ <a class="header-anchor" href="#具体怎么做" aria-hidden="true">#</a></h2><p>直接一次性修复全部错误码是不现实的，因此错误码的修复需要分阶段进行，同时为了避免每修复完一个错误码就出现增量，需要在修复完一个错误码之后马上在 CI 上控制增量。</p><p>为了能够实现这样的目标，整体的思路是先将 Flake8 引入 pre-commit（CI）中，之后在配置文件中禁用现存错误码（<a href="https://github.com/PaddlePaddle/Paddle/pull/45943" target="_blank" rel="noreferrer">#45943</a>），这样可以保证当前配置下直接运行 flake8 不会报错。之后我们可以每修复一个错误码就从配置文件中移除错误码，使其成为 flake8 的检测项目，避免增量的出现。</p><p>如在 <a href="https://github.com/PaddlePaddle/Paddle/pull/46698" target="_blank" rel="noreferrer">#46698</a> 修复 F402 问题后，<a href="https://github.com/PaddlePaddle/Paddle/pull/46699" target="_blank" rel="noreferrer">#46699</a> 就可以将 F402 从配置文件中移除啦。</p><p>整体来说就是这么简单啦，接下来是一些具体的操作流程～</p>`,13),o=[e];function c(t,r,C,A,i,d){return n(),a("div",null,o)}const h=s(p,[["render",c]]);export{D as __pageData,h as default};

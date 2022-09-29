import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Flake8 project',
  description: 'Flake8 引入小组协作指南',
  base: '/paddle-flake8-project/',
  themeConfig: {
    nav: [
      {
        text: '常用链接',
        items: [
          {
            text: 'PaddlePaddle 贡献指南',
            link: 'https://www.paddlepaddle.org.cn/documentation/docs/zh/develop/dev_guides/index_cn.html',
          },
          {
            text: 'Flake8 tracking issue',
            link: 'https://github.com/PaddlePaddle/Paddle/issues/46039',
          },
          { text: 'F401 Project', link: 'https://github.com/orgs/cattidea/projects/4' },
          {
            text: 'Flake8 Error Code (F)',
            link: 'https://flake8.pycqa.org/en/latest/user/error-codes.html',
          },
          {
            text: 'pycodestyle Error Code (E, W)',
            link: 'https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes',
          },
        ],
      },
    ],

    sidebar: {
      '/': [
        {
          text: '任务介绍',
          items: [
            {
              text: '介绍',
              link: '/',
            },
          ],
        },
        {
          text: '快速开始',
          items: [
            {
              text: '协作流程',
              link: '/guide/process.html',
            },
            {
              text: 'CI 常见问题',
              link: '/guide/ci.html',
            },
            {
              text: 'Git 常用命令',
              link: '/guide/git.html',
            },
          ],
        },
        {
          text: '错误码',
          items: [
            {
              text: 'Flake8 错误码',
              link: '/error-codes/index.html',
            },
            {
              text: 'F401',
              link: '/error-codes/F401.html',
            },
          ],
        },
      ],
    },

    footer: {
      message: 'Released under the CC0 1.0 License.',
      copyright: 'Copyright © 2022-present cattidea flake8 group',
    },

    editLink: {
      pattern: 'https://github.com/cattidea/paddle-flake8-project/edit/main/docs/:path',
      text: '为此页提供修改建议',
    },

    socialLinks: [{ icon: 'github', link: 'https://github.com/cattidea/paddle-flake8-project' }],
  },
})

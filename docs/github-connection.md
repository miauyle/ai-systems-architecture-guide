# 云端 Codex、GitHub 仓库与 Pages 怎么配置？

[返回目录](../README.md) · [发布命令](publishing.md)

## 先分清四个配置层

| 配置层 | 解决的问题 | 常见配置方式 |
| --- | --- | --- |
| GitHub 连接器 / GitHub App | 助手通过 API 访问哪些账号和仓库？ | 在产品中连接 GitHub，完成授权并选择仓库范围 |
| Codex 云端任务环境 | 任务在哪个工作区或仓库执行？ | 在支持仓库环境的 Codex 界面创建或选择环境，关联仓库与任务分支 |
| 终端 Git / GitHub CLI 凭据 | shell 中的 clone、push 或 gh 命令如何认证？ | 平台注入凭据、凭据助手、PAT 或 SSH，取决于环境 |
| GitHub Pages | 仓库内容怎样构建并成为网站？ | 选择主题、配置构建和 Pages 发布来源 |

连接器能读取仓库，不等于终端已经能推送。配置了 Token，也不等于任务自动选择了目标仓库或已经配置网站发布。

## 推荐起点：使用已有 GitHub 连接

1. 在当前产品的设置或连接管理页面找到 GitHub；具体入口名称随版本变化。
2. 完成 GitHub 授权，给 GitHub App 选择需要访问的仓库；组织仓库可能还需要组织管理员允许安装或访问。
3. 指定要操作的完整仓库名或 URL，以及任务应使用的分支。
4. 若使用 Codex 网页中的仓库任务，在相应环境配置中选择该仓库。
5. 确认仓库访问权限与目标操作匹配；能读取不代表能写入，能写入也可能受到分支保护约束。

已有有效授权时，通常不需要再给助手粘贴个人访问令牌。新仓库不可见时，先检查安装范围、组织授权和连接是否需要刷新。

## 什么时候才需要 Token？

如果要在自定义云端终端执行 GitHub API、`gh` 或私有仓库 HTTPS 操作，而平台没有提供可用认证，可以考虑 PAT。也可以根据环境选择 SSH 或其他凭据方式。

优先使用限定目标仓库的 fine-grained PAT，按实际操作选择权限：

- 查看代码通常需要 Contents 读取权限。
- 提交文档或代码通常需要 Contents 写入权限。
- 创建 PR 需要相应的 Pull requests 权限。
- 修改 `.github/workflows/` 文件时，可能还需要 Workflows 写入权限。
- 创建新仓库、组织策略或其他管理操作，另有账号与组织权限要求；不能仅凭 Contents 写入权限推断。

令牌应配置到平台的凭据或加密 Secret 入口，不放进 Markdown、远程仓库 URL 或聊天正文。给 `gh` 配置 `GH_TOKEN` 是常见方式，但不自动证明普通 `git` 命令已使用它。

安装了 GitHub CLI 且认证已准备好时，可以用以下方式检查和配置 Git 凭据助手：

```bash
gh auth status
gh auth setup-git
```

这些命令依赖当前 CLI、网络与环境配置。平台已经有注入式凭据助手时，优先沿用它，避免不必要地覆盖。SSH 方案则需要相应的密钥、GitHub 授权和 SSH 网络可达性。

## 写入前还需要明确什么？

- **目标仓库：**完整的 `owner/repository` 或 URL。
- **目标分支：**已有分支还是新建分支。
- **交付方式：**直接提交、创建 PR，或先提供本地文件。
- **公开范围：**新仓库是否公开，以及文档是否包含受限数据。

授权与任务范围明确后，助手可以使用已连接的工具执行支持的仓库操作。是否支持创建新仓库，需要检查当前工具能力；不能仅凭有 GitHub 连接就保证所有管理动作都可执行。

## GitHub Pages 与主题

GitHub Pages 是网站托管服务，仓库权限和命令行认证只是内容管理的一部分。还要配置构建工具、导航、静态资源路径和部署来源。

常见网站地址：

- 用户站点：仓库通常命名为 `用户名.github.io`，地址为 `https://用户名.github.io/`。
- 项目站点：常见地址为 `https://用户名.github.io/仓库名/`。

选定主题后，需要检查它使用 Jekyll、其他静态站点工具还是纯静态文件，并适配数学公式和 Mermaid。GitHub 仓库页面支持这些语法，不代表 Pages 主题也会自动渲染它们。

项目站点尤其要检查子路径配置、导航和资源链接。发布来源可按方案选择分支目录或 GitHub Actions；部署流程需要匹配相应的 Pages 权限和设置。

当前文档保持为独立 Markdown 内容，主题与部署配置在选定主题后添加。

## 资料入口

- [Codex 云端文档](https://developers.openai.com/codex/cloud/)
- [GitHub 个人访问令牌管理](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [GitHub Pages 介绍](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages)
- [GitHub CLI：auth setup-git](https://cli.github.com/manual/gh_auth_setup-git)

配置界面与产品能力会变化，以当前界面和实际认证结果为准。

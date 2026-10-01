# GitHub 发布说明

[返回目录](../README.md)

## 当前交付状态

本交付包含本地 Git 仓库和 Markdown 文件。没有提供远程仓库 URL，也没有完成远程发布。

云端 Codex 的连接器授权与终端 Git 凭据是两个配置层，参见[GitHub 连接说明](github-connection.md)。后续 GitHub Pages 的主题与发布配置在选定主题后添加。

## 在你自己的机器发布

解压 ZIP 后可以初始化 Git；直接使用已初始化的工作区目录时，跳过初始化。先确认安装 Git；若使用 GitHub CLI，还需已有 GitHub 登录。

```bash
cd llm-architecture-guide
# 仅当解压后的目录没有 .git 时执行下面三行
git init -b main
git add .
git commit -m "docs: add Chinese LLM architecture guide"
```

使用 GitHub CLI 创建并推送私有仓库的一种方式：

```bash
gh repo create llm-architecture-guide --private --source=. --remote=origin --push
```

`--private` 可按你的分享意图改成 `--public`。如果希望发布到组织账号，应明确完整的 `组织名/仓库名`。仓库已经存在时，不要再次创建；可以添加该仓库提供的远程地址后推送。

```bash
git remote add origin <你的远程仓库地址>
git push -u origin main
```

这里的尖括号内容需要替换，不是可直接执行的真实地址。如果已有 `origin`，先查看并确认它指向正确目标。

## 不使用命令行

在 GitHub 创建空仓库，通过网页上传解压后的文件夹内容。保留 `README.md` 在根目录，并保留 `docs/` 和 `templates/` 的相对结构。

## 分享前

若加入了真实企业案例，检查其中是否含不适合公开的内容。若计划允许他人复用，应自行选择文档授权协议；当前没有擅自为你的文档指定许可证。

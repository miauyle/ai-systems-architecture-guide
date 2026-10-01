# GitHub 仓库与发布说明

[返回目录](../README.md)

## 当前仓库

远程为 [miauyle/ai-systems-notes](https://github.com/miauyle/ai-systems-notes)，唯一长期主线为 `master`。用户已删除 `main`，无需维持两条内容相同的分支。

文档通过已有 GPT–GitHub 授权交付，不需要把个人 Token 放进仓库。连接器授权与终端 Git 凭据是两个配置层，具体见[GitHub 连接说明](github-connection.md)。

当前为 Markdown 源码仓库，尚未配置 GitHub Pages 主题或网站部署。待用户确定主题后，再适配课程/专题导航、数学、Mermaid 和项目子路径；PR 合并不等于 Pages 已部署。

## 后续修改流程

从最新 `master` 建立临时分支，修改并验证，向 `master` 提 PR，再合并、删除临时分支。用户已要求助手按此方式自行合并；本仓库不通过直接更新 `master` 绕过 PR。

已有终端 GitHub 授权时，命令示意如下：

```bash
git switch master
git pull --ff-only
git switch -c docs/example-change
# 修改文件并运行相关检查后提交
git add .
git commit -m "docs: explain a concrete mechanism"
git push -u origin docs/example-change
gh pr create --base master --head docs/example-change
# 核对实际 diff、验证结果与待合并提交后
gh pr merge docs/example-change --merge --delete-branch
```

PR 描述围绕最终问题和改动，记录实际运行的验证，不能把预期结果写成已执行结果。若终端 push 的凭据不可用，可通过同一 GitHub 授权的 Git 数据 API 上传提交和临时分支，再走相同 PR 流程；核对树、提交和文件内容。

## 建立自己的副本

直接 Fork 本仓库可以保留文件结构。解压源码 ZIP 后也可以在新目录初始化 Git：

```bash
cd ai-systems-notes
git init -b master
git add .
git commit -m "docs: add AI systems notes"
```

仅在解压目录没有 `.git` 时初始化。使用 GitHub CLI 建立私有副本的一种方式：

```bash
gh repo create ai-systems-notes --private --source=. --remote=origin --push
```

按分享意图调整公开性；仓库已存在时不要重复创建。后续修改依然采用临时分支与 PR。网页上传时保留根目录 README，以及 `course/`、`docs/`、`examples/` 的相对结构。

## 分享与复用

若加入真实企业资料，应先确定分享范围。文档复用协议需要由仓库所有者选择，当前未擅自指定许可证。下载包排除 `.git/`、临时文件和凭据，与最终主线文件保持一致。

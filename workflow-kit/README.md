# 抖音 AI 科普自动运营工作流包

这是一套可迁移的抖音图文自动发布工作流包。它把已经跑通的 Codex 流程整理成通用文件夹，方便安装到 OpenClaw、Hermes 或其他智能体系统里执行。

它不绑定某一个模型，也不强制使用某一个智能体。模型只要能完成“读热点、写文案、生成图片提示词、调用图片生成器、调用发布器”这些动作，就可以使用这套方法。

## 能做什么

1. 从抖音发布页读取实时热点。
2. 挑选适合 AI 科普账号的热点。
3. 将热点强关联到 OpenClaw/Hermes/智能体工作流。
4. 生成 1 条图文正文。
5. 生成 3 张竖版 3:4 图片的提示词。
6. 检查图片、标题、正文、标签、热点是否齐全。
7. 调用发布器上传图片、选择热点、选择音乐、确认封面并发布。
8. 记录发布结果。

## 推荐安装方式

```powershell
cd C:\path\to\douyin-agent-workflow-kit
python tools\init_project.py --target C:\douyin-ai-project --account-alias your-account-alias --display-name "你的抖音名"
```

生成项目后，进入新项目：

```powershell
cd C:\douyin-ai-project
```

先把 3 张图片放到 `assets/images/demo/`，或把 `schedules/publish_plan.csv` 改成你的真实作品，再运行检查。

如果只是测试目录和检查工具，可以生成 3 张占位图：

```powershell
python ..\douyin-agent-workflow-kit\tools\make_demo_images.py --project . --id demo
```

```powershell
python ..\douyin-agent-workflow-kit\tools\check_note_ready.py --project . --id demo
```

如果使用 social-auto-upload 作为发布器：

```powershell
python ..\douyin-agent-workflow-kit\tools\publish_with_sau.py --project . --id demo --social-root C:\path\to\social-auto-upload
```

## 目录说明

```text
agent_specs/              给 OpenClaw、Hermes、通用智能体看的任务说明
adapters/social-auto-upload/  发布器适配说明
configs/                  配置示例
prompts/                  可复用提示词
templates/project/        新项目模板
tools/                    初始化、检查、生成命令、发布脚本
workflow/                 阶段化工作流说明
```

## 重要约定

- 不保存账号密码、验证码、扫码信息。
- 抖音热点必须在发布页真实可选，选不上就停止，不强发。
- 图文默认 3 张图：1 张主图 + 2 张附图。
- 图片建议统一为 1080x1440。
- 每个热点必须有不同画面隐喻，避免模板感。
- 图片可以由任意模型生成，质量差也能跑；质量好坏只影响内容效果，不影响流程。

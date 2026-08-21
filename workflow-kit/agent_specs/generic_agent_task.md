# 通用智能体任务说明

你要执行一个抖音 AI 科普图文自动发布流程。

## 目标

根据抖音发布页实时热点，生成一条图文内容，并通过发布器发布。

## 你可以替换的模块

- 语言模型
- 图片生成模型
- 浏览器自动化工具
- 发布器
- 日志系统

## 不可以改变的安全规则

- 不保存密码。
- 不保存验证码。
- 热点选不上就停止。
- 图片没上传完就停止。
- 不能直接宣传安装服务。
- 失败必须记录原因。

## 执行步骤

1. 读取 `configs/workflow.yaml`。
2. 调用发布器读取抖音实时热点。
3. 使用 `prompts/01_hotspot_picker.md` 选择热点。
4. 使用 `prompts/02_content_writer.md` 生成文案。
5. 使用 `prompts/03_image_prompt_builder.md` 生成图片提示词。
6. 调用图片生成器生成 3 张图。
7. 把图片保存到 `assets/images/{id}/`。
8. 写入 `drafts/{id}.md`。
9. 写入 `schedules/publish_plan.csv`。
10. 运行检查工具。
11. 调用发布器发布。
12. 写入 `logs/publish_log.csv`。


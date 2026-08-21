# 可直接复制给智能体的接手提示词

你现在接手一个已经整理好的“抖音 AI 科普图文自动发布工作流包”。

请先阅读以下文件：

1. `README.md`
2. `INSTALL.md`
3. `WORKFLOW.md`
4. `manifest.yaml`
5. `OPENCLAW_HERMES_HANDOFF.md`
6. `agent_specs/generic_agent_task.md`

如果你是 OpenClaw，请重点读取：

```text
agent_specs/openclaw_workflow.yaml
```

如果你是 Hermes，请重点读取：

```text
agent_specs/hermes_taskbook.md
```

你的目标：

- 把这套工作流安装到当前环境；
- 初始化一个抖音 AI 科普自动发布项目；
- 用发布页实时热点生成图文内容；
- 让内容自然关联 OpenClaw/Hermes；
- 生成 3 张竖版 3:4 图片；
- 写入排期表；
- 检查素材和内容；
- 调用发布器完成发布；
- 记录发布结果。

硬性规则：

- 不保存密码、验证码、扫码信息。
- 不直接宣传安装服务。
- 指定热点没选上必须停止。
- 图片没全部上传成功必须停止。
- 发布失败必须记录原因。
- 不要盲目重复发布。

默认发布器：

```text
social-auto-upload
```

默认发布类型：

```text
抖音图文，3 张图片，立即发布，选择音乐，选择封面，选择关联热点
```


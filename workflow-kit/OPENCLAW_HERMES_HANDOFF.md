# OpenClaw / Hermes 交付说明

这个文件用于把本工作流包交给 OpenClaw、Hermes 或其他智能体系统接手。

## 交付方式

把整个压缩包发送给 OpenClaw/Hermes：

```text
douyin-agent-workflow-kit.zip
```

对方解压后，先阅读：

1. `README.md`
2. `INSTALL.md`
3. `WORKFLOW.md`
4. `manifest.yaml`
5. `agent_specs/generic_agent_task.md`

如果是 OpenClaw，重点读取：

```text
agent_specs/openclaw_workflow.yaml
```

如果是 Hermes，重点读取：

```text
agent_specs/hermes_taskbook.md
```

## 给 OpenClaw 的接手指令

```text
你现在接手一个“抖音 AI 科普图文自动发布工作流包”。

请先读取 README.md、INSTALL.md、WORKFLOW.md、manifest.yaml，以及 agent_specs/openclaw_workflow.yaml。

你的任务是把这个工作流安装到当前环境中，并按阶段执行：
1. 初始化项目目录
2. 配置账号别名和发布器路径
3. 读取抖音发布页热点
4. 选择适合 AI 科普账号的热点
5. 生成图文文案和三张图片提示词
6. 调用图片生成器生成图片
7. 写入 schedules/publish_plan.csv
8. 运行发布前检查
9. 调用发布器发布
10. 记录发布结果

安全规则：
- 不保存密码、验证码、扫码信息。
- 指定热点没选上必须停止。
- 图片没全部上传成功必须停止。
- 不直接宣传安装服务。
- 失败必须记录原因。
```

## 给 Hermes 的接手指令

```text
你现在接手一个“抖音 AI 科普自动发布工作流”的记忆与复盘任务。

请先读取 README.md、WORKFLOW.md、manifest.yaml，以及 agent_specs/hermes_taskbook.md。

你的任务不是直接发布，而是记录和复盘：
1. 记录每次选中的热点
2. 记录标题、正文、标签、图片提示词和图片路径
3. 记录 OpenClaw/Hermes 的关联角度
4. 记录发布成功或失败原因
5. 避免下一次重复选题、重复视觉风格、重复表达角度

请把每次运行结果沉淀成可复用经验。
```

## 新手测试流程

如果对方只是想验证包能否使用，可以先运行：

```powershell
python tools\init_project.py --target C:\douyin-ai-project --account-alias your-account-alias --display-name "你的抖音名"
python tools\make_demo_images.py --project C:\douyin-ai-project --id demo
python tools\check_note_ready.py --project C:\douyin-ai-project --id demo
```

这只会初始化项目和检查文件，不会发布。

## 真正发布流程

确认已经安装并登录 social-auto-upload 后：

```powershell
python tools\publish_with_sau.py --project C:\douyin-ai-project --id demo --social-root C:\path\to\social-auto-upload
```

真实发布前，必须把 demo 占位图替换成正式图片，并把热点换成抖音发布页当前真实存在的热点。


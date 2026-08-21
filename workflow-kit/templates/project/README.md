# 抖音 AI 工作流项目

这个目录由 `douyin-agent-workflow-kit` 初始化生成。

## 常用目录

```text
accounts/       账号说明，不放密码
assets/images/  图文图片
assets/videos/  视频素材
drafts/         草稿
failed/         失败截图和失败记录
logs/           发布日志
published/      已发布归档
schedules/      排期表
configs/        本项目配置
```

## 下一步

1. 登录抖音创作者中心。
2. 填写 `configs/account.yaml` 和 `configs/publisher.yaml`。
3. 把图片放进 `assets/images/`。
4. 填写 `schedules/publish_plan.csv`。
5. 用工具包里的 `check_note_ready.py` 检查。
6. 用发布器发布。


# 安装说明

## 1. 准备环境

需要：

- Python 3.10 或更高版本
- 一个可用的图片生成工具
- 一个可用的发布器，默认建议 social-auto-upload
- 浏览器里已经登录抖音创作者中心

## 2. 初始化项目

```powershell
cd C:\path\to\douyin-agent-workflow-kit
python tools\init_project.py --target C:\douyin-ai-project --account-alias your-account-alias --display-name "你的抖音昵称"
```

初始化后会生成：

```text
C:\douyin-ai-project
  accounts/
  assets/images/
  assets/videos/
  drafts/
  failed/
  logs/
  published/
  schedules/
  configs/
```

## 3. 配置发布器

复制配置示例：

```text
configs/publisher.example.yaml
```

把里面的 `social_auto_upload_root` 改成你的 social-auto-upload 路径。

## 4. 写入一条作品

编辑：

```text
schedules/publish_plan.csv
```

至少填写：

- `id`
- `account`
- `type`
- `asset_paths`
- `title`
- `body`
- `tags`
- `hotspot`
- `status`

## 5. 发布前检查

如果只是测试流程，可以先生成 3 张占位图：

```powershell
python C:\path\to\douyin-agent-workflow-kit\tools\make_demo_images.py --project C:\douyin-ai-project --id demo
```

真实发布前请替换成正式图片。

```powershell
python C:\path\to\douyin-agent-workflow-kit\tools\check_note_ready.py --project C:\douyin-ai-project --id 你的作品ID
```

## 6. 生成发布命令

```powershell
python C:\path\to\douyin-agent-workflow-kit\tools\build_sau_command.py --project C:\douyin-ai-project --id 你的作品ID --social-root C:\path\to\social-auto-upload
```

## 7. 直接发布

```powershell
python C:\path\to\douyin-agent-workflow-kit\tools\publish_with_sau.py --project C:\douyin-ai-project --id 你的作品ID --social-root C:\path\to\social-auto-upload
```

## 失败处理

- 如果热点选不上：重新读取抖音发布页热点，换一个当前存在的热点。
- 如果图片没上传完：发布器必须等待 3 张图全部上传完成。
- 如果封面未选择：发布器必须进入封面设置页并确认。
- 如果正文被吞：检查敏感表达，改成更温和的 AI 科普说法。

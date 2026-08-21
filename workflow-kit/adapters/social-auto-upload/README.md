# social-auto-upload 适配器

本工作流默认使用 social-auto-upload 作为抖音发布器。

## 需要的能力

发布器需要支持：

```text
douyin list-hotspots
douyin upload-note --hotspot
```

并且发布图文时必须具备：

- 等待所有图片上传完成。
- 指定热点选不上就停止。
- 自动选择音乐。
- 自动确认封面。
- 失败时截图或返回错误。

## 推荐环境变量

```powershell
$env:SAU_DOUYIN_AUTO_MUSIC = "1"
$env:SAU_DOUYIN_HOTSPOT_LIMIT = "50"
$env:SAU_DOUYIN_HOTSPOT_SCROLLS = "6"
```

## 发布命令形态

```powershell
python sau_cli.py douyin upload-note `
  --account your-account-alias `
  --images image1.png image2.png image3.png `
  --title "标题" `
  --note "正文" `
  --tags "AI科普,智能体,OpenClaw,Hermes" `
  --hotspot "抖音热点标题" `
  --headed
```

## 读取热点命令形态

```powershell
python sau_cli.py douyin list-hotspots `
  --account your-account-alias `
  --images temp.png `
  --limit 50 `
  --scrolls 6 `
  --headed
```


# 发布器契约

任何发布器只要满足这个契约，都可以替换 social-auto-upload。

## list_hotspots

输入：

```json
{
  "account": "your-account-alias",
  "probe_image": "path/to/image.png",
  "limit": 50,
  "scrolls": 6
}
```

输出：

```json
[
  {"title": "热点标题", "heat": "1000万在看"}
]
```

## upload_note

输入：

```json
{
  "account": "your-account-alias",
  "images": ["01-cover.png", "02-detail.png", "03-workflow.png"],
  "title": "",
  "body": "",
  "tags": ["AI科普", "智能体"],
  "hotspot": "",
  "select_music": true,
  "handle_cover": true
}
```

输出：

```json
{
  "status": "published",
  "selected_hotspot": "",
  "message": ""
}
```

## 必须停止的情况

- 找不到指定热点。
- 图片上传失败或超时。
- 标题或正文没有填入。
- 发布按钮无法点击。
- 平台返回异常。


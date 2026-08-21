# 输入输出契约

## Plan Row

排期表字段：

```csv
id,account,type,asset_paths,title,body,tags,hotspot,schedule,status,result
```

字段说明：

- `id`：作品 ID。
- `account`：发布器账号别名。
- `type`：`note` 或 `video`。
- `asset_paths`：素材路径，多张图用 `|` 分隔。
- `title`：标题。
- `body`：正文。
- `tags`：英文逗号分隔。
- `hotspot`：抖音发布页需要选择的关联热点。
- `schedule`：空表示立即发布。
- `status`：`draft`、`pending`、`published`、`failed`。
- `result`：发布结果备注。

## Publisher Result

```json
{
  "status": "published|failed",
  "plan_id": "",
  "message": "",
  "selected_hotspot": "",
  "screenshot": ""
}
```

## Error Rules

- `HOTSPOT_NOT_FOUND`：指定热点不在当前发布页列表。
- `IMAGE_UPLOAD_TIMEOUT`：图片上传未完成。
- `COVER_NOT_SELECTED`：封面未设置。
- `PUBLISH_FAILED`：平台返回发布失败。


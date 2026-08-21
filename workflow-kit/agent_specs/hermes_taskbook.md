# Hermes Taskbook

Hermes 在这套流程里主要承担“记录、沉淀、复盘”的角色。

## 记忆对象

每条作品都要记录：

- plan_id
- hotspot
- hotspot_heat
- selected_reason
- title
- body
- tags
- image_prompts
- image_paths
- publish_status
- publish_time
- failure_reason

## 运行前读取

1. 读取最近 10 条已发布作品。
2. 避免重复选题。
3. 避免重复图片风格。
4. 避免连续多条都使用同一个 OpenClaw/Hermes 角度。

## 运行后写入

成功时：

```json
{
  "status": "published",
  "hotspot": "",
  "title": "",
  "visual_style": "",
  "openclaw_angle": "",
  "hermes_angle": ""
}
```

失败时：

```json
{
  "status": "failed",
  "stage": "",
  "reason": "",
  "next_action": ""
}
```

## 复盘问题

- 这个热点是否真的适合账号定位？
- 图片是否和上一条明显不同？
- OpenClaw/Hermes 是否自然出现？
- 正文是否像科普，而不是硬广？
- 发布失败是否可复现？


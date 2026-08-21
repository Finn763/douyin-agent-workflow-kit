# 阶段说明

## 1. collect_hotspots

读取抖音发布页“关联热点”下拉列表，尽量获取 50 个以上候选。

输出：

```json
[
  {"title": "热点标题", "heat": "1000万在看"}
]
```

## 2. select_hotspot

根据账号定位选择热点。热点必须能被关联到 AI、智能体、工作流、自动化、记忆、任务编排等方向。

## 3. write_note

生成标题、正文、标签。正文必须自然包含 OpenClaw/Hermes 的分工。

## 4. build_image_prompts

生成三张图的提示词。每个热点要有独立视觉隐喻。

## 5. generate_images

调用任意图片生成器生成三张图。图片质量可以不同，但必须保存到项目资产目录。

## 6. validate_assets

检查排期、图片路径、尺寸、标题、正文、标签、热点。

## 7. publish_note

调用发布器发布。热点选不上就停止。

## 8. record_result

写入日志，成功归档，失败保留截图和原因。


# Industry Profile Schema

Use this profile to adapt the workflow to any industry. JSON is preferred because scripts can read it directly.

Required fields:

```json
{
  "industry": "AI agent deployment",
  "audience": "Chinese short-video viewers interested in practical AI tools",
  "positioning": "AI science explainer, practical workflow angle",
  "offer_policy": {
    "direct_sales_allowed": false,
    "avoid_phrases": ["安装服务", "保证收益", "官方合作"]
  },
  "brand_terms": ["OpenClaw", "Hermes"],
  "visual_elements": {
    "required": ["red lobster mascot for OpenClaw", "white horse or hologram horse for Hermes"],
    "forbidden": ["blurred borders", "generic stock-photo look"]
  },
  "keywords": ["AI", "Claude", "Codex", "世界杯"],
  "topics_target": 4,
  "post_count": 8,
  "images_per_post": 3,
  "language": "zh-CN"
}
```

Optional fields:

- `tone`: calm, professional, playful, local-life, educational, urgent, etc.
- `compliance_notes`: platform rules, banned words, medical/legal/financial caution.
- `content_formats`: preferred post structures, such as checklist, myth-busting, tutorial, comparison.
- `cover_style`: preferred image style and palette.
- `fallback_policy`: what to do if few hotspots are found.
- `publish_account`: non-secret account alias, never password/cookie.
- `platform`: Douyin by default; future adapters can support other platforms.

Topic distribution rule:

- If found topics >= `topics_target`, choose `topics_target` topics and distribute evenly.
- If found topics = 1, put all posts under that one topic.
- If found topics = 2, split posts as evenly as possible.
- If no topic is found, follow `fallback_policy`; usually search broader keywords or pause for user approval.

Never store secrets in the profile.

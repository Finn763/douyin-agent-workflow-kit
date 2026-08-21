---
name: douyin-industry-auto-publisher
description: Use this skill when a user wants to run or adapt a Douyin creator-center auto-publishing workflow: search related hot topics by keywords, choose usable hotspots, generate industry-specific posts and image prompts, create multi-image note assets, select the matching hotspot and BGM during publishing, and record batch logs. The workflow is configurable for any industry or account positioning, not only AI content.
---

# Douyin Industry Auto Publisher

This skill turns a Douyin note-publishing process into a reusable, industry-configurable workflow. It is designed for agents that can browse/control Douyin Creator Center, generate images, and call local scripts or publishing tools such as `social-auto-upload`.

Core idea:

1. Search Douyin related-hotspot keywords.
2. Pick real usable hotspots.
3. Generate content for the user's industry profile.
4. Generate one direct AI cover plus two support cards per post.
5. Publish each note while re-searching and selecting the matching hotspot.
6. Select BGM and verify it has a music name plus duration.
7. Write logs to files, not chat.

## Safety Rules

- Do not install this skill or modify the user's active `.codex/skills`, `.codex`, cookies, existing projects, or presets unless explicitly asked.
- Do not include login cookies, tokens, account secrets, or private browser profiles inside the skill.
- Keep all generated assets, logs, and batch files under the current project workspace unless the user names another folder.
- For long logs, write files and report a short summary.
- If publishing to a real account, verify the intended account/session when there is any doubt.

## Required Inputs

Read or create an industry profile before generating a batch. The profile can be JSON, YAML, or plain instructions. Minimum fields:

- `industry`: the business/domain.
- `audience`: who the content is for.
- `positioning`: account voice and content goal.
- `offer_policy`: what can and cannot be said directly.
- `brand_terms`: required names, products, mascots, or concepts.
- `visual_elements`: required and forbidden image elements.
- `keywords`: hotspot search keywords.
- `post_count`: total posts.
- `topics_target`: how many distinct hotspots to prefer.

For the full schema, see `references/industry-config.md`.

## Workflow

Use this sequence unless the user changes it:

1. Load the industry profile.
2. Search Douyin related hotspots by the profile keywords.
3. Choose up to `topics_target` relevant real hotspots. If fewer are found, distribute `post_count` across the found topics.
4. Generate different angles for each post. Same hotspot does not mean same layout or same copy.
5. Generate main covers directly with an image model/tool as complete covers. Do not create a generic background and overlay title later.
6. Generate support cards with deterministic text rendering when exact text matters.
7. Validate image sizes are 3:4 vertical, usually `1080x1440`.
8. Publish. During publishing, re-open the related hotspot field, search the hotspot keyword, then select the matching topic.
9. Select music/BGM. Treat it as selected only when the page shows a chosen music row with a title/name and a duration such as `00:30`.
10. After the batch, summarize: selected topics, post count, publish success count, hotspot-selected count, BGM-selected count, and log folder.

Detailed workflow notes are in `references/workflow.md`.

## Content Rules

Content must be adapted to the industry profile:

- Tie the copy to the hotspot itself, not only to the account's product.
- Connect the hotspot to the user's industry through a useful explanation, checklist, workflow, comparison, mistake, or scenario.
- Do not force direct sales claims unless the profile explicitly allows them.
- Avoid sensitive, exaggerated, medical/legal/financial claims unless the user has provided compliant wording.
- Use varied structure across posts: question angle, checklist angle, mistake angle, process angle, case angle, comparison angle, myth-busting angle.

See `references/content-rules.md`.

## Image Rules

Per post:

- Image 1: main cover, generated directly by image model/tool with all key Chinese cover text already in the image.
- Image 2: support card explaining the hotspot or problem.
- Image 3: support card connecting the industry solution/workflow.

Main cover:

- Must be vertical 3:4.
- Must not use blurred side borders, stretched padding, or phone screenshot frames.
- Must include required brand/industry visual elements from the profile.
- Must vary scene, palette, composition, and angle across posts.
- Must leave safe margins so title text is not cropped.

See `references/image-rules.md`.

## Publishing Rules

If using Douyin Creator Center:

- Search topics once during planning.
- Search again during each actual publish step before selecting the hotspot.
- Prefer exact title match. If exact title is unavailable, use a close match only when it is clearly the same topic.
- If the topic disappeared, publish without the hotspot only if the user or profile allows fallback.
- Select BGM and confirm with music name plus duration.
- Save per-post logs.

See `references/publish-rules.md`.

## Useful Bundled Scripts

The scripts are templates. Copy or run them from a project workspace, then adapt paths and tool commands as needed.

- `scripts/create_batch_plan.py`: Create a batch plan from an industry profile and searched hotspots.
- `scripts/render_support_cards.py`: Render support card images from a batch plan using Pillow.
- `scripts/publish_batch_template.py`: Cross-platform publishing wrapper for `social-auto-upload`.

Example profiles:

- `examples/industry_profile_ai_openclaw_hermes.json`
- `examples/industry_profile_local_life_restaurant.json`

## Cross-Platform Notes

- Use `pathlib.Path`, not hard-coded Windows separators.
- Put local paths in environment variables such as `SAU_ROOT`, `DOUYIN_ACCOUNT`, `WORKSPACE_ROOT`.
- On macOS, the publishing browser/session must be logged in on that Mac. Cookies are not packaged here.
- On Windows, use PowerShell or Python commands; on macOS, use shell or Python commands.
- Keep generated images and logs in a project-local folder, for example `douyin-auto-project/outputs` and `douyin-auto-project/logs`.

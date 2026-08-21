# Workflow

## 1. Prepare

Load the industry profile and confirm:

- account positioning
- keywords to search
- total post count
- number of hotspots to prefer
- image rules
- forbidden claims or phrases

For real publishing, make sure the target browser/session is already logged in.

## 2. Search Hotspots

Search the related-hotspot field on the Douyin publishing page with each keyword.

Collect:

- title
- heat/view count if visible
- source keyword

Prefer topics that:

- are real selectable Douyin related hotspots
- match the industry profile
- can be naturally connected to the user's content
- are not purely entertainment unless the profile can use that angle

## 3. Allocate Posts

Distribute posts across selected topics. Example:

- 4 topics, 8 posts -> 2 posts each
- 3 topics, 8 posts -> 3, 3, 2
- 2 topics, 8 posts -> 4, 4
- 1 topic, 8 posts -> 8

## 4. Generate Content

For each post, produce:

- title
- body copy
- tags
- hotspot title
- hotspot search keyword
- main cover prompt
- support card 1 title and bullets
- support card 2 title and bullets

Each post should use a distinct angle. Avoid repeating the same first sentence, same outline, or same image scene.

## 5. Generate Images

Main cover:

- Use image generation directly.
- The cover title must be part of the generated image.
- Inspect or preview final covers when possible.

Support cards:

- Use deterministic rendering for exact text.
- Keep large readable Chinese text.

Validate all final images are `1080x1440` or another profile-approved 3:4 size.

## 6. Publish

For each post:

1. Upload images.
2. Fill title, body, and tags.
3. Open related hotspot field.
4. Search the post's `hotspot_search_keyword`.
5. Select the exact or clearly matching `hotspot`.
6. Select BGM.
7. Confirm BGM has a visible name and duration.
8. Select cover.
9. Publish.
10. Save log.

## 7. Verify

Batch summary should include:

- total attempted
- published count
- failed count
- hotspot selected count
- BGM selected count
- log folder
- any fallback used

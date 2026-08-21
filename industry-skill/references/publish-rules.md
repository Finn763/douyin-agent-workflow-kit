# Publish Rules

## Related Hotspot

Planning-time topic search is not enough. During each actual publish:

1. Open the related hotspot field.
2. Type the post's `hotspot_search_keyword`.
3. Wait for results.
4. Select the exact or clearly matching `hotspot` title.
5. Log the selected topic and heat if visible.

If the topic is not found:

- try the full hotspot title
- try a shorter keyword from the topic
- if still not found, follow the profile fallback policy

If fallback publishing is allowed, log: "published without matching hotspot".

## BGM

Do not treat BGM as selected just because a button says "modify music".

Confirm:

- the selected music row is visible
- it has a music title/name
- it has a duration like `00:30`

If BGM cannot be confirmed:

- retry by scrolling/clicking visible music candidates
- if still not confirmed, follow the profile fallback policy

## Logs

Write one log per post. Also keep a batch summary.

Useful fields:

- post id
- title
- hotspot
- search keyword
- selected hotspot result
- selected music result
- image paths
- return code
- timestamps

In chat, only summarize the result.

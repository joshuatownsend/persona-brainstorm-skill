# assets

| File | Purpose |
| --- | --- |
| `social-card.html` | Source for the social card. Self-contained: no external fonts, images, or scripts. |
| `social-card.png` | Rendered card, 1280×640 — the size GitHub wants for a repo social preview. |

## Regenerating the PNG

The card is a fixed 1280×640 page, so a plain viewport screenshot at that size is
the whole render step:

```sh
# from the repo root
npx playwright screenshot \
  --viewport-size=1280,640 \
  "file://$PWD/assets/social-card.html" \
  assets/social-card.png
```

Any headless-Chrome screenshot tool works; the only requirements are a 1280×640
viewport and no full-page flag.

The card carries no external resources, so a `file://` URL renders identically to
one served over HTTP — no local web server needed.

## Two things the card's CSS depends on

Both are commented in the source, and both fail *quietly* — the render succeeds
and looks wrong, rather than erroring:

- **The wordmark is sized to fit.** `persona-brainstorm` is 18 characters, about
  9.9em wide at the card's tracking. 96px keeps it inside the 1136px content box;
  raising it overflows the right edge.
- **The connector SVG is hand-aligned to the rows beside it.** Its two curves
  start at y=13 and y=57, which are the dot centres produced by a 26px row height
  and an 18px gap. Change either and the arrow detaches from the dots it joins.

The coverage marks are drawn as inline SVG rather than typed as the ✅ ◐ ○ ⚡
characters the document itself uses. Those are emoji, and emoji rasterise
differently on every renderer this card might be regenerated on.

## Where it's used

- Shown at the top of the repo `README.md`.
- Uploaded as the repo's Open Graph image under **Settings → General → Social
  preview**. That upload is manual and does *not* update when this file changes —
  re-upload after regenerating.

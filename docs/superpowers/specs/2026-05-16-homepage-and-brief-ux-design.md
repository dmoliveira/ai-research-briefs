# Homepage And Brief UX Design

## Goal

Refine `ai-research-briefs` into a more legible, more premium, and more useful GitHub Pages archive while keeping the current top-bar shell. The design should move toward a dashboard-editorial hybrid: strong overview at the top, denser archive navigation in the middle, and cleaner scanning behavior across digest pages.

## Direction

- Keep the current warm editorial palette and serif-led reading tone.
- Preserve the top navigation bar instead of adopting a permanent left sidebar.
- Increase information density without making the site feel productized or noisy.
- Use the supplied reference as a hierarchy reference, not as a literal clone.
- Favor minimalist structure, stronger grouping, and clearer action surfaces over decorative complexity.

## Homepage Changes

### 1. Top shell

- Keep the top bar with brand, GitHub, CV, and LinkedIn.
- Add a slimmer archive-status strip feel through spacing, muted utility copy, and cadence cues.
- Do not introduce a side navigation rail.

### 2. Hero

- Tighten the hero vertically.
- Keep the large editorial headline.
- Add clearer utility through a primary CTA and an archive exploration CTA.
- Keep the method panel, but make it feel more like a compact operating note than a separate feature block.

### 3. Metrics band

- Place a cleaner metrics row directly below the hero.
- Show:
  - number of briefs
  - indexed papers/items
  - active themes
  - cadence
- Style as compact stat modules with icons or stronger labels.

### 4. Main discovery block

- Replace the current “latest briefs” area with a more intentional two-column surface:
  - `Latest Brief`
  - `Featured Papers`
- `Latest Brief` should show:
  - date
  - paper count
  - summary
  - tags
  - primary read action
- `Featured Papers` should show the top 3-4 papers from the latest issue in ranked form.

### 5. Theme exploration

- Add a structured `Explore by Theme` section.
- Show theme cards for the most common tags, using a small icon, short description, and count.
- Keep the number of theme cards intentionally small and stable.

### 6. Archive navigation

- Add a `Recent Briefs` table or ledger card.
- Include:
  - date
  - paper count
  - compact theme indicators
  - concise theme labels
  - open action
- This should become the primary archive-browsing surface on the homepage.

### 7. Footer

- Reduce visual heaviness.
- Keep support and related projects, but structure them as lightweight editorial panels.
- Preserve links to `top-uni` and `master-philosophers`.

## Brief Page Changes

### 1. Page intro

- Keep the existing intro shell, but make it more structured.
- Add a compact issue overview band below the summary:
  - run date
  - item count
  - freshness window
  - key caveat if applicable

### 2. Quick navigation

- Add a digest map near the top of the article for fast scanning:
  - executive summary
  - key trends
  - read first
  - theme anchors
- Use internal links only if they stay robust in markdown/Jekyll output.

### 3. Section presentation

- Tighten section spacing.
- Make headings feel more like research report sections and less like a generic blog post.
- Keep card treatment, but reduce repetitive bulk where possible.

### 4. Paper entry cards

- Keep each paper as a structured card.
- Improve scanning hierarchy:
  - title and summary first
  - metadata in a tighter two-column grid
  - analysis fields as concise labeled rows or grouped blocks
- Preserve readability for long author lists and links.

### 5. Caveats

- Keep caveats visible and editorially honest.
- Style them as a distinct concluding note rather than generic bullets.

## Data And Generation Implications

- `scripts/generate_index.py` must render the new homepage sections consistently from digest front matter.
- The generator should compute:
  - total briefs
  - total indexed items
  - theme frequencies
  - latest brief metadata
  - archive rows
- Theme descriptions and icons may need a small static mapping in the generator.

## README Changes

- Align the README more closely with the new visual system.
- Keep the existing badges and banner, but improve structure and section rhythm.
- Clarify that the site now follows a Monday/Wednesday/Friday digest cadence.

## Constraints

- Keep the stack GitHub Pages friendly.
- No JS-heavy frontend rewrite.
- Preserve markdown-first publishing.
- Changes must be shared-layout driven, not one-off page hacks.
- Mobile behavior must remain clean and legible.

## Testing

- Regenerate homepage and RSS locally.
- Review generated markdown/HTML output for:
  - broken links
  - layout regressions
  - missing latest-brief data
  - poor mobile wrapping in metric cards, theme cards, and archive table
- Push and verify the live Pages deployment.

## Recommendation

Implement the redesign in one shared pass across:

- `docs/_layouts/default.html`
- `docs/assets/style.css`
- `scripts/generate_index.py`
- `README.md`

This keeps the design system coherent and avoids homepage-only polish that leaves article pages behind.

# Dashboard Editorial Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `ai-research-briefs` into a denser dashboard-editorial GitHub Pages archive while keeping the current top bar and improving both homepage discovery and brief-page scanability.

**Architecture:** Keep the site static and generator-driven. Extend `scripts/generate_index.py` so the homepage emits richer sections from digest front matter, then update the shared Jekyll layout and stylesheet so homepage, brief pages, and footer all inherit the same design language.

**Tech Stack:** GitHub Pages, Jekyll layouts, markdown, Python 3 generator scripts, CSS

---

## File Structure

- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/scripts/generate_index.py`
  - Render dashboard-style homepage sections and derive theme/archive summaries from digest front matter.
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/_layouts/default.html`
  - Add shared top utility strip and richer brief intro scaffolding.
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/assets/style.css`
  - Implement the new visual system for homepage modules, overview bands, archive tables, theme cards, and refined article cards.
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/2026/05/2026-05-16.md`
  - Add anchor ids and brief overview metadata where needed for new quick-jump and overview UI.
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/README.md`
  - Sync README structure and wording with the new cadence and visual hierarchy.
- Verify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/index.md`
  - Regenerated output should match the new homepage structure.

### Task 1: Extend Homepage Generator

**Files:**
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/scripts/generate_index.py`
- Verify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/index.md`

- [ ] **Step 1: Add a theme metadata mapping and helper functions**

```python
THEME_META = {
    "agents": {"label": "Agents", "icon": "◎", "description": "Planning, tool use, memory, and multi-step reasoning."},
    "llm": {"label": "LLM", "icon": "◌", "description": "Model capabilities, alignment, and reasoning."},
    "multimodal": {"label": "Multimodal", "icon": "◍", "description": "Vision, audio, and cross-modal understanding."},
    "evaluation": {"label": "Evaluation", "icon": "◇", "description": "Benchmarks, metrics, and robustness."},
    "privacy": {"label": "Privacy & Safety", "icon": "◈", "description": "Privacy, safeguards, and responsible AI."},
}

def normalized_tags(digest: dict[str, Any]) -> list[str]:
    tags = digest["tags"] if isinstance(digest["tags"], list) else []
    return [tag for tag in tags if isinstance(tag, str)]
```
Expected result: generator has explicit theme labels and descriptions instead of deriving vague card text.

- [ ] **Step 2: Reshape `render_index` to emit the new homepage sections**

```python
theme_rows = []
for tag, count in tag_counts.most_common(5):
    meta = THEME_META.get(tag, {"label": tag.title(), "icon": "•", "description": "Tracked across recent briefs."})
    theme_rows.append(
        f'''
        <article class="theme-tile">
          <span class="theme-tile-icon">{meta["icon"]}</span>
          <p class="section-kicker">{meta["label"]}</p>
          <h3>{meta["label"]}</h3>
          <p>{meta["description"]}</p>
          <strong>{count} paper{"s" if count != 1 else ""}</strong>
        </article>
        '''
    )
```
Expected result: homepage includes `Latest Brief`, `Featured Papers`, `Explore by Theme`, and `Recent Briefs`.

- [ ] **Step 3: Regenerate the homepage and confirm output shape**

Run: `python3 scripts/generate_index.py && sed -n '1,260p' docs/index.md`
Expected: generated `docs/index.md` contains metrics band, discovery split, theme tiles, and archive table markup.

- [ ] **Step 4: Commit generator changes**

```bash
git add scripts/generate_index.py docs/index.md
git commit -m "Redesign generated homepage structure"
```

### Task 2: Upgrade Shared Layout For Brief Pages

**Files:**
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/_layouts/default.html`
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/2026/05/2026-05-16.md`

- [ ] **Step 1: Add a slim utility strip and richer article intro shell in the layout**

```html
<div class="top-note">
  <p>✧ Independent. Lightweight. Unbiased.</p>
  <p>Updated weekly rhythm · Every Mon · Wed · Fri</p>
</div>
```

```liquid
{% if page.url != "/" %}
  <section class="issue-overview">
    <span class="overview-chip">{{ page.date | date: "%Y-%m-%d" }}</span>
    {% if page.source_count %}<span class="overview-chip">{{ page.source_count }} papers</span>{% endif %}
    <span class="overview-chip">Window: prior 7 days</span>
  </section>
{% endif %}
```
Expected result: shared shell gives homepage and briefs a clearer editorial framing.

- [ ] **Step 2: Add stable anchor ids and quick-jump markup to the sample brief**

```md
<nav class="brief-jump-nav">
  <a href="#executive-summary">Executive Summary</a>
  <a href="#key-trends">Key Trends</a>
  <a href="#read-first">Read First</a>
  <a href="#theme-agent-skills-planning-and-reflection">Agents</a>
  <a href="#theme-multimodal-and-spatial-agents">Multimodal</a>
  <a href="#theme-privacy-and-deployment-infrastructure">Privacy</a>
</nav>

## <span id="executive-summary">Executive Summary</span>
```
Expected result: brief pages expose faster navigation without changing the markdown-first model.

- [ ] **Step 3: Verify the article markup renders cleanly**

Run: `sed -n '1,220p' docs/2026/05/2026-05-16.md`
Expected: headings, ids, and quick-jump links are present and readable.

- [ ] **Step 4: Commit layout changes**

```bash
git add docs/_layouts/default.html docs/2026/05/2026-05-16.md
git commit -m "Refine shared layout and brief overview"
```

### Task 3: Implement CSS Redesign

**Files:**
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/assets/style.css`

- [ ] **Step 1: Introduce new shared modules for utility strip, metrics, discovery split, theme tiles, archive ledger, and issue overview**

```css
.top-note,
.metrics-ribbon,
.discovery-grid,
.theme-tile-grid,
.archive-ledger,
.issue-overview,
.brief-jump-nav {
  display: grid;
}

.metrics-ribbon {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
```
Expected result: stylesheet has named modules that correspond directly to the spec and generated markup.

- [ ] **Step 2: Refine typography, spacing, and card hierarchy**

```css
.hero {
  padding: 24px 26px;
}

.discovery-card,
.feature-panel,
.theme-tile,
.archive-row {
  border-radius: 20px;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.58);
}
```
Expected result: homepage becomes denser and more structured without losing the warm editorial tone.

- [ ] **Step 3: Add responsive rules for mobile**

```css
@media (max-width: 900px) {
  .metrics-ribbon,
  .discovery-grid,
  .theme-tile-grid,
  .archive-ledger-row {
    grid-template-columns: 1fr;
  }
}
```
Expected result: cards and archive rows collapse cleanly on smaller screens.

- [ ] **Step 4: Commit style changes**

```bash
git add docs/assets/style.css
git commit -m "Apply dashboard editorial visual system"
```

### Task 4: Sync README And Derived Outputs

**Files:**
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/README.md`
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/index.md`
- Modify: `/Users/diego/Documents/Codex/2026-05-16/simplest-way-1-open-codex-https/docs/rss.xml`

- [ ] **Step 1: Update README cadence and section rhythm**

```md
## ✦ Publishing Rhythm

- Monday, Wednesday, and Friday
- concise, theme-grouped issues
- public archive + RSS output
```
Expected result: README reflects the redesigned site structure and current publishing cadence.

- [ ] **Step 2: Regenerate derived files**

Run: `python3 scripts/generate_index.py && python3 scripts/rss.py`
Expected: `docs/index.md` and `docs/rss.xml` are up to date with redesigned content.

- [ ] **Step 3: Run final verification**

Run: `git diff --stat && python3 -m http.server 8000 -d docs`
Expected: diff is limited to the intended redesign files; local preview can be inspected if needed.

- [ ] **Step 4: Commit and publish**

```bash
git add README.md docs/index.md docs/rss.xml
git commit -m "Polish homepage, brief pages, and README"
git push
```

## Self-Review

- Spec coverage:
  - top shell, hero, metrics band, discovery split, theme exploration, archive navigation, brief intro, quick navigation, and README sync are each mapped to tasks.
- Placeholder scan:
  - no TODO or TBD markers remain in the task steps.
- Type consistency:
  - homepage sections are referred to consistently as metrics ribbon, discovery grid, theme tiles, archive ledger, issue overview, and brief jump nav.

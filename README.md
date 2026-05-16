# ai-research-briefs

Public GitHub Pages archive for concise AI research digests.

## What This Repository Does

- Publishes dated markdown digests under `docs/YYYY/MM/YYYY-MM-DD.md`
- Generates a homepage index from digest metadata
- Generates an RSS feed for new briefs
- Stays simple enough for Codex automation to maintain

## Repository Layout

```text
docs/
  _config.yml
  _layouts/default.html
  assets/style.css
  tags/.gitkeep
  index.md
  rss.xml
  2026/05/2026-05-16.md
scripts/
  generate_index.py
  rss.py
.github/workflows/
  publish.yml
```

## Content Model

Each digest file uses front matter like:

```yaml
---
title: "AI Research Brief: 2026-05-16"
date: 2026-05-16
summary: "Top AI, ML, agent, and recommender research from the week."
tags:
  - ai
  - ml
  - llm
  - agents
  - recommenders
featured:
  - "Paper title"
source_count: 12
---
```

The body is grouped by semantic theme and optimized for scanning.

## Local Usage

Generate the homepage index:

```bash
python3 scripts/generate_index.py
```

Generate RSS:

```bash
python3 scripts/rss.py
```

## GitHub Pages

This repository is designed for GitHub Pages deployment from a workflow. The workflow regenerates the index and RSS, then publishes the `docs/` directory.

## Automation Shape

A Codex automation for this repo should:

1. Find strong items from the previous 7 days.
2. Create or update a digest file in `docs/YYYY/MM/YYYY-MM-DD.md`.
3. Run `scripts/generate_index.py`.
4. Run `scripts/rss.py`.
5. Commit and push only if there is meaningful new content.

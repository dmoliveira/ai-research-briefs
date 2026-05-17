#!/usr/bin/env python3

from __future__ import annotations

import datetime as dt
import pathlib
import re
from collections import Counter
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
THEME_META: dict[str, dict[str, str]] = {
    "agents": {
        "label": "Agents",
        "icon": "◎",
        "description": "Planning, tool use, memory, and multi-step reasoning.",
    },
    "llm": {
        "label": "LLM",
        "icon": "◌",
        "description": "Model capabilities, alignment, and reasoning.",
    },
    "multimodal": {
        "label": "Multimodal",
        "icon": "◍",
        "description": "Vision, audio, and cross-modal understanding.",
    },
    "evaluation": {
        "label": "Evaluation",
        "icon": "◇",
        "description": "Benchmarks, metrics, and robustness.",
    },
    "privacy": {
        "label": "Privacy & Safety",
        "icon": "◈",
        "description": "Privacy, safeguards, and responsible AI.",
    },
}


def parse_front_matter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
      return {}
    end = text.find("\n---\n", 4)
    if end == -1:
      return {}

    data: dict[str, Any] = {}
    lines = text[4:end].splitlines()
    current_list_key: str | None = None
    for raw_line in lines:
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") and current_list_key:
            data.setdefault(current_list_key, []).append(line[4:].strip().strip('"'))
            continue
        if line.startswith("- ") and current_list_key:
            data.setdefault(current_list_key, []).append(line[2:].strip().strip('"'))
            continue

        current_list_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            current_list_key = key
            data[key] = []
            continue
        data[key] = value.strip('"')
    return data


def collect_digests() -> list[dict[str, Any]]:
    digests: list[dict[str, Any]] = []
    for path in DOCS.rglob("*.md"):
        if path.name == "index.md" or path.parts[-2] == "tags":
            continue
        if not DATE_RE.match(path.stem):
            continue
        text = path.read_text(encoding="utf-8")
        front_matter = parse_front_matter(text)
        date_str = str(front_matter.get("date", path.stem))
        try:
            parsed_date = dt.date.fromisoformat(date_str)
        except ValueError:
            continue
        digests.append(
            {
                "title": front_matter.get("title", f"AI Research Brief: {date_str}"),
                "date": parsed_date,
                "summary": front_matter.get("summary", ""),
                "tags": front_matter.get("tags", []),
                "featured": front_matter.get("featured", []),
                "source_count": front_matter.get("source_count", ""),
                "path": path.relative_to(DOCS).with_suffix(".html").as_posix(),
            }
        )
    return sorted(digests, key=lambda item: item["date"], reverse=True)


def normalized_tags(digest: dict[str, Any]) -> list[str]:
    raw_tags = digest["tags"] if isinstance(digest["tags"], list) else []
    return [tag for tag in raw_tags if isinstance(tag, str)]


def tag_meta(tag: str) -> dict[str, str]:
    fallback = {
        "label": tag.replace("-", " ").title(),
        "icon": "•",
        "description": "Tracked across recent briefs.",
    }
    return THEME_META.get(tag, fallback)


def render_index(digests: list[dict[str, Any]]) -> str:
    tag_counts = Counter()
    archive_counts = Counter()
    total_sources = 0
    for digest in digests:
        for tag in normalized_tags(digest):
            tag_counts[tag] += 1
        archive_counts[digest["date"].strftime("%Y-%m")] += 1
        source_value = str(digest["source_count"])
        if source_value.isdigit():
            total_sources += int(source_value)

    header = f"""---
title: Research Briefs
summary: Public archive of concise AI research digests.
---

<section class="hero">
  <div class="hero-grid">
    <div class="hero-copy">
      <p class="section-kicker">Public archive · editorial research digest</p>
      <h1>AI research briefs, organized for fast reading.</h1>
      <p>
        Dated issues covering strong new work in AI, ML, LLMs, agents, recommender systems,
        and adjacent engineering research, shaped for applied builders rather than hype cycles.
      </p>
      <div class="hero-actions">
        <a class="button primary" href="{digests[0]['path'] if digests else '#'}">Open latest brief</a>
        <a class="button tertiary" href="#recent-briefs">Explore archive</a>
      </div>
    </div>
    <aside class="hero-panel">
      <p class="section-kicker">Our method</p>
      <h2>Concise by default.</h2>
      <p>
        Each issue groups related work by theme, flags stronger papers first, and keeps caveats
        visible when source freshness or review status is weak.
      </p>
      <ul class="bullet-list">
        <li>10-20 high-signal papers, articles, or technical notes</li>
        <li>Theme-first structure for skimmability</li>
        <li>Ratings, reading-time estimates, and practical takeaways</li>
      </ul>
    </aside>
  </div>
</section>

<section class="metrics-ribbon">
"""
    if not digests:
        return header + '\n<div class="home-empty">No briefs published yet.</div>\n</section>\n'

    lines = [header]
    featured_digest = digests[0]
    tags = normalized_tags(featured_digest)
    featured = featured_digest["featured"] if isinstance(featured_digest["featured"], list) else []
    pills = "".join(f'<span class="pill">{tag}</span>' for tag in tags[:5])
    source_count = f'{featured_digest["source_count"]} papers' if featured_digest["source_count"] else "Digest"
    lines.extend(
        [
            '  <article class="metric-block">',
            '    <span class="metric-icon">▣</span>',
            '    <span class="metric-copy"><span class="metric-label">Briefs</span><strong class="metric-value">' + str(len(digests)) + '</strong><span class="metric-sub">Total issues</span></span>',
            '  </article>',
            '  <article class="metric-block">',
            '    <span class="metric-icon">◫</span>',
            '    <span class="metric-copy"><span class="metric-label">Papers archived</span><strong class="metric-value">' + str(total_sources) + '</strong><span class="metric-sub">Across all briefs</span></span>',
            '  </article>',
            '  <article class="metric-block">',
            '    <span class="metric-icon">◌</span>',
            '    <span class="metric-copy"><span class="metric-label">Core themes</span><strong class="metric-value">' + str(min(len(tag_counts), 12)) + '</strong><span class="metric-sub">Current archive surface</span></span>',
            '  </article>',
            '  <article class="metric-block">',
            '    <span class="metric-icon">◷</span>',
            '    <span class="metric-copy"><span class="metric-label">Cadence</span><strong class="metric-value">Mon · Wed · Fri</strong><span class="metric-sub">Scheduled publication</span></span>',
            '  </article>',
            '</section>',
            '<section class="home-section discovery-section">',
            '  <div class="section-heading-row">',
            '    <div>',
            '      <h2>Latest Brief</h2>',
            '      <p class="home-section-intro">Each issue is written as a dated briefing note: short enough to skim quickly, dense enough to be useful.</p>',
            '    </div>',
            '  </div>',
            '  <div class="discovery-grid">',
            '    <article class="discovery-card latest-brief-card">',
            f'      <p class="meta">{featured_digest["date"].isoformat()} · {source_count}</p>',
            f'      <h3><a href="{featured_digest["path"]}">{featured_digest["title"]}</a></h3>',
            f'      <p class="digest-summary">{featured_digest["summary"]}</p>',
            '      <div class="digest-meta-cluster">',
            f'        <span class="digest-meta-chip">{featured_digest["date"].strftime("%b %d, %Y")}</span>',
            f'        <span class="digest-meta-chip">{source_count}</span>',
            '        <span class="digest-meta-chip">Verified window</span>',
            '      </div>',
            f'      <div class="pill-row">{pills}</div>' if pills else "",
            f'      <a class="text-link" href="{featured_digest["path"]}">Read full brief</a>',
            '    </article>',
            '    <aside class="feature-panel">',
            '      <p class="section-kicker">Featured papers</p>',
            '      <p class="feature-panel-intro">Ranked from the latest issue for fastest triage.</p>',
            '      <ol class="featured-paper-list">',
        ]
    )
    for index, item in enumerate(featured[:4], start=1):
        lines.append(f'        <li><span class="featured-rank">{index}</span><span>{item}</span></li>')
    if not featured:
        lines.append('        <li><span>Open the latest issue for the strongest papers in the current window.</span></li>')
    lines.extend(
        [
            '      </ol>',
            f'      <a class="text-link" href="{featured_digest["path"]}">View all {featured_digest["source_count"]} papers</a>' if featured_digest["source_count"] else f'      <a class="text-link" href="{featured_digest["path"]}">Open latest issue</a>',
            '    </aside>',
            '  </div>',
            '</section>',
        ]
    )
    lines.extend(
        [
            '<section class="home-section">',
            '  <div class="section-heading-row">',
            '    <div>',
            '      <h2>Explore by Theme</h2>',
            '      <p class="home-section-intro">Jump into the topics shaping AI research this week.</p>',
            '    </div>',
            f'    <a class="section-heading-link" href="{featured_digest["path"]}">From latest issue</a>',
            '  </div>',
            '  <div class="theme-tile-grid">',
        ]
    )
    for tag, count in tag_counts.most_common(5):
        meta = tag_meta(tag)
        lines.extend(
            [
                f'    <article class="theme-tile" data-theme="{tag}">',
                f'      <span class="theme-tile-icon">{meta["icon"]}</span>',
                f'      <p class="section-kicker">{meta["label"]}</p>',
                f'      <h3>{meta["label"]}</h3>',
                f'      <p>{meta["description"]}</p>',
                f'      <strong>{"Current focus" if count == 1 else f"Seen in {count} briefs"}</strong>',
                '    </article>',
            ]
        )
    lines.extend(
        [
            '  </div>',
            '</section>',
            '<section class="home-section" id="recent-briefs">',
            '  <div class="section-heading-row">',
            '    <div>',
            '      <h2>Recent Briefs</h2>',
            '      <p class="home-section-intro">Browse the most recent issues as a dated research ledger.</p>',
            '    </div>',
            '    <a class="section-heading-link" href="rss.xml">Follow via RSS</a>',
            '  </div>',
            '  <div class="archive-status-note">',
            '    <p><strong>Publishing rhythm:</strong> the Codex pipeline scans on Monday, Wednesday, and Friday mornings in Melbourne time and only posts when the issue clears the quality bar.</p>',
            '    <p class="archive-status-subtle">Every brief is meant to read like a durable research ledger entry rather than a feed item.</p>',
            '  </div>',
            '  <div class="archive-ledger">',
            '    <div class="archive-ledger-head">',
            '      <span>Date</span>',
            '      <span>Papers</span>',
            '      <span>Themes</span>',
            '      <span></span>',
            '    </div>',
        ]
    )
    for digest in digests[:8]:
        digest_tags = normalized_tags(digest)
        theme_pills = "".join(
            f'<span class="theme-dot" title="{tag_meta(tag)["label"]}">{tag_meta(tag)["icon"]}</span>'
            for tag in digest_tags[:5]
        )
        theme_labels = ", ".join(tag_meta(tag)["label"] for tag in digest_tags[:5])
        lines.extend(
            [
                '    <article class="archive-ledger-row">',
                f'      <span class="archive-date">{digest["date"].isoformat()}</span>',
                f'      <span class="archive-count">{digest["source_count"]} items</span>',
                f'      <span class="archive-themes"><span class="theme-dot-row">{theme_pills}</span><span class="archive-theme-labels">{theme_labels}</span></span>',
                f'      <a class="archive-open" href="{digest["path"]}" aria-label="Open {digest["title"]}">Open issue</a>',
                '    </article>',
            ]
        )
    lines.extend(['  </div>', '</section>'])
    return "\n".join(line for line in lines if line != "")


def main() -> None:
    digests = collect_digests()
    (DOCS / "index.md").write_text(render_index(digests), encoding="utf-8")


if __name__ == "__main__":
    main()

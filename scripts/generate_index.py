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
                "path": path.relative_to(DOCS).as_posix(),
            }
        )
    return sorted(digests, key=lambda item: item["date"], reverse=True)


def render_index(digests: list[dict[str, Any]]) -> str:
    tag_counts = Counter()
    archive_counts = Counter()
    total_sources = 0
    for digest in digests:
        for tag in digest["tags"] if isinstance(digest["tags"], list) else []:
            tag_counts[tag] += 1
        archive_counts[digest["date"].strftime("%Y-%m")] += 1
        source_value = str(digest["source_count"])
        if source_value.isdigit():
            total_sources += int(source_value)

    header = f"""---
title: Research Briefs
summary: Weekly archive of concise AI research digests.
---

<section class="hero">
  <div class="hero-grid">
    <div class="hero-copy">
      <p class="section-kicker">Public archive · editorial research digest</p>
      <h1>AI research briefs, organized for fast reading.</h1>
      <p>
        Weekly issues covering strong new work in AI, ML, LLMs, agents, recommender systems,
        and adjacent engineering research, shaped for applied builders rather than hype cycles.
      </p>
      <div class="metric-strip">
        <div class="stat-card">
          <span class="metric-label">Briefs</span>
          <strong class="metric-value">{len(digests)}</strong>
        </div>
        <div class="stat-card">
          <span class="metric-label">Indexed items</span>
          <strong class="metric-value">{total_sources}</strong>
        </div>
        <div class="stat-card">
          <span class="metric-label">Cadence</span>
          <strong class="metric-value">Weekly</strong>
        </div>
      </div>
    </div>
    <aside class="hero-panel">
      <p class="section-kicker">Method</p>
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

<section class="home-section">
  <h2>Latest Briefs</h2>
"""
    if not digests:
        return header + '\n<div class="home-empty">No briefs published yet.</div>\n</section>\n'

    lines = [header, '<ul class="digest-list">']
    for digest in digests:
        tags = digest["tags"] if isinstance(digest["tags"], list) else []
        featured = digest["featured"] if isinstance(digest["featured"], list) else []
        pills = "".join(f'<span class="pill">{tag}</span>' for tag in tags[:5])
        featured_line = ""
        if featured:
            featured_line = f'<p class="digest-summary"><strong>Read first:</strong> {", ".join(featured[:3])}</p>'
        source_count = f'{digest["source_count"]} items' if digest["source_count"] else "Digest"
        lines.extend(
            [
                '  <li class="digest-card">',
                f'    <p class="meta">{digest["date"].isoformat()} · {source_count}</p>',
                f'    <h3><a href="{digest["path"]}">{digest["title"]}</a></h3>',
                f'    <p class="digest-summary">{digest["summary"]}</p>',
                f"    {featured_line}" if featured_line else "",
                f'    <div class="pill-row">{pills}</div>' if pills else "",
                "  </li>",
            ]
        )
    lines.append("</ul>")
    lines.append("</section>")
    lines.extend(
        [
            '<section class="home-section">',
            '  <div class="theme-grid">',
            '    <div class="theme-card">',
            '      <p class="section-kicker">Active themes</p>',
            '      <h2>What the archive tracks most.</h2>',
            '      <div class="pill-row">',
        ]
    )
    for tag, _count in tag_counts.most_common(8):
        lines.append(f'        <span class="pill">{tag}</span>')
    lines.extend(
        [
            "      </div>",
            "    </div>",
            '    <div class="theme-card">',
            '      <p class="section-kicker">Archive rhythm</p>',
            '      <h2>Published as a dated research ledger.</h2>',
            '      <ul class="archive-list">',
        ]
    )
    for month, count in sorted(archive_counts.items(), reverse=True)[:6]:
        lines.append(f"        <li>{month}: {count} brief{'s' if count != 1 else ''}</li>")
    lines.extend(
        [
            "      </ul>",
            "    </div>",
            "  </div>",
            "</section>",
        ]
    )
    return "\n".join(line for line in lines if line != "")


def main() -> None:
    digests = collect_digests()
    (DOCS / "index.md").write_text(render_index(digests), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from __future__ import annotations

import datetime as dt
import pathlib
import re
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
    header = """---
title: Research Briefs
summary: Weekly archive of concise AI research digests.
---

<section class="hero">
  <p class="meta">Public archive</p>
  <h1>AI research briefs, organized for fast reading.</h1>
  <p>
    Weekly digests covering strong new work in AI, ML, LLMs, agents, recommender systems,
    and adjacent engineering research.
  </p>
</section>

## Latest Briefs
"""
    if not digests:
        return header + "\n_No briefs published yet._\n"

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
    return "\n".join(line for line in lines if line != "")


def main() -> None:
    digests = collect_digests()
    (DOCS / "index.md").write_text(render_index(digests), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from __future__ import annotations

import html
import os
import pathlib
import xml.etree.ElementTree as ET

from generate_index import collect_digests


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE_URL = os.environ.get("SITE_URL", "https://dmoliveira.github.io/ai-research-briefs").rstrip("/")


def build_rss() -> ET.Element:
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "ai-research-briefs"
    ET.SubElement(channel, "link").text = f"{SITE_URL}/"
    ET.SubElement(channel, "description").text = "Concise AI research digests."

    for digest in collect_digests()[:30]:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = digest["title"]
        ET.SubElement(item, "link").text = f'{SITE_URL}/{digest["path"]}'
        ET.SubElement(item, "guid").text = f'{SITE_URL}/{digest["path"]}'
        ET.SubElement(item, "pubDate").text = digest["date"].strftime("%a, %d %b %Y 00:00:00 +0000")
        ET.SubElement(item, "description").text = html.escape(digest["summary"])
    return rss


def main() -> None:
    rss = build_rss()
    xml_bytes = ET.tostring(rss, encoding="utf-8", xml_declaration=True)
    (DOCS / "rss.xml").write_bytes(xml_bytes)


if __name__ == "__main__":
    main()

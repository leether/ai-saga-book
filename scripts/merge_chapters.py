#!/usr/bin/env python3
"""Merge all chapter markdown files into a single file for Pandoc."""
from pathlib import Path
import re

BOOK_DIR = Path(__file__).parent.parent / "book" / "src"
OUT = Path(__file__).parent.parent / "全书.md"

VOLUME_HEADERS = {
    1: "# 卷一 破晓\n",
    6: "# 卷二 扩散\n",
    11: "# 卷三 权力\n",
    16: "# 卷四 入侵现实\n",
    22: "# 卷五 裂缝与重构\n",
    30: "# 卷六 智能体时代\n",
}

parts = []
parts.append("% 智能涌动\n% 新褶\n\n")

for i in range(1, 35):
    if i in VOLUME_HEADERS:
        parts.append(VOLUME_HEADERS[i])
        parts.append("\n")
    ch = BOOK_DIR / f"ch{i:02d}.md"
    parts.append(ch.read_text(encoding="utf-8"))
    parts.append("\n\n")

OUT.write_text("".join(parts), encoding="utf-8")
print(f"Merged: {OUT}")

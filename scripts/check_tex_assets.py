#!/usr/bin/env python3
"""Fail when an active LaTeX includegraphics target cannot be resolved."""

from __future__ import annotations

import re
import sys
from pathlib import Path


GRAPHIC_EXTENSIONS = ("", ".pdf", ".png", ".jpg", ".jpeg")


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        match = re.search(r"(?<!\\)%", line)
        lines.append(line[: match.start()] if match else line)
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_tex_assets.py DOCUMENT_DIR", file=sys.stderr)
        return 2

    document_dir = Path(sys.argv[1]).resolve()
    tex_files = sorted(document_dir.rglob("*.tex"))
    if not tex_files:
        print(f"no .tex files found in {document_dir}", file=sys.stderr)
        return 2

    text = "\n".join(
        strip_comments(path.read_text(encoding="utf-8")) for path in tex_files
    )
    search_dirs = [document_dir]
    for block in re.findall(r"\\graphicspath\{((?:\{[^{}]+\})+)\}", text):
        search_dirs.extend(
            document_dir / item for item in re.findall(r"\{([^{}]+)\}", block)
        )

    targets = set(
        re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^{}]+)\}", text)
    )
    missing = [
        target
        for target in sorted(targets)
        if not any(
            (directory / f"{target}{extension}").is_file()
            for directory in search_dirs
            for extension in GRAPHIC_EXTENSIONS
        )
    ]

    if missing:
        print("missing LaTeX graphics:", file=sys.stderr)
        for target in missing:
            print(f"  - {target}", file=sys.stderr)
        return 1

    print(f"assets ok: {document_dir.name} ({len(tex_files)} TeX file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

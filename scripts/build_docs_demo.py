#!/usr/bin/env python3
"""Regenerate docs/demo/demo.html for the docs home page (assets are committed)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "example" / "demo.py"), "--docs"],
        check=True,
        cwd=ROOT,
    )
    reveal_js = ROOT / "docs" / "demo" / "revealjs" / "dist" / "reveal.js"
    if not reveal_js.is_file():
        raise SystemExit(
            "reveal.js bundle missing. Run: git submodule update --init --recursive"
        )


if __name__ == "__main__":
    main()
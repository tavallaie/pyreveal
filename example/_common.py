"""Shared paths and offline-safe placeholder assets."""

import shutil
from base64 import b64encode
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DEMO_DIR = ROOT / "docs" / "demo"
ASSETS_DIR = DOCS_DEMO_DIR / "assets"
OUTPUT_DIR = Path(__file__).parent / "presentations"


def output(filename: str, *, output_dir: Path = OUTPUT_DIR) -> Path:
    return output_dir / filename


def copy_assets(target_dir: Path) -> None:
    """Copy committed demo assets next to the exported deck when needed."""
    if not ASSETS_DIR.is_dir() or target_dir / "assets" == ASSETS_DIR:
        return
    dest = target_dir / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for path in ASSETS_DIR.iterdir():
        if not path.is_file():
            continue
        target = dest / path.name
        if target.exists():
            continue
        shutil.copy2(path, target)


def svg_image(label: str, *, fill: str = "#3d5a80") -> str:
    """Inline SVG data URI (works offline, no external requests)."""
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540">'
        f'<rect width="100%" height="100%" fill="{fill}"/>'
        f'<text x="50%" y="50%" fill="#ffffff" font-family="sans-serif" '
        f'font-size="36" text-anchor="middle" dominant-baseline="middle">'
        f"{label}</text></svg>"
    )
    encoded = b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{encoded}"
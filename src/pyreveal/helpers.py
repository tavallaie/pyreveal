from __future__ import annotations

import os
import shutil
from pathlib import Path

from .background import ImageBackground, VideoBackground
from .element import ImageElement, VideoElement


def is_remote_asset(path: str) -> bool:
    """Return True when *path* should not be copied to the output folder."""
    return path.startswith(("http://", "https://", "data:"))


def is_local_file(path: str) -> bool:
    return not is_remote_asset(path) and Path(path).is_file()


def validate_color(color: str) -> str:
    if not color.startswith("#") or len(color) not in (4, 7):
        raise ValueError(f"Invalid color format: {color}")
    return color


def validate_opacity(opacity: float) -> float:
    if not 0.0 <= opacity <= 1.0:
        raise ValueError(
            f"Invalid opacity value: {opacity}. It should be between 0.0 and 1.0."
        )
    return opacity


def copy_asset(path: str, assets_dir: Path, presentations_dir: Path) -> str:
    """Copy a local asset into *assets_dir* and return a relative path."""
    if is_remote_asset(path) or not Path(path).is_file():
        return path
    new_path = shutil.copy(path, assets_dir)
    return os.path.relpath(new_path, presentations_dir)


def copy_element_assets(element, assets_dir, presentations_dir):
    if isinstance(element, ImageElement):
        element.content = copy_asset(element.content, assets_dir, presentations_dir)
    elif isinstance(element, VideoElement):
        element.content = copy_asset(element.content, assets_dir, presentations_dir)

    for child in element.children:
        copy_element_assets(child, assets_dir, presentations_dir)


def copy_assets_for_slide(slide, assets_dir, presentations_dir):
    background = slide.background
    if background and isinstance(background, ImageBackground):
        slide.background.image_url = copy_asset(
            background.image_url, assets_dir, presentations_dir
        )
    elif background and isinstance(background, VideoBackground):
        slide.background.video_urls = [
            copy_asset(url, assets_dir, presentations_dir)
            for url in background.video_urls
        ]
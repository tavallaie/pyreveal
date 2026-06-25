import os
import shutil

from .background import ImageBackground, VideoBackground
from .element import ImageElement, VideoElement


def validate_color(color):
    if not color.startswith("#") or len(color) not in [4, 7]:
        raise ValueError(f"Invalid color format: {color}")
    return color


def validate_url(url):
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL format: {url}")
    return url


def validate_percentage(value):
    if not value.endswith("%"):
        raise ValueError(f"Invalid percentage format: {value}")
    return value


def validate_opacity(opacity):
    if not 0.0 <= opacity <= 1.0:
        raise ValueError(
            f"Invalid opacity value: {opacity}. It should be between 0.0 and 1.0."
        )
    return opacity


class CSSProperties:
    @staticmethod
    def position(value):
        valid_positions = ["top", "bottom", "left", "right", "center"]
        if value not in valid_positions:
            raise ValueError(
                f"Invalid position value: {value}. Valid values are: {', '.join(valid_positions)}"
            )
        return value

    @staticmethod
    def size(value):
        if not value.endswith(("px", "%", "em", "rem", "vw", "vh")):
            raise ValueError(f"Invalid size format: {value}")
        return value

    @staticmethod
    def repeat(value):
        valid_repeats = ["repeat", "repeat-x", "repeat-y", "no-repeat"]
        if value not in valid_repeats:
            raise ValueError(
                f"Invalid repeat value: {value}. Valid values are: {', '.join(valid_repeats)}"
            )
        return value


def copy_element_assets(element, assets_dir, presentations_dir):
    if isinstance(element, ImageElement):
        new_image_path = shutil.copy(element.content, assets_dir)
        element.content = os.path.relpath(new_image_path, presentations_dir)
    elif isinstance(element, VideoElement):
        new_video_path = shutil.copy(element.content, assets_dir)
        element.content = os.path.relpath(new_video_path, presentations_dir)

    for child in element.children:
        copy_element_assets(child, assets_dir, presentations_dir)


def copy_assets_for_slide(slide, assets_dir, presentations_dir):
    background = slide.background
    if background and isinstance(background, ImageBackground):
        new_image_path = shutil.copy(background.image_url, assets_dir)
        slide.background.image_url = os.path.relpath(new_image_path, presentations_dir)
    elif background and isinstance(background, VideoBackground):
        new_video_path = shutil.copy(background.video_url, assets_dir)
        slide.background.video_url = os.path.relpath(new_video_path, presentations_dir)
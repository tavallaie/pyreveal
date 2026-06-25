from __future__ import annotations

from html import escape

from .exceptions import InvalidBackgroundTypeError


class Background:
    """Base class for reveal.js slide backgrounds."""

    def __init__(
        self,
        *,
        opacity: float | None = None,
        position: str | None = None,
        repeat: str | None = None,
        transition: str | None = None,
        parallax: str | None = None,
    ):
        self.opacity = opacity
        self.position = position
        self.repeat = repeat
        self.transition = transition
        self.parallax = parallax

    def _common_attributes(self) -> str:
        attrs: list[str] = []
        if self.opacity is not None:
            attrs.append(f'data-background-opacity="{self.opacity}"')
        if self.position:
            attrs.append(f'data-background-position="{escape(self.position)}"')
        if self.repeat:
            attrs.append(f'data-background-repeat="{escape(self.repeat)}"')
        if self.transition:
            attrs.append(f'data-background-transition="{escape(self.transition)}"')
        if self.parallax:
            attrs.append(f'data-background-parallax="{escape(self.parallax)}"')
        return (" " + " ".join(attrs)) if attrs else ""

    def generate_html(self) -> str:
        raise NotImplementedError


class ColorBackground(Background):
    def __init__(self, color: str, **kwargs):
        super().__init__(**kwargs)
        self.color = color

    def generate_html(self) -> str:
        return f' data-background-color="{escape(self.color)}"{self._common_attributes()}'


class ImageBackground(Background):
    def __init__(self, image_url: str, size: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.image_url = image_url
        self.size = size

    def generate_html(self) -> str:
        size_str = (
            f' data-background-size="{escape(self.size)}"' if self.size else ""
        )
        return (
            f' data-background="{escape(self.image_url)}"{size_str}'
            f"{self._common_attributes()}"
        )


class VideoBackground(Background):
    def __init__(self, video_url: str, **kwargs):
        super().__init__(**kwargs)
        self.video_url = video_url

    def generate_html(self) -> str:
        return (
            f' data-background-video="{escape(self.video_url)}"'
            f"{self._common_attributes()}"
        )


class IframeBackground(Background):
    def __init__(self, iframe_url: str, **kwargs):
        super().__init__(**kwargs)
        self.iframe_url = iframe_url

    def generate_html(self) -> str:
        return (
            f' data-background-iframe="{escape(self.iframe_url)}"'
            f"{self._common_attributes()}"
        )


class BackgroundFactory:
    @staticmethod
    def create_background(bg_type: str, value: str, **kwargs) -> Background:
        if bg_type == "color":
            return ColorBackground(value, **kwargs)
        if bg_type == "image":
            return ImageBackground(value, **kwargs)
        if bg_type == "video":
            return VideoBackground(value, **kwargs)
        if bg_type == "iframe":
            return IframeBackground(value, **kwargs)
        raise InvalidBackgroundTypeError(bg_type)
from __future__ import annotations

from html import escape

from .choices import BackgroundType, coerce_background_type
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
        color: str | None = None,
    ):
        self.opacity = opacity
        self.position = position
        self.repeat = repeat
        self.transition = transition
        self.parallax = parallax
        self.color = color

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
        if self.color:
            attrs.append(f'data-background-color="{escape(self.color)}"')
        return (" " + " ".join(attrs)) if attrs else ""


class ColorBackground(Background):
    def __init__(self, color: str, **kwargs):
        super().__init__(**kwargs)
        self._bg_color = color

    def generate_html(self) -> str:
        return (
            f' data-background-color="{escape(self._bg_color)}"'
            f"{self._common_attributes()}"
        )


class GradientBackground(Background):
    def __init__(self, gradient: str, **kwargs):
        super().__init__(**kwargs)
        self.gradient = gradient

    def generate_html(self) -> str:
        return (
            f' data-background-gradient="{escape(self.gradient)}"'
            f"{self._common_attributes()}"
        )


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
    def __init__(
        self,
        video_url: str | list[str] | None = None,
        *,
        sources: list[str] | None = None,
        preload: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        urls = sources or ([video_url] if isinstance(video_url, str) else video_url)
        if not urls:
            raise ValueError("VideoBackground requires at least one video URL.")
        self.video_urls = urls
        self.preload = preload

    @property
    def video_url(self) -> str:
        return ",".join(self.video_urls)

    def generate_html(self) -> str:
        preload_attr = " data-preload" if self.preload else ""
        return (
            f' data-background-video="{escape(self.video_url)}"'
            f"{preload_attr}{self._common_attributes()}"
        )


class IframeBackground(Background):
    def __init__(
        self,
        iframe_url: str,
        *,
        interactive: bool = False,
        preload: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.iframe_url = iframe_url
        self.interactive = interactive
        self.preload = preload

    def generate_html(self) -> str:
        interactive_attr = (
            " data-background-interactive" if self.interactive else ""
        )
        preload_attr = " data-preload" if self.preload else ""
        return (
            f' data-background-iframe="{escape(self.iframe_url)}"'
            f"{interactive_attr}{preload_attr}{self._common_attributes()}"
        )


class BackgroundFactory:
    @staticmethod
    def create_background(
        bg_type: BackgroundType | str, value: str, **kwargs
    ) -> Background:
        try:
            kind = coerce_background_type(bg_type)
        except ValueError as exc:
            raise InvalidBackgroundTypeError(bg_type) from exc
        if kind == BackgroundType.COLOR.value:
            return ColorBackground(value, **kwargs)
        if kind == BackgroundType.GRADIENT.value:
            return GradientBackground(value, **kwargs)
        if kind == BackgroundType.IMAGE.value:
            return ImageBackground(value, **kwargs)
        if kind == BackgroundType.VIDEO.value:
            return VideoBackground(value, **kwargs)
        if kind == BackgroundType.IFRAME.value:
            return IframeBackground(value, **kwargs)
        raise InvalidBackgroundTypeError(bg_type)
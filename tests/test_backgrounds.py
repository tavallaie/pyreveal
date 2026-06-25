import pytest

from pyreveal import (
    BackgroundFactory,
    ColorBackground,
    IframeBackground,
    ImageBackground,
    VideoBackground,
)
from pyreveal.exceptions import InvalidBackgroundTypeError


def test_color_background_with_opacity():
    bg = ColorBackground("#112233", opacity=0.5)
    html = bg.generate_html()
    assert 'data-background-color="#112233"' in html
    assert 'data-background-opacity="0.5"' in html


def test_image_background_with_position_and_size():
    bg = ImageBackground("bg.jpg", size="cover", position="center")
    html = bg.generate_html()
    assert 'data-background="bg.jpg"' in html
    assert 'data-background-size="cover"' in html
    assert 'data-background-position="center"' in html


def test_video_background():
    bg = VideoBackground("loop.mp4", repeat="no-repeat")
    html = bg.generate_html()
    assert 'data-background-video="loop.mp4"' in html
    assert 'data-background-repeat="no-repeat"' in html


def test_iframe_background():
    bg = IframeBackground("https://example.com")
    assert 'data-background-iframe="https://example.com"' in bg.generate_html()


def test_background_factory_iframe():
    bg = BackgroundFactory.create_background("iframe", "https://example.com")
    assert isinstance(bg, IframeBackground)


def test_background_factory_invalid_type():
    with pytest.raises(InvalidBackgroundTypeError):
        BackgroundFactory.create_background("gradient", "#fff")
from .style import Style


class Element:
    def __init__(
        self, tag="div", content=None, style=None, data_id=None, attributes=None
    ):
        self.tag = tag
        self.content = content or ""
        self.attributes = attributes or {}
        self.style = style or Style()
        self.data_id = data_id
        self.children = []  # List to hold child elements

    def add_child(self, child_element):
        """Add a child element to this element."""
        if not isinstance(child_element, Element):
            raise ValueError("Child element must be an instance of Element.")
        self.children.append(child_element)

    def generate_html(self):
        style_str = f' style="{self.style.generate_css()}"' if self.style else ""
        attributes_str = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        children_html = "".join([child.generate_html() for child in self.children])

        return f"<{self.tag} {attributes_str}{style_str}>{self.content}{children_html}</{self.tag}>"

    def set_data_id(self, data_id):
        """
        Set the data-id attribute for the element.
        """
        self.data_id = data_id

    def get_data_id(self):
        """
        Get the data-id attribute of the element.
        """
        return self.data_id


class ImageElement(Element):
    def __init__(self, image_url, alt_text="", **kwargs):
        super().__init__(content=image_url, tag="img", **kwargs)
        self.alt_text = alt_text

    def generate_html(self):
        css_string = self.style.generate_css()
        children_html = "".join([child.generate_html() for child in self.children])
        return f'<img src="{self.content}" alt="{self.alt_text}" style="{css_string}" data-id="{self.data_id}">{children_html}</img>'


class VideoElement(Element):
    def __init__(self, video_url, **kwargs):
        super().__init__(content=video_url, **kwargs)

    def generate_html(self):
        css_string = self.style.generate_css()
        children_html = "".join([child.generate_html() for child in self.children])
        return f'<video src="{self.content}" style="{css_string}" data-id="{self.data_id}">{children_html}</video>'

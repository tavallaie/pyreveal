class Slide:
    def __init__(self, content=None, title=None, background=None):
        self.content = content or ""
        self.title = title
        self.background = background
        self.elements = []
        self.vertical_slides = []

    def add_element(self, element):
        self.elements.append(element)

    def add_vertical_slide(self, slide):
        if isinstance(slide, Slide):
            self.vertical_slides.append(slide)
        else:
            raise ValueError("Invalid slide type. Expected an instance of Slide.")

    def set_background(self, background):
        self.background = background

    def generate_html(self):
        background_html = self.background.generate_html() if self.background else ""
        elements_html = "".join(element.generate_html() for element in self.elements)
        return f"<section{background_html}>{self.content}{elements_html}</section>"

    def render(self):
        return self.generate_html()
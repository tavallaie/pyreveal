class Slide:
    def __init__(self, content=None, title=None, background=None):
        self.content = content or ""
        self.title = title
        self.background = background  # This can be an instance of the Background class
        self.elements = (
            []
        )  # List to store additional elements like images, videos, etc.

    def add_element(self, element):
        """
        Add an element (like an image, video, etc.) to the slide.
        For backward compatibility, we'll ensure that any new attributes or methods we add won't interfere with this basic structure.
        """
        self.elements.append(element)

    def add_vertical_slide(self, slide):
        if isinstance(slide, Slide):
            self.vertical_slides.append(slide)
        else:
            raise ValueError("Invalid slide type. Expected an instance of Slide.")

    def set_background(self, background):
        """
        Set the background for the slide.
        """
        self.background = background

    def generate_html(self):
        """
        Generate the HTML representation of the slide.
        """
        background_html = ""
        if self.background:
            background_html = self.background.generate_html()

        elements_html = "".join([element.generate_html() for element in self.elements])
        slide_html = f"<section{background_html}>{elements_html}</section>"

        return slide_html

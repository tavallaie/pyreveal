# example/basic_usage.py
import sys

sys.path.insert(0, "/home/labmanager/Documents/Project/pyreveal")
from pyreveal import PyReveal


def create_presentation():
    # Create a new presentation
    presentation = PyReveal(title="My Presentation", theme="sky", transition="fade")

    # Add slides to the presentation
    presentation.add_slide(content="Welcome to my presentation!")
    presentation.add_slide(content="Here's the second slide.", title="Slide 2")
    presentation.add_slide(content="And this is the third slide.", title="Slide 3")

    # Change the theme or transition if needed
    presentation.set_theme("night")
    presentation.set_transition("slide")

    # Generate the HTML representation (for preview or further processing)
    html_content = presentation.generate_html()
    print(html_content)  # This will print the generated HTML to the console

    # Save the presentation to an HTML file
    presentation.save_to_file(filename="my_presentation.html")

    print(
        "Presentation saved to 'my_presentation.html'. Open this file in a web browser to view the presentation."
    )


if __name__ == "__main__":
    create_presentation()

# example/basic_usage.py
import sys

sys.path.insert(0, "/home/labmanager/Documents/Project/pyreveal")
from pyreveal import PyReveal

# Initialize the PyReveal class
presentation = PyReveal(title="My Presentation", theme="black", transition="slide")

# Add horizontal slides
presentation.add_slide(content="Welcome to My Presentation!", title="Intro")
presentation.add_slide(content="This is a horizontal slide.", title="HorizontalSlide")

# Add vertical slides under the "Intro" slide
presentation.add_slide(content="This is the first vertical slide.", group="Intro")
presentation.add_slide(content="This is the second vertical slide.", group="Intro")

# Generate the presentation HTML
html_content = presentation.generate_html()

# Save the presentation to a file
presentation.save_to_file(filename="my_presentation.html")

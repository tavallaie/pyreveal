from pyreveal import PyReveal

presentation = PyReveal(title="My Presentation", theme="black", transition="slide")

presentation.add_slide(content="Welcome to My Presentation!", title="Intro")
presentation.add_slide(content="This is a horizontal slide.", title="HorizontalSlide")

presentation.add_slide(content="This is the first vertical slide.", group="Intro")
presentation.add_slide(content="This is the second vertical slide.", group="Intro")

html_content = presentation.generate_html()
print(html_content[:200], "...")

presentation.save_to_file(filename="my_presentation.html")
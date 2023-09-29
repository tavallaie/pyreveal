================
PyReveal Library
================

PyReveal is a Python library that allows users to generate Reveal.js presentations programmatically. With PyReveal, you can easily create slides, set themes, transitions, and even add custom backgrounds like images or videos.

Features
========

- Create Reveal.js presentations using Python.
- Support for slide themes and transitions.
- Error handling and validation for slide content.
- Export presentations to HTML.
- Support for slide backgrounds, including images, videos, and colors.
- Parallax background support.

Installation
============

.. code-block:: bash

   pip install pyreveal

Usage
=====

.. code-block:: python

   from pyreveal import PyReveal, ImageBackground

   presentation = PyReveal(title="My Presentation", theme="white", transition="slide")
   presentation.add_slide("Welcome to PyReveal!")
   bg_image = ImageBackground(image_url="path/to/image.jpg")
   presentation.add_slide("This slide has a background image!", background=bg_image)
   presentation.save_to_file("my_presentation.html")

For more advanced usage and features, please refer to the documentation.

Contribute
==========

- Issue Tracker: `https://github.com/tavallaie/pyreveal/issues`
- Source Code: `https://github.com/tavallaie/pyreveal`

Support
=======

If you are having issues, please let us know. You can report issues on the issue tracker mentioned above.


License
=======

The project is licensed under the MIT license. See the `LICENSE`_ file for more details.

.. _LICENSE: ./LICENSE

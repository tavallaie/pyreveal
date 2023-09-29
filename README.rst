======================
pyreveal
======================

A Python library designed to simplify the creation of presentations using Reveal.js.

Overview
========

With an intuitive Pythonic interface, users can effortlessly generate dynamic and interactive web-based presentations without delving into the intricacies of HTML or JavaScript.

Key Features
------------

- **Pythonic Interface**: Create slides, set themes, and define transitions all through a clean and straightforward Python API.
- **Customizable**: Choose from a variety of themes and transitions to make your presentation stand out.
- **Export to PDF**: Easily export your presentation to a PDF format for offline viewing or sharing.
- **Error Handling**: Built-in validation ensures that your presentation looks and functions as expected.
- **No Web Development Required**: While `pyreveal` leverages the power of Reveal.js, users don't need any prior web development experience.

Installation
============

To install `pyreveal`, use pip:

.. code-block:: bash

   pip install pyreveal

Usage
=====

.. code-block:: python

   from pyreveal import PyReveal

   presentation = PyReveal()
   # ... your code to create slides ...

   presentation.show()

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

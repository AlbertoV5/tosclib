Welcome to tosclib!
===================================

Generate and edit Touch OSC templates with XML trees through a few custom classes and functions that help navigate the structure of the .tosc file.

For more go to the `TouchOSC control reference. <https://hexler.net/touchosc/manual/controls>`_

And more details on the `TouchOSC scripting reference. <https://hexler.net/touchosc/manual/script>`_

.. attention::

   **Disclaimer**: This project has no relation to Hexler, the developer of TouchOSC. Backup your templates before editing them with third party tools.


.. _installation:

Installation
------------------

.. code-block:: console

   $ pip install tosclib


Changelog
------------------

- 0.3.5
   - Moved to python 3.10 only for now. 
   - Added mypy support.
   - Improved code structure.
   - Added numpad demo.
   - Polished layouts.

- 0.3.0
   - Final code refactoring for the library's structure.
   - The abstraction flows like this:
      - elements -> controls -> tosc -> layout
   - Added layout decorators and a few other features
   - Changed setFrame and setColor to receive a tuple instead of args
   - Improved code and flow for Enums and ElementTOSC

- 0.2.5
   - Improved code in general and added a lot of general use functions.
   - Tested with possible lxml support.

- 0.2.0
   - Added multiple enumerations that mirror Hexlers'

- 0.1.10
   - Tested on python 3.8, 3.9, 3.10.
   - Probably last refactoring for a while.
   - General design is set, still lacks features.
   - Need to add MIDI, LOCAL, GAMEPAD messages.
   - Need to add more enums for default values.
   - Need to add test cases and shortcuts.

Contents
--------

.. toctree::
   
   guide
   demos
   api
   
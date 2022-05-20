Usage
=====

.. _installation:

Installation
------------

Install it using pip:

.. code-block:: console

   (.venv) $ pip install tosclib

Loading a .tosc file
------------------------

To load a .tosc file you can use the ``tosclib.tosc.load()`` function:

.. autofunction:: tosclib.tosc.load()

For example:

>>> from tosclib import tosc
>>> tosc.load("stuff/test.tosc")


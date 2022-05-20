Usage
=====

.. _installation:

Installation
------------

Install it using pip:

.. code-block:: console

   (.venv) $ pip install tosclib

Creating a script
----------------

To load a .tosc file you can use the ``tosclib.tosc.load()`` function:

.. autofunction:: tosclib.tosc.load()

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
will raise an exception.

.. autoexception:: lumache.InvalidKindError

For example:

>>> from tosclib import tosc
>>> tosc.load("stuff/test.tosc")
['shells', 'gorgonzola', 'parsley']


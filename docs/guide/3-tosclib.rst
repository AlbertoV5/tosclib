Using tosclib
====================

.. _installation:

Installation
------------------

Requires python >= 3.9

.. code-block:: console

   $ pip install tosclib

Guide
---------------

Tosclib tries to simplify editing and generating .tosc files.

Once you learn the structure of the .tosc file and the structure of tosclib, it becomes easier to focus on the algorithm of whatever you want to do rather than dealing with XML Element Trees that try to find a needle in a haystack in an inefficient way.

For example, changing the colors of a specific Node Element:

.. code-block::
   
   import tosclib as tosc
   
   root = tosc.load("demos/files/test.tosc")
   parent = tosc.ElementTOSC(root[0])
   target = tosc.ElementTOSC(parent.findChild("target"))
   target.showProperty("color")

.. code-block::

   colors = {"r":"0", "g":"0", "b":"1", "a":"1"}
   target.setPropertyValue("color", params = colors)
   target.showProperty("color")

.. code-block::

   tosc.write(root, "demos/files/out.tosc")

Working with .tosc files
-----------------------------

Load a .tosc file directly into a root Element and handle it with **tosclib** or **xml**.

.. autofunction:: tosclib.tosc.load

Then pass the parent Node to the ElementTOSC class to get its SubElements.

.. autoclass:: tosclib.tosc.ElementTOSC

.. autoclass:: tosclib.tosc.SubElements
   :members:
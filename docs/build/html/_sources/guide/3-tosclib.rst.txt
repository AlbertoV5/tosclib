Working with .tosc files
=================================

Once you have learned the structure of the .tosc file and tosclib, it becomes easier to focus on the algorithm of whatever you want to do rather than dealing with raw XML Element Tree functions and parsing.

The basic concept is to load a regular XML Element and create a new ElementTOSC instance with it. Then you can handle it with **tosclib** and regular **xml**.

.. code-block::
   :caption: We can start by loading a root Element and passing it's first child to ElementTOSC.

   import tosclib as tosc
   
   root = tosc.load("demos/files/test.tosc")
   parent = tosc.ElementTOSC(root[0])

.. code-block::
   :caption: Then we can use ElementTOSC methods to find navigate through the tree.

   target = tosc.ElementTOSC(parent.findChild("target"))
   target.showProperty("color")

.. code-block::
   :caption: Finally we can modify the Elements, for example changing the 'color' Property.
   
   colors = {"r":"0", "g":"0", "b":"1", "a":"1"}
   target.setPropertyValue("color", params = colors)

.. code-block::
   :caption: Alternatively, we can use a shortcut instead to set the color property directly:
   
   target.setColor(1, 0, 0, 1)
   target.showProperty("color")

.. code-block::
   :caption: In order to write back to .tosc, we use the original root Element with the tosclib write function.
   
   tosc.write(root, "demos/files/out.tosc")


Classes and Functions
-----------------------------

Here are more details on the functions and methods we used:

.. autofunction:: tosclib.tosc.load

.. autoclass:: tosclib.tosc.ElementTOSC

.. autofunction:: tosclib.tosc.ElementTOSC.setPropertyValue

.. autofunction:: tosclib.tosc.ElementTOSC.setColor

.. autofunction:: tosclib.tosc.write
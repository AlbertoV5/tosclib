Valid Elements
=================================

Touch OSC allows you to add any new Property to a .tosc file. It doesn't allow adding new Values or Sub Element categories. This means that you can't add a :guilabel:`<Style>` Element under :guilabel:`<Node>` but you can add a :guilabel:`<Property><key>Style` Element under :guilabel:`<Properties>`.

You can't add new functions to the script Property either, as Touch OSC only allows `these functions. <https://hexler.net/touchosc/manual/script-objects-control#functions>`_

You can always add new messages as long as they belong to OSC, MIDI, LOCAL, `etc <https://hexler.net/touchosc/manual/script-functions-global#message>`_.

**Example:**
   
Creating a new Property directly in the parent Node.

.. code-block::

   import tosclib as tosc

   root = tosc.load("demos/files/test.tosc")
   parent = tosc.ElementTOSC(root[0])

   parent.createProperty("s", "CustomProperty", "1007")

   print("Added Property:\n")
   parent.showProperty("CustomProperty")
   
   tosc.write(root, "demos/files/out.tosc")


Adding a Child Node and then adding a Property to the empty Child.

.. code-block::

   box = tosc.ElementTOSC(parent.createNode("BOX"))

   box.createProperty("c", "color", "", {
                        "r" : str(1),
                        "g" : str(1),
                        "b" : str(0),
                        "a" : "1"
                     })

   print(box.__dict__)


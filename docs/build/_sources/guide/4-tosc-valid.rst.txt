Valid Elements
=================================

Touch OSC allows you to add any new Property to a .tosc file. It doesn't allow adding new Values or Sub Element categories. This means that you can't add a :guilabel:`<Style>` Element under :guilabel:`<Node>` but you can add a :guilabel:`<Property><key>Style` Element under :guilabel:`<Properties>`.

You can't add new 'functions' to the 'script' Property either, as Touch OSC only allows `these functions. <https://hexler.net/touchosc/manual/script-objects-control#functions>`_

You can always add new messages as long as they belong to OSC, MIDI, LOCAL, `etc <https://hexler.net/touchosc/manual/script-functions-global#message>`_.

**Example for creating custom properties:**
   
.. code-block::
   :caption: Creating a new Property directly in the parent Node.

   import tosclib as tosc

   root = tosc.load("docs/demos/files/test.tosc")
   parent = tosc.ElementTOSC(root[0])

   parent.createProperty(tosc.Property("s", "CustomProperty", "1007"))
   
   tosc.write(root, "docs/demos/files/out.tosc")

You can then access the property from .lua inside the TouchOSC Editor.

.. code-block:: lua
   :caption: Lua code in the editor.

    function init()
        self.values.text = self.parent.CustomProperty
    end

Adding a non-valid Element would look like this:

.. code-block::
   :caption: Trying to add a <styles> sub element to <node>

   import xml.etree.ElementTree as ET
   import tosclib as tosc

   root = tosc.load("docs/demos/files/test.tosc")
   node = tosc.ElementTOSC(root[0])

   styles = ET.SubElement(node, "styles")
   styles.text = "CustomProperty"

   tosc.write(root, "docs/demos/files/out.tosc")

Touch OSC won't accept the new Sub Element when loading the template in the Editor. 

You could add a <property> under <properties> manually too.

.. code-block:: python
   :caption: Using ET to add a <property>

   import xml.etree.ElementTree as ET
   import tosclib as tosc

   root = tosc.load("docs/demos/files/test.tosc")
   
   properties = root[0].find("properties")
   prop = ET.SubElement(properties, "property")
   key = ET.SubElement(prop, "key")
   key.text = "CustomProperty"
   value = ET.SubElement(prop, "value")
   value.text = "1007"

   tosc.write(root, "docs/demos/files/out.tosc")

Or just use tosclib instead.
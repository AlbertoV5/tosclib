Custom Property
-------------------

Add a new custom Property to the parent Node.

.. literalinclude:: 1-custom-property.py
    :language: python


Then you can access that Property in Touch OSC Editor with .lua like this:

.. code-block:: lua
    
    --This is lua code inside the touch osc editor--
    function onValueChanged(key, value)
        if key == "touch" and self.values.touch == true then
            print(self.parent.CustomProperty)
            self.parent.CustomProperty = self.parent.children.label2.values.text
        end
    end

**Demo Files:**

- `Input .tosc <https://github.com/AlbertoV5/tosclib/blob/main/demos/files/test2.tosc>`_
- `Output .tosc <https://github.com/AlbertoV5/tosclib/blob/main/demos/files/customProp.tosc>`_


**GIFS**

1. Call script that changes the Custom Property, then call another one that sets the label text to the Custom Property.

.. image:: ../images/tosclib-property1.GIF

2. Save and close the template. Then load it again and you'll see the label text remains, as it sets its value to the Custom Property on init.

.. image:: ../images/tosclib-property2.GIF


.. code-block:: lua
    :caption: This is the lua code in the label

    function init()
        self.parent.children.label3.values.text = self.parent.CustomProperty
    end

    function onValueChanged(key, value)
        if key == "touch" and self.values.touch == true then
            print(self.parent.CustomProperty)
            self.parent.children.label3.values.text = self.parent.CustomProperty
        end
    end
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
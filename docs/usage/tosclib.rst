Using tosclib
====================

.. _installation:

Installation
------------------

Requires python >= 3.9

.. code-block:: console

   $ conda activate py39
   $ pip install tosclib

Usage
---------------

Example, changing the colors of a Node Element:

.. code-block:: console

   $ python

>>> import tosclib as tosc
>>> root = tosc.load("demos/files/test.tosc")
>>> e = tosc.e(root[0])
>>> t = tosc.e(e.findChild("target"))
>>> t.showProperty("color")
<property type="c">
  <key>color</key>
  <value>
    <r>0.25</r>
    <g>0.25</g>
    <b>0.25</b>
    <a>1</a>
  </value>
</property>
>>> colors = {"r":"0", "g":"0", "b":"1", "a":"1"}
>>> t.setPropertyValue("color", params = colors)
True
>>> t.showProperty("color")
<property type="c">
  <key>color</key>
  <value>
    <r>0</r>
    <g>0</g>
    <b>1</b>
    <a>1</a>
  </value>
</property>
>>> tosc.write(root, "demos/files/out.tosc") 
True

Working with .tosc files
-----------------------------

Load a .tosc file directly into a root Element and handle it with **tosclib** or **xml**.

.. autofunction:: tosclib.tosc.load

Then pass the parent Node to the ElementTOSC class to get its SubElements.

.. autoclass:: tosclib.tosc.ElementTOSC

.. autoclass:: tosclib.SubElements
   :members:

**Example:**
   
.. code-block:: py
   :caption: Create a new Property

   import tosclib as tosc
   import argparse

   def addProperty(args):
      
      root = tosc.load(args.Input)
      parent = tosc.ElementTOSC(root[0])

      # Creating Property in parent Node
      parent.createProperty(
                              type = args.Type, 
                              key = args.Property, 
                              text = args.Value
                           )

      print("Added Property: ")
      parent.showProperty(args.Property)
      tosc.write(root, args.Output)


   if __name__ == "__main__":

      parser = argparse.ArgumentParser()
      parser.add_argument("-i", "--Input", help = ".tosc input file", required=True)
      parser.add_argument("-o", "--Output", help = ".tosc output file", required=True)
      parser.add_argument("-p", "--Property", help = "Name of the Property", required=True)
      parser.add_argument("-v", "--Value", help = "Contents of the Property", required=True)
      parser.add_argument("-t", "--Type", help = "Type of the property. Best is 's'.", choices = ['s', 'b', 'c', 'r'], required = True)

      args = parser.parse_args()

      addProperty(args)

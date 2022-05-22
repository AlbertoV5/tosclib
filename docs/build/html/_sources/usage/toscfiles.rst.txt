Understanding .tosc files
-----------------------------

Touch OSC uses zlib to compress XML tree files into .tosc.

The Touch OSC editor can access all the Elements and provides tools to edit them as well as an UI.
However, it only displays the Elements that its designed to handle.

This section will try to describe those Elements and how they are organized in the .tosc file.

Let's start with the XML header and the root:
    
.. code-block:: xml
   
   <?xml version='1.0' encoding='UTF-8'?>
   <lexml version='3'></lexml>

.. code-block:: console
   :caption: The root holds the parent Node, which in turn, holds a few key SubElements: 
   
   <root>
   |__<node>
      |__<properties>
      |  |__<property>
      |     |__<key>
      |     |  |__key.text
      |     |__<value>
      |        |__value.text
      |        |__<x>
      |           |__x.text
      |__<values>
      |__<children>
        |__<node>

The editor tree view only displays the Nodes in each Children SubElement.

.. figure:: ../images/toscTree.JPG

The rest of the Elements are displayed in the Control, Values, Messages and Script tabs.

.. figure:: ../images/toscOtherElements.JPG
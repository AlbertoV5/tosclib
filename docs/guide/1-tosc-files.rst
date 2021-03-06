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

.. code-block:: xml
   :caption: The root holds the parent Node, which in turn, holds a few key SubElements: 
   
   <root>
   |__<node>
      |__<properties>
      |  |__<property>
      |     |__<key>
      |     |  |__text
      |     |__<value>
      |        |__text
      |        |__<x>
      |           |__text
      |__<values>
      |  |__<value>
      |     |__<key>
      |     |  |__text
      |     |__<locked>
      |     |  |__text
      |     |__<lockedDefaultCurrent>
      |     |  |__text
      |     |__<default>
      |     |  |__text
      |     |__<defaultPull>
      |        |__text
      |__<messages>
      |  |__<osc>
      |  |__<midi>
      |  |__<local>
      |__<children>
        |__<node>



The editor tree view only displays the Nodes in each Children SubElement.

.. figure:: ../images/toscTree.JPG

The rest of the Elements are displayed in the Control, Values, Messages and Script tabs.

.. figure:: ../images/toscOtherElements.JPG

`Here <https://hexler.net/touchosc/manual/script-properties-and-values>`_ is a list of the available Properties and Values.
Understanding .tosc files
-----------------------------

The files are formatted as XML trees with the declaration:

.. code-block:: xml
   
   <?xml version='1.0' encoding='UTF-8'?>

And the root:

.. code-block:: xml

   <lexml version='3'>

After the root, the main element is the node, which has this basic structure:

.. code-block:: console

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
   
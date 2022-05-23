Message Elements
-----------------------------

We are going to take a closer look to how each message type is constructed:

**Editor view:**

.. figure:: ../images/msg1.JPG


**OSC Messages:**

.. code-block:: xml
   
   <node>
      |__<messages>
      |  |__<osc>
      |  |  |__<enabled>
      |  |  |  |__text
      |  |  |__<send>
      |  |  |  |__text
      |  |  |__<receive>
      |  |  |  |__text
      |  |  |__<feedback>
      |  |  |  |__text
      |  |  |__<connections>
      |  |  |  |__text
      |  |  |__<triggers>
      |  |  |  |__<trigger>
      |  |  |     |__<var>
      |  |  |     |  |__text
      |  |  |     |__<condition>
      |  |  |        |__text
      |  |  |__<path>
      |  |  |  |__<partial>
      |  |  |  |  |__<type>
      |  |  |  |  |  |__text
      |  |  |  |  |__<conversion>
      |  |  |  |  |  |__text
      |  |  |  |  |__<value>
      |  |  |  |  |  |__text
      |  |  |  |  |__<scaleMin>
      |  |  |  |  |  |__text
      |  |  |  |  |__<scaleMax>
      |  |  |  |  |  |__text
      |  |  |  |__<partial>
      |  |  |__<arguments>
      |  |  |  |__<partial>
      |  |  |  |  |__<type>
      |  |  |  |  |  |__text
      |  |  |  |  |__<conversion>
      |  |  |  |  |  |__text
      |  |  |  |  |__<value>
      |  |  |  |  |  |__text
      |  |  |  |  |__<scaleMin>
      |  |  |  |  |  |__text
      |  |  |  |  |__<scaleMax>
      |  |  |  |  |  |__text
      |  |  |  |__<partial>
      |  |  |  |  |__etc etc
      |__<children>
         |__<node>

**LOCAL messages:**

.. code-block:: xml

   <node>
      |__<messages>
      |  |__<local>
      |  |  |__<enabled>
      |  |  |  |__text
      |  |  |__<triggers>
      |  |  |  |__<trigger>
      |  |  |     |__<var>
      |  |  |     |  |__text
      |  |  |     |__<condition>
      |  |  |        |__text
      |  |  |__<type>
      |  |  |  |__text
      |  |  |__<conversion>
      |  |  |  |__text
      |  |  |__<value>
      |  |  |  |__text
      |  |  |__<scaleMin>
      |  |  |  |__text
      |  |  |__<scaleMax>
      |  |  |  |__text
      |  |  |__<dstType>
      |  |  |  |__text
      |  |  |__<dstVar>
      |  |  |  |__text
      |  |  |__<dstID>
      |  |  |  |__text
      |__<children>
         |__<node>


Work in progress. 

There are different valid values per Element that have to be added to the diagrams.

The MIDI messages have to be added too.

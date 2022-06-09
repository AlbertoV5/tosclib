OSC Message Elements
=================================

In order to create a correct OSC message, we will use a few classes that set the specific Sub Elements of the <osc> Element.

We can create a message from ElementTOSC with:

.. automethod:: tosclib.tosc.ElementTOSC.createOSC

Then we can construct a custom osc message with the help of these classes:

.. autoclass:: tosclib.tosc.OSC

.. autoclass:: tosclib.tosc.Trigger

.. autoclass:: tosclib.tosc.Partial


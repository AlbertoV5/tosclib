Types
============

We are using the following type classes for validation:

1. `Literals: <https://docs.python.org/3/library/typing.html#typing.Literal>`_
    - Used for constants and tuples of constants.
2. `TypeAlias: <https://docs.python.org/3/library/typing.html#typing.TypeAlias>`_
    - Used for reducing multiple types to a single variable.


.. note:: 
    
    For more information on where are these types used, go to the source or the `API <./api.html>`_


.. rubric:: Control Attributes

.. autoclass:: tosclib.PropertyType
.. autoclass:: tosclib.PropertyValue
.. autoclass:: tosclib.ValueKey
.. autoclass:: tosclib.ValueDefault
.. autoclass:: tosclib.Condition
.. autoclass:: tosclib.SourceType
.. autoclass:: tosclib.Conversion
.. autoclass:: tosclib.MidiType
.. autoclass:: tosclib.ControlType

Type Hints
============

This library uses 4 categories of aliasing and hinting:

1. `Literals: <https://docs.python.org/3/library/typing.html#typing.Literal>`_
    - Used for hinting constants and tuples of constants.
2. `TypeAlias: <https://docs.python.org/3/library/typing.html#typing.TypeAlias>`_
    - Used for hinting tuples of types.


.. note:: 
    
    Because of how __annotations__ and __docs__ work, Sphinx has a hard time dealing with type aliases.
    As a result, the original docstrings reference TypeAlias, NewType, Literals docstrings. So I removed them.
    For more information on these types, go to the source or the `API <./api.html>`_


.. automodule:: tosclib

    .. rubric:: Attributes of Control (Not Classes)

    .. autoclass:: PropertyType
    .. autoclass:: PropertyValue
    .. autoclass:: ValueKey
    .. autoclass:: ValueDefault
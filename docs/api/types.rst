Type Hints
============

This library uses 4 categories of aliasing and hinting:

1. `Literals: <https://docs.python.org/3/library/typing.html#typing.Literal>`_
    - Used for hinting constants and tuples of constants.
2. `TypeAlias: <https://docs.python.org/3/library/typing.html#typing.TypeAlias>`_
    - Used for hinting tuples of types.
3. `NewType: <https://docs.python.org/3/library/typing.html#typing.NewType>`_
    - Used for more complex tuples of tuples of types.
4. `Protocol: <https://docs.python.org/3/library/typing.html#typing.Protocol>`_
    - Used for hinting classes that share the same structure.


.. note:: 
    
    Because of how __annotations__ and __docs__ work, Sphinx has a hard time dealing with type aliases.
    As a result, the original docstrings reference TypeAlias, NewType, Literals docstrings. So I removed them.
    For more information on these types, go to the source or the `API <./api.html>`_


.. automodule:: tosclib.core

    .. rubric:: Highest Level (Class)

    .. autoclass:: Control
        
        .. automethod:: Control.get
        .. automethod:: Control.set
        .. automethod:: Control.get_frame
        .. automethod:: Control.get_color
        .. automethod:: Control.set_frame
        .. automethod:: Control.set_color

    .. rubric:: Attributes of Control (Not Classes)

    .. autoclass:: Property
    .. autoclass:: Value
    .. autoclass:: Message

    .. rubric:: Constant Literal Types (Not Classes)

    .. class:: PropertyType
    .. class:: ValueKey
    .. class:: TriggerType
    .. class:: PartialType
    .. class:: ConversionType
    .. class:: MidiMsgType
    .. class:: ControlType
    
    .. rubric:: Intermediary Types (Not Classes)

    .. class:: PropertyValue
    .. class:: ValueDefault
    .. class:: Partial
    .. class:: Trigger
    .. class:: MidiMsg
    .. class:: MidiValue
    .. class:: MsgConfig
    .. class:: LocalSrc
    .. class:: LocalDst

    .. rubric:: Message Types

    .. autoclass:: MessageOSC
    .. autoclass:: MessageMIDI
    .. autoclass:: MessageLOCAL

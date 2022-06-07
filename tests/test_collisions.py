import pytest
import tosclib as tosc
from tosclib import Property
from .profiler import profile
from tosclib.elements import ControlType


@profile
def test_collisions() -> tosc.ElementTOSC:
    root = tosc.createTemplate()
    element = tosc.ElementTOSC(root[0])
    assert element

    """Error with collisions. Raise exception."""
    assert element.createProperty(Property("s", "name", "geoff"))
    with pytest.raises(ValueError):
        assert element.createProperty(Property("s", "name", "craig"))
    assert element.createProperty(Property("s", "name2", "craig"))

    """No Error with collisions. Replace value."""
    fader = tosc.ElementTOSC(element.createChild(ControlType.FADER))
    assert fader.setFrame((0, -200, 40, 200))
    assert fader.setFrame((0, 0, 69, 420))

    """No Error with collisions. Replace value."""
    fader = tosc.ElementTOSC(element.createChild(ControlType.FADER))
    assert fader.setColor((0, 0, 0, 1))
    assert fader.setColor((0.25, 0.25, 1, 1))

    """No Error with collisions. Repeat value."""
    fader = tosc.ElementTOSC(element.createChild(ControlType.FADER))
    path = [tosc.Partial(), tosc.Partial(type="PROPERTY", value="name")]
    assert type(path[0]) is tosc.Partial
    assert fader.createOSC() is not None
    assert fader.createOSC(tosc.OSC(path=path)) is not None
    assert fader.createOSC(tosc.OSC(path=path)) is not None

    return "tests/test_collisions.prof"

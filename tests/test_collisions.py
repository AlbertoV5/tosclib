import pytest
import tosclib as tosc


def test_create_template() -> tosc.ElementTOSC:
    root = tosc.createTemplate()
    element = tosc.ElementTOSC(root[0])
    assert element
    return element


def test_create_property():
    """Error with collisions. Raise exception."""
    element = test_create_template()
    assert element.createProperty("s", "name", "geoff")
    with pytest.raises(ValueError):
        assert element.createProperty("s", "name", "craig")
    assert element.createProperty("s", "name2", "craig")


def test_set_frame():
    """No Error with collisions. Replace value."""
    element = test_create_template()
    fader = tosc.ElementTOSC(element.createNode("FADER"))
    assert fader.setFrame(0, -200, 40, 200)
    assert fader.setFrame(0, 0, 69, 420)


def test_set_color():
    """No Error with collisions. Replace value."""
    element = test_create_template()
    fader = tosc.ElementTOSC(element.createNode("FADER"))
    assert fader.setColor(0, 0, 0, 1)
    assert fader.setColor(0.25, 0.25, 1, 1)


def test_osc_messages():
    """No Error with collisions. Repeat value."""
    element = test_create_template()
    fader = tosc.ElementTOSC(element.createNode("FADER"))
    path = [tosc.Partial(), tosc.Partial(typ="PROPERTY", val="name")]
    assert type(path[0]) is tosc.Partial
    assert fader.createOSC()
    assert fader.createOSC(tosc.OSC(path=path))
    assert fader.createOSC(tosc.OSC(path=path))

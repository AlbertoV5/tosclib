import pytest
import tosclib as tosc
from .profiler import profile


@profile
def test_collisions():
    root = tosc.createTemplate()
    element = tosc.Node(root[0])
    assert element
    control = tosc.to_ctrl(element.node)
    assert control

    """Error with collisions. Raise exception."""
    assert (prop := tosc.prop("name", "Geoff"))
    assert element.set_prop(prop)
    with pytest.raises(ValueError):
        assert element.add_prop(tosc.prop("name", "Craig"))
    assert element.add_prop(tosc.prop("name2", "craig"))
    
    """No Error with collisions. Replace value."""
    fader = tosc.Fader()
    assert fader.set_frame((0, -200, 40, 200))
    assert fader.set_color((0, 0, 69, 420))
    efader = tosc.Node(tosc.xml_control(fader))
    assert efader

    """No Error with collisions. Replace value."""
    fader = tosc.Fader()
    assert fader.set_color((0, 0, 0, 1))
    assert fader.set_color((0.25, 0.25, 1, 1))

    """No Error with collisions. Repeat value."""
    fader = tosc.Node(tosc.xml_control(tosc.Fader()))
    address = tosc.address()
    msg = tosc.osc()
    assert fader.add_msg(msg)
    assert fader.add_msg(tosc.osc(addrs = address))
    assert fader.add_msg(tosc.osc(addrs = address))

"""
Testing: Decoder.

    test_working_file:
        load correct file

    test_broken_file
        load incorrect file

    test_edited_working_file:
        edit, save and verify correct file

"""
from tosclib import Template, Control, Property, Value
from tosclib import String, Frame, Color
import pydantic
import tosclib
import pytest
import logging


class Console:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def log(self, *data):
        return self.logger.debug(" ".join(str(d) for d in data))


console = Console()


@pytest.mark.profile
def test_working_file(file_default_messages: Template):
    """load correct file"""
    temp = file_default_messages
    assert temp.root.node
    temp.dump("tests/resources/deleteme.xml")


@pytest.mark.short
def test_properties(template_empty: Template):
    """Create, modify and validate properties.

    Tests:
        1. Pydantic validates properties created programatically.
        2. Check type of each item in properties and assert they are Property instances.
        3. Expect pydantic validation error when trying to set invalid property param.
    """
    temp = template_empty.copy()
    control = temp.root.node
    props = {
        "s": {"name": "myControl", "tag": "tag1"},
        "r": {"frame": (100, 100, 0, 0)},
        "c": {"color": (0.5, 0.3, 0.2, 1.0)},
        "b": {"outline": True},
        "i": {"outlineStyle": 1},
        "f": {"cornerRadius": 0.5},
    }
    control.properties = [
        Property(at_type=typ, key=key, value=props[typ][key])
        for typ in props
        for key in props[typ]
    ]
    console.log(control.properties)
    for prop in control.properties:
        console.log(type(prop))
        assert isinstance(prop, Property)
        with pytest.raises(pydantic.ValidationError) as e_info:
            prop.at_type = "w"


@pytest.mark.short
def test_controls(template_empty: Template):
    temp = template_empty.copy()
    parent = temp.root.node
    parent.children = [
        Control(
            at_type="FADER",
            properties=[
                String("name", "myFader"),
                Frame("frame", (x, 0, 100, 400)),
                Color("color", (1.0, 0.3, 0.3, 1.0)),
            ],
            values=[Value(key="x", default=0.5)],
        )
        for x in range(0, 400, 100)
    ]
    console.log(parent.children)
    temp.dump("tests/resources/deleteme.xml")
    temp.save("tests/resources/deleteme.tosc")


def test_broken_file():
    """load incorrect file"""


def test_edited_working_file():
    """edit, save and verify correct file"""

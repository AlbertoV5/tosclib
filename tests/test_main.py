"""
Testing: Tosclib.
TODO: Test multiple message types in one control
"""
from tosclib.template import Template
from tosclib.control import Control
from tosclib.value import Value, X
from tosclib.property import Property, String, Frame, Color
import pydantic
import pytest
import logging


class Console:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def log(self, *data):
        return self.logger.debug(" ".join(str(d) for d in data))


console = Console()


@pytest.mark.io
def test_working_file(file_default_messages: Template):
    """Load and validate basic file."""
    template = file_default_messages
    assert template.control


@pytest.mark.io
def test_default_controls(file_default_controls: Template):
    """Load and validate all controls."""
    template = file_default_controls
    assert template.control


@pytest.mark.short
def test_properties(template_empty: Template):
    """Create, modify and validate properties.

    Tests:
        1. Pydantic validates properties created programatically.
        2. Check type of each item in properties and assert they are Property instances.
        3. Expect pydantic validation error when trying to set invalid property param.
    """
    temp = template_empty.copy()
    control = temp.control
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
    """Create controls and add them to an empty template.

    Tests:
        1. Create controls and their attributes programatically
    """
    template = template_empty.copy()
    root = template.control
    root.children = [
        Control(
            at_type="FADER",
            properties=[
                String("name", "myFader"),
                Frame("frame", (x, 0, 100, 400)),
                Color("color", (1.0, 0.3, 0.3, 1.0)),
            ],
            values=[X(default=0.5)],
        )
        for x in range(0, 400, 100)
    ]
    for control in root.children:
        console.log(type(control))
        value = control.values[0]
        console.log(type(value))
        assert isinstance(control, Control)
        assert isinstance(value, Value)
        with pytest.raises(TypeError) as e_info:
            control.add_controls([0])

    console.log(root.children[-1])
    template.save("tests/resources/deleteme.tosc", xml=True)


def test_nested_file(template_empty: Template):
    """Create nested controls"""
    template = template_empty
    root = template.control
    red = Color("color", (1.0, 0.2, 0.2, 1.0))
    root.add_controls(
        [
            Control(properties=[Frame("frame", (0, 0, 200, 400))]).add_controls(
                [
                    Control(
                        at_type="FADER",
                        properties=[red, Frame("frame", (x, 0, 100, 400))],
                    )
                    for x in range(0, 200, 100)
                ]
            ),
            Control(properties=[Frame("frame", (200, 0, 200, 400))]).add_controls(
                [
                    Control(
                        at_type="RADIAL",
                        properties=[red, Frame("frame", (x, 0, 100, 400))],
                    )
                    for x in range(0, 200, 100)
                ]
            ),
        ]
    )
    template.save("tests/resources/nested.tosc", xml=True)
    console.log(root.children)


@pytest.mark.short
def test_different_messages(file_different_messages: Template):
    t = file_different_messages
    c = t.control
    for m in c[1].messages:
        console.log(type(m))
    t.save("tests/resources/nested2.tosc", xml=True)


def test_broken_file():
    """load incorrect file"""


def test_edited_working_file():
    """edit, save and verify correct file"""

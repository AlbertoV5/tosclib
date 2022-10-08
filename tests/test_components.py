"""
Create a complete component.

Requirements:
    The template will be an 8 channel mixer. 
    Each channel must have:
        1. A main fader.
        2. Support Mute and Solo buttons.
    Each channel will include two state change buttons:
        1. Will hide main fader and display 4 radials.
        2. Will hide main fader and display 8 buttons.
"""

import pytest
import logging
from conftest import Toscdb

from tosclib.template import Template
from tosclib.control import Control
from tosclib.message import Osc, Midi, Local, Gamepad
from tosclib.value import Value
from tosclib.property import Boolean, Integer, Float, String, Frame, Color


class Console:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def log(self, *data):
        return self.logger.debug(" ".join(str(d) for d in data))


console = Console()


@pytest.fixture
def component_fader() -> Control:
    """Puts together all controls"""
    frame = (0, 0, 640, 1500)
    container = Control()
    container.properties = [Frame("frame", frame)]
    container.children = [Control(at_type="FADER") for i in range(0, 8)]
    # Add properties, values and messages to each fader
    return container


@pytest.mark.long
def test_template(db: Toscdb, component_fader: Control):
    """Roundtrip"""
    template = Template(component_fader)
    db.component.insert_one(template.dict(with_id=True))
    console.log(template.control.children[0])

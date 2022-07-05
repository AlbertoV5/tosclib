"""
Fixtures: Touch OSC Templates and defaults.

    template_default_controls:
        version: 1.1.4.143

"""
from typing import Iterator
import pytest
import tosclib as tosc
from pathlib import Path
from xml.etree.ElementTree import Element, fromstring

INPUT_PATH: Path = Path("tests") / Path("input") 

class Archive:
    DEFAULT_CONTROLS: Path = INPUT_PATH / Path(
        "default_controls.tosc"
    )
    DEFAULT_VALUES: Path = INPUT_PATH / Path(
        "default_values.tosc"
    )
    DEFAULT_MESSAGES: Path = INPUT_PATH / Path(
        "default_messages.tosc"
    )

@pytest.fixture(scope = "session")
def tosc_default_controls() -> Element:
    """
    Returns a template with all controls in their default state.
    """
    template = tosc.load(Archive.DEFAULT_CONTROLS)
    assert template
    return template


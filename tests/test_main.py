"""
Testing: Decoder.

    test_working_file:
        load correct file

    test_broken_file
        load incorrect file

    test_edited_working_file:
        edit, save and verify correct file

"""
from tosclib import Template, Property, ps
import pydantic
import tosclib
import pytest
import logging

log = logging.getLogger(__name__)


@pytest.mark.profile
def test_working_file(file_default_messages: Template):
    """load correct file"""
    t = file_default_messages
    assert t.root.control


@pytest.mark.short
def test_properties(template_empty: Template):
    """Create, modify and validate properties."""
    temp = template_empty.copy()
    control = temp.root.control
    props = {
        "s": {"name": "myControl", "tag": "tag1"},
        "r": {"frame": (100, 100, 0, 0)},
    }
    control.properties = [
        Property(at_type=t, key=k, value=props[t][k]) for t in props for k in props[t]
    ]
    log.debug(control.properties)
    for prop in control.properties:
        assert isinstance(prop, tosclib.Property)
        with pytest.raises(pydantic.ValidationError) as e_info:
            prop.at_type = "w"


@pytest.mark.short
def test_controls(template_empty: Template):
    t = template_empty.copy()
    log.debug(ps.defaults)


def test_broken_file():
    """load incorrect file"""


def test_edited_working_file():
    """edit, save and verify correct file"""

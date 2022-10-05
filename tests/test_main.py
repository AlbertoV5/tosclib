"""
Testing: Decoder.

    test_working_file:
        load correct file

    test_broken_file
        load incorrect file

    test_edited_working_file:
        edit, save and verify correct file

"""
from tosclib import Template, p
import pydantic
import tosclib
import pytest
import logging

log = logging.getLogger(__name__)


@pytest.mark.profile
def test_working_file(file_default_messages: Template):
    """load correct file"""
    t = file_default_messages
    assert t.root.node


@pytest.mark.short
def test_properties(template_empty: Template):
    """Create, modify and validate properties."""
    t = template_empty
    node = t.root.node
    node.properties = [
        p.name("base"),
        p.frame(),
        p.color(),
    ]
    log.debug(node)
    for prop in node.properties:
        assert isinstance(prop, tosclib.Property)
        with pytest.raises(pydantic.ValidationError) as e_info:
            prop.at_type = "w"


def test_broken_file():
    """load incorrect file"""


def test_edited_working_file():
    """edit, save and verify correct file"""

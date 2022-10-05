"""
Testing: Decoder.

    test_working_file:
        load correct file

    test_broken_file
        load incorrect file

    test_edited_working_file:
        edit, save and verify correct file

"""
import pydantic
from tosclib import Template, prop
import tosclib
import pytest
import logging

log = logging.getLogger(__name__)


@pytest.mark.profile
def test_working_file(file_default_messages: Template):
    """load correct file"""
    t = file_default_messages
    assert t.root.node


def test_properties(template_empty: Template):
    """Create, modify and validate properties."""
    t = template_empty
    node = t.root.node
    node.properties = [
        prop.frame(),
        prop.color(),
    ]
    for p in node.properties:
        assert isinstance(p, tosclib.Property)
        with pytest.raises(pydantic.ValidationError) as e_info:
            p.at_type = "w"


def test_broken_file():
    """load incorrect file"""


def test_edited_working_file():
    """edit, save and verify correct file"""

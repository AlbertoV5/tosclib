"""
Testing: Decoder.

    test_working_file:
        load correct file

    test_broken_file
        load incorrect file

    test_edited_working_file:
        edit, save and verify correct file

"""
import pytest
import logging
import tosclib as tosc

log = logging.getLogger(__name__)


@pytest.mark.profile
def test_working_file(file_default_controls):
    """load correct file"""
    root = file_default_controls
    tosc.to_ctrl(root[0])


def test_broken_file():
    """load incorrect file"""


def test_edited_working_file():
    """edit, save and verify correct file"""

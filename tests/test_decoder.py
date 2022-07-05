"""
Testing: Decoder.

    test_working_file:
        load correct file

    test_broken_file
        load incorrect file

    test_edited_working_case:
        edit, save and verify correct file

"""
import pytest
import logging

log = logging.getLogger(__name__)


def test_working_file(tosc_default_controls):
    """load correct file"""
    root = tosc_default_controls


def test_broken_file():
    """load incorrect file"""


def test_edited_working_case():
    """edit, save and verify correct file"""

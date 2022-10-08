"""
Mongo db tests.
"""
from typing import Callable
from bson.json_util import dumps, LEGACY_JSON_OPTIONS
import logging
import pytest

from tosclib.template import Template
from tosclib.control import Control
from conftest import Toscdb


class Console:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def log(self, *data):
        return self.logger.debug(" ".join(str(d) for d in data))


console = Console()


@pytest.mark.db
def test_database_base(db: Toscdb, template_empty: Template):
    """Insert empty Template into database."""
    template = template_empty
    db.test.insert_one(template.dict(with_id=True))
    _id = template.control.at_ID
    assert db.test.find_one({"_id": _id}) is not None


@pytest.mark.db
def test_database_medium(db: Toscdb, file_default_controls: Template):
    """Insert medium-sized Template into database."""
    template = file_default_controls
    db.test.insert_one(template.dict(with_id=True))
    _id = template.control.at_ID
    assert db.test.find_one({"_id": _id}) is not None


@pytest.mark.db
def test_database_nested(
    db: Toscdb, nested_controls: Callable[[int, Control], Control]
):
    template = Template()
    nested_controls(7, template.control)
    db.test.insert_one(template.dict(with_id=True))
    _id = template.control.at_ID
    data: dict = db.test.find_one({"_id": _id})
    assert data is not None
    # test json for compatibility
    with open("tests/resources/nested.json", "w") as file:
        file.write(dumps(data, json_options=LEGACY_JSON_OPTIONS, indent=2))
    # roundtrip
    roundtrip = Template(data)
    assert isinstance(roundtrip.control, Control)


@pytest.mark.long
def test_database_complex(db: Toscdb, template_complex: Template):
    template = template_complex
    assert template.control is not None
    _id = template.control.at_ID
    db.template.insert_one(template.dict(with_id=True))
    roundtrip = Template(db.template.find_one({"_id": _id}))
    assert isinstance(roundtrip.control, Control)

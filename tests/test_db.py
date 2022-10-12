"""
Mongo db tests.
"""
from typing import Callable
from pymongo.errors import DuplicateKeyError
from bson.json_util import dumps, LEGACY_JSON_OPTIONS
from bson.objectid import ObjectId
import logging
import pymongo
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
    console.log(template)
    fix_id = ObjectId()
    db.test.insert_one(template.dict(_id=fix_id))
    roundtrip = db.test.find_one({"_id": fix_id})
    assert Template(roundtrip) == template


@pytest.mark.db
def test_database_medium(db: Toscdb, file_default_controls: Template):
    """Insert medium-sized Template into database."""
    template = file_default_controls
    fix_id = ObjectId()
    db.test.insert_one(template.dict(_id=fix_id))
    roundtrip = db.test.find_one({"_id": fix_id})
    assert Template(roundtrip) == template


@pytest.mark.db
def test_database_nested(
    db: Toscdb, nested_controls: Callable[[int, Control], Control]
):
    template = Template()
    nested_controls(7, template.control)
    fix_id = ObjectId()
    db.test.insert_one(template.dict(_id=fix_id))
    roundtrip = db.test.find_one({"_id": fix_id})
    # JSON
    with open("tests/resources/nested.json", "w") as file:
        file.write(dumps(roundtrip, json_options=LEGACY_JSON_OPTIONS, indent=2))
    assert Template(roundtrip) == template


@pytest.mark.long
def test_database_complex(db: Toscdb, template_complex: Template):
    """Uploads a complex template to the template database.
    Then it fetches it and asserts that parsing is OK.
    Then it deletes it and asserts that it was deleted."""
    template = template_complex
    fix_id = ObjectId()
    try:
        db.template.insert_one(template.dict(_id=fix_id))
    except DuplicateKeyError:
        console.log(f"Template {fix_id} was not deleted.")
    roundtrip = db.template.find_one({"_id": fix_id})
    assert Template(roundtrip) == template
    result = db.template.delete_one({"_id": fix_id})
    assert result.deleted_count == 1

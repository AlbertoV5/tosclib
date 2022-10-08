from typing import Callable
from bson.json_util import dumps, LEGACY_JSON_OPTIONS
from pymongo.database import Database
import logging
import pytest

from tosclib.template import Template
from tosclib.control import Control


class Console:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def log(self, *data):
        return self.logger.debug(" ".join(str(d) for d in data))


console = Console()


@pytest.mark.db
def test_database_base(toscdb: Database, template_empty: Template):
    """Insert empty Template into database."""
    template = template_empty
    toscdb["templates"].insert_one(template.dict(with_id=True))
    _id = template.control.at_ID
    assert toscdb["templates"].find_one({"_id": _id}) is not None


@pytest.mark.db
def test_database_medium(toscdb: Database, file_default_controls: Template):
    """Insert medium-sized Template into database."""
    template = file_default_controls
    toscdb["templates"].insert_one(template.dict(with_id=True))
    _id = template.control.at_ID
    assert toscdb["templates"].find_one({"_id": _id}) is not None
    console.log(template)


@pytest.mark.db
def test_database_nested(
    toscdb: Database, nested_controls: Callable[[int, Control], Control]
):
    template = Template()
    nested_controls(7, template.control)
    toscdb["templates"].insert_one(template.dict(with_id=True))
    _id = template.control.at_ID
    dictionary: dict = toscdb["templates"].find_one({"_id": _id})
    assert dictionary is not None
    #
    # STORING THE RESUlTS
    #
    # test json for compatibility
    with open("tests/resources/nested.json", "w") as file:
        file.write(dumps(dictionary, json_options=LEGACY_JSON_OPTIONS, indent=2))
    #
    # roundtrip
    template2 = Template(dictionary)
    assert isinstance(template2.control, Control)

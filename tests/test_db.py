import pytest
import logging
from tosclib.template import Template
from pymongo.database import Database


class Console:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def log(self, *data):
        return self.logger.debug(" ".join(str(d) for d in data))


console = Console()


@pytest.mark.db
def test_database_base(toscdb: Database, template_empty: Template):
    """Insert empty Template into database."""
    toscdb["templates"].drop()
    toscdb["templates"].insert_many([template_empty.dict(with_id=True)])
    _id = template_empty.node.at_ID
    assert toscdb["templates"].find_one({"_id": _id}) is not None


@pytest.mark.db
def test_database_heavy(toscdb: Database, file_default_messages: Template):
    """Load Heavy Template and insert it into database."""
    toscdb["templates"].drop()
    toscdb["templates"].insert_many([file_default_messages.dict(with_id=True)])
    _id = file_default_messages.node.at_ID
    assert toscdb["templates"].find_one({"_id": _id}) is not None

import pytest
import logging


class Console:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def log(self, *data):
        return self.logger.debug(" ".join(str(d) for d in data))


console = Console()


def test_database(toscdb):
    db = toscdb
    console.log(db)

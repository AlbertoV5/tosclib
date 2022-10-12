"""
Fixtures: Default templates and files.
"""
from typing import Callable
from pathlib import Path
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import MongoClient
import pytest

from tosclib.template import Template
from tosclib.control import Control


TESTS_PATH: Path = Path.cwd() / Path("tests").resolve()
INPUT_PATH: Path = TESTS_PATH / "resources"


@pytest.fixture(scope="session")
def file_default_controls() -> Template:
    """Returns a template with all controls in their default state."""
    return Template(INPUT_PATH / "default_controls.tosc")


@pytest.fixture(scope="session")
def file_default_messages() -> Template:
    """Returns a template with all messages in their default state."""
    return Template(INPUT_PATH / "default_messages.tosc")


@pytest.fixture(scope="session")
def file_different_messages() -> Template:
    """Returns a template with one control with many messages."""
    return Template(INPUT_PATH / "different_messages.tosc")


@pytest.fixture(scope="session")
def template_empty() -> Template:
    """Call Template constructor with no arguments"""
    return Template()


@pytest.fixture(scope="session")
def template_complex() -> Template:
    """Returns a multi-layered and complex template."""
    return Template(INPUT_PATH / "stoic.tosc")


@pytest.fixture(scope="session")
def nested_controls() -> Callable[[int], Template]:
    """
    Add a given level of control hierarchies to a given control.

    nested_controls(level, control)

    If we add the Control to the hierarchy, we have level + 1.
    """

    def nested(level: int, control: Control = None):
        if level == 0:
            return control
        return control.add_controls([nested(level - 1, Control())])

    return nested


class Toscdb(Database):
    """Pseudo-schema"""

    test: Collection
    template: Collection
    component: Collection


@pytest.fixture(scope="session")
def db() -> Toscdb:
    """Connect to the Mongo Database"""
    mongo_settings = {"uuidRepresentation": "standard"}
    db: Toscdb = MongoClient(**mongo_settings)["toscdb"]
    assert db is not None
    # Drop test collection by default
    db.test.drop()
    return db

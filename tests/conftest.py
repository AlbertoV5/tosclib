"""
Fixtures: Default templates and files.

    file_default_controls: version 1.1.4.143
        This file contains all objects in their default state.

"""
import pytest
from tosclib import Template
from pathlib import Path
from pymongo.database import Database
from pymongo import MongoClient


TESTS_PATH: Path = Path.cwd() / Path("tests").resolve()
INPUT_PATH: Path = TESTS_PATH / "resources"
OUTPUT_PATH: Path = TESTS_PATH / "output"


class Resources:
    """Store input paths."""

    DEFAULT_CONTROLS: Path = INPUT_PATH / "default_controls.tosc"
    DEFAULT_VALUES: Path = INPUT_PATH / "default_values.tosc"
    DEFAULT_MESSAGES: Path = INPUT_PATH / "default_messages.tosc"
    DIFFERENT_MESSAGES: Path = INPUT_PATH / "different_messages.tosc"


@pytest.fixture(scope="session")
def input_path() -> Path:
    """Checks if input path exists and returns it.

    Returns:
        Path: INPUT_PATH
    """
    assert INPUT_PATH.is_dir()
    return INPUT_PATH


@pytest.fixture(scope="session")
def output_path() -> Path:
    """Checks if output path exists and returns it.

    Returns:
        Path: OUTPUT_PATH
    """
    assert OUTPUT_PATH.is_dir()
    return OUTPUT_PATH


@pytest.fixture(scope="session")
def file_default_controls() -> Template:
    """
    Returns a template with all controls in their default state.
    """
    return Template(Resources.DEFAULT_CONTROLS)


@pytest.fixture(scope="session")
def file_default_messages() -> Template:
    """
    Returns a template with all messages in their default state.
    """
    return Template(Resources.DEFAULT_MESSAGES)


@pytest.fixture(scope="session")
def file_different_messages() -> Template:
    """
    Returns a template with one control with many messages.
    """
    return Template(Resources.DIFFERENT_MESSAGES)


@pytest.fixture(scope="session")
def template_empty() -> Template:
    """Call Template constructor with no arguments"""
    return Template()


@pytest.fixture(scope="session")
def toscdb() -> Database:
    """Connect to the Mongo Database"""
    db = MongoClient().toscdb
    assert db is not None
    return db

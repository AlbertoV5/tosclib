"""
Fixtures: Default templates and files.

    file_default_controls: version 1.1.4.143
        This file contains all objects in their default state.

"""
import pytest
import tosclib as tosc
from pathlib import Path

TESTS_PATH: Path = Path.cwd() / Path("tests")
INPUT_PATH: Path = TESTS_PATH / "resources"
OUTPUT_PATH: Path = TESTS_PATH / "output"


class Resources:
    """Store input paths."""

    DEFAULT_CONTROLS: Path = INPUT_PATH / "default_controls.tosc"
    DEFAULT_VALUES: Path = INPUT_PATH / "default_values.tosc"
    DEFAULT_MESSAGES: Path = INPUT_PATH / "default_messages.tosc"


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
def file_default_controls() -> tosc.Element:
    """
    Returns a template with all controls in their default state.
    """
    template = tosc.load(Resources.DEFAULT_CONTROLS)
    assert template
    return template
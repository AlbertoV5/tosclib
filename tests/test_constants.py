import tosclib as tosc
import pytest
import sys


def test_print_enum(capture_stdout):
    """ """
    enum = tosc.SubElements
    print(enum.PROPERTIES.value)
    print(enum.VALUES.value)
    print(enum.MESSAGES.value)
    print(enum.CHILDREN.value)
    assert capture_stdout["stdout"] == "properties\nvalues\nmessages\nchildren\n"


@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s):
        buffer["stdout"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, "write", fake_write)
    return buffer

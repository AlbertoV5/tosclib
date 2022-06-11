from .profiler import profile2
import tosclib as tosc
import pytest
import sys
from tosclib import controls


@profile2
def test_constants(capture_stdout):

    partial = tosc.Partial()
    print(
        partial.type,
        partial.conversion,
        partial.value,
        partial.scaleMin,
        partial.scaleMax,
    )
    assert capture_stdout["stdout"] == "CONSTANT STRING / 0 1\n"
    capture_stdout["stdout"] = ""

    trigger = tosc.Trigger()
    print(trigger.var, trigger.condition)
    assert capture_stdout["stdout"] == "x ANY\n"
    capture_stdout["stdout"] = ""

    e = tosc.ElementTOSC(tosc.createTemplate()[0])
    for attribute, value in e.__dict__.items():
        print(attribute)
    assert capture_stdout["stdout"] == "node\nproperties\nvalues\nmessages\nchildren\n"
    capture_stdout["stdout"] = ""

    buttonProps = controls.ButtonProperties().build()
    button = controls.Button(properties=buttonProps)

    controls.ControlConverter.toXML(button)

    return "tests/test_constants.prof"


@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s):
        buffer["stdout"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, "write", fake_write)
    return buffer

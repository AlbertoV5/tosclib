from tosclib import decode
from tosclib import etosc
import tosclib as tosc
from .profiler import profile


@profile
def test_decode():
    root = etosc.load("docs/demos/files/msgs.tosc")
    e = root[0]

    b = e.find(".//node[@type='BUTTON']/messages/osc/../..")

    button = decode.to_ctrl(b)

    print(button)

    frame = button.get_prop("frame")
    msgs = button.messages

    xml_frame = tosc.xml_property(frame)
    assert xml_frame
    xml_msg = tosc.xml_message(msgs[0])
    assert xml_msg

    for i in xml_msg:
        print(i)

    value = tosc.value("x", True, True, "0", 0)
    property = tosc.prop("name", "whatever")

    xml_value = tosc.xml_value(value)
    xml_property = tosc.xml_property(property)

    print(xml_value)
    print(xml_property)

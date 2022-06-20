from tosclib import decode
from tosclib import etosc
import tosclib as tosc

root = etosc.load("docs/demos/files/msgs.tosc")
e = root[0]

b = e.find(".//node[@type='BUTTON']/messages/osc/../..")

button = decode.to_ctrl(b)

print(button)

frame = tosc.get_prop(button, "frame")

oscs = tosc.get_msglist(button, "osc")

xml_frame = tosc.xml_property(frame)

xml_osc = tosc.xml_message(oscs[0])

for i in xml_osc:
    print(i)


value = tosc.value("x", True, True, "0", 0)
property = tosc.prop("name", "whatever")

xml_value = tosc.xml_value(value)
xml_property = tosc.xml_property(property)

print()
print(xml_value)
print(xml_property)
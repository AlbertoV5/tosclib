from tosclib import decode
from tosclib import etosc2
from tosclib import controls
import tosclib as tosc

root = etosc2.load("docs/demos/files/msgs.tosc")
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


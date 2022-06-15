from tosclib import decode
from tosclib import etosc2
from tosclib import controls
import tosclib as tosc

root = etosc2.load("docs/demos/files/msgs.tosc")
e = root[0]

b = e.find(".//node[@type='BUTTON']/messages/osc/../..")

button = decode.to_ctrl(b)

button.print()

frame = tosc.get_prop(button, "frame")

e = tosc.xml_property(("frame", (0,0,100,100)))
print(e)
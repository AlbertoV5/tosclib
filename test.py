from tosclib import decode
from tosclib import etosc2
from tosclib.elements import Message, Control
from xml.etree import ElementTree as ET

root = etosc2.load("docs/demos/files/msgs.tosc")
e = root[0]

b = e.find(".//node[@type='BUTTON']/messages/osc/../..")

button = decode.to_ctrl(b)

button.print()

ctrl = decode.to_ctrl(e)

def print_msgs(ctrl:Control):
    for m in ctrl.messages:
        # print(d)
        print(m)


# for m in ctrl.children:
#     print_msgs(m)


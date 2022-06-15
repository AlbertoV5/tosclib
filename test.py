from tosclib import verify
from tosclib import etosc2
from tosclib.elements import Message, Control

root = etosc2.load("docs/demos/files/msgs.tosc")
e = root[0]

ctrl = verify.to_ctrl(e)

def print_msgs(ctrl:Control):
    for m in ctrl.messages:
        # print(d)
        print(m)


for m in ctrl.children:
    print_msgs(m)


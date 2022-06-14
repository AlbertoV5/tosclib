from tosclib import verify
from tosclib import etosc2
from tosclib.elements import Message

root = etosc2.load("docs/demos/files/msgs.tosc")
e = root[0]

ctrl = verify.to_ctrl(e)

def print_msg(msg:Message):
    return print(msg)

for m in ctrl.children[0].messages:
    print_msg(m)


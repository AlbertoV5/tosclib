from tosclib import verify
from tosclib import etosc2
from tosclib.elements import Message

root = etosc2.load("docs/demos/files/msgs.tosc")
e = root[0]

ctrl = verify.to_ctrl(e)

def print_msg(msg:Message):
    dic = ("config", "triggs", "path", "args")
    for m, d in zip(msg,dic):
        print(d)
        print(m)



for m in ctrl.children[0].messages:
    print_msg(m)


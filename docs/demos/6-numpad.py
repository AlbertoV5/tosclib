import cProfile
from copy import deepcopy
import logging
import pstats
import uuid
import tosclib as tosc
import subprocess

bgGradient1 = ((0.25, 0.25, 0.25, 1.0), (0.5, 0.25, 0.25, 1.0))
bgGradient2 = ((1.0, 0.0, 0.0, 1.0), (0.5, 0.0, 0.5, 1.0))
names = (
    7,
    4,
    1,
    8,
    5,
    2,
    9,
    6,
    3,
)
id_label_value = str(uuid.uuid4())


@tosc.layout.column
def layoutBase(children: list[tosc.Control]):

    layoutTop: tosc.Control = layoutValues(
        children[0],
        "GROUP",
        size=(1, 1),
        colors=bgGradient1,
    )

    layoutMid: tosc.Control = layoutNumbers(
        children[1], "GROUP", size=(3, 3), colors=bgGradient1, colorStyle=2
    )

    layoutBot: tosc.Control = layoutClear(
        children[2],
        "GROUP",
        size=(1, 1, 1),
        colors=bgGradient1,
    )

    local_msg_0 = tosc.local(
        True,
        triggers=(tosc.Trigger(("x", "RISE")),),
        source=tosc.LocalSrc(("PROPERTY", "STRING", "name", 0, 1)),
        destination=tosc.LocalDst(("VALUE", "text", id_label_value)),
    )

    for child in layoutMid.children:
        child.children[0].messages.append(local_msg_0)

    layoutBot.children[1].children[0].messages.append(local_msg_0)

    local_msg_1 = tosc.local(
        True,
        (tosc.Trigger(("x", "RISE")),),
        source=tosc.LocalSrc(
            ("CONSTANT", "STRING", "0", 0, 1),
        ),
        destination=tosc.LocalDst(("PROPERTY", "sum", id_label_value)),
    )

    local_msg_2 = tosc.local(
        True,
        (tosc.Trigger(("x", "FALL")),),
        source=tosc.LocalSrc(
            ("CONSTANT", "STRING", "", 0, 1),
        ),
        destination=tosc.LocalDst(("VALUE", "text", id_label_value)),
    )

    layoutBot.children[0].children[0].messages.append(local_msg_1)
    layoutBot.children[0].children[0].messages.append(local_msg_2)
    layoutBot.children[2].children[0].messages.append(local_msg_2)

    return tosc.prop("name", "numpad")


@tosc.layout.row
def layoutValues(controls: list[tosc.Control]):

    controls[0].set_prop(("name", "value"))
    controls[0].children.append(
        tosc.controls.Button(
            name="valueButton",
            color=controls[0].get_color(),
            frame=controls[0].get_frame(),
        )
    )
    controls[0].children.append(
        tosc.Label(
            id=id_label_value,
            values=[("text", False, False, "", 0)],
            name="valueLabel",
            background=False,
            color=controls[0].get_color(),
            frame=controls[0].get_frame(),
            textSize=60,
            sum="",
            max="127",
            script=(
                """
self.sum = "0"
self.values.text = self.sum

function onValueChanged(key,value)
    self.sum = self.sum..self.values.text
    if tonumber(self.sum) >= tonumber(self.max) then
        self.sum = self.max
    end
    if tonumber(self.sum) == 0 then
        self.values.text = "0"
    end
    self.values.text = self.sum
end"""
            ),
        )
    )

    controls[1].set_prop(("name", "send"))
    controls[1].children.append(
        tosc.Button(
            name="sendButton",
            color=controls[1].get_color(),
            frame=controls[0].get_frame(),
        )
    )
    controls[1].children.append(
        tosc.Label(
            values=[("text", False, False, "SEND", 0)],
            name="sendLabel",
            color=controls[1].get_color(),
            frame=controls[0].get_frame(),
            textSize=60,
            background=False,
        )
    )

    return ("name", "Values")


@tosc.layout.grid
def layoutNumbers(controls: list[tosc.Control]):

    f = controls[0].get_frame()
    frame = (int(f[2] * 0.1), int(f[3] * 0.1), int(f[2] * 0.8), int(f[3] * 0.8))
    label = tosc.Label(
        frame=frame,
        textColor=(1.0, 1.0, 1.0, 1.0),
        textSize=48,
        background=False,
    )
    button = tosc.Button(
        frame=frame,
        outline=False,
        color2=(0.5, 0.5, 0.5, 1.0),
    )
    for n, c in zip(names, controls):
        label.values.append(("text", False, False, str(n), 0))
        label.set_prop(("name", str(n)))
        button.set_prop(("name", str(n)))
        button.set_prop(("color", c.get_color()))
        c.children.append(deepcopy(button))
        c.children.append(deepcopy(label))

    return ("outline", True), ("name", "numbers")


@tosc.layout.row
def layoutClear(controls: list[tosc.Control]):

    controls[0].set_prop(("name", "clear"))
    controls[0].children.append(
        tosc.Button(
            name="clearButton",
            frame=controls[0].get_frame(),
            color=controls[0].get_color(),
        )
    )
    controls[0].children.append(
        tosc.Label(
            values=[("text", False, False, "CLR", 0)],
            name="clearLabel",
            outlineStyle=1,
            frame=controls[0].get_frame(),
            color=controls[0].get_color(),
            textSize=48,
            background=False,
        )
    )

    controls[1].set_prop(("name", "zero"))
    controls[1].children.append(
        tosc.Button(
            name="0", frame=controls[0].get_frame(), color=controls[1].get_color()
        )
    )
    controls[1].children.append(
        tosc.Label(
            values=[("text", False, False, "0", 0)],
            name="0",
            outlineStyle=1,
            frame=controls[0].get_frame(),
            color=controls[1].get_color(),
            textSize=48,
            background=False,
        )
    )

    #
    controls[2].set_prop(("name", "del"))
    controls[2].children.append(
        tosc.Label(
            name="0", frame=controls[2].get_frame(), color=controls[2].get_color()
        )
    )
    controls[2].children.append(
        tosc.Label(
            values=[("text", False, False, "DEL", 0)],
            name="0",
            outlineStyle=1,
            frame=controls[0].get_frame(),
            color=controls[2].get_color(),
            textSize=48,
            background=False,
        )
    )

    return ("name", "clearDel")


def main():

    root = tosc.createTemplate(frame=(0, 0, 500, 800))
    template = tosc.Node(root[0])
    
    control:tosc.Control = tosc.to_ctrl(template.node)

    layoutBase(control, "GROUP", size=(1, 3, 1), colors=bgGradient1)
    root[0] = tosc.xml_control(control)

    """Save it as a template"""
    tosc.write(root, "docs/demos/numpad.tosc")


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="docs/demos/numpad.prof")

    subprocess.run(["open", "docs/demos/numpad.tosc"])

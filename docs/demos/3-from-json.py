import tosclib as tosc
import json


def get_json(fileName: str):
    with open(fileName, "r") as file:
        return json.loads(file.read())


def create_osc() -> tosc.MessageOSC:
    """Create a message with a path constructed with custom Partials"""
    return tosc.osc(
        tosc.msgconfig(),
        (tosc.trigger(),),
        (
            tosc.partial(),
            tosc.partial("PROPERTY", "STRING", "parent.name"),
            tosc.partial(),
            tosc.partial("PROPERTY", "STRING", "name"),
        ),
        (tosc.partial("VALUE", "FLOAT", "x"),),
    )


def create_fader(e: tosc.Node, name, width, limit, i, msg):
    """Create a Fader object, then convert it to XML"""
    fader = tosc.Fader()
    fader.set_prop(("name", name))
    fader.set_prop(("frame", (int(width * i), 0, int(width), 1080)))
    fader.set_prop(("color", (i / limit, 0, 1 - i / limit, 1)))
    fader.messages.append(msg)
    efader = tosc.Node(tosc.xml_control(fader))
    e.append(efader)
    return efader


def create_group(e: tosc.Node, name, frame, color):
    group = tosc.Group()
    group.set_prop(("name", name), ("frame", frame), ("color", color))
    egroup = tosc.Node(tosc.xml_control(group))
    e.append(egroup)
    return egroup


def main(jsonFile, outputFile):
    root = tosc.createTemplate()
    base = tosc.Node(root[0])
    base.add_prop(("name", "template"))
    base.add_prop(("frame", (0, 0, 1920, 1080)))

    group = create_group(base, "Controls", (420, 0, 1080, 1080), (0.25, 0.25, 0.25, 1))

    jsonData = get_json(jsonFile)
    limit = 10
    width = int(420 / limit)
    msg = create_osc()

    for i, param in enumerate(jsonData):
        create_fader(group, param["name"], width, limit, i, msg)
        print(param["name"])
        if i == limit:
            break

    tosc.write(root, outputFile)


if __name__ == "__main__":
    main(
        "docs/demos/files/Pro-C 2 (FabFilter).json", "docs/demos/files/newTemplate.tosc"
    )

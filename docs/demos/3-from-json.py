import tosclib as tosc
import json


def getJson(fileName: str):
    with open(fileName, "r") as file:
        return json.loads(file.read())


def oscMsg() -> tosc.OSC:
    """Create a message with a path constructed with custom Partials"""
    return tosc.OSC(
        path=[
            tosc.Partial(),  # Default is the constant '/'
            tosc.Partial(type="PROPERTY", value="parent.name"),
            tosc.Partial(),
            tosc.Partial(type="PROPERTY", value="name"),
        ]
    )


def createFader(e: tosc.ElementTOSC, name, width, limit, i, msg):
    fader = tosc.ElementTOSC(e.createChild("FADER"))
    fader.createProperty("s", "name", name)
    fader.setFrame(width * i, 0, width, 1080)
    fader.setColor(i / limit, 0, 1 - i / limit, 1)
    fader.createOSC(message=msg)  # Creates a new message from custom tosc.OSC


def main(jsonFile, outputFile):
    root = tosc.createTemplate()
    base = tosc.ElementTOSC(root[0])
    base.createProperty("s", "name", "template")
    base.setFrame(0, 0, 1920, 1080)

    # Group container for the faders
    group = tosc.ElementTOSC(base.createChild("GROUP"))
    group.createProperty("s", "name", "Controls")
    group.setFrame(420, 0, 1080, 1080)
    group.setColor(0.25, 0.25, 0.25, 1)

    # Create faders based on Json data
    jsonData = getJson(jsonFile)
    limit = 10
    width = int(group.getPropertyParam("frame", "w").text) / limit
    msg = oscMsg()

    for i, param in enumerate(jsonData):
        createFader(group, param["name"], width, limit, i, msg)
        if i == limit:
            break

    print([tosc.ElementTOSC(i).getPropertyValue("name").text for i in group.children])
    tosc.write(root, outputFile)


if __name__ == "__main__":
    main("demos/files/Pro-C 2 (FabFilter).json", "demos/files/newTemplate.tosc")

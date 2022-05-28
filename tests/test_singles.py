import tosclib as tosc
from tosclib.tosc import Partial

def test_singles():

    root = tosc.createTemplate()
    element = tosc.ElementTOSC(root)

    element.createValue(tosc.Value())

    element.setValue(tosc.Value("touch", "1", "1", "true", "1"))

    element.showValues()

    element.createOSC(
        message=tosc.OSC(
            "0",
            "0",
            "0",
            "1",
            "00001",
            [tosc.Trigger()],
            [tosc.Partial(), tosc.Partial()],
            [Partial(), Partial()],
        )
    )

    element.createProperty("f", "frame", "", {"r":"0", "g":"1", "b":"0", "a":"1"})
    element.showProperty("frame")
    element.setProperty("frame", "", {"r":"0", "g":"0", "b":"1", "a":"1"})

    # element.setFrame(1, 0, 0, 1)

if __name__ == "__main__":
    test_singles()
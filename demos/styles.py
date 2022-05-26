import tosclib as tosc
from PIL import ImageColor

def rgb(rgb : str) -> tuple[int]:
    return tuple([str(i/255) for i in ImageColor.getcolor(rgb, "RGB")])

root = tosc.load("demos/files/test.tosc")

parent = tosc.ElementTOSC(root[0])

boxy = tosc.ElementTOSC(parent.findChild("boxy"))

(r,g,b) = rgb("#23a9dd")

with open("demos/files/test_func.lua", "r") as file:
    boxy.createProperty("s", "script", file.read())

boxy.createProperty("c", "style1", "", {"r":r, "g":g, "b":b, "a":"1"})

boxy.showProperty("style1")

tosc.write(root, "demos/files/o_custom.tosc")
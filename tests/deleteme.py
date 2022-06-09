import tosclib as tosc
from tosclib.elements import ControlType, Frame, Color, PropertyFactory


prop = PropertyFactory.build("name", "Geoff")

for p in prop.__slots__:
    print(p)
    print(getattr(prop, p))


frame = PropertyFactory.build("frame", (0,0,100,100))
color = PropertyFactory.build("color", (0.25, 0.25, 0.25, 1.0))

root = tosc.createTemplate(frame = (0, 0, 800, 800))
template = tosc.ElementTOSC(root[0])


box = tosc.asEtosc(template.createChild(ControlType.BOX))
box.createProperty(frame)
box.createProperty(color)

for prop in box.properties:
    print(prop)

tosc.write(root, "tests/deleteme.tosc")
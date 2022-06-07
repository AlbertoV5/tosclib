import cProfile
import logging
import pstats
import tosclib as tosc
from tosclib import Value
from tosclib import controls
from tosclib.controls import ButtonProperties, ControlFactory, LabelProperties
from tosclib.elements import LOCAL, PropertyFactory, Trigger, Property
from tosclib.tosc import ControlType, ElementTOSC
from tosclib.layout import layoutColumn, layoutGrid

"""WORK IN PROGRESS"""

bgColor = ((0.25, 0.25, 0.25, 1.0), (0.25, 0.25, 0.25, 1.0))


@layoutColumn
def layoutBase(children: list[ElementTOSC]):

    numbers(children[1], ControlType.GROUP, size=(3, 3), colors=bgColor)

    return (PropertyFactory.name("Numpad"),)

@layoutGrid
def numbers(children: list[ElementTOSC]):

    frame = children[0].getFrame()
    with open("docs/modules/button.lua", "r") as file:
        script = file.read()
    buttonProps = ButtonProperties(name="button", frame=frame, script=script)
    labelProps = LabelProperties(
        name="label", textSize=48, background=False, frame=frame
    )

    label = controls.Label(properties=labelProps.build())
    button = controls.Button(properties=buttonProps.build())
    logging.warning(button)

    for c in children:
        c.children.append(ControlFactory.build(label))
        c.children.append(ControlFactory.build(button))

    return (PropertyFactory.outline(False),PropertyFactory.name("numbers"))


def main():

    root = tosc.createTemplate(frame=(0, 0, 800, 800))
    template = ElementTOSC(root[0])

    layoutBase(template, ControlType.GROUP, size=(1, 3, 1), colors=bgColor)

    """Save it as a template"""
    tosc.write(root, "docs/modules/numpad.tosc")


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="docs/modules/test.prof")

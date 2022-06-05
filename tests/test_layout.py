import tosclib as tosc
from tosclib import layoutColumn
from tosclib import ElementTOSC
from tosclib.layout import layoutGrid, layoutRow
from .profiler import profile


@layoutColumn
def columns(groups: list[ElementTOSC]):
    for g in groups:
        g.setOutline(False)
    return


@layoutGrid
def grid(groups: list[ElementTOSC]):
    for g in groups:
        g.setOutline(False)
    return


@layoutRow
def row(groups: list[ElementTOSC]):
    for g in groups:
        g.setOutline(False)
    return


@profile
def main():

    # TO DO: Expand layout tests!
    frame = (0, 0, 1600, 1600)

    root = tosc.createTemplate(frame=frame)
    rootosc = ElementTOSC(root[0])

    columnLayout: ElementTOSC = columns(
        size=tuple(1 for i in range(4)),
        frame=(0, 0, 400, 1200),
        colors=((0.8, 0.8, 0.8, 1.0), (0.2, 0.2, 0.2, 1.0)),
    )

    gridLayout: ElementTOSC = grid(
        frame=(400, 0, 1200, 1200),
        size=(5, 3),
        colors=("#3E8989FF", "#564D65FF"),
        colorStyle=0,
    )

    rowLayout: ElementTOSC = row(
        frame=(0, 1200, 1600, 400), colors=("#3E8989FF", "#564D65FF")
    )

    assert rootosc.append(gridLayout)
    assert rootosc.append(columnLayout)
    assert rootosc.append(rowLayout)

    tosc.write(root, "tests/deleteme.tosc")

    return "tests/deleteme.prof"


if __name__ == "__main__":
    main()

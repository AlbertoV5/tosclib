import tosclib as tosc
from tosclib import layoutColumn
from tosclib import ElementTOSC
from tosclib.layout import layoutGrid
from PIL import ImageColor as ic


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


def main():
    frame = (0, 0, 1200, 800)

    root = tosc.createTemplate(frame=frame)
    top = columns(
        size=tuple(1 for i in range(8)),
        gradient=((0.8, 0.8, 0.8, 1.0), (0.2, 0.2, 0.2, 1.0)),
    )

    _grid = grid()

    ElementTOSC(root[0]).append(_grid)

    ElementTOSC(root[0]).append(top)
    tosc.write(root, "tests/deleteme.tosc")


if __name__ == "__main__":
    main()

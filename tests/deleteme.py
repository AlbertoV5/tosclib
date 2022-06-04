import tosclib as tosc
from tosclib import layoutColumn
from tosclib import ElementTOSC as etosc
from tosclib.layout import layoutGrid


@layoutColumn
def columns(group: etosc):

    return


@layoutGrid
def grid(group: etosc):

    return


def main():

    root = tosc.createTemplate(frame=(0, 0, 2560, 1600))
    top = columns(ratio=(1, 1, 1, 1))
    #gradient=((0, 0, 0, 1), (0.5, 0.5, 0.5, 1), (1, 1, 1, 1))
    _grid = grid()

    # for i in top:
    #     print(etosc(i).getName())

    etosc(root[0]).append(top)
    tosc.write(root, "tests/deleteme.tosc")


if __name__ == "__main__":
    main()

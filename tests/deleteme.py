import tosclib as tosc
from tosclib import layoutColumn
from tosclib import ElementTOSC as etosc


@layoutColumn
def columns(group: etosc):
    color = (0.25, 0.25, 0.25, 1.0)

    return color


def main():

    root = tosc.createTemplate(frame=(0, 0, 2560, 1600))
    top = columns((1, 1, 1, 1))

    # for i in top:
    #     print(etosc(i).getName())

    etosc(root[0]).append(top)
    tosc.write(root, "tests/deleteme.tosc")


if __name__ == "__main__":
    main()

import tosclib as tosc


def main():
    root = tosc.load("docs/demos/files/test2.tosc")
    group = tosc.Node(root[0])

    group.add_prop(("CustomProperty", "Craig"))
    group.show_prop("CustomProperty")

    tosc.write(root, "docs/demos/files/customProp.tosc")


if __name__ == "__main__":
    main()

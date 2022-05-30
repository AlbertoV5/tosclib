import tosclib as tosc

if __name__ == "__main__":

    root = tosc.load("docs/demos/files/test2.tosc")
    parent = tosc.ElementTOSC(root[0])

    # Set the property to the parent node, not the root node.
    prop = tosc.Property("s", "CustomProperty", "Craig")
    parent.createProperty(prop)

    print("Added Property: ")
    parent.showProperty("CustomProperty")

    tosc.write(root, "docs/demos/files/customProp.tosc")

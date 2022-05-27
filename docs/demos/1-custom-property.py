import tosclib as tosc

if __name__ == "__main__":

    root = tosc.load("demos/files/test2.tosc")
    parent = tosc.ElementTOSC(root[0])

    # Set the property to the parent node, not the root node.
    parent.createProperty(type="s", key="CustomProperty", text="1612")

    print("Added Property: ")
    parent.showProperty("CustomProperty")

    tosc.write(root, "demos/files/customProp.tosc")

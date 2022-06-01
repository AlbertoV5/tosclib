import tosclib as tosc
from tosclib import Control, Property, Value
import re
from tosclib.tosc import ControlType


def test_module_1():

    file = "docs/demos/files/Numpad_basic.tosc"
    outputFile = "docs/demos/files/Numpad_modded.tosc"
    root = tosc.load(file)
    group = tosc.ElementTOSC(root[0])
    group1 = tosc.ElementTOSC(group.findChildByName("group1"))
    data = Control.parseProperties(group1.children, "name", "script")

    for i, d in enumerate(data):
        if "num" in d["name"] and d["script"]:

            if re.search(r"\d", d["name"]):
                pass
                # print("---",d["name"],"---")
                # print(d["script"])

    group2 = tosc.ElementTOSC(group.createChild(ControlType.GROUP))
    group2.setName("group2mod")
    group1.moveChildren(group2, ControlType.BUTTON)

    for child in group1.children:
        child = tosc.ElementTOSC(child)
        name = child.getPropertyValue("name").text
        if re.search(r"\d", name) and (child.isControl(ControlType.BUTTON)):
            # print(name)
            indexName = name.replace("num", "")

            subGroup = tosc.ElementTOSC(group2.createChild(ControlType.GROUP))
            subGroup.setName(indexName)
            f = [e.text for e in child.getPropertyValue("frame")]
            print(f)
            subGroup.setFrame(f[0], f[1], f[2], f[3])
            subGroup.setColor(0.25, 0.25, 0.25, 1)

            subButton = tosc.ElementTOSC(subGroup.createChild(ControlType.BUTTON))
            subButton.setFrame(0, 0, f[2], f[3])
            subButton.setName(f"button{indexName}")
            subButton.setColor(0.25, 0.25, 0.25, 1)

            subLabel = tosc.ElementTOSC(subGroup.createChild(ControlType.LABEL))
            subLabel.setName(f"label{indexName}")
            subLabel.setFrame(0, 0, f[2], f[3])
            subLabel.setColor(1, 1, 1, 1)
            subLabel.setBackground(False)
            subLabel.createValue(Value(key="text", default=indexName))

            subButton.setScript(
                f"""
function onValueChanged(key)
    if (key == "x" and self.values.x == 1) then
        self.parent.parent.children.numvalue:notify(self.parent.name)
    end
end
    """
            )
        elif not re.search(r"\d", name) and not child.isControl(ControlType.LABEL):
            # print(child.getPropertyValue("name").text)
            group2.children.append(child.node)
            # child.showProperty("script")

    tosc.write(root, outputFile)


if __name__ == "__main__":
    test_module_1()

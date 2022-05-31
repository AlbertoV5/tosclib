from tosclib import tosc
from tosclib.tosc import Partial, Value
from tosclib.tosc import Controls
import sys
import xml.etree.ElementTree as ET
import time

def test_singles():

    root = tosc.createTemplate()
    element = tosc.ElementTOSC(root[0])

    element.setName("Craig")
    element.setTag("Scottish")
    element.createValue(Value())

    element.showValue("touch")
    element.setValue(Value("touch", "1", "1", "true", "1"))

    element.createOSC(
        message=tosc.OSC(
            "0",
            "0",
            "0",
            "1",
            "00001",
            [tosc.Trigger()],
            [tosc.Partial(), tosc.Partial()],
            [Partial(), Partial()],
        )
    )

    element.setColor(1, 0, 0, 1)
    element.setFrame(0, 0, 1, 1)

    # element.showProperty("frame")

    print(tosc.Controls.BOX.FRAME)
    print(Controls.BOX.BACKGROUND)
    
    print(Controls.BOX.SHAPE)

    def size(data):
        return print(sys.getsizeof(data))
    
    size(ET.Element("test"))

    count = 0
    for i in dir(tosc.ElementTOSC):
        if "__" not in i:
            count += 1
    print(count)

    tag = tosc.pullValueFromKey2(root, "name", "Craig", "tag")
    print(tag)


    def go1(n):
        start = time.process_time()
        for i in range(n):
            x = tosc.ControlElements.PROPERTIES
        end = time.process_time()
        print(x, end - start)

    go1(10000000)
    print(tosc.outlineStyle.__name__)
    
    def go2(n):
        start = time.process_time()
        for i in range(n):
            x = element.setColor(1, 0, 0, 1)
        end = time.process_time()
        print(x, end - start)
    

    print(element.getID())
    go2(10000)

if __name__ == "__main__":
    test_singles()

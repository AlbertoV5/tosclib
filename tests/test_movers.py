import tosclib as tosc
import pytest
import sys
from pathlib import Path
from tosclib import Property
from tosclib.tosc import ControlElements, ControlType
import time

def test_movers():

    root = tosc.createTemplate()
    node = tosc.ElementTOSC(root[0])
    node.setName("node1")
    
    for var in vars(ControlType):
        if not "_" in var:
            child = tosc.ElementTOSC(node.createChild(var))
            child.setName(var.lower())
    
    node.createOSC()
    node.createMIDI()
    node.createLOCAL()
    
    root2 = tosc.createTemplate()
    node2 = tosc.ElementTOSC(root2[0])
    node2.setName("node2")
    node2.setFrame(0, 0, 100, 100)
    node2.setColor(1, 0, 0, 1)

    node2.moveProperties(node, "frame")
    # node.showProperty("frame")
    node.moveMessages(node2, ControlElements.OSC)
    
    node.moveChildren(node2, ControlType.BOX)
    # for child in node2.children:
    #     child = tosc.ElementTOSC(child)
    #     print(child.getPropertyValue("name").text)


if __name__ == "__main__":
    
    start = time.process_time()
    for i in range(1000):
        test_movers()
    
    end = time.process_time()
    print("-", end - start)
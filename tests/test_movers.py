import unittest
import tosclib as tosc
import pytest
import sys
from pathlib import Path
from tosclib import Property
from tosclib.tosc import ControlType


def test_movers():
    
    root = tosc.createTemplate()
    node = tosc.ElementTOSC(root[0])
    node.setName("node1")
    node.createChild(ControlType.BOX)
    node.createChild(ControlType.BOX)
    node.createChild(ControlType.BUTTON)
    node.createChild(ControlType.ENCODER)
    
    root2 = tosc.createTemplate()
    node2 = tosc.ElementTOSC(root2[0])
    node2.setName("node2")
    node2.setFrame(0,0,100,100)
    node2.setColor(1,0,0,1)
    
    node2.moveProperties(node, "frame")
    node.showProperty("frame")
    

if __name__ == "__main__":
    test_movers()
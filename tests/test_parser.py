import time
import tosclib as tosc
import xml.etree.ElementTree as ET
from tosclib.tosc import ControlElements, Property

class PropertyParser:
    maxDepth = 0
    depth = 0
    
    def __init__(self, targetProperty: str, depth : int = None):
        self.targetKey = targetProperty
        self.depthClose = depth
        self.control = False
        self.property = False
        self.key = False
        self.value = False
        self.targetFound = False
        self.numberOfNodes = 0
        self.targetList = []
        self.multiLine = ""

    def start(self, tag, attrib):
        self.tag = tag
        if tag == ControlElements.NODE:
            self.depth += 1
            if self.depth > self.maxDepth:
                self.maxDepth = self.depth
            self.control = True
        elif self.control and tag == ControlElements.PROPERTY:
            self.property = True
        elif self.property and tag == Property.Elements.KEY:
            self.key = True
        elif self.property and tag == Property.Elements.VALUE:
            self.value = True
            
    def end(self, tag):
        if tag == ControlElements.NODE:
            self.control = False
            self.depth = 1
            self.numberOfNodes += 1
        elif self.control and tag == ControlElements.PROPERTY:
            self.property = False
        elif self.property and tag == Property.Elements.KEY:
            self.key = False
        elif self.property and tag == Property.Elements.VALUE:
            self.value = False
        
        if self.targetFound and tag == Property.Elements.VALUE:
            self.targetFound = False
            self.targetList.append(self.multiLine)
            self.multiLine = ""
        
        if self.depthClose == self.depth:
            return self.close()
        
    def data(self, data):
        if self.control and self.property and self.key and data == self.targetKey:
            self.targetFound = True
        if self.control and self.property and self.value and self.targetFound:
            self.multiLine = f"{self.multiLine}{data}"
            
    def close(self):
        return self.targetList


def parseNode(element: ET.Element, target : PropertyParser):
    start = time.process_time()
    line = ET.tostring(element, encoding="unicode")
    parser = ET.XMLParser(target=target)
    parser.feed(line)
    result = parser.close()
    end = time.process_time()
    print("-", end - start)
    return result

root = tosc.load("docs/demos/files/Numpad_basic.tosc")
result = parseNode(root, PropertyParser(targetProperty="name", depth = 2))

print(result)
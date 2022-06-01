import time
import tosclib as tosc
import xml.etree.ElementTree as ET
from tosclib.tosc import ControlElements, Property

class NameParser:
    maxDepth = 0
    depth = 0
    
    def __init__(self):
        self.nodeName = ""
        self.node = False
        self.property = False
        self.key = False
        self.value = False
        self.name = False
        self.numberOfNodes = 0

    def start(self, tag, attrib):
        self.tag = tag
        if tag == ControlElements.NODE:
            self.depth += 1
            if self.depth > self.maxDepth:
                self.maxDepth = self.depth    
            self.node = True
        elif tag == ControlElements.PROPERTY and self.node:
            self.property = True
        elif tag == Property.Elements.KEY and self.property:
            self.key = True
        elif tag == Property.Elements.VALUE and self.property:
            self.value = True
            
    def end(self, tag):
        if tag == ControlElements.NODE:
            self.node = False
            self.depth = 1
            self.numberOfNodes += 1
        elif tag == ControlElements.PROPERTY and self.node:
            self.property = False
        elif tag == Property.Elements.KEY and self.property:
            self.key = False
        elif tag == Property.Elements.VALUE and self.property:
            self.value = False
        
    def data(self, data):
        if data == "name" and self.node and self.property and self.key:
            self.name = True
        if self.node and self.property and self.name and self.value:
            self.nodeName = data
            print(" " * self.depth, self.maxDepth, "Name:", data)
            self.name = False

    def close(self):
        return self.numberOfNodes


def parser(element: ET.Element, target : NameParser = NameParser()):
    start = time.process_time()
    
    line = ET.tostring(element, encoding="unicode")
    parser = ET.XMLParser(target=target)
    parser.feed(line)
    depth = parser.close()
    end = time.process_time()
    print(depth, "-", end - start)


root = tosc.load("docs/demos/files/Numpad_basic.tosc")
parser(root)



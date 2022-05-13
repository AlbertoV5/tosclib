# Python 3.9
# Alberto Valdez
# 
import xml.etree.ElementTree as ET
from uuid import uuid4
from pathlib import Path

def isParent(element):
    return True if element.find("children") != None else False


def getObjectName(object):
    for prop in object.find("properties"):
        if prop.find("key").text == "name":
            return prop.find("value").text
        

file = "test.xml"
path = Path.cwd() / "copy-scripts" / file

xmlTree = ET.parse(path)
root = xmlTree.getroot()
template = root[0]
children = template.find("children")

ET.indent(children, "  ")

for child in children:
    # print(ET.tostring(child, encoding='unicode'), "\n")
    print(child.get("type"))
    name = getObjectName(child)
    print(name)

    # for property in child.find("properties"):
    #     key = property[0]
    #     value = property[1]
    #     print(key.text)

        # print(property.find("key"), property.find("value"))

    # if isParent(child):
    #     [print(c) for c in child.find("children")]
"""
Simplify navigating, editing and generating .tosc files.

Documentation: https://tosc-generate.readthedocs.io/en/latest/

"""
from xml.dom.minidom import Element
import xml.etree.ElementTree as ET
import re, zlib, uuid
from enum import Enum, unique

@unique
class Items(Enum):
    """ Enum for the default items in <node> 
    
    :cvar PROPERTIES: Find <properties> of Element.
    :cvar VALUES: Find <values> of Element.
    :cvar CHILDREN: Find <children> of Element.
    """
    PROPERTIES = "properties"
    VALUES = "values"
    CHILDREN = "children"

    @classmethod
    def new(cls, name : str, args : dict) -> Enum:
        return Enum(name, {item.name:item.value for item in cls} | args)

class ElementTOSC:
    """ 
    Wrapper for the basic .tosc Elements and SubElements.
    Creates new SubElements if they are not found.

    :param e: This is a <node> Element
    :param enum: These are the items of the <node> Element

    :cvar node: Node is always equal to the e parameter
    :ivar enum.value1: SubElement
    :ivar enum...: Find SubElements of node from Enum values

    :returns: ElementTOSC
    """
    def __init__(self, e : ET.Element, enum : Enum = Items):
        self.node = e
        [
            setattr(self, item.value, e.find(item.value)) 
            if e.find(item.value) else
            setattr(self, item.value, ET.SubElement(e, item.value))
            for item in enum
        ]
    @classmethod
    def fromFile(cls, file : str, enum : Enum = Items):
        """ Returns ElementTOSC Debug purposes """
        return cls(load(file)[0], enum)

    def getPropertyValue(self, key : str) -> ET.Element:
        """ Find the value.text from a known key """
        for p in self.properties:
            if re.fullmatch(p.find("key").text, key):
                return p.find("value")

    def setPropertyValue(self, key : str, text : str = "", params : dict = {}) -> bool:
        """ Set the key's value.text and/or value's {<element> : element.text} """
        for property in self.properties:
            if re.fullmatch(property.find("key").text, key):
                value = property.find("value")
                for paramKey in params:
                    param = ET.SubElement(value, paramKey)
                    param.text = params[paramKey]

                value.text = text if text else ""
                return True
        return False

    def createProperty(self, type : str, key : str, text : str, params : dict = {}) -> bool:
        """ Add a new property with key, value and/or value's {<element> : element.text} """
        property = ET.SubElement(self.properties, "property", attrib = {"type":type})
        keyElement = ET.SubElement(property, "key") 
        valueElement = ET.SubElement(property, "value")
        keyElement.text = key
        valueElement.text = text

        for paramKey in params:
            subElement = ET.SubElement(valueElement, paramKey)
            subElement.text = params[paramKey]
        
        return ET.iselement(property)

    def createNode(self, type : str) -> ET.Element:
        """
        Create and return a children Element with attrib = {'ID' : str(uuid4()), 'type' : type}
        """
        return ET.SubElement(
                                self.children, 
                                "node",
                                attrib = {
                                            "ID":str(uuid.uuid4()), 
                                            "type":type
                                        }
                            )
    def show(self):
        """ Print indented XML as UTF-8 """
        ET.indent(self.node, "  ")
        print(ET.tostring(self.node).decode("utf-8"))

    def showValues(self):
        """ Print indented XML as UTF-8 """
        ET.indent(self.values, "  ")
        print(ET.tostring(self.values).decode("utf-8"))

    def showProperty(self, name : str):
        """ Print indented XML of a single property by name as utf-8"""
        for property in self.properties:
            if re.fullmatch(property.find("key").text, name):
                ET.indent(property, "  ")
                print(ET.tostring(property).decode("utf-8"))
    
    def display(self):
        """ Print a tree like structure """
        etosc = self.node
        print(etosc)
        print("|")
        for item, val in zip(self.Items, self.__dict__.values):
            print("_", item.value, "_", val )

"""ElementTOSC alias"""
e : ElementTOSC = ElementTOSC #: ElementTOSC alias

def load(inputPath : str) -> ET.Element:
    """ Reads .tosc and returns the xml root element
    
    :param inputPath: the path to the .tosc file
    """
    with open (inputPath, "rb") as file:
        return ET.fromstring(zlib.decompress(file.read()))

def write(root : ET.Element, outputPath : str = None) -> bool:
    """ Encodes a root element directly to UTF-8 and compresses to .tosc"""
    with open (outputPath, "wb") as file:
        treeFile = ET.tostring(root, encoding = "UTF-8", method = "xml")
        file.write(zlib.compress(treeFile))
        return True

def findChildByName(element : ET.Element, name : str) -> ET.Element:
    """ Returns the first child element by name """
    for child in element.find("children"):
        if not child.find("properties"):
            continue
        if re.fullmatch(getTextValueFromKey(child.find("properties"), "name"), name):
            return child
            
def getTextValueFromKey(properties : ET.Element, key : str) -> str:
    """ Find the value.text from a known key """
    for property in properties:
        if re.fullmatch(property.find("key").text, key):
            return property.find("value").text

def pullValueFromKey(inputFile : str, key : str, value : str, targetKey : str) -> str:
    """ Find a value from a known key, value and target key"""
    parser = ET.XMLPullParser()
    with open(inputFile, "rb") as file:
        parser.feed(zlib.decompress(file.read()))
        for _, e in parser.read_events(): # event, element
            if not e.find("properties"):
                continue
            if re.fullmatch(getTextValueFromKey(e.find("properties"), key),value):
                parser.close()
                return getTextValueFromKey(e.find("properties"), targetKey)

    parser.close()
    return ""

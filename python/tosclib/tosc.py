"""
Simplify navigating, editing and generating .tosc files.

Requires python 3.9.

github.com/AlbertoV5

"""
__version__ = "0.1.0"

import xml.etree.ElementTree as ET
import re, zlib, uuid

class ElementTOSC:
    def __init__(self, e : ET.Element):
        """ 
        Wrapper for the essential TOSC elements. 
        Creates empty SubElements if not found.

        <node>
            <properties>
                <property>
                    <key>
                        text
                    <value>
                        text
                        
                        <paramKey> 
                            paramValue

            <values>

            <children>
        """
        self.node : ET.Element = e
        self.properties : ET.Element = e.find("properties") if e.find("properties") else ET.SubElement(e, "properties")
        self.values : ET.Element = e.find("values") if e.find("values") else ET.SubElement(e, "values")
        self.children : ET.Element = e.find("children") if e.find("children") else ET.SubElement(e, "children")

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

    def showProperty(self, name : str):
        """ Print indented XML of a single property by name as utf-8"""
        for property in self.properties:
            if re.fullmatch(property.find("key").text, name):
                ET.indent(property, "  ")
                print(ET.tostring(property).decode("utf-8"))
        
"""
FUNCTIONS
"""
def load(inputPath : str = None) -> ET.Element:
    """ Reads .tosc file as bytes and returns the xml root element"""
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

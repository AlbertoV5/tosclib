"""
Simplify navigating, editing and generating .tosc files

Requires python 3.9

github.com/AlbertoV5

"""
import xml.etree.ElementTree as ET
from pathlib import Path
import re, zlib, uuid

def load(inputPath : str = None) -> ET.Element:
    """ Reads .tosc file and returns the xml root"""
    if not inputPath:
        inputPath = input("Enter the .tosc file: ")
    if Path(inputPath).suffix != ".tosc":
        return None
    with open (inputPath, "rb") as file:
        root = ET.fromstring(zlib.decompress(file.read()))
        return root

def write(root : ET.Element, outputPath : str = None) -> bool:
    """ Encodes a root element directly to UTF-8 and compresses to .tosc"""
    if not outputPath:
        outputPath = input("Enter the .tosc output file:")
    if Path(outputPath).suffix != ".tosc":
        return False
    with open (outputPath, "wb") as file:
        treeFile = ET.tostring(root, encoding = "UTF-8", method = "xml")
        file.write(zlib.compress(treeFile))
        return True

def show(element : ET.Element):
    """ Print indented XML as UTF-8 """
    ET.indent(element, "  ")
    print(ET.tostring(element, encoding="UTF-8"))

class Node():
    """ Methods to build and handle <node>"""
    @staticmethod
    def create(parent : ET.Element, type : str):
        """Create a node element and main elements and return dict"""
        
        children = parent.find("children")
        attrib = {
                    "ID":str(uuid.uuid5(uuid.NAMESPACE_DNS, "tosc")), 
                    "type":type
                }
        node = ET.SubElement(children, "node", attrib = attrib)

        return ({
                    "node":node,
                    "properties":ET.SubElement(node, "properties"),
                    "values":ET.SubElement(node, "values"),
                    "children":ET.SubElement(node, "children")
                })

    @staticmethod
    def getMainElements(node : ET.Element) -> dict:
        """ Returns a dictionary of Elements based on the standard tosc xml.
        
        Returns
        -------
        {node:<node>, properties:<properties>, values:<values>, children:<children>}
        """

        properties = node.find("properties")
        values = node.find("values")
        children = node.find("children")

        return ({
                    "node":node,
                    "properties": properties if properties else ET.SubElement(node, "properties"),
                    "values": values if values else ET.SubElement(node, "values"),
                    "children": children if children else ET.SubElement(node, "children")
                })

    def findChildByName(node : ET.Element, name : str) -> ET.Element:
        """ Returns the first child element by name """
        for child in node.find("children"):
            if not child.find("properties"):
                continue
            if re.fullmatch(Property.getValueFromKey(child, "name"), name):
                return child
            
                
class Property():
    """ Methods that use properties, property, key and value"""
    @staticmethod
    def getValueFromKey(node : ET.Element, key : str) -> str:
        """ Find the value.text from a known key"""
        for property in node.find("properties"):
            if property.find("key").text == key:
                return property.find("value").text

    @staticmethod
    def setValueFromKey(node : ET.Element, key : str, value : str) -> bool:
        """ Modify the value.text of an existing <value> from known key"""
        for property in node.find("properties"):
            if property.find("key").text == key:
                property.find("value").text = value
                return True
        return False

    @staticmethod
    def create(
            node : ET.Element, 
            type : str, 
            key : str, 
            value : str,
            params : dict = {}) -> bool:
        """ Add a new property to the node Element

        <properties>
            <property type = {type}>
                <key>
                    {key}
                <value>
                    {value}

                    <params key>
                        {params value}
                
        """
        property = ET.SubElement(
                                    node.find("properties"), 
                                    "property", 
                                    attrib = {"type":type}
                                )
        keyElement = ET.SubElement(property, "key") 
        valueElement = ET.SubElement(property, "value")
        keyElement.text = key
        valueElement.text = value

        for p in params:
            subElement = ET.SubElement(valueElement, p)
            subElement.text = params[p]
        
        return ET.iselement(property)

    @staticmethod
    def pullValueFromKey(inputFile : str, key : str, value : str, targetKey : str) -> str:
        """ Find a value from a known key, value and target key"""
        parser = ET.XMLPullParser()
        if not inputFile:
            inputFile = input("Enter the input .tosc file: ")
        with open(inputFile, "rb") as file:
            parser.feed(zlib.decompress(file.read()))
            for _, e in parser.read_events(): # event, element
                if not e.find("properties"):
                    continue
                if re.fullmatch(Property.getValueFromKey(e, key),value):
                    parser.close()
                    return Property.getValueFromKey(e, targetKey)
                
        parser.close()
        return ""

class Util():
    """ Various pre designed functions to do common tasks"""
    @staticmethod
    def createBox(
                    node : ET.Element, 
                    colorParams : dict, 
                    frameParams : dict, 
                    name : str):
        
        box = Node.create(node, "BOX")

        Property.create(
                            node = box["node"], type = "c", 
                            key = "color", value = "", 
                            params = colorParams,
                        )
        Property.create(
                            box["node"], "r", 
                            "frame", "", frameParams
                        )
        Property.create(
                            box["node"], "s",
                            "name", name
                        )
        Property.create(
                            box["node"], "b", 
                            "background", "1"
                        )
  

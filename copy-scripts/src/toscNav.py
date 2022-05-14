import xml.etree.ElementTree as ET
import re

def getBases_old(root : ET.Element) -> (ET.Element):
    """ Returns a (Element, SubElement, SubElement, SubElement) tuple
    based on the standard tosc xml.
    """
    node = root.find("node")
    return (
    node,
    node.find("properties"),
    node.find("values"),
    node.find("children"),)

def getBases(root : ET.Element) -> dict:
    """ Returns a dictionary of Elements
    based on the standard tosc xml.
    
    Returns
    -------
    {node:<node>, properties:<properties>, values:<values>, children:<children>}
    """
    node = root.find("node")
    return ({
        "node":node,
        "properties":node.find("properties"),
        "values":node.find("values"),
        "children":node.find("children")})

def getValueFromKey(
            element : ET.Element,
            base : str,
            key : str) -> str:
    """ 
    Attributes
    ----------
    element:
        Element to search
    base:
        properties, values, children
    key:
        Known key for value you want to get
    """
    for property in element.find(base):
        if property.find("key").text == key:
            return property.find("value").text

def setValueFromKey(
            element : ET.Element,
            base : str,
            key : str, 
            value : str) -> bool:
    """
    Attributes
    ----------
    element:
        Element to set value to
    base:
        properties, values, children
    key:
        Known key
    value:
        Known value to set on key
    """
    for property in element.find(base):
        if property.find("key").text == key:
            property.find("value").text = value
            return True
    return False

def createValueKey(
            element : ET.Element,
            base : str,
            subBase :str,
            attributes : dict,
            key : str,
            value : str) -> bool:
    """
    Attributes
    ----------
    element:
        Element where generate
    base:
        properties, values, children
    subBase:
        property, value, node
    attributes:
        dictionary as {"type":'s'}
    key:
        Known key
    value:
        Known value to set on key
    """
    property = ET.SubElement(element.find(base), subBase, attrib = attributes)
    keyElement, valueElement = ET.SubElement(property, "key"), ET.SubElement(property, "value")
    keyElement.text, valueElement.text = key, value
    return ET.iselement(property)
    

def pullTarget(
        filePath : str,
        key : str,  
        value : str,
        targetKey : str,) -> str:
    """ Find a value from a known key, value and target key
    
    Attributes
    ----------
    key
        Known key string to get value
    value
        Known value string to match
    targetKey
        The key of the value you are looking for

    Returns
    -------
    targetValue
        Value that corresponds to targetKey
    """
    parser = ET.XMLPullParser()
    with open(filePath, "r") as file:
        parser.feed(file.read())
        for _, e in parser.read_events(): # event, element
            if not e.find("properties"):
                continue
            if re.fullmatch(getValueFromKey(e, "properties", key),value):
                return getValueFromKey(e, "properties", targetKey)
            
        parser.close()
    return ""

if __name__ == "__main__":
    path = "copy-scripts/input/"

    print(pullTarget(
            f"{path}/test.xml",
            key = "name",
            value = "source", 
            targetKey = "script"))

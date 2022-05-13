from xml.dom.minidom import Element
import xml.etree.ElementTree as ET
from uuid import uuid4
from pathlib import Path

def getObjectName(object : Element):
    """ Returns the name of a TOSC object
    """
    for prop in object.find("properties"):
        if prop.find("key").text == "name":
            return prop.find("value").text

    
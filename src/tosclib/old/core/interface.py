"""
Interface for the XML Library of choice.
"""

from xml.etree.ElementTree import (
    Element,
    SubElement,
    fromstring,
    indent,
    tostring,
    XMLPullParser,
)

# Python 3.9
# Alberto Valdez
import xml.etree.ElementTree as ET
from uuid import uuid4
from pathlib import Path
from src import toscNav
import re

def main(inputFile, outputFile):

    # Fast Stream pull
    script = toscNav.pullTarget(
                    filePath = inputFile, 
                    key = "name", 
                    value = "source",
                    targetKey = "script")

    # Slow Tree based edits
    tree = ET.parse(inputFile)
    root = tree.getroot()
    main = toscNav.getBases(root)

    for child in main["children"]:

        name = toscNav.getValueFromKey(
                        element = child, 
                        base = "properties", 
                        key = "name")

        if not re.fullmatch(name, "targets"):
            continue

        for c in child.find("children").findall("*"):
            if not c.find("properties"):
                continue
            _retval = toscNav.createValueKey(
                            element = c,
                            base = "properties",
                            subBase = "property",
                            attributes = {"type":"s"},
                            key = "script",
                            value = script)

            print("Failed to create") if not _retval else None

    tree.write(outputFile)

if __name__ == "__main__":
    
    path = Path.cwd() / "copy-scripts"

    main(path / "test.xml", path / "out.xml")
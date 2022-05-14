# Python 3.9
# Alberto Valdez
import xml.etree.ElementTree as ET
from pathlib import Path
from src import toscNav
import re

def copyScripts(
        inputFile : Path, 
        outputFile: Path, 
        script : str,
        targetName : str,):
    """ Finds target and add a script object to all its children

    Attributes
    ----------
    script
        complete script string
    targetName
        name of group whose children will receive the script copy
    """
    tree = ET.parse(inputFile)
    root = tree.getroot()
    main = toscNav.getBases(root)

    for child in main["children"]:

        name = toscNav.getValueFromKey(
                        element = child, 
                        base = "properties", 
                        key = "name")

        if not re.fullmatch(name, targetName):
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

    tree.write(f"{outputFile}.xml")
    tree.write(f"{outputFile}.tosc")


if __name__ == "__main__":
    
    path = Path.cwd() / "copy-scripts"
    inputFile = path / "input" / "test.xml"
    outputFile = path / "output" / "out" # xml and tosc

    # Fast Stream pull
    script = toscNav.pullTarget(
                    filePath = inputFile, 
                    key = "name", 
                    value = "source",
                    targetKey = "script")

    # Tree based object insertion
    copyScripts(inputFile, outputFile, script, "targets")
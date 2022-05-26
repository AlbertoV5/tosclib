import tosclib as tosc
import re

def CopyScripts(input : str, output : str, source : str = "source", target : str = "target"):
    """Find the script in source and copy it to all children in target"""
    
    script = tosc.pullValueFromKey(
                        inputFile = input,
                        key = "name",
                        value = source,
                        targetKey = "script")
                        
    root = tosc.load(input)
    main = tosc.ElementTOSC(root[0])

    for primary in main.children:
        primary = tosc.ElementTOSC(primary)

        if re.fullmatch(primary.getPropertyValue("name").text, target):
            continue
        
        for secondary in primary.children:
            secondary = tosc.ElementTOSC(secondary)
            secondary.createProperty("s", "script", script)
 
        tosc.write(root, output)

        return print(f"Wrote:\n \n{script}\nTo file: {output}")

if __name__ == "__main__":

    CopyScripts(
                    "../demos/files/test.tosc", 
                    "../demos/files/out.tosc", 
                    "source",
                    "target"
                )

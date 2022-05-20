# tosc-generate
Using XML trees to generate simple Touch OSC XML templates. Make sure to backup your .tosc files before editing them.

Custom classes and functions that help navigate the structure of the .tosc file. Example:

```python
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
```

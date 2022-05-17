# tosc-generate
Using XML trees to generate simple Touch OSC XML templates.

./python/tosclib has a few handy functions that help dealing with .tosc files.

Examples: 
```python
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
```

```python
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

```


Currently prototyping with Python but I want to move to a more performant Rust + JS or something stack in the future and adding Reaper -> xml -> tosc -> Reaper support. 

## copy-scripts

Find a source object by name, copies its script and adds it to all children objects of a target object.

### Usage

1. Set up a template so you have a source object and a target group.
2. Open or run copy-scripts.py with arguments.
3. Open .tosc file.

Example:
```console
python python/copy-scripts.py -i "test.tosc" -o "out.tosc" -s "source" -t "target"
```

### Example source and targets
![dlme2](https://user-images.githubusercontent.com/58243333/168412916-70d5f2ba-90b2-4f46-bc84-bce338ec3e1d.jpg)


## image-tosc

Convert a .jpg image to .tosc using small boxes as pixels. Currently using fixed inputs but in the future will generate from scratch.

### Usage

1. Set up a template where you have a "canvas" object on top level.
2. Open or Run image-tosc.py with arguments.
3. Open .tosc file.

Example:
```console
python python/image-tosc.py -i "test.tosc" -o "out.tosc" -j "logo.jpg" -t "canvas"
```

Use these for setting the image size.
```python
converter.image_size = 64
converter.pixel_size = 8
```
This means the image will be scaled down to 64x64 but the "pixel" boxes in Touch OSC will be of size 8.
I don't recommend going above 256x256 for image_size as performance and filesize take a hit. Plus the XML tree is stored in memory, not streamed, so it can cause issues when generating it.

### Example output:

![deleteme](https://user-images.githubusercontent.com/58243333/168332352-cb848b15-13fc-4573-861d-27b47f6da2ee.jpg)


To do: Working on other XML generation scripts that could simplify the template creation workflow.

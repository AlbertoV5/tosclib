# tosc-generate
Using XML trees to generate simple Touch OSC XML templates. Make sure to backup your .tosc files before hacking them.

Requirements:

```
python>=3.9
numpy==1.22.3
Pillow==9.1.0
```
## python/tosclib
Custom classes and functions that help navigate the structure of the .tosc file.
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

## python/custom-property.py
```console
python python/custom-property.py -i stuff/test2.tosc -o stuff/customProp.tosc --Property CustomProperty --Value 1612 --Type s
```
Turns out you can insert your own XML elements into Touch OSC files and the Editor will respect that. This means you can access those properties in lua and they will keep their values after you save and exit. For example:
```lua
--This is code inside the touch osc editor
function onValueChanged(key, value)
  if key == "touch" and self.values.touch == true then
    print(self.parent.CustomProperty) --prints 1612 to console
    self.parent.CustomProperty = self.parent.children.label2.values.text -- replaces 1612 with whatever value label2 has
  end
end
```
You can use custom-property.py to insert new properties in your .tosc file and use them as globals or config parameters. 

## python/copy-scripts.py
```console
python python/copy-scripts.py -i "stuff/test.tosc" -o "stuff/out.tosc" --Source "source" --Target "target"
```
Find a source object by name, copies its script and adds it to all children objects of a target object.

1. Set up a template where you a source object and a target group in top level.
2. Open or run copy-scripts.py with arguments.
3. Open .tosc file.

## python/image-tosc.py
```console
python python/image-tosc.py -i "stuff/test.tosc" -o "stuff/out.tosc" --Image "stuff/logo.jpg" --Target "canvas"
```
Convert a .jpg image to .tosc using small boxes as pixels. This will look for a Target group object to place the boxes into.

1. Set up a template where you have a "canvas" group on top level.
2. Open or run image-tosc.py with arguments.
3. Open .tosc file.

Use these for setting the image size.
```python
converter.image_size = 64
converter.pixel_size = 8
```
This means the image will be scaled down to 64x64 but the "pixel" boxes in Touch OSC will be of size 8.
I don't recommend going above 256x256 for image_size as performance and filesize take a hit. Plus the XML tree is stored in memory, not streamed, so it can cause issues when generating it.

### Example output:

![deleteme](https://user-images.githubusercontent.com/58243333/168332352-cb848b15-13fc-4573-861d-27b47f6da2ee.jpg)

## TO DO
Currently prototyping with Python but I want to move to a more performant Rust + JS or something stack in the future and adding Reaper -> xml -> tosc -> Reaper support. 

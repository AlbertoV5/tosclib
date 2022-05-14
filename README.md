# tosc-generate
 Using XML trees to generate simple Touch OSC XML templates.

Currently prototyping with Python but I want to move to a more performant Rust + JS or something stack in the future and adding Reaper -> xml -> tosc -> Reaper support. 

## copy-scripts

Find a source object by name, copies its script and adds it to all children objects of a target object.

### Usage

1. Set up a template so you have a source object and a target group.
2. Tweak and run copy-scripts.py
3. Open output with Touch OSC editor and save once.

All the tosc related xml functions are in toscNav.py. For example, fast stream pull:
```python
parser = ET.XMLPullParser()
with open(filePath, "r") as file:
    parser.feed(file.read())
    for _, e in parser.read_events(): # event, element
        if not e.find("properties"):
            continue
        if re.fullmatch(getValueFromKey(e, "properties", key),value):
            parser.close()
            return getValueFromKey(e, "properties", targetKey)
        
parser.close()
```
### Example source and targets:
![dlme2](https://user-images.githubusercontent.com/58243333/168412916-70d5f2ba-90b2-4f46-bc84-bce338ec3e1d.jpg)



## image-tosc

Convert a .jpg image to .tosc using small boxes as pixels. Currently using fixed inputs but in the future will generate from scratch.

### Usage

1. Install requirements.txt
2. Run convert.py
3. Use the UI for browsing .jpg and then hit Convert
4. Open output/output.tosc with the Touch OSC editor
5. Save it once

Use these for setting the image size.
```python
tosc.image_size = 64
tosc.pixel_size = 8
```
This means the image will be scaled down to 64x64 but the "pixel" boxes in Touch OSC will be of size 8.
I don't recommend going above 128x128 for image_size as performance and filesize take a hit. Plus the XML tree is stored in memory, not streamed, so it can cause issues when generating it.

### Example output:

![deleteme](https://user-images.githubusercontent.com/58243333/168332352-cb848b15-13fc-4573-861d-27b47f6da2ee.jpg)


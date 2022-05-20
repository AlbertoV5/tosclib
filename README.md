# tosc-generate

This repo contains info about **[tosclib](https://pypi.org/project/tosclib)** as well as demo projects that use it.

# [tosclib](https://tosc-generate.readthedocs.io/en/latest/)

```console
pip install tosclib
```

## Demo Projects:

Start with:
```console
$ git clone https://github.com/AlbertoV5/tosc-generate.git
$ cd tosc-generate
$ cd demos
$ pip install -r requirements.txt
```
## custom-property.py
You can insert your own XML elements into Touch OSC files and the Editor will respect them. This means you can access those properties in lua and they will keep their values after you save and exit the Touch OSC editor. For example:
```lua
--This is lua code inside the touch osc editor--
function onValueChanged(key, value)
  if key == "touch" and self.values.touch == true then
    print(self.parent.CustomProperty)
    self.parent.CustomProperty = self.parent.children.label2.values.text
  end
end
```
You can use custom-property.py to insert new properties in your .tosc file and use them as globals or config parameters. Console:
```console
$ python custom-property.py -i "files/test2.tosc" -o "files/customProp.tosc" --Property "CustomProperty" --Value "1612" --Type s
```

## copy-scripts.py
Find a source object by name in the top level of the template, copies its script and adds it to all children objects of a target object.
1. Set up a template where you a source object and a target group in top level.
Open or run copy-scripts.py with arguments.
2. Console:
```console
$ python copy-scripts.py -i "files/test.tosc" -o "files/out.tosc" --Source "source" --Target "target"
```
3. Open .tosc file.


## image-tosc.py

Convert a .jpg image to .tosc using small boxes as pixels. This will look for a Target group object to place the boxes into.

1. Set up a template where you have a "canvas" group on top level.
2. Console:
```console
$ python image-tosc.py -i "files/test.tosc" -o "files/out.tosc" --Image "files/logo.jpg" --Target "canvas"
```
3. Use the user interface to find new image and convert. 
4. Open .tosc file.

You want to change these if you want to change the image size.
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

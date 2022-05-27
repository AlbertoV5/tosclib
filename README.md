# tosclib
Generate and edit Touch OSC templates with XML trees through a few custom classes and functions that help navigate the structure of the .tosc file.

**Disclaimer**: This project has no relation to Hexler, the developer of TouchOSC. Backup your templates before editing them with third party tools.

![Test](https://github.com/albertov5/tosclib/actions/workflows/tests.yaml/badge.svg) ![pypi](https://img.shields.io/pypi/v/tosclib)
![License](https://img.shields.io/github/license/albertov5/tosclib)
![Pages](https://github.com/AlbertoV5/tosclib/actions/workflows/pages/pages-build-deployment/badge.svg)

## [Documentation here!](https://albertov5.github.io/tosclib)

Requires python >= 3.9

```console
$ pip install tosclib
```

# Contribute:

1. Clone Repo
```console
$ git clone https://github.com/{your-name}/tosclib.git
$ cd tosclib\src\tosclib
```
2. Make your changes.
3. Make a pull request :)


# Demo Projects:

```console
$ git clone https://github.com/AlbertoV5/tosclib.git
$ cd tosc-generate\demos
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
$ python custom-property.py -i "files/test2.tosc" -o "files/customProp.tosc" --Property "CustomProperty" --Value "1612" --Type "s"
```

## copy-scripts.py
Find a source object by name in the top level of the template, copies its script and adds it to all children objects of a target object.
1. Set up a template where you a source object and a target group in top level.
2. 
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

Change these if you want to change the image size.
```python
converter.image_size = 64
converter.pixel_size = 8
```
This means the image will be scaled down to 64x64 but the "pixel" boxes in Touch OSC will be of size 8.
I don't recommend going above 256x256 for image_size as performance and filesize take a hit. Plus the XML tree is stored in memory, not streamed, so it can cause issues when generating it.

### Example output:

![deleteme](https://user-images.githubusercontent.com/58243333/168332352-cb848b15-13fc-4573-861d-27b47f6da2ee.jpg)

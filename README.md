# tosclib
Generate and edit Touch OSC templates with XML trees through a few custom classes and functions that help navigate the structure of the .tosc file.

**Disclaimer**: This project has no relation to Hexler, the developer of TouchOSC. Backup your templates before editing them with third party tools.

![Test](https://github.com/albertov5/tosclib/actions/workflows/tests.yaml/badge.svg) ![pypi](https://img.shields.io/pypi/v/tosclib)
![License](https://img.shields.io/github/license/albertov5/tosclib)
![Pages](https://github.com/AlbertoV5/tosclib/actions/workflows/pages/pages-build-deployment/badge.svg)

## [Documentation here!](https://albertov5.github.io/tosclib)

```console
$ pip install tosclib
```

# Contribute:

Feel free to make a fork and contribute to the tosclib or documentation or whatever.

Requirements dev:

```python
tox==3.25.0
numpy==1.22.3
Pillow==9.1.1
pytest==7.1.2
setuptools==61.2.0
pytest-cov==3.0.0
```
Requirements docs:
```python
sphinx==4.5.0
furo==2022.4.7
sphinx_copybutton==0.5.0
```
For testing run:
```console
$ tox
```

# Design:
**0.3.0:**

elements -> controls -> tosc -> layout

- Elements are mostly data classes and enums (named tuples) that define the basic xml element parts, like valid attributes, children elements like: Property, Values, OSC and MIDI messages, etc.
- Controls are classes with specific attributes that are analogous to Touch OSC's Controls, like Fader, Button, Label, Group, etc. can be used as templates to construct xml trees.
- ElementTOSC is the wrapper class that handles the Control's xml tree: Node->(Properties, Messages, Values and Children). Tosclib is sort of built around it.
- Layout contains functions that help manipulate many ElementTOSC objects like automatic children arrangement, color gradients, copying properties, etc. 

Those are the basics, the goal is to build on top of that and have a solid 1.0 version with plenty of layout features and that can be fun to use.

In the future this could have "modules" or "templates" on top of "layout" which would consist of a few templates that can be built programatically with custom parameters, for example a pop up menu for entering digits or a radial menu for settings, etc.

# Demo Projects:

## New location for Demo Projects is [here](https://albertov5.github.io/tosclib/docs/build/html/demos.html).


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


## image-tosc.py

Convert a .jpg image to .tosc using small boxes as pixels. This will look for a Target group object to place the boxes into.

This means the image will be scaled down to 64x64 but the "pixel" boxes in Touch OSC will be of size 8.
I don't recommend going above 256x256 for image_size as performance and filesize take a hit. Plus the XML tree is stored in memory, not streamed, so it can cause issues when generating it.

### Example output:

![deleteme](https://user-images.githubusercontent.com/58243333/168332352-cb848b15-13fc-4573-861d-27b47f6da2ee.jpg)

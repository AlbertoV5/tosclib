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

## [Demo Projects here!](https://albertov5.github.io/tosclib/docs/build/html/demos.html)


# Design:

**0.5.0**

## Main Module

```py
import tosclib as tosc
```

**Data Structures**:
1. elements: type-hinted tuples.
2. controls: classes that follow a common Protocol.
3. etosc: wrapper class for xml elements.

**Factories**:
1. factory: creates elements.

**Converters**:
1. decode: xml -> control.
2. encode: control -> xml.

## Extra Modules

```py
from tosclib.properties import *
from tosclib.layout import *
```

**Factories**:
1. properties: creates specific properties with default values.

**Compositors**:
1. layout: arranges controls into tree structures.

**0.3.0:**

elements -> controls -> tosc -> layout

- Elements are mostly data classes and enums (named tuples) that define the basic xml element parts, like valid attributes, children elements like: Property, Values, OSC and MIDI messages, etc.
- Controls are classes with specific attributes that are analogous to Touch OSC's Controls, like Fader, Button, Label, Group, etc. can be used as templates to construct xml trees.
- ElementTOSC is the wrapper class that handles the Control's xml tree: Node->(Properties, Messages, Values and Children). Tosclib is sort of built around it.
- Layout contains functions that help manipulate many ElementTOSC objects like automatic children arrangement, color gradients, copying properties, etc. 

Those are the basics, the goal is to build on top of that and have a solid 1.0 version with plenty of layout features and that can be fun to use.

In the future this could have "modules" or "templates" on top of "layout" which would consist of a few templates that can be built programatically with custom parameters, for example a pop up menu for entering digits or a radial menu for settings, etc.


# To-do:

1. <s>Sort out tests for new design.</s>
2. <s>Change ElementTOSC class name to Node.</s>
3. <s>Fix docs for 0.5 (wip)</s>
4. <s>Add Default Propertiy Creator module.</s>
5. Cover all API documentation exhaustively.
6. Replace bad tests with better unit testing.
7. Convert demos to unit tests.


"""Property factory module"""
from pydantic import BaseModel
from .tosclib import Property as p

# # https://github.com/AlbertoV5/tosclib/blob/main/src/tosclib/controls.py
# class Defaults(BaseModel):
#     name = p("s", "name", "")
#     tag = p("s", "tag", "")
#     script = p("s", "script", "")
#     frame = p("r", "frame", (100, 100, 0, 0))
#     color = p("c", "color", (0.25, 0.25, 0.25, 1.0))
#     locked = p("b", "locked", False)
#     visible = p("b", "visible", True)
#     interactive = p("b", "interactive", True)
#     background = p("b", "background", True)
#     outline = p("b", "outline", True)
#     outlineStyle = p("i", "outlineStyle", 1)


# defaults = Defaults()

"""
Default Property Factories.

Extra resource to create type-hinted Properties with default values.
Based on: https://hexler.net/touchosc/manual/script-properties-and-values

"""
from typing import Literal, final

__all__ = [
    "PropsBox",
    "PropsButton",
    "PropsEncoder",
    "PropsFader",
    "PropsGrid",
    "PropsGroup",
    "PropsLabel",
    "PropsPage",
    "PropsPager",
    "PropsRadial",
    "PropsRadar",
    "PropsRadio",
    "PropsText",
    "PropsXy",
]


"""
"PRIVATE" CLASSES

General definitions that apply to more than one Control.
"""


class _ControlProperties:
    """Common properties across all Control Types
    https://hexler.net/touchosc/manual/script-properties-and-values"""

    @staticmethod
    def name(value: str = " ") -> tuple[Literal["name"], str]:
        """Control Tag. Any string."""
        return ("name", value)

    @staticmethod
    def tag(value: str = " ") -> tuple[Literal["tag"], str]:
        """Control Tag. Any string."""
        return ("tag", value)

    @staticmethod
    def script(value: str = " ") -> tuple[Literal["script"], str]:
        """Control Lua Script. Any string."""
        return ("script", value)

    @staticmethod
    def frame(
        value: tuple[int, ...] = (0, 0, 100, 100)
    ) -> tuple[Literal["frame"], tuple[int, ...]]:
        """Control Frame. x,y,w,h int tuple."""
        return ("frame", value)

    @staticmethod
    def color(
        value: tuple[float, ...] = (0.25, 0.25, 0.25, 1.0)
    ) -> tuple[Literal["color"], tuple[float, ...]]:
        """Control Color. r,g,b,a float tuple."""
        return ("color", value)

    @staticmethod
    def locked(value: bool = False) -> tuple[Literal["locked"], bool]:
        """Control locked in Editor or not."""
        return ("locked", value)

    @staticmethod
    def visible(value: bool = True) -> tuple[Literal["visible"], bool]:
        """Control visible or not."""
        return ("visible", value)

    @staticmethod
    def interactive(value: bool = True) -> tuple[Literal["interactive"], bool]:
        """Control responds to touch or not."""
        return ("interactive", value)

    @staticmethod
    def background(value: bool = True) -> tuple[Literal["background"], bool]:
        """Background visible or not."""
        return ("background", value)

    @staticmethod
    def outline(value: bool = True) -> tuple[Literal["outline"], bool]:
        """Outline visible or not."""
        return ("outline", value)

    @staticmethod
    def outlineStyle(
        value: Literal[0, 1, 2] = 1
    ) -> tuple[Literal["outlineStyle"], Literal[0, 1, 2]]:
        """Outline options. 0,1,2, = Full, Corner, Edges."""
        return ("outlineStyle", value)

    @staticmethod
    def grabFocus(value: bool = True) -> tuple[Literal["grabFocus"], bool]:
        """Gives up priority to overlayed controls. Groups are False."""
        return ("grabFocus", value)

    @staticmethod
    def pointerPriority(
        value: Literal[0, 1] = 0
    ) -> tuple[Literal["pointerPriority"], Literal[0, 1]]:
        """Priority for simultaneous touch. 0,1 = Oldest, Newest."""
        return ("pointerPriority", value)

    @staticmethod
    def cornerRadius(value: float = 0.0) -> tuple[Literal["cornerRadius"], float]:
        """Roundess or corners. Float from 0 to 10."""
        return ("cornerRadius", value)

    @staticmethod
    def orientation(
        value: Literal[0, 1, 2, 3] = 0
    ) -> tuple[Literal["orientation"], Literal[0, 1, 2, 3]]:
        """Control shape orientation. 0,1,2,3 = North, East, South, West."""
        return ("orientation", value)


class _BoxProperties:
    @staticmethod
    def shape(
        value: Literal[0, 1, 2, 3, 4, 5] = 0
    ) -> tuple[Literal["shape"], Literal[0, 1, 2, 3, 4, 5]]:
        """0,1,2,3,4,5 Rectangle, Circle, Triangle, Diamond, Pentagon, Hexagon"""
        return ("shape", value)


class _GridProperties:
    @staticmethod
    def grid(value: bool = True) -> tuple[Literal["grid"], bool]:
        """Grid visible or not."""
        return ("grid", value)

    @staticmethod
    def gridSteps(value: int = 10) -> tuple[Literal["gridSteps"], int]:
        """Number of grid steps."""
        return ("gridSteps", value)


class _ResponseProperties:
    @staticmethod
    def response(value: Literal[0, 1] = 0) -> tuple[Literal["response"], Literal[0, 1]]:
        """Control's Message response. 0,1 = Absolute, Relative"""
        return ("response", value)

    @staticmethod
    def responseFactor(value: int = 100) -> tuple[Literal["responseFactor"], int]:
        """How much the Control's Value responds to touch. An int from 1 to 100."""
        return ("responseFactor", value)


class _CursorProperties:
    @staticmethod
    def cursor(value: bool = True) -> tuple[Literal["cursor"], bool]:
        """If the Control's cursor is visible or not."""
        return ("cursor", value)

    @staticmethod
    def cursorDisplay(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["cursorDisplay"], Literal[0, 1, 2]]:
        """Cursor display. 0, 1, 2 = always, active, inactive"""
        return ("cursorDisplay", value)


class _LineProperties:
    @staticmethod
    def lines(value: bool = True) -> tuple[Literal["lines"], bool]:
        """If lines on the Control are visible or not."""
        return ("lines", value)

    @staticmethod
    def linesDisplay(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["linesDisplay"], Literal[0, 1, 2]]:
        """Cursor display 0, 1, 2 = always, active, inactive"""
        return ("linesDisplay", value)


class _XyProperties:
    @staticmethod
    def lockX(value: bool = False) -> tuple[Literal["lockX"], bool]:
        """Locks the X axis or not."""
        return ("lockX", value)

    @staticmethod
    def lockY(value: bool = False) -> tuple[Literal["lockY"], bool]:
        """Locks the Y axis or not."""
        return ("lockY", value)

    @staticmethod
    def gridX(value: bool = True) -> tuple[Literal["gridX"], bool]:
        """Grid on X Axis is visible or not."""
        return ("gridX", value)

    @staticmethod
    def gridY(value: bool = True) -> tuple[Literal["gridY"], bool]:
        """Grid on Y Axis is visible or not."""
        return ("gridY", value)

    @staticmethod
    def gridStepsX(value: int = 10) -> tuple[Literal["gridStepsX"], int]:
        """Number of steps on grid on X axis."""
        return ("gridStepsX", value)

    @staticmethod
    def gridStepsY(value: int = 10) -> tuple[Literal["gridStepsY"], int]:
        """Number of steps on grid on X axis."""
        return ("gridStepsY", value)


class _TextProperties:
    @staticmethod
    def font(value: Literal[0, 1] = 0) -> tuple[Literal["font"], Literal[0, 1]]:
        """0, 1 = default, monospaced"""
        return ("font", value)

    @staticmethod
    def textSize(value: int = 14) -> tuple[Literal["textSize"], int]:
        """Font size. Any int."""
        return ("textSize", value)

    @staticmethod
    def textColor(
        value: tuple[float, ...] = (1.0, 1.0, 1.0, 1.0)
    ) -> tuple[Literal["textColor"], tuple[float, ...]]:
        """Font color. Tuple of r,g,b,a floats."""
        return ("textColor", value)

    @staticmethod
    def textAlignH(
        value: Literal[1, 2, 3] = 2
    ) -> tuple[Literal["textAlignH"], Literal[1, 2, 3]]:
        """1,2,3 = left, center, right"""
        return ("textAlignH", value)


"""
PUBLIC CLASSES

Controls with specific methods and different defaults.
"""


class PropsBox(_ControlProperties, _BoxProperties):
    pass


class PropsButton(_ControlProperties, _BoxProperties):
    @staticmethod
    def buttonType(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["buttonType"], Literal[0, 1, 2]]:
        """0,1,2 = Momentary, Toggle_Release, Toggle_Press"""
        return ("buttonType", value)

    @staticmethod
    def press(value: bool = True) -> tuple[Literal["press"], bool]:
        """Enable or Disable response to Press (rise)."""
        return ("press", value)

    @staticmethod
    def release(value: bool = True) -> tuple[Literal["release"], bool]:
        """Enable or Disable response to Release (fall)."""
        return ("release", value)

    @staticmethod
    def valuePosition(value: bool = False) -> tuple[Literal["valuePosition"], bool]:
        """Button Value follows the touch/pointer x, y position."""
        return ("valuePosition", value)


class PropsLabel(_ControlProperties, _TextProperties):
    @staticmethod
    def textLength(value: int = 14) -> tuple[Literal["textLength"], int]:
        """How much text is showed at once. 0 is infinite."""
        return ("textLength", value)

    @staticmethod
    def textClip(value: bool = True) -> tuple[Literal["textClip"], bool]:
        """Text is clipped at end of label or not."""
        return ("textClip", value)


class PropsText(_ControlProperties, _TextProperties):
    pass


class PropsEncoder(_ControlProperties, _ResponseProperties, _GridProperties):
    @staticmethod
    def outlineStyle(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["outlineStyle"], Literal[0, 1, 2]]:
        """Outline options. 0,1,2, = Full, Corner, Edges."""
        return ("outlineStyle", value)


class PropsFader(
    _ControlProperties, _ResponseProperties, _GridProperties, _CursorProperties
):
    @staticmethod
    def bar(value: bool = True) -> tuple[Literal["bar"], bool]:
        """Shows Fader bar or not."""
        return ("bar", value)

    @staticmethod
    def barDisplay(
        value: Literal[0, 1, 2]
    ) -> tuple[Literal["barDisplay"], Literal[0, 1, 2]]:
        """Same as Cursor display. 0, 1, 2 = always, active, inactive"""
        return ("barDisplay", value)


class PropsRadial(
    _ControlProperties,
    _ResponseProperties,
    _GridProperties,
    _CursorProperties,
):
    @staticmethod
    def outlineStyle(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["outlineStyle"], Literal[0, 1, 2]]:
        """Outline options. 0,1,2, = Full, Corner, Edges."""
        return ("outlineStyle", value)

    @staticmethod
    def inverted(value: bool = False) -> tuple[Literal["inverted"], bool]:
        """Radial orientation is inverted or not."""
        return ("inverted", value)

    @staticmethod
    def centered(value: bool = False) -> tuple[Literal["centered"], bool]:
        """Radial is centered or not."""
        return ("centered", value)


class PropsRadar(
    _ControlProperties,
    _CursorProperties,
    _LineProperties,
    _XyProperties,
):
    pass


class PropsRadio(_ControlProperties):
    @staticmethod
    def steps(value: int = 5) -> tuple[Literal["steps"], int]:
        """Amount of radio steps/boxes."""
        return ("steps", value)

    @staticmethod
    def radioType(value: Literal[0, 1]) -> tuple[Literal["radioType"], Literal[0, 1]]:
        """Radio behaves as: 0,1 = select, meter"""
        return ("radioType", value)


class PropsGroup(_ControlProperties):
    @staticmethod
    def outlineStyle(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["outlineStyle"], Literal[0, 1, 2]]:
        """0,1,2, = Full, Corner, Edges"""
        return ("outlineStyle", value)

    @staticmethod
    def grabFocus(value: bool = False) -> tuple[Literal["grabFocus"], bool]:
        """Groups give up priority to children controls."""
        return ("grabFocus", value)


class PropsGrid(_ControlProperties):
    @staticmethod
    def grabFocus(value: bool = False) -> tuple[Literal["grabFocus"], bool]:
        """Groups give up priority to children controls."""
        return ("grabFocus", value)

    @staticmethod
    def exclusive(value: bool = False) -> tuple[Literal["exclusive"], bool]:
        """Makes it so only one child can be non-zero at a time."""
        return ("exclusive", value)

    @staticmethod
    def gridNaming(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["gridNaming"], Literal[0, 1, 2]]:
        """0,1,2 = Index, Column, Row"""
        return ("gridNaming", value)

    @staticmethod
    def gridOrder(
        value: Literal[0, 1] = 0
    ) -> tuple[Literal["gridOrder"], Literal[0, 1]]:
        """0,1 = Row, Column"""
        return ("gridOrder", value)

    @staticmethod
    def gridStart(
        value: Literal[0, 1, 2, 3] = 0
    ) -> tuple[Literal["gridStart"], Literal[0, 1, 2, 3]]:
        """0,1,2,3 = Top left, Top right, Bottom Left, Bottom Right"""
        return ("gridStart", value)

    @staticmethod
    def gridType(
        value: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8] = 4
    ) -> tuple[Literal["gridType"], Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]]:
        """Children Control Type.
        0 = BOX,
        1 = BUTTON,
        2 = LABEL,
        3 = TEXT,
        4 = FADER,
        5 = XY,
        6 = RADIAL,
        7 = ENCODER,
        8 = RADAR"""
        return ("gridType", value)

    @staticmethod
    def gridX(value: int = 2) -> tuple[Literal["gridX"], int]:
        """amount of elements on X"""
        return ("gridX", value)

    @staticmethod
    def gridY(value: int = 2) -> tuple[Literal["gridY"], int]:
        """amount of elements on Y"""
        return ("gridY", value)


class PropsPager(_ControlProperties):
    @staticmethod
    def outlineStyle(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["outlineStyle"], Literal[0, 1, 2]]:
        """0,1,2, = Full, Corner, Edges"""
        return ("outlineStyle", value)

    @staticmethod
    def grabFocus(value: bool = False) -> tuple[Literal["grabFocus"], bool]:
        """Groups give up priority to children controls."""
        return ("grabFocus", value)

    @staticmethod
    def tabLabels(value: bool = True) -> tuple[Literal["tabLabels"], bool]:
        """Show tab labels or not."""
        return ("tabLabels", value)

    @staticmethod
    def tabbar(value: bool = True) -> tuple[Literal["tabbar"], bool]:
        """Show tab bars or not."""
        return ("tabbar", value)

    @staticmethod
    def tabbarDoubleTap(value: bool = True) -> tuple[Literal["tabbarDoubleTap"], bool]:
        """Makes so switching tabs requires double tap or not."""
        return ("tabbarDoubleTap", value)

    @staticmethod
    def tabbarSize(value: int = 40) -> tuple[Literal["tabbarSize"], int]:
        """Size of bar. An int from 10 to 300"""
        return ("tabbarSize", value)

    @staticmethod
    def textSizeOff(value: int = 14) -> tuple[Literal["textSizeOff"], int]:
        """Size of bar text when off. Any int."""
        return ("textSizeOff", value)

    @staticmethod
    def textSizeOn(value: int = 14) -> tuple[Literal["textSizeOn"], int]:
        """Size of bar text when on. Any int."""
        return ("textSizeOn", value)


class PropsPage(_ControlProperties):
    @staticmethod
    def outlineStyle(
        value: Literal[0, 1, 2] = 0
    ) -> tuple[Literal["outlineStyle"], Literal[0, 1, 2]]:
        """0,1,2, = Full, Corner, Edges"""
        return ("outlineStyle", value)

    @staticmethod
    def grabFocus(value: bool = False) -> tuple[Literal["grabFocus"], bool]:
        """Groups give up priority to children controls."""
        return ("grabFocus", value)

    @staticmethod
    def name(value: str = "1") -> tuple[Literal["name"], str]:
        """Page name. Please add programmatically by index."""
        return ("name", value)

    @staticmethod
    def tabLabel(value: str = "1") -> tuple[Literal["tabLabel"], str]:
        """Page label. Please add programmatically by index."""
        return ("tabLabel", value)

    @staticmethod
    def tabColorOff(
        value: tuple[float, ...] = (0.25, 0.25, 0.25, 1.0)
    ) -> tuple[Literal["tabColorOff"], tuple[float, ...]]:
        """Page Color when off. r,g,b,a float tuple."""
        return ("tabColorOff", value)

    @staticmethod
    def tabColorOn(
        value: tuple[float, ...] = (0.0, 0.0, 0.0, 1.0)
    ) -> tuple[Literal["tabColorOn"], tuple[float, ...]]:
        """Page Color when on. r,g,b,a float tuple."""
        return ("tabColorOn", value)

    @staticmethod
    def textColorOff(
        value: tuple[float, ...] = (1.0, 1.0, 1.0, 1.0)
    ) -> tuple[Literal["textColorOff"], tuple[float, ...]]:
        """Text Color when Page off. r,g,b,a float tuple."""
        return ("textColorOff", value)

    @staticmethod
    def textColorOn(
        value: tuple[float, ...] = (1.0, 1.0, 1.0, 1.0)
    ) -> tuple[Literal["textColorOn"], tuple[float, ...]]:
        """Text Color when Page on. r,g,b,a float tuple."""
        return ("textColorOn", value)


class PropsXy(
    _ControlProperties,
    _ResponseProperties,
    _CursorProperties,
    _XyProperties,
):
    pass

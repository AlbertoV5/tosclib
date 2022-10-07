"""
Template Module
"""
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from pathlib import Path
import xmltodict
import zlib

from . import control


class Root(BaseModel):
    """Model for the XML root. Kept for structural consistency with XML.
    The Control is named 'node' in the XML.
    """

    at_version: float = 3.0
    node: control.Control = Field(default_factory=lambda: control.Control())

    class Config:
        validate_assignment = True


class Template:
    """Represents a .tosc file.

    It will parse and unparse the data from XML to Pydantic models and back.
    It doesn't deal with the structural content of the file and will keep a Root model
    before the first Control.

    Example:

        .. code-block::

            t = Template('myfile.tosc')
            msg = Midi()
            t.root.node[0].messages.append(msg)
            t.save('newfile.tosc')
    """

    root: Root
    id: UUID
    encoding: str = "UTF-8"

    def __init__(self, source: str | Path | Root | None = None):
        """Load a compressed .tosc or uncompressed .xml file and parse it.
        From XML to dictionary to Pydantic models.

        If filepath is None, it will create a new Template from a default Root.
        Can raise Type Error if source is not compatible type.

        Args:
            source (str | Path | Root | None, optional): File or Root object. Defaults to None.
        """
        if isinstance(source, Root):
            self.root = source
            return None
        elif source is None:
            self.root = Root()
            return None
        elif isinstance(source, str):
            ext = f".{source.split('.')[1]}"
        elif isinstance(source, Path):
            ext = source.suffix
        else:
            raise TypeError(f"{source} is not a valid source.")
        with open(source, "rb") as file:
            self.root = Root(
                **xmltodict.parse(
                    zlib.decompress(file.read()) if ext == ".tosc" else file.read(),
                    attr_prefix="at_",
                    postprocessor=self.decode_postprocessor,
                    encoding=self.encoding,
                    force_list=["midi", "osc", "local", "gamepad"],
                )["lexml"]
            )
        self.id = self.root.node.at_ID

    def dump(self, filepath: str, pretty=True):
        """Write uncompressed .xml file.

        Args:
            filepath (str): XML file path.
        """
        with open(filepath, "w") as file:
            xmltodict.unparse(
                {"lexml": self.root.dict()},
                pretty=pretty,
                indent="  ",
                attr_prefix="at_",
                preprocessor=self.encode_preprocessor,
                output=file,
                encoding=self.encoding,
            )

    def dumps(self, pretty=True):
        """Returns a string representation.

        Returns:
            (str): XML string.
        """
        return xmltodict.unparse(
            {"lexml": self.root.dict()},
            pretty=pretty,
            indent="  ",
            attr_prefix="at_",
            preprocessor=self.encode_preprocessor,
            encoding=self.encoding,
        )

    def save(self, filepath: str):
        """Write contents to a compressed file.

        Args:
            filepath (str): File path.
        """
        with open(filepath, "wb") as file:
            file.write(
                zlib.compress(
                    xmltodict.unparse(
                        {"lexml": self.root.dict()},
                        attr_prefix="at_",
                        preprocessor=self.encode_preprocessor,
                        encoding=self.encoding,
                    ).encode(self.encoding)
                )
            )

    def __repr__(self):
        return f"Template with Control ID: {self.root.node.at_ID}"

    def copy(self):
        """Create a new Template object and call Pydantic's deep copy on the root."""
        return Template(self.root.copy(deep=True))

    def decode_postprocessor(self, path: tuple, key: str, value: str):
        """Reorganize and process elements based on path patterns.

        Args:
            path (tuple): The structure of the path to the element.
            key (str): The key of the element, tag.
            value (str): The value of the element, text, attr.

        Returns:
            str, Any: Modified key, value structure.
        """
        match path[-1]:
            case ("properties", None):
                return key, value["property"]
            case ("children", None):
                return key, value["node"] if isinstance(value["node"], list) else [
                    value["node"]
                ]

        match path[-2:]:
            case ((_, {"type": "c"}), ("value", None)):
                return key, tuple(value[k] for k in dict(value))
            case ((_, {"type": "r"}), ("value", None)):
                return key, tuple(value[k] for k in dict(value))
            case (("node", _), ("values", None)):
                return key, value["value"] if isinstance(value["value"], list) else [
                    value["value"]
                ]
            case (_, ("path" | "arguments", None)):
                return key, value["partial"] if isinstance(
                    value["partial"], list
                ) else [value["partial"]]
            case (_, ("triggers", None)):
                return key, value["trigger"] if isinstance(
                    value["trigger"], list
                ) else [value["trigger"]]
            case (("midi", None), ("values", _)):
                return key, value["value"]
        return key, value

    def encode_preprocessor(self, key: str, value: str):
        """Prepare encoding by key, value pattern matching.
        Reverts the processing done from the encoding function.

        Args:
            key (str): Dictionary key from pydantic model attr.
            value (str): Dictionary value.

        Returns:
            (tuple): key, value pair with value modified.

        Description:
            The callback doesn't provide a path because the data is a dictionary
            so we only have key, value to match against element tag and content.
        """
        match key, value:
            case ("properties", list()):
                return key, {"property": value}
            case ("values", list()):
                return key, {"value": value}
            case ("children", list()):
                return key, {"node": value}
            case ("triggers", list()):
                return key, {"trigger": value}
            case ("path" | "arguments", list()):
                return key, {"partial": value}
            case ("value", (float(), float(), float(), float())):
                return key, {"r": value[0], "g": value[1], "b": value[2], "a": value[3]}
            case ("value", (int(), int(), int(), int())):
                return key, {"x": value[0], "y": value[1], "w": value[2], "h": value[3]}
            case ("value" | "locked" | "lockedDefaultCurrent", bool()):
                return key, "0" if value == False else "1"
        return key, value

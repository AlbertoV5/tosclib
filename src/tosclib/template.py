"""
Template Module
"""
from pathlib import Path
from bson import ObjectId
import xmltodict
import zlib

from .control import Control


class Template:
    """Represents a .tosc file.

    It will parse and unparse the data from XML to Pydantic models.

    Template
        |___version
        |___encoding
        |___control
            |___properties
            |___values
            |___messages
            |___children
                |___control
                |___...

    Example:

        .. code-block::

            t = Template('myfile.tosc')
            msg = Midi()
            t.root[0].messages.append(msg)
            t.save('newfile.tosc')
    """

    # root: Root
    at_version: float = 3.0
    encoding: str = "UTF-8"
    control: Control

    def __init__(
        self, source: str | Path | Control | dict | None = None, encoding: str = "UTF-8"
    ):
        """Load a .tosc or .xml file and parse it. Use xmltodict to Pydantic models.

        Depending on the source type, it will either:

        1. None: Create an empty Control and attach it to the Template.
        2. Control: Attach given Control to the Template.
        3. dict: Create new data and Control via the Control constructor, pydantic validates it.
        4. Path | str: Load file from filepath and parse it.
        5. Other: Raise TypeError.

        Args:
            source (str | Path | Control, optional): File or Control object. Defaults to None.
            encoding (str): Defaults to "UTF-8".
        """
        self.encoding = encoding
        match source:
            case None:
                self.control = Control()
                return
            case Control():
                self.control = source
                return
            case dict():
                self.at_version: float = source["lexml"]["at_version"]
                self.control: Control = Control(**source["lexml"]["node"])
                return
            case str():
                ext = f".{source.split('.')[1]}"
            case Path():
                ext = source.suffix
            case _:
                raise TypeError(f"{source} is not a valid source.")

        with open(source, "rb") as file:
            data = xmltodict.parse(
                zlib.decompress(file.read()) if ext == ".tosc" else file.read(),
                attr_prefix="at_",
                postprocessor=self.decode_postprocessor,
                encoding=self.encoding,
                force_list=["midi", "osc", "local", "gamepad"],
            )
            self.at_version: float = data["lexml"]["at_version"]
            self.control: Control = Control(**data["lexml"]["node"])

    def dumps(self, pretty=True):
        """Returns a string representation.

        Returns:
            (str): XML string.
        """
        return xmltodict.unparse(
            self.dict(),
            pretty=pretty,
            indent="  ",
            attr_prefix="at_",
            preprocessor=self.encode_preprocessor,
            encoding=self.encoding,
        )

    def save(self, filepath: str | Path, xml: bool = False, pretty: bool = True):
        """Write Template data to a .tosc file.

        Args:
            filepath (str | Path): Filepath with whatever suffix.
            xml (bool, optional): If also writes an XML file. Defaults to False.
            pretty (bool, optional): If indent XML file. Defaults to True.
        """
        if isinstance(filepath, str):
            filepath = Path(filepath)
        with open(filepath.with_suffix(".tosc"), "wb") as file:
            file.write(
                zlib.compress(
                    xmltodict.unparse(
                        self.dict(),
                        attr_prefix="at_",
                        preprocessor=self.encode_preprocessor,
                        encoding=self.encoding,
                    ).encode(self.encoding)
                )
            )
        if xml:
            with open(filepath.with_suffix(".xml"), "w") as file:
                xmltodict.unparse(
                    self.dict(),
                    pretty=pretty,
                    indent="  ",
                    attr_prefix="at_",
                    preprocessor=self.encode_preprocessor,
                    output=file,
                    encoding=self.encoding,
                )

    def dict(self, with_id: bool = False):
        """Returns a dictionary of the Template.

        Args:
            with_id (bool, Optional): Includes self.node.at_ID as _id value for mongo databases. Default False.
        """
        if with_id:
            return {
                "_id": self.control.at_ID,
                "lexml": {"at_version": self.at_version, "node": self.control.dict()},
            }
        return {"lexml": {"at_version": self.at_version, "node": self.control.dict()}}

    def __repr__(self):
        return f"Template with Root Control ID: {self.control.at_ID}"

    def copy(self):
        """Create a new Template object and call Pydantic's deep copy on the root."""
        return Template(self.control.copy(deep=True))

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

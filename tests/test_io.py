import unittest
import tosclib as tosc
import pytest
import sys
from pathlib import Path


class TestTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = Path(__file__).absolute().parent / "files"
        try:
            Path.mkdir(cls.directory)
        except FileExistsError:
            [Path.unlink(file) for file in cls.directory.iterdir()]
            cls.directory.rmdir()
            Path.mkdir(cls.directory)

        cls.fileName = "test.tosc"
        cls.root = tosc.createTemplate()
        cls.template = tosc.ElementTOSC(cls.root[0])
        cls.template.createChild("GROUP")
        assert cls.template.createProperty("b", "background", "0")
        assert cls.template.setColor(0, 0, 0, 1)
        assert cls.template.createProperty("f", "cornerRadius", "0")
        assert cls.template.setFrame(0, 0, 640, 860)
        assert cls.template.createProperty("b", "grabFocus", "0")
        assert cls.template.createProperty("b", "interactive", "0")
        assert cls.template.createProperty("b", "locked", "0")
        assert cls.template.createProperty("i", "orientation", "0")
        assert cls.template.createProperty("b", "outline", "1")
        assert cls.template.createProperty("i", "outlineStyle", "0")
        assert cls.template.createProperty("i", "pointerPriority", "0")
        assert cls.template.createProperty("i", "shape", "1")
        assert cls.template.createProperty("b", "visible", "1")
        assert cls.template.createValue(tosc.Value("touch", "0", "0", "false", "0"))
        tosc.write(cls.root, cls.directory / cls.fileName)

    def test_change_properties(self):
        (x, y, w, h) = (0, 0, 1920, 1080)
        assert self.template.setFrame(x, y, w, h)
        self.assertEqual(self.template.getPropertyParam("frame", "w").text, str(w))
        self.assertEqual(self.template.getPropertyParam("frame", "h").text, str(h))

    def test_from_file(self):
        self.assertIsInstance(
            tosc.ElementTOSC.fromFile(self.directory / self.fileName), tosc.ElementTOSC
        )

    @classmethod
    def tearDownClass(cls):
        [Path.unlink(file) for file in cls.directory.iterdir()]
        cls.directory.rmdir()
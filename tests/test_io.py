import unittest
import tosclib as tosc
from pathlib import Path
from tosclib import Property
from tosclib.elements import ControlType
from .profiler import profile


class TestTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = Path(__file__).absolute().parent / "files"

        if Path.is_dir(cls.directory):
            [Path.unlink(file) for file in cls.directory.iterdir()]
            cls.directory.rmdir()

        Path.mkdir(cls.directory)

        cls.fileName = "test.tosc"
        cls.root = tosc.createTemplate()
        cls.template = tosc.ElementTOSC(cls.root[0])
        tosc.write(cls.root, cls.directory / cls.fileName)

    @profile
    def test_io(self):
        self.assertIsInstance(
            tosc.ElementTOSC.fromFile(self.directory / self.fileName), tosc.ElementTOSC
        )
        self.template.createChild(ControlType.GROUP)
        assert self.template.createProperty(Property("b", "background", "0"))
        assert self.template.setColor((0, 0, 0, 1))
        assert self.template.createProperty(Property("f", "cornerRadius", "0"))
        assert self.template.setFrame((0, 0, 640, 860))
        assert self.template.createProperty(Property("b", "grabFocus", "0"))
        assert self.template.createProperty(Property("b", "interactive", "0"))
        assert self.template.createProperty(Property("b", "locked", "0"))
        assert self.template.createProperty(Property("i", "orientation", "0"))
        assert self.template.createProperty(Property("b", "outline", "1"))
        assert self.template.createProperty(Property("i", "outlineStyle", "0"))
        assert self.template.createProperty(Property("i", "pointerPriority", "0"))
        assert self.template.createProperty(Property("i", "shape", "1"))
        assert self.template.createProperty(Property("b", "visible", "1"))
        assert self.template.createValue(tosc.Value("touch", "0", "0", "false", "0"))
        (x, y, w, h) = (0, 0, 1920, 1080)
        assert self.template.setFrame((x, y, w, h))
        self.assertEqual(self.template.getPropertyParam("frame", "w").text, str(w))
        self.assertEqual(self.template.getPropertyParam("frame", "h").text, str(h))

    @classmethod
    def tearDownClass(cls):
        [Path.unlink(file) for file in cls.directory.iterdir()]
        cls.directory.rmdir()

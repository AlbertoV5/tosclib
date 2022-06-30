import logging
import unittest
import tosclib as tosc
from pathlib import Path
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
        cls.template = tosc.Node(cls.root[0])
        tosc.write(cls.root, cls.directory / cls.fileName)

    @profile
    def test_io(self):
        self.template.children.append(tosc.xml_control(tosc.Group()))
        assert self.template.set_prop(("background", False))
        assert self.template.set_prop(("color", (0.0, 0.0, 0.0, 1.0)))
        assert self.template.set_prop(("cornerRadius", 0.0))
        assert self.template.set_prop(("frame", (0, 0, 640, 860)))
        assert self.template.set_prop(("grabFocus", False))
        assert self.template.set_prop(("interactive", False))
        assert self.template.set_prop(("shape", 1))
        assert self.template.set_prop(("outlineStyle", 0))
        assert self.template.add_value(tosc.value("touch", False, False, True, 0))
        frame = (x, y, w, h) = (0, 0, 1920, 1080)
        assert self.template.set_prop(("frame", frame))
        self.assertEqual(self.template.get_prop("frame")[1][2], w)
        self.assertEqual(self.template.get_prop("frame")[1][3], h)

    @classmethod
    def tearDownClass(cls):
        [Path.unlink(file) for file in cls.directory.iterdir()]
        cls.directory.rmdir()

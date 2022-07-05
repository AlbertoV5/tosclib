import inspect
import logging
import tosclib as tosc
from tosclib.controls import NOT_PROPERTIES
from .profiler import profile
import unittest
from pathlib import Path


class Replacer(unittest.TestCase):
    input_path: Path = Path("docs/demos/files/msgs.tosc")
    output_path: Path = Path("docs/demos/files/msgs_out.tosc")
    eroot: tosc.Element
    ebutton: tosc.Element
    ebutton_new: tosc.Element
    button: tosc.Control
    button2: tosc.Control
    frame: tosc.Property
    msgs: tosc.Messages
    eframe: tosc.Element
    emidi: tosc.Element

    def load_file(self):
        self.eroot = tosc.load(self.input_path)
        self.assertIsNotNone(self.eroot)

    def find_button_with_osc_msg(self):
        self.ebutton = self.eroot.find(".//node[@type='BUTTON']/messages/osc/../..")
        self.assertIsNotNone(self.ebutton)

    def decode_xml_to_ctrl(self):
        self.button = tosc.to_ctrl(self.ebutton)
        self.assertIsNotNone(self.button)

    def get_ctrl_attributes(self):
        self.frame = self.button.get_prop("frame")
        self.msgs = self.button.messages
        self.assertGreater(len(self.frame[1]), 0)
        self.assertGreater(len(self.msgs), 0)

    def modify_ctrl_attributes(self):
        self.button.set_prop(("frame", (50, 50, 450, 300)))
        self.msgs.append(tosc.midi())
        self.assertEqual(self.button.get_prop("frame")[1][3], 300)
        self.assertEqual(self.msgs[-1][0], "midi")

    def convert_ctrl_attributes_to_xml(self):
        self.eframe = tosc.xml_property(self.frame)
        self.emidi = tosc.xml_message(self.msgs[-1])
        self.assertNotEqual(self.eframe.tag, "none")
        self.assertNotEqual(self.emidi.tag, "none")

    def get_button2_as_ctrl(self):
        self.button2 = tosc.to_ctrl(self.ebutton)
        self.assertIsNotNone(self.button2)

    def compare_buttons_as_ctrls(self):
        for attr1, attr2 in zip(vars(self.button), vars(self.button2)):
            b1, b2 = getattr(self.button, attr1), getattr(self.button2, attr2)
            if attr1 in tosc.NOT_PROPERTIES:
                if attr1 == "messages":
                    self.assertNotEqual(b1, b2)
                else:
                    self.assertEqual(b1, b2)
            else:
                if attr1 == "frame":
                    self.assertNotEqual(b1, b2)
                else:
                    self.assertEqual(b1, b2)

    def add_custom_properties_to_button(self):
        self.assertIsInstance(
            self.button.set_prop(("custom1", "12345"))
            .set_prop(("verified", True))
            .set_prop(("color2", (0.1, 0.5, 1.0, 1.0)))
            .set_prop(("frame2", (0, 1, 500, 500))),
            tosc.Button,
        )

    def convert_button_to_xml(self):
        self.ebutton_new = tosc.xml_control(self.button)
        self.assertNotEqual(self.ebutton.tag, "none")

    def replace_new_button_in_root(self):
        prop = self.ebutton_new.find(".//property/[key='verified']")
        self.assertEqual(prop[0].text, "verified")
        self.assertEqual(prop[1].text, "1")
        tosc.replace_element(self.ebutton, self.ebutton_new)
        prop = self.ebutton.find(".//property/[key='verified']")
        self.assertEqual(prop[0].text, "verified")
        self.assertEqual(prop[1].text, "1")

    def write_file(self):
        self.assertTrue(tosc.write(self.eroot, self.output_path))

    @profile
    def test_replacer(self):
        self.load_file()
        self.find_button_with_osc_msg()
        self.decode_xml_to_ctrl()
        self.get_ctrl_attributes()
        self.modify_ctrl_attributes()
        self.convert_ctrl_attributes_to_xml()
        self.get_button2_as_ctrl()
        self.compare_buttons_as_ctrls()
        self.add_custom_properties_to_button()
        self.convert_button_to_xml()
        self.replace_new_button_in_root()
        self.write_file()

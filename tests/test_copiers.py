from copy import deepcopy
import logging
from multiprocessing.sharedctypes import Value
from tokenize import group
import tosclib as tosc
from tosclib.properties import *
import pytest
from .profiler import profile
import inspect
import unittest

class Copier(unittest.TestCase):
    """Create different groups, copy attrs and compare them."""
    template1: tosc.Control
    template2: tosc.Control
    group1: tosc.Control
    group2: tosc.Control
    proplist1: list = []
    proplist2: list = []

    def create_different_groups(self):
        self.template1 = tosc.Group(name = "template1", frame = (0,0,800,800))
        self.template2 = tosc.Group(name = "template2")
        self.group1 = tosc.Group(name = "group1", frame = (0,0,400,400))
        self.group2 = tosc.Group(name ="group2")
        self.template1.children.append(self.group1)
        self.template2.children.append(self.group2)

    def create_properties_for_group1(self):
        for func in inspect.getmembers(PropsGroup, predicate=inspect.isfunction):
            if "__" not in func[0]:
                p = func[1]()
                self.proplist1.append(p)
                assert self.group1.set_prop(p)

    def copy_properties_from_group1_to_group2(self):
        assert self.group1 is not self.group2
        assert tosc.copy_properties(self.group1, self.group2)
        assert self.proplist1.sort() == self.proplist2.sort()

    def assert_properties_of_group2(self):
        for p in vars(self.group2):
            if p not in tosc.NOT_PROPERTIES:
                prop = getattr(self.group2, p)
                self.proplist2.append(p)
                assert self.group2.get_prop(p) == prop

    def create_values_for_group1(self):
        val_keys = ("touch", "x", "y", "text")
        val_defs = (False, 0.0, 0.55, "test")
        values = [
            tosc.value(val_keys[0], default = val_defs[0]),
            tosc.value(val_keys[1], True, True, val_defs[1], 100),
            tosc.value(val_keys[2], True, False, val_defs[2], 50),
            tosc.value(val_keys[3], False, False, val_defs[3], 0),
        ]
        self.group1.values = values
        for v,k,d in zip(self.group1.values, val_keys, val_defs):
            assert v
            assert v[0] == k
            assert v[3] == d

    def copy_values_from_group1_to_group2(self):
        tosc.copy_values(self.group1, self.group2)
        assert self.group1.values.sort() == self.group2.values.sort()

    def create_messages_for_group1(self):
        msg_keys = ("osc", "midi", "local")
        messages = [
            tosc.osc(),
            tosc.midi(),
            tosc.local()
        ]
        self.group1.messages = messages
        for m, k in zip(self.group1.messages, msg_keys):
            assert m
            assert m[0] == k

    def copy_messages_from_group1_to_group2(self):
        tosc.copy_messages(self.group1, self.group2)
        assert self.group1.messages.sort() == self.group2.messages.sort()

    def remove_osc_messages_from_group1(self):
        for m in deepcopy(self.group1.messages):
            if m[0] == "osc":
                logging.debug(f"On {self.group1.type}, {self.group1.id}:\nRemoved message {m[0]}: {m}")
                self.group1.messages.remove(m)
            
    def look_for_osc_messages_in_group1(self):
        with pytest.raises(ValueError):
            osc_msgs = [m for m in self.group1.messages if m[0] == "osc"]
            if len(osc_msgs) == 0:
                raise ValueError(f"{self.group1.id} has no osc msgs")

    def look_for_osc_messages_in_group2(self):
        osc_msgs = [m for m in self.group2.messages if m[0] == "osc"]
        assert len(osc_msgs) > 0

    @profile
    def test_copiers(self,):
        """Properties"""
        self.create_different_groups()
        self.create_properties_for_group1()
        self.copy_properties_from_group1_to_group2()
        self.assert_properties_of_group2()
        """Values"""
        self.create_values_for_group1()
        self.copy_values_from_group1_to_group2()
        """Messages"""
        self.create_messages_for_group1()
        self.copy_messages_from_group1_to_group2()
        self.remove_osc_messages_from_group1()
        self.look_for_osc_messages_in_group1()
        self.look_for_osc_messages_in_group2()
        
        # # COPY CHILDREN
        # controlsList = []
        # for c in ControlType:
        #     child = tosc.Node(node.createChild(c))
        #     child.setName(c.value)
        #     controlsList.append(c.value)

        # assert tosc.copyChildren(
        #     node,
        #     node2,
        #     ControlType.BOX,
        #     ControlType.BUTTON,
        #     ControlType.ENCODER,
        #     ControlType.GROUP,
        # )

        # with pytest.raises(ValueError):
        #     assert tosc.copyChildren(node2, node2, ControlType.FADER)

        # childList = []
        # for n1 in node.children:
        #     n1 = tosc.Node(n1)
        #     childList.append(n1.getPropertyValue("name").text)
        # for n2 in node2.children:
        #     n2 = tosc.Node(n2)
        #     childList.append(n2.getPropertyValue("name").text)

        # assert controlsList.sort() == childList.sort()

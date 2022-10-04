import tosclib as tosc
from tosclib.properties import *
from copy import deepcopy
import logging
import pytest
import inspect
import unittest


class Copier(unittest.TestCase):
    """Create different groups, copy attrs and compare them."""

    template1: tosc.Control
    template2: tosc.Control
    group1: tosc.Control
    group2: tosc.Control
    proplist1: list[tosc.Property] = []
    proplist2: list[tosc.Property] = []

    def create_different_groups(self):
        self.template1 = tosc.Group(
            props={"name": "template1", "frame": (0, 0, 800, 800)}
        )
        self.template2 = tosc.Group(props={"name": "template2"})
        self.group1 = tosc.Group(props={"name": "group1", "frame": (0, 0, 400, 400)})
        self.group2 = tosc.Group(props={"name": "group2"})
        self.template1.children.append(self.group1)
        self.template2.children.append(self.group2)

    def create_properties_for_group1(self):
        for func in inspect.getmembers(PropsGroup, predicate=inspect.isfunction):
            if "__" not in func[0]:
                p = func[1]()
                self.proplist1.append(p)
                assert self.group1.set(p[0], p[1])

    def copy_properties_from_group1_to_group2(self):
        assert self.group1 is not self.group2
        self.group2.props = self.group1.props
        assert self.group2
        assert self.proplist1.sort() == self.proplist2.sort()

    def assert_properties_of_group2(self):
        for p in self.group2.props:
            prop = self.group2.props[p]
            self.proplist2.append(p)
            assert self.group2.get(p) == prop

    def create_values_for_group1(self):
        val_keys = ("touch", "x", "y", "text")
        val_defs = (False, 0.0, 0.55, "test")
        values = [
            tosc.value(val_keys[0], default=val_defs[0]),
            tosc.value(val_keys[1], True, True, val_defs[1], 100),
            tosc.value(val_keys[2], True, False, val_defs[2], 50),
            tosc.value(val_keys[3], False, False, val_defs[3], 0),
        ]
        self.group1.values = values
        for v, k, d in zip(self.group1.values, val_keys, val_defs):
            assert v
            assert v[0] == k
            assert v[3] == d

    def copy_values_from_group1_to_group2(self):
        tosc.copy_values(self.group1, self.group2)
        assert self.group1.values.sort() == self.group2.values.sort()

    def create_messages_for_group1(self):
        msg_keys = ("osc", "midi", "local")
        messages = [tosc.osc(), tosc.midi(), tosc.local()]
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
                logging.debug(
                    f"""Removed message {m[0]}
                    on {self.group1.type}, {self.group1.id}"""
                )
                self.group1.messages.remove(m)

    def look_for_osc_messages_in_group1(self):
        with pytest.raises(ValueError):
            osc_msgs = [m for m in self.group1.messages if m[0] == "osc"]
            if len(osc_msgs) == 0:
                raise ValueError(f"{self.group1.id} has no osc msgs")

    def look_for_osc_messages_in_group2(self):
        osc_msgs = [m for m in self.group2.messages if m[0] == "osc"]
        assert len(osc_msgs) > 0

    def test_copiers(
        self,
    ):
        """Controls"""
        self.create_different_groups()
        """Properties"""
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
        """Children"""
        ...
        # to-do: add copy children

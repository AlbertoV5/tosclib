import logging
import tosclib as tosc
from .profiler import profile


@profile
def test_basics():
    root = tosc.createTemplate()
    base = tosc.Node(root[0])

    name = "Craig"
    tag = "Scottish"
    control = tosc.Group(name=name, tag=tag)
    control.values.append(tosc.value())
    control.messages = [tosc.osc()]
    control.set_color((1.0, 0.0, 0.0, 1.0))
    control.set_frame((0, 0, 1, 1))
    base.children.append(tosc.xml_control(control))

    tag2 = tosc.pull_value_from_key_2(root, "name", "Craig", "tag")
    name2 = tosc.pull_value_from_key_2(root, "tag", tag2, "name")
    assert tag == tag2
    assert name == name2

    """NESTED"""

    arguments: tosc.Arguments = (
        tosc.partial(),
        tosc.partial("PROPERTY", "STRING", "parent.name"),
        tosc.partial(),
        tosc.partial("PROPERTY", "STRING", "name"),
    )
    osc = tosc.osc(args=arguments)
    group = tosc.Group(messages=[osc])

    lim = 8
    for i in range(lim):
        button: tosc.Control = tosc.Button()
        assert button.set_prop(("name", f"button{i}")) is not None
        assert button.set_frame((i * 100, 0, 100, 50)) is not None
        assert button.set_color((1 - i / lim, 0, lim, 1)) is not None
        assert (value := tosc.value("x", False, False, 0.0, 0)) is not None
        button.values.append(value)
        button.messages.append(osc)
        assert isinstance(button, tosc.ControlBuilder)
        group.children.append(button)

    egroup: tosc.Element = tosc.xml_control(group)

    for i in range(lim):
        assert (result := tosc.find_child(egroup, f"button{i}"))
        assert result.tag != "none"

    buttonBad: tosc.Control = tosc.Button(name="buttonBad")
    logging.debug("Expecting following Sentinel Element:")
    (sentinel := tosc.find_child(egroup, "buttonBad"))
    assert sentinel.tag == "none"

    assert tosc.copy_properties(button, buttonBad)
    assert tosc.copy_values(button, buttonBad)
    assert tosc.copy_messages(button, buttonBad)
    # buttonBetter = tosc.xml_control(buttonBad)

    assert (group2 := tosc.Group()) is not None
    assert tosc.copy_children(group, group2)
    assert group2.set_type("GRID")

    tgroup = tosc.Node(egroup)
    for child in tgroup.children:
        echild = tosc.Node(child)
        echild.set_prop(("background", False))
        echild.set_prop(("background", True))
        echild.set_prop(("locked", False))
        echild.set_prop(("visible", False))
        echild.set_prop(("outline", True))
        echild.set_prop(("interactive", False))
        echild.set_prop(
            (
                "script",
                """
function init()
    self.values.x = 1
end
        """,
            )
        )

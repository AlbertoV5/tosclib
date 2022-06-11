import cProfile
import logging
import pstats

import tosclib as tosc
from tosclib import controls
from tosclib.elements import MessageLOCAL, Trigger
from tosclib.etosc import ControlType, Value
from tosclib.controls import PropertyFactory as pf
from tosclib.controls import ControlConverter as cc
from tosclib.etosc import ElementTOSC as et
import subprocess

bgGradient1 = ((0.25, 0.25, 0.25, 1.0), (0.5, 0.25, 0.25, 1.0))
bgGradient2 = ((1.0, 0.0, 0.0, 1.0), (0.5, 0.0, 0.5, 1.0))
names = (7,4,1,8,5,2,9,6,3,)


@tosc.layout.column
def layoutBase(children: list[et]):

    layoutTop: et = layoutValues(
        children[0],
        ControlType.GROUP,
        size=(1,1),
        colors=bgGradient1,
    )

    layoutMid: et = layoutNumbers(
        children[1], 
        ControlType.GROUP, 
        size=(3, 3), 
        colors=bgGradient1,
        colorStyle=2
        )
    
    layoutBot: et = layoutClear(
        children[2],
        ControlType.GROUP,
        size = (1,1,1),
        colors=bgGradient1,
    )

    id = tosc.pullIdfromName(layoutTop.node, "valueLabel")

    local0 = MessageLOCAL(
        triggers=[Trigger("x", "RISE")],
        type="PROPERTY",
        conversion="STRING",
        value = "name",
        dstType="VALUE",
        dstVar="text",
        dstID=id,)

    for c in layoutMid:
        et(c)[0].createLOCAL(local0)

    layoutBot[1][0].createLOCAL(local0)

    local1 = MessageLOCAL(
        triggers=[Trigger("x", "RISE")],
        type="CONSTANT",
        conversion="STRING",
        value = "0",
        dstType="PROPERTY",
        dstVar="sum",
        dstID=id,)

    local2 = MessageLOCAL(
        triggers=[Trigger("x", "FALL")],
        type="CONSTANT",
        conversion="STRING",
        value = "",
        dstType="VALUE",
        dstVar="text",
        dstID=id,)

    layoutBot[0][0].createLOCAL(local1)
    layoutBot[0][0].createLOCAL(local2)

    local3 = MessageLOCAL(
        triggers=[Trigger("x", "FALL")],
        type="CONSTANT",
        conversion="STRING",
        value = "",
        dstType="VALUE",
        dstVar="text",
        dstID=id,)
        
    layoutBot[2][0].createLOCAL(local3)

    return [pf.name("Numpad")]


@tosc.layout.row
def layoutValues(children: list[et]):

    frame = children[0].getFrame()
    button0 = controls.Button(
        properties = [
            pf.name("valueButton"),
            pf.color(children[0].getColor()),
            pf.frame(frame)
        ]
    )
    label0 = controls.Label(
        properties = [
            pf.name("valueLabel"),
            pf.background(False),
            pf.color(children[0].getColor()),
            pf.buildAny("frame", frame),
            pf.textSize(60),
            pf.buildAny("sum", ""),
            pf.buildAny("max", "127"),
            pf.script("""
self.sum = "0"
self.values.text = self.sum

function onValueChanged(key,value)
    self.sum = self.sum..self.values.text
    if tonumber(self.sum) >= tonumber(self.max) then
        self.sum = self.max
    end
    if tonumber(self.sum) == 0 then
        self.values.text = "0"
    end
    self.values.text = self.sum
end""")
        ],
        values = [Value("text", default="0")]
    )
    
    children[0].setName("value")
    children[0].children.append(cc.toXML(button0))
    children[0].children.append(cc.toXML(label0))

    label1 = controls.Label(
        properties = [
            pf.name("sendLabel"),
            pf.color(children[1].getColor()),
            pf.frame(frame),
            pf.textSize(60),
            pf.background(False),
        ],
        values=[Value("text", default="SEND")]
    )
    button1 = controls.Button(
        properties = [
            pf.name("sendButton"),
            pf.color(children[1].getColor()),
            pf.frame(frame),
        ]
    )

    children[1].setName("send")
    children[1].children.append(cc.toXML(button1))
    children[1].children.append(cc.toXML(label1))

    return [pf.name("Values")]


@tosc.layout.grid
def layoutNumbers(children: list[et]):

    f = children[0].getFrame()
    framepad = (int(f[2]*0.1),int(f[3]*0.1),int(f[2]*0.8),int(f[3]*0.8))
    label = controls.Label(
        properties = [
            pf.frame(framepad),
            pf.textColor((1.0,1.0,1.0,1.0,)),
            pf.textSize(48),
            pf.background(False),
        ]
    )
    button = controls.Button(
        properties=[
            pf.frame(f),
            pf.outline(False),
            pf.buildAny("color2", (0.5,0.5,0.5,1.0,)),
        ]
    )
    

    for n, c in zip(names, children):

        label.values.append(Value("text", default = str(n)))
        label.properties.append(pf.name(str(n)))
        button.properties.append(pf.name(str(n)))
        button.properties.append(pf.color(c.getColor()))

        c.children.append(cc.toXML(button))
        c.children.append(cc.toXML(label))
        
    return [pf.outline(True),pf.name("numbers")]


@tosc.layout.row
def layoutClear(children: list[et]):

    button0 = controls.Button(
        properties= [
            pf.name("clearButton"),
            pf.frame(children[0].getFrame()), #type: ignore
            pf.color(children[0].getColor()), #type: ignore
        ]
    )
    label0 = controls.Label(
        properties= [
            pf.name("clearLabel"),
            pf.outlineStyle(1),
            pf.frame(children[0].getFrame()), #type: ignore
            pf.color(children[0].getColor()), #type: ignore
            pf.textSize(48),
            pf.background(False),
        ],
        values = [Value("text", default="CLR")]
    )

    children[0].setName("clear")
    children[0].children.append(cc.toXML(button0))
    children[0].children.append(cc.toXML(label0))

    frame = children[0].getFrame()
    button1 = controls.Button(
        properties= [
            pf.name("0"),
            pf.frame(frame),
            pf.color(children[1].getColor()),
        ]
    )
    label1 = controls.Label(
        properties= [
            pf.name("0"),
            pf.outlineStyle(1),
            pf.frame(frame),
            pf.color(children[1].getColor()),
            pf.textSize(48),
            pf.background(False),
        ],
        values = [Value("text", default="0")]
    )

    children[1].setName("zero")
    children[1].children.append(cc.toXML(button1))
    children[1].children.append(cc.toXML(label1))

    button2 = controls.Button(
        properties= [
            pf.name("0"),
            pf.frame(frame),
            pf.color(children[2].getColor()),
        ]
    )
    label2 = controls.Label(
        properties= [
            pf.name("0"),
            pf.outlineStyle(1),
            pf.frame(frame),
            pf.color(children[2].getColor()),
            pf.textSize(48),
            pf.background(False),
        ],
        values = [Value("text", default="DEL")]
    )

    children[2].setName("del")
    children[2].children.append(cc.toXML(button2))
    children[2].children.append(cc.toXML(label2))
    

    return [pf.name("ClearDel")]

def main():

    root = tosc.createTemplate(frame=(0, 0, 500, 800))
    template = et(root[0])

    layoutBase(
        template, 
        ControlType.GROUP, 
        size=(1, 3, 1), 
        colors=bgGradient1
        )
    
    """Save it as a template"""
    tosc.write(root, "docs/demos/numpad.tosc")


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="docs/demos/numpad.prof")

    subprocess.run(["open", "docs/demos/numpad.tosc"])
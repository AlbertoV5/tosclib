from typing import Any
from tosclib.elements import *
from xml.etree.ElementTree import Element, SubElement, fromstring

def tup_value(args:tuple) -> Value:
    match args:
        case (
            ("x" | "y" | "touch" | "text"),
            "0" | "1", "0" | "1", _ , _):
            match args[0]: 
                case "x" | "y":
                    d = float(args[3])
                case "touch":
                    d = bool(args[3])
                case _:
                    d = args[3]
            return Value(
                (args[0],bool(int(args[1])),bool(int(args[2])),d,int(args[4]))
                )
        case _:
            raise TypeError(f"{args} is not a valid Value.")

def tup_prop(args:tuple) -> Property:
    match args[0]:
        case "b":
            return args[1]
        case _:
            raise TypeError

def tup_node(e:Element) -> Any:
    match e.tag:
        case "value":
            return tup_value((
                (e[0].text, e[1].text, e[2].text, e[3].text, e[4].text)
                ))
        case "property":
            match e[0].text:
                case "r" | "c":   
                    return tup_prop((
                        e[0].text, 
                        e[1][0].text,
                        e[1][1].text,
                        e[1][2].text,
                        e[1][3].text
                        ))
                case "b" | "f" | "i" | "s":
                    return tup_prop((e[0].text, e[1].text))
                case _:
                    raise ValueError
        case _:
            raise ValueError

xml = """
<value>
<key>x</key>
<locked>0</locked>
<lockedDefaultCurrent>0</lockedDefaultCurrent>
<default>0</default>
<defaultPull>0</defaultPull>
</value>
"""

e = fromstring(xml)
val = tup_node(e)

print(val)


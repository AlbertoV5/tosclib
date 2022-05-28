import tosclib as tosc


root = tosc.createTemplate()
element = tosc.ElementTOSC(root)

element.createValue("alsjdnas", "1", "0", "aksjdbas", "0")

element.showValues()
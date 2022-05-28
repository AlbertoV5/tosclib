import tosclib as tosc


root = tosc.createTemplate()
element = tosc.ElementTOSC(root)

element.createValue("test", "1", "0", "1234", "0")

element.setValue("test", "0", "1", "4321", "1")

element.showValues()

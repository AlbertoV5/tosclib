import tosclib as tosc
root = tosc.load("../demos/files/test.tosc")
print(root)

newEnum = tosc.SubElements.new("Styled", {"STYLES":"styles"})
e = tosc.e(root[0], newEnum)

for k in e.__dict__:
    print(k, e.__dict__[k])
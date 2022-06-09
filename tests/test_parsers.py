import tosclib as tosc
from .profiler import profile


@profile
def test_parsers():

    known = "name"
    unknown = "script"
    sameFile = "docs/demos/files/Numpad_basic.tosc"
    sameName = "num7"
    root = tosc.load(sameFile)

    script0 = tosc.parseProperties(root, known, unknown)
    script1 = tosc.pullValueFromKey(sameFile, known, sameName, unknown)
    script2 = tosc.pullValueFromKey2(root, known, sameName, unknown)

    for i in script0:
        if i["name"] == sameName:
            script0 = i["script"]
            break

    assert script0 == script1 == script2


if __name__ == "__main__":
    test_parsers()

import time
import tosclib as tosc


def property_parser(sameFile, known, unknown):
    root = tosc.load(sameFile)
    start = time.process_time()
    result = tosc.Control.parseProperties(root, known, unknown)
    end = time.process_time()
    print("-", end - start)
    return result


def test_all_parsers():

    known = "name"
    unknown = "script"
    sameFile = "docs/demos/files/Numpad_basic.tosc"
    sameName = "num7"

    script0 = property_parser(sameFile, known, unknown)
    script1 = tosc.pullValueFromKey(sameFile, known, sameName, unknown)
    script2 = tosc.pullValueFromKey2(tosc.load(sameFile), known, sameName, unknown)

    for i in script0:
        if i["name"] == sameName:
            script0 = i["script"]
            break

    print(script0)
    print(script1)
    print(script2)

    assert script0 == script1 == script2

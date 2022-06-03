import cProfile
import pstats
import tosclib as tosc

def profile(func):
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            for i in range(1):
                func(*args, **kwargs)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats(filename="tests/test_parsers.prof")
    return wrapper


@profile
def test_all_parsers():

    known = "name"
    unknown = "script"
    sameFile = "docs/demos/files/Numpad_basic.tosc"
    sameName = "num7"
    root = tosc.load(sameFile)

    script0 = tosc.Control.parseProperties(root, known, unknown)
    script1 = tosc.pullValueFromKey(sameFile, known, sameName, unknown)
    script2 = tosc.pullValueFromKey2(root, known, sameName, unknown)

    for i in script0:
        if i["name"] == sameName:
            script0 = i["script"]
            break

    # print(script0)
    # print(script1)
    # print(script2)

    assert script0 == script1 == script2

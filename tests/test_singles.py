import cProfile
import pstats
from tosclib import tosc
from tosclib.tosc import Partial, Value


def profile(func):
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            for i in range(1):
                func(*args, **kwargs)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats(filename="tests/test_singles.prof")

    return wrapper


@profile
def test_singles():

    root = tosc.createTemplate()
    element = tosc.ElementTOSC(root[0])

    element.setName("Craig")
    element.setTag("Scottish")
    element.createValue(Value())

    element.showValue("touch")
    element.setValue(Value("touch", "1", "1", "true", "1"))

    element.createOSC(
        message=tosc.OSC(
            "0",
            "0",
            "0",
            "1",
            "00001",
            [tosc.Trigger()],
            [tosc.Partial(), tosc.Partial()],
            [Partial(), Partial()],
        )
    )

    element.setColor(1, 0, 0, 1)
    element.setFrame(0, 0, 1, 1)

    count = 0
    for i in dir(tosc.ElementTOSC):
        if "__" not in i:
            count += 1

    tag = tosc.pullValueFromKey2(root, "name", "Craig", "tag")

    x = tosc.ControlElements.PROPERTIES
    x = element.setColor(1, 0, 0, 1)

import cProfile
import pstats
import tosclib as tosc
from tosclib import layoutColumn
from tosclib import ElementTOSC
from tosclib.layout import layoutGrid
from PIL.ImageColor import getrgb

def profile(func):
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            name = func(*args, **kwargs)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats(filename=name)

    return wrapper

@layoutColumn
def columns(groups: list[ElementTOSC]):
    for g in groups:
        g.setOutline(False)
    return

@layoutGrid
def grid(groups: list[ElementTOSC]):
    for g in groups:
        g.setOutline(False)
    return

@profile
def main():
    frame = (0, 0, 2560, 1600)

    root = tosc.createTemplate(frame=frame)
    rootosc = ElementTOSC(root[0])
    
    topLayout = columns(
        size=tuple(1 for i in range(8)),
        frame=(0,0,400,1600),
        gradient=((0.8, 0.8, 0.8, 1.0), (0.2, 0.2, 0.2, 1.0)),
    )
    
    gridLayout: ElementTOSC = grid(frame = (400, 0, 1600, 1600),
                                   size = (4,4),
                                   gradient = ("#564D65FF",
                                              "#3E8989FF",
                                               "#1A181BFF",
                                               "#2CDA9DFF"),
                                   gradientCenter = 8)
    
    rootosc.append(gridLayout)
    rootosc.append(topLayout)
    
    tosc.write(root, "tests/deleteme.tosc")

    return "tests/deleteme.prof"

    
if __name__ == "__main__":
    main()

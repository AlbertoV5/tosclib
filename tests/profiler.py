import cProfile
import pstats

def profile(func):
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            name = func(*args, **kwargs)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats(filename=name)

    return wrapper


def profile2(func):
    def wrapper(capture_stdout):
        with cProfile.Profile() as pr:
            name = func(capture_stdout)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats(filename=name)

    return wrapper
import cProfile
import pstats

def profile(func):
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            func(*args, **kwargs)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            name = func.__name__.replace("test", "prof")
            stats.dump_stats(filename=f"tests/{name}.prof")

    return wrapper


def profile2(func):
    def wrapper(capture_stdout):
        with cProfile.Profile() as pr:
            func(capture_stdout)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            name = func.__name__.replace("test", "prof")
            stats.dump_stats(filename=f"tests/{name}.prof")
            
    return wrapper

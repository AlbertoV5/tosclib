"""Basic profiler wrapper."""
from pstats import Stats
from cProfile import Profile

__all__ = ["profile"]

def profile(func):
    """Run a profiler from cProfile on the wrapped function."""
    def wrapper(*args, **kwargs):
        with Profile() as profile:
            func(*args, **kwargs)
            stats = Stats(profile)
            stats.sort_stats("time")
            stats.dump_stats(filename=f"profs/{func.__name__}.prof")
    return wrapper

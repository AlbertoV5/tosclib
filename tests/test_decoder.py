"""
Testing: Decoder.

    load_correct_file_and_decode_all:	load .tosc file
    create_incorrect_file_and_catch:	generate bad xml
"""
import pytest
from logging import debug
from cProfile import Profile
from unittest import TestCase
from pstats import Stats, SortKey


def profile(func):
    """Logs execution of wrapped func."""
    def wrapper(*args, **kwargs):
        with Profile() as pr:
            func(*args, **kwargs)
            stats = Stats(pr)
            stats.sort_stats(SortKey.TIME)
            name = func.__name__.replace("test", "prof")
            stats.dump_stats(filename=f"tests/{name}.prof")
    return wrapper

class TestDecoder(TestCase):
    
    def load_correct_file_and_decode_all(self):
        """load .tosc file"""
        # breakpoint()

    def create_incorrect_file_and_catch(self):
        """generate bad xml"""
        # breakpoint()

    @profile
    def test_decoder(self):
        self.load_correct_file_and_decode_all()
        self.create_incorrect_file_and_catch()
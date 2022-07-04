"""
Testing: Name.

    test_this_first:
        __summary__

    test_this_then:
        __summary__

    test_this_last:
        __summary__

"""
import pytest
import logging
from pstats import Stats
from cProfile import Profile

# Logging Setup
# formatter = logging.Formatter("%(asctime)s\n%(name)s:%(message)s")
# log_file_handler = logging.FileHandler("logs/test_deleteme.log")
# log_file_handler.setFormatter(formatter)
# log = logging.getLogger(__name__)
# log.addHandler(log_file_handler)

log = logging.getLogger(__name__)

def test_1():
    """__summary__"""
    log.debug("Hello there.")
    
def test_2():
    """__summary__"""
    
def test_3():
    """__summary__"""

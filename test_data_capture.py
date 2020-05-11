import pytest

from data_capture import DataCapture
from stats_computers import GreaterLessBetweenStats, StatsBase

# Fixtures
@pytest.fixture
def stats():
    return GreaterLessBetweenStats()


@pytest.fixture
def capture(stats):
    return DataCapture()


@pytest.fixture
def populated_capture(capture):
    """Setup according to exercise instructions"""
    capture.add(3)
    capture.add(9)
    capture.add(3)
    capture.add(4)
    capture.add(6)
    return capture


@pytest.fixture
def populated_capture_stats(populated_capture):
    return populated_capture.build_stats()


# Main Tests


def test_build_stats_method(capture):
    stats = capture.build_stats()
    assert isinstance(stats, StatsBase)


def test_stats_less_method_on_empty_data_is_zero(stats):
    assert isinstance(stats.less(4), int)
    assert stats.less(4) == 0


def test_stats_between_method_on_empty_data_is_zero(stats):
    assert isinstance(stats.between(3, 6), int)
    assert stats.between(3, 6) == 0


def test_stats_greater_method_on_empty_data_is_zero(stats):
    assert isinstance(stats.greater(6), int)
    assert stats.greater(6) == 0


def test_add_values(stats):
    capture = DataCapture(stats)
    assert stats.count == 0
    capture.add(3)
    assert stats.count == 1
    capture.add(3)
    assert stats.count == 2


def test_less_than(populated_capture_stats):
    assert populated_capture_stats.less(4) == 2


def test_greater_than(populated_capture_stats):
    assert populated_capture_stats.greater(4) == 2


def test_between(populated_capture_stats):
    assert populated_capture_stats.between(3, 6) == 4

import pytest

from apimes import utils

def test_queue_name_with_valid_value():
    expected="andrea_cars"
    result = utils.get_queue_name("cars", "andrea")
    assert result == expected

def test_queue_name_with_invalid_chars():
    result = utils.get_queue_name("cars*", "Louis")
    expected = None
    assert result == expected

def test_queue_name_invalid_length():
    name = "andrea" * 255
    result = utils.get_queue_name(name, "1")
    expected = None
    assert result == expected

def test_queue_name_special_valid_chars():
    result = utils.get_queue_name("cars.:", "-test")
    expected = "-test_cars.:"
    assert result == expected

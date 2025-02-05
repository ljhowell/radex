# fmt: off
# pylint: disable=line-too-long

"""Test the Expression method from radex.expression"""

import pytest
from radex.expression import Expression


@pytest.fixture
def _expression():
    """Create an instance of the Expression class"""
    return Expression()

def test_parse_string_bool(_expression):
    """Test the boolean logic"""

    assert _expression.parse_string("a & b | c") == [
        [ ['a ', '&', 'b '], '|', 'c' ]
    ]
    assert _expression.parse_string("a & (b | c)") == [
        [ 'a ', '&', ['b ', '|', 'c'] ]
    ]
    assert _expression.parse_string("a & ¬b") == [
        [ 'a ', '&', ['¬', 'b'] ]
    ]
    assert _expression.parse_string("a & ¬(b | c)") == [
        [ 'a ', '&', ['¬', ['b ', '|', 'c']] ]
    ]
    assert _expression.parse_string("a & ¬(b | c)", verbose=True) == [
        [ 'a ', '&', ['¬', ['b ', '|', 'c']] ]
    ]

def test_parse_string_modifiers(_expression):
    """Strings with modifiers"""
    assert _expression.parse_string("quick ~~1 dog & brown ~1 fox | camel* & ¬hippo?") == [
        [['quick ~~1 dog ', '&', 'brown ~1 fox '], '|', ['camel* ', '&', ['¬', 'hippo?']]]
    ]

    assert _expression.parse_string("quick NEAR1 dog AND brown THEN1 fox OR camel* EXCEPT hippo?") == [
        [['quick ~~1 dog ', '&', 'brown ~1 fox '], '|', ['camel* ', '&', ['¬', 'hippo?']]]
    ]

def test_parse_string_invalid(_expression):
    """Invalid input strings"""
    with pytest.raises(ValueError):
        _expression.parse_string("quick~1dog & brown~1fox | camel* & ¬hippo(")
    with pytest.raises(ValueError):
        _expression.parse_string("a & b | c)")
    with pytest.raises(ValueError):
        _expression.parse_string("a ~~~2 c")
    with pytest.raises(ValueError):
        _expression.parse_string("a & ¬%b | c")
    with pytest.raises(ValueError):
        _expression.parse_string("a ~~2")

def test_check_input_string(_expression):
    """Valid input strings"""
    assert _expression.check_input_string("quick~1dog & brown~1fox | camel* & ¬hippo")
    assert _expression.check_input_string("a & b | c")
    assert _expression.check_input_string("a & (b | c)")
    assert _expression.check_input_string("a & ¬b")
    assert _expression.check_input_string("a & ¬(b | c)")

def test_check_input_string_invalid(_expression):
    """Invalid input strings"""
    with pytest.raises(ValueError):
        _expression.check_input_string("quick~1dog & brown~1fox | camel* & ¬hippo(")
    with pytest.raises(ValueError):
        _expression.check_input_string("a & b | c)")
    with pytest.raises(ValueError):
        _expression.check_input_string("a ~~~2 c")
    with pytest.raises(ValueError):
        _expression.check_input_string("a & ¬%b | c")

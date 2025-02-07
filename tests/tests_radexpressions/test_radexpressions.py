# fmt: off
# pylint: disable=line-too-long

"""Test the Expression method from radex.expression"""

import pytest
from radex.radexpressions import evaluate_regex, get_regex_wildcards, get_regex_proximity, string_search, wildcard_search

def test_evaluate_regex():
    """Evaluate a regular expression"""
    candidate = "The quick brown fox jumps over the lazy dog"
    regex = r"\bquick\b"
    expected_result = [("quick", 4, 9)]
    assert evaluate_regex(candidate, regex) == expected_result

    candidate = "The quick brown fox jumps over the lazy dog"
    regex = r"\bnonexistent\b"
    expected_result = []
    assert evaluate_regex(candidate, regex) == expected_result

def test_get_regex_wildcards():
    """Test the get_regex_wildcards function"""
    expression = "colour"
    expected_result = r"\bcolour\b"
    assert get_regex_wildcards(expression) == expected_result

    expression = "colou?r"
    expected_result = r"\bcolou.?r\b"
    assert get_regex_wildcards(expression) == expected_result

    expression = "colou*r"
    expected_result = r"\bcolou\w*r\b"
    assert get_regex_wildcards(expression) == expected_result

def test_get_regex_proximity():
    """Test the proximity search function"""
    # Centre proximity search
    word1 = "quick"
    word2 = "fox"
    max_distance = 2
    direction = "centre"
    expected_result = r"\bquick\b\W+(?:\w+\W+){0,2}?\bfox\b|\bfox\b\W+(?:\w+\W+){0,2}?\bquick\b"
    assert get_regex_proximity(word1, word2, max_distance, direction) == expected_result

    # Right proximity search
    word1 = "quick"
    word2 = "fox"
    max_distance = 2
    direction = "right"
    expected_result = r"\bquick\b\W+(?:\w+\W+){0,2}?\bfox\b"
    assert get_regex_proximity(word1, word2, max_distance, direction) == expected_result

    # Left proximity search
    word1 = "quick"
    word2 = "fox"
    max_distance = 2
    direction = "left"
    expected_result = r"\bfox\b\W+(?:\w+\W+){0,2}?\bquick\b"
    assert get_regex_proximity(word1, word2, max_distance, direction) == expected_result

    # Invalid direction
    word1 = "quick"
    word2 = "fox"
    max_distance = 2
    direction = "invalid"
    with pytest.raises(ValueError):
        get_regex_proximity(word1, word2, max_distance, direction)

    # Invalid max_distance
    word1 = "quick"
    word2 = "fox"
    max_distance = "2"
    direction = "centre"
    with pytest.raises(ValueError):
        get_regex_proximity(word1, word2, max_distance, direction) # type: ignore

    # Negative max_distance
    word1 = "quick"
    word2 = "fox"
    max_distance = -2
    direction = "centre"
    with pytest.raises(ValueError):
        get_regex_proximity(word1, word2, max_distance, direction)

    # Invalid word1 or word2
    word1 = 123
    word2 = "fox"
    max_distance = 2
    direction = "centre"
    with pytest.raises(ValueError):
        get_regex_proximity(word1, word2, max_distance, direction) # type: ignore
        
    # Invalid direction
    word1 = "quick"
    word2 = "fox"
    max_distance = 2
    direction = "NOT A DIRECTION"
    with pytest.raises(ValueError):
        get_regex_proximity(word1, word2, max_distance, direction) # type: ignore

def test_string_search():
    """Test the string_search function which wraps the regex evaluation"""
    candidate = "The quick brown fox jumps over the lazy dog"

    # No match
    expression = "badger"
    expected_result = []
    assert string_search(candidate, expression) == (False, expected_result)

    # Matching a single word with wildcard
    expression = "qui*"
    expected_result = [("quick", 4, 9)]
    assert string_search(candidate, expression) == (True, expected_result)

    # Matching with proximity search
    expression = "quick~2fox"
    expected_result = [("quick brown fox", 4, 19)]
    assert string_search(candidate, expression) == (True, expected_result)

    # Invalid expression
    expression = "quick ~~2 fox ~~2 dog"
    with pytest.raises(ValueError):
        string_search(candidate, expression)

    expression = "quick ~~X fox"
    with pytest.raises(ValueError):
        string_search(candidate, expression)

def test_wildcard_search():
    """Test the wildcard_search function"""

    # Matching a single word with wildcard *
    string = "The quick brown fox jumps over the lazy dog"
    pattern = "qui*"
    expected_result = [("quick", 4, 9)]
    assert wildcard_search(string, pattern) == expected_result

    # Matching a single word with wildcard ?
    string = "The quick brown fox jumps over the lazy dog"
    pattern = "qui?k"
    expected_result = [("quick", 4, 9)]
    assert wildcard_search(string, pattern) == expected_result

    # Matching a single word with wildcard ? II
    string = "The quick brown fox jumps over the lazy dog"
    pattern = "qui?ck"
    expected_result = [("quick", 4, 9)]
    assert wildcard_search(string, pattern) == expected_result

    # No match
    string = "The quick brown fox jumps over the lazy dog"
    pattern = "nonexistent"
    expected_result = []
    assert wildcard_search(string, pattern) == expected_result

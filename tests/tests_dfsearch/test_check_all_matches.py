# fmt: off
# pylint: disable=line-too-long

"""Test the check_all_matches function from df_search"""

from radex.dfsearch import check_all_matches

def test_check_all_matches_0():
    """No match"""
    candidate = "the quick brown fox jumps over the lazy dog"
    expression = ["badger"]
    expected_result = {
        "badger": (False, [])
    }
    assert check_all_matches(candidate, expression) == expected_result

def test_check_all_matches_1():
    """1 search, 1 match"""
    candidate = "the quick brown fox jumps over the lazy dog"
    expression = ["quick"]
    expected_result = {
        "quick": (True, [("quick", 4, 9)])
    }
    assert check_all_matches(candidate, expression) == expected_result

def test_check_all_matches_2():
    """2 searches, 2 matches"""
    candidate = "the quick brown fox jumps over the lazy dog"
    expression = ["fox", "quick"]
    expected_result = {
        "fox": (True, [("fox", 16, 19)]),
        "quick": (True, [("quick", 4, 9)]),
    }
    assert check_all_matches(candidate, expression) == expected_result

def test_check_all_matches_3():
    """1 search, 2 matches"""
    candidate = "the quick brown fox jumps over the lazy dog"
    expression = ["the"]
    expected_result = {
        "the": (True, [("the", 0, 3), ("the", 31, 34)]),
    }
    assert check_all_matches(candidate, expression) == expected_result

def test_check_all_matches_4():
    """2 searches, 1 match"""
    candidate = "the quick brown fox jumps over the lazy dog"
    expression = ["fox", "badger"]
    expected_result = {
        "fox": (True, [("fox", 16, 19)]),
        "badger": (False, []),
    }
    assert check_all_matches(candidate, expression) == expected_result

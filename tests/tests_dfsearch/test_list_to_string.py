# fmt: off
# pylint: disable=line-too-long

"""Test the list_to_string function from df_search"""

from radex.dfsearch import list_to_string

def test_string_to_string():
    """Test list_to_string with a single string element"""
    assert list_to_string("a") == "a"

def test_list_to_string_empty_list():
    """Test list_to_string with an empty list"""
    assert list_to_string([]) == "()"

def test_list_to_string_single_element_list():
    """Test list_to_string with a single element list"""
    assert list_to_string([1]) == "(1)"

def test_list_to_string_multiple_element_list():
    """Test list_to_string with a multiple element list"""
    assert list_to_string([1, 2, 3]) == "(1, 2, 3)"

def test_list_to_string_nested_list():
    """Test list_to_string with a nested list"""
    assert list_to_string([[1, 2], [3, 4]]) == "((1, 2), (3, 4))"

def test_list_to_string_mixed_data_types():
    """Test list_to_string with a list containing mixed data types"""
    assert list_to_string([1, "a", True]) == "(1, a, True)"

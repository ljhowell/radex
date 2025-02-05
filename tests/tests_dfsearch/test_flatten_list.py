# fmt: off
# pylint: disable=line-too-long

"""Test the flatten_list function from df_search"""

from radex.dfsearch import flatten_list

def test_flatten_ints():
    """Test nested lists of integers."""
    assert flatten_list([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]
    assert flatten_list([1, 2, 3, 4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert flatten_list([[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]
    assert flatten_list([[1, 2], [3, 4], [5, 6], 7]) == [1, 2, 3, 4, 5, 6, 7]
    assert flatten_list([1, [2, 3], [4, [5, 6], 7]]) == [1, 2, 3, 4, 5, 6, 7]
    assert flatten_list([1, [2, 3], [4, [5, 6], 7], 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert flatten_list([1, [2, 3], [4, [5, 6], 7], 8, [9, 10]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert flatten_list([1, [2, 3], [4, [5, 6], 7], 8, [9, 10], 11]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    assert flatten_list([1, [2, 3], [4, [5, 6], 7], 8, [9, 10], 11, [12, 13]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    assert flatten_list([[[1,1]]]) == [1, 1]

def test_flatten_others():
    """Test other types of lists."""
    assert flatten_list(["a", ["b", "c"], ["d", ["e", "f"]]]) == ["a", "b", "c", "d", "e", "f"]
    assert flatten_list(["a", "bar", "car", "dar", "ear", "far"]) == ["a", "bar", "car", "dar", "ear", "far"]
    assert flatten_list(["2.1", ["2.2", "2.3"], ["2.4", ["2.5", "2.6"]]]) == ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6"]
    assert flatten_list([1, "a", [2, "b"], [[3, "c"], [4, "d"]]]) == [1, "a", 2, "b", 3, "c", 4, "d"]
                        
def test_flatten_empty_list():
    """Test empty list."""
    assert flatten_list([]) == []
    assert flatten_list([[], [[]], [[], []]]) == []

def test_flatten_single_element_list():  
    """Test single element list."""  
    assert flatten_list([1]) == [1]
    assert flatten_list(["a"]) == ["a"]
    assert flatten_list([[2]]) == [2]
    assert flatten_list([[3, "b"]]) == [3, "b"]

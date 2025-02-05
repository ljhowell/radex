# pylint: disable=redefined-outer-name
# pylint: disable=line-too-long
# fmt: off

"""Test the search_dataframe function from df_search"""

import pandas as pd
import pytest
from radex.dfsearch import search_dataframe

@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe"""
    df = pd.DataFrame({
        'text': ['the quick brown fox', 
                 'jumps over the lazy dog', 
                 'the quick brown dog. the slow pink cat'
                ],
        'number': [1, 2, 3]
    })
    return df

def test_search_dataframe_single_word(sample_dataframe):
    """Test searching for a single word"""
    result = search_dataframe(sample_dataframe, 'text', ['quick'])
    assert result['text_matches'].tolist() == [True, False, True]

def test_search_dataframe_no_matches(sample_dataframe):
    """Test searching where no matches are found"""
    result = search_dataframe(sample_dataframe, 'text', ['badger'])
    assert result['text_matches'].tolist() == [False, False, False]

def test_search_dataframe_phrase(sample_dataframe):
    """Test searching for a phrase"""
    result = search_dataframe(sample_dataframe, 'text', ['the quick brown'])
    assert result['text_matches'].tolist() == [True, False, True]

def test_search_dataframe_phrase_with_wildcard(sample_dataframe):
    """Test searching for a phrase with wildcard"""
    result = search_dataframe(sample_dataframe, 'text', ['the quick *'])
    assert result['text_matches'].tolist() == [True, False, True]

def test_search_dataframe_phrase_with_proximity(sample_dataframe):
    """Test searching for a phrase with proximity"""
    result = search_dataframe(sample_dataframe, 'text', ['the ~1 brown'])
    assert result['text_matches'].tolist() == [True, False, True]

def test_search_dataframe_new_column_name(sample_dataframe):
    """Test new_column_name option"""
    result = search_dataframe(sample_dataframe, 'text', ['the ~2 quick'], new_column_name='quick_animals')
    assert result['quick_animals'].tolist() == [True, False, True]

def test_search_dataframe_sentencizer_option_dog(sample_dataframe):
    """Test searching with sentencizer option for 'dog'"""
    result = search_dataframe(sample_dataframe, 'text', ['quick ~10 dog'], sentencizer=True)
    assert result['text_matches'].tolist() == [False, False, True]

def test_search_dataframe_sentencizer_option_cat(sample_dataframe):
    """Test searching with sentencizer option for 'cat'"""
    result = search_dataframe(sample_dataframe, 'text', ['quick ~10 cat'], sentencizer=True)
    assert result['text_matches'].tolist() == [False, False, False]

def test_search_dataframe_debug_column_option(sample_dataframe):
    """Test searching with debug_column option"""
    result = search_dataframe(sample_dataframe, 'text', ['quick'], debug_column=True)
    assert result['text_matches'].tolist() == [True, False, True]
    assert result['text_matches_matches'].tolist() == [
        {'quick': (True, [('quick', 4, 9)])},
        {'quick': (False, [])},
        {'quick': (True, [('quick', 4, 9)])}
    ]

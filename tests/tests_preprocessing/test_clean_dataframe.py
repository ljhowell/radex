# fmt: off
# pylint: disable=line-too-long

"""Tests for radex.preprocessing"""

import pytest
import pandas as pd
import numpy as np

from radex.preprocessing import clean_dataframe, remove_negated_phrases, merge_columns
from negex.negexPython.negex import sortRules

@pytest.fixture
def _sample_dataframe():
    """Create a sample dataframe"""
    df = pd.DataFrame({
        'text': ['Hello World!', 
                 'Unusual words kept pizza cow common words dropped the to he she it they them', 
                 'The dog was fast, but the fox was not fast. The rabbit was fastest.',
                 np.nan,
                 'Hello World!', # repeated
                ],
        'numbers': ['1', '2', '3', '4', '5']
    })
    return df

@pytest.fixture
def _sample_stopwords():
    """Create a sample list of stopwords"""
    return ['the', 'to', 'he', 'she', 'it', 'they', 'them', 'was', 'but']

@pytest.fixture
def _sample_negation_rules():
    """Create a sample list of negation rules"""    
    rules = '''not certain if		[PSEU]
    not		[PREN]
    no		[PREN]
    possible		[PREP]
    was ruled out		[POST]
    may be ruled out		[POSP]
    but		[CONJ]'''
    rules = rules.split("\n")

    return sortRules(rules)

def test_clean_dataframe(_sample_dataframe, _sample_stopwords, _sample_negation_rules):
    """Test the clean_dataframe function"""
    # Clean the dataframe
    cleaned_df = clean_dataframe(_sample_dataframe,
                                 text_columns='text',
                                 drop_duplicates=True,
                                 drop_nulls=True,
                                 drop_negatives=_sample_negation_rules,
                                 drop_stopwords=_sample_stopwords,
                                 )

    # Check if duplicates and nulls are dropped
    assert len(cleaned_df) == 3

    # Check if numbers column is unchanged
    assert cleaned_df['numbers'].tolist() == ['1', '2', '3']

    # Check if text is cleaned correctly
    assert cleaned_df['text'].tolist() == ['hello world',
                                           'unusual words kept pizza cow common words dropped',
                                           'dog fast fox not XXXXX. rabbit fastest'
                                          ]

def test_remove_negated_phrases(_sample_negation_rules):
    """Test the remove_negated_phrases function"""
    assert remove_negated_phrases('The dog was brown',
                                  _sample_negation_rules) == 'The dog was brown'
    assert remove_negated_phrases('The dog was not brown',
                                  _sample_negation_rules) == 'The dog was not XXXXX'
    assert remove_negated_phrases('The dog was not brown but the cat was brown',
                                  _sample_negation_rules) == 'The dog was not XXXXX but the cat was brown'
    assert remove_negated_phrases('The dog was not brown or white',
                                    _sample_negation_rules) == 'The dog was not XXXXX'
    assert remove_negated_phrases('The dog was not brown but it was white',
                                    _sample_negation_rules) == 'The dog was not XXXXX but it was white'
    assert remove_negated_phrases('The dog was not brown or white',
                                    _sample_negation_rules) == 'The dog was not XXXXX'
    assert remove_negated_phrases('The dog was not brown. It was white',
                                    _sample_negation_rules, verbose=True) == 'The dog was not XXXXX. It was white'


def test_merge_columns(_sample_dataframe):
    """Test the merge_columns function"""
    # Merge columns
    merged_df = merge_columns(_sample_dataframe, ['text', 'numbers'], 'merged')

    # Check if merged column is created
    assert 'merged' in merged_df.columns

    # Check if merged column is correct
    assert merged_df['merged'].tolist() == ['Hello World! 1',
                                            'Unusual words kept pizza cow common words dropped the to he she it they them 2',
                                            'The dog was fast, but the fox was not fast. The rabbit was fastest. 3',
                                            np.nan,
                                            'Hello World! 5'
                                           ]

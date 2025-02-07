# fmt: off
# pylint: disable=line-too-long

"""Test the Expression method from radex.expression"""

import pytest
import Radex
import os

def test_example_searches():
    """Test the example searches"""
    radex = Radex()
    radex.read_data('data/synthetic_ultrasound_reports/ex_usreports_validation.csv')
    radex.preprocess_data()
    radex.run_example_searches()
    radex.save_output("output.csv")
    assert radex.output_data is not None
    assert len(radex.output_data) > 0
    assert len(radex.output_data == len(radex.data))
    assert "output.csv" in os.listdir()
    os.remove("output.csv")
    
def test_simple_search_negative():
    """Test a simple search which should return all False"""
    radex = Radex()
    radex.read_data('data/synthetic_ultrasound_reports/ex_usreports_validation.csv')
    radex.preprocess_data()
    radex.searches = {'THIS_IS_NOT_IN_TEXT': 'THIS_IS_NOT_IN_TEXT'}
    radex.run_searches()
    assert len(radex.output_data == len(radex.data))
    assert all(radex.output_data['THIS_IS_NOT_IN_TEXT'] is False)
    
def test_simple_search_positive():
    """Test a simple search which should return all True"""
    radex = Radex()
    radex.read_data('data/synthetic_ultrasound_reports/ex_usreports_validation.csv')
    radex.preprocess_data()
    radex.searches = {'thyroid': 'thyr*'}
    radex.run_searches()
    assert len(radex.output_data == len(radex.data))
    assert all(radex.output_data['report'] is True)
    
def test_value_error():
    """Test the value error returns"""
    radex = Radex()
    # asseert preprocess before read returns a value error
    with pytest.raises(ValueError):
        radex.preprocess_data()

    with pytest.raises(ValueError):
        radex.run_searches()
        
    with pytest.raises(ValueError):
        radex.save_output('output.csv')
        
    radex.read_data('data/synthetic_ultrasound_reports/ex_usreports_validation.csv')
    
    with pytest.raises(ValueError):
        radex.run_searches()
    
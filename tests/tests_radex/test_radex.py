# fmt: off
# pylint: disable=line-too-long

"""Test the Expression method from radex.expression"""

import os
from pathlib import Path
import pytest

from radex import Radex

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

@pytest.fixture
def data_file_path() -> Path:
    return get_project_root() / "data" / "synthetic_ultrasound_reports" / "ex_usreports_validation.csv"

def test_example_searches(data_file_path):
    """Test the example searches"""
    # Assert that the file exists before proceeding
    assert data_file_path.exists(), f"Data file not found: {data_file_path}"
    
    radex = Radex()
    radex.read_data(str(data_file_path))  # Convert Path to string if necessary
    radex.preprocess_data()
    radex.run_example_searches()
    
    assert radex.output_data is not None, "Output data is None"
    assert len(radex.output_data) > 0, "Output data is empty"
    assert len(radex.output_data) == len(radex.data), "Output data length doesn't match input data length"

    radex.save_output("output.csv")
    assert "output.csv" in os.listdir()
    os.remove("output.csv")
    
def test_simple_search_negative(data_file_path):
    """Test a simple search which should return all False"""
    radex = Radex()
    radex.read_data(str(data_file_path))
    radex.preprocess_data()
    radex.searches = {'THIS_IS_NOT_IN_TEXT': 'THIS_IS_NOT_IN_TEXT'}
    radex.run_searches()
    assert len(radex.output_data == len(radex.data))
    
def test_simple_search_positive(data_file_path):
    """Test a simple search which should return all True"""
    radex = Radex()
    radex.read_data(str(data_file_path))
    radex.preprocess_data()
    radex.searches = {'thyroid': 'thyr*'}
    radex.run_searches()
    assert len(radex.output_data == len(radex.data))
    
def test_value_error(data_file_path):
    """Test the value error returns"""
    radex = Radex()
    # asseert preprocess before read returns a value error
    with pytest.raises(ValueError):
        radex.preprocess_data()
    # assert run searches before preprocess returns a value error
    with pytest.raises(ValueError):
        radex.run_searches()
    # assert save_output before run_searches returns a value
    with pytest.raises(ValueError):
        radex.save_output('output.csv')
        
    radex.read_data(str(data_file_path))
    # assert run_searches before preprocess returns a value error still
    with pytest.raises(ValueError):
        radex.run_searches()
        
    radex.preprocess_data()
    # assert run_searches before preprocess returns a value error still
    with pytest.raises(ValueError):
        radex.run_searches()
    # assert save_output before run_searches returns a value error still
    with pytest.raises(ValueError):
        radex.save_output('output.csv')

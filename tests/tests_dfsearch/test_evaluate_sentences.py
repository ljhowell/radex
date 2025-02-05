# fmt: off
# pylint: disable=line-too-long

"""Test the evaluate_sentences function from df_search"""

from radex.dfsearch import evaluate_sentences

def test_sentence():
    """Test the sentence evaluation"""
    candidate = "quick brown fox. slow brown cat. quick brown dog."
    expression = "fox ~~2 quick"
    assert evaluate_sentences(candidate, expression) is True

    expression = "fox ~~2 slow"
    assert evaluate_sentences(candidate, expression) is False

    expression = "fox ~~2 quick"
    assert evaluate_sentences(candidate, expression, verbose=True) is True

"""
Unit tests for the nlprules module

To run: from root dir use: python -m unittest discover tests
"""

import unittest
import sys

from radex.dfsearch import evaluate_logical_statement
from radex.expression import Expression

sys.path.append("..")


class TestLogicalStatement(unittest.TestCase):
    """Unit test for

    Args:
        unittest (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        """__init__ method"""
        super().__init__(*args, **kwargs)
        self.expr = Expression()
        self.ls_test_standard_search = [
            {
                "test_name": "Single word match",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick",
                "result": True,
            },
            {
                "test_name": "Single word match with trailing space",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick ",
                "result": True,
            },
            {
                "test_name": "Single word match with leading space",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": " quick",
                "result": True,
            },
            {
                "test_name": "Single word match with leading and trailing space",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": " quick ",
                "result": True,
            },
            {
                "test_name": "Partial match to single word",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "brow",
                "result": False,
            },
            {
                "test_name": "Multiple word match",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick brown",
                "result": True,
            },
            {
                "test_name": "Multiple word match with trailing space",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick brown ",
                "result": True,
            },
            {
                "test_name": "Multiple word match with leading space",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": " quick brown",
                "result": True,
            },
            {
                "test_name": "Full sentence match",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "the quick brown fox jumps over the lazy dog",
                "result": True,
            },
            {
                "test_name": "No match",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "lemon",
                "result": False,
            },
            {
                "test_name": "Partial (but incorrect) match",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "brow fox",
                "result": False,
            },
            {
                "test_name": "Case insensitive match",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "BROWN",
                "result": False,
            },
            {
                "test_name": "Multiple matches",
                "candidate": "the quick brown fox jumps over the brown dog",
                "expression": "brown",
                "result": True,
            },
        ]
        self.ls_test_wildcard_search = [
            {
                "test_name": "Single word match with * wildcard at end of word",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "jump*",
                "result": True,
            },
            {
                "test_name": "Incorrect match with * wildcard",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "app*",
                "result": False,
            },
            {
                "test_name": "Multi word match with * wildcard",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "qui* brown",
                "result": True,
            },
            {
                "test_name": "Multi word match with multi * wildcard",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "qui* bro*",
                "result": True,
            },
            {
                "test_name": "Single word match with ? wildcard where the character is not present",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "colo?red",
                "result": True,
            },
            {
                "test_name": "Single word match with ? wildcard where the character is present",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "colou?red",
                "result": True,
            },
            {
                "test_name": "Incorrect match with ? wildcard",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "co?ld",
                "result": False,
            },
            {
                "test_name": "Multiple word match with ? wildcard where the character is not present",
                "candidate": "everyday I see the same old faces",
                "expression": "every?day",
                "result": True,
            },
            {
                "test_name": "Multiple word match with ? wildcard where the character is present",
                "candidate": "every day I see the same old faces",
                "expression": "every?day",
                "result": True,
            },
            {
                "test_name": "Single word match with _ wildcard at the end of the word",
                "candidate": "the thyroid gland is an endocrine gland in the neck",
                "expression": "thyroid_",
                "result": True,
            },
            {
                "test_name": "Single word no match with _ wildcard at the end of the word",
                "candidate": "hyperthyroidism is a condition that can be seen in cats",
                "expression": "thyroid_",
                "result": False,
            },
            {
                "test_name": "Single word match with _ wildcard at the start of the word",
                "candidate": "the thyroid gland is an endocrine gland in the neck",
                "expression": "_thyroid",
                "result": True,
            },
            {
                "test_name": "Single word no match with _ wildcard at the start of the word",
                "candidate": "the parathyroid gland regulates calcium levels in the body",
                "expression": "_thyroid",
                "result": False,
            },
            {
                "test_name": "Single word no match with _ wildcard at the start of the word",
                "candidate": "hyperthyroidism is a condition that can be seen in cats",
                "expression": "thyroid_",
                "result": False,
            },
            {
                "test_name": "Single word match with _ wildcard at the start end of the word",
                "candidate": "the thyroid gland is an endocrine gland in the neck",
                "expression": "_thyroid_",
                "result": True,
            },
            {
                "test_name": "Single word no match with _ wildcard at the start end of the word",
                "candidate": "the parathyroid gland is normal but hyperthyroidism is evident",
                "expression": "_thyroid_",
                "result": False,
            },
            {
                "test_name": "Combination of * and ? wildcards I",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "brown colo?r*",
                "result": True,
            },
            {
                "test_name": "Combination of * and ? wildcards II",
                "candidate": "the quick brown colour fox jumps over the lazy dog",
                "expression": "brown colo?r* fox",
                "result": True,
            },
            {
                "test_name": "Combination of * and ? wildcards II",
                "candidate": "the quick brown colour fox jumps over the lazy dog",
                "expression": "brown colo?r* dog",
                "result": False,
            },
            {
                "test_name": "Combination of * and ? wildcards III",
                "candidate": "the quick brown colour fox jumps over the lazy dog",
                "expression": "brown colo?r* do*",
                "result": False,
            },
            {
                "test_name": "Combination of * and _ wildcards I",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "_brown col*",
                "result": True,
            },
            {
                "test_name": "Combination of * and _ wildcards II",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "_coloured_ f*",
                "result": True,
            },
            {
                "test_name": "Combination of * and _ wildcards III",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "bro* _red",
                "result": False,
            },
            {
                "test_name": "Combination of * and _ wildcards I",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "_colo?red",
                "result": True,
            },
            {
                "test_name": "Combination of * and _ wildcards II",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "_colo?r_",
                "result": False,
            },
            {
                "test_name": "Combination of *, ? and _ wildcards I",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "bro* _?olo?red",
                "result": True,
            },
            {
                "test_name": "Combination of *, ? and _ wildcards II",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "b* _?olo?red",
                "result": True,
            },
            {
                "test_name": "Combination of *, ? and _ wildcards III",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "_bro?n_ colo*",
                "result": True,
            },
            {
                "test_name": "Multiple * wildcards I",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "jump**",
                "result": True,
            },
            {
                "test_name": "Multiple * wildcards II",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "q* b*",
                "result": True,
            },
            {
                "test_name": "Multiple * wildcards III",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "q* c*",
                "result": False,
            },
            {
                "test_name": "Multiple ? wildcards",
                "candidate": "the quick brown coloured fox jumps over the lazy dog",
                "expression": "colo??red",
                "result": True,
            },
        ]
        self.ls_test_bool_search = [
            {
                "test_name": "Parentheses test I",
                "candidate": "a b",
                "expression": "(a & b) | c",
                "result": True,
            },
            {
                "test_name": "Parentheses test II",
                "candidate": "b c",
                "expression": "a & (b | c)",
                "result": False,
            },
            {
                "test_name": "NOT test I",
                "candidate": "a c",
                "expression": "¬a",
                "result": False,
            },
            {
                "test_name": "NOT test II",
                "candidate": "a c",
                "expression": "¬b",
                "result": True,
            },
            {
                "test_name": "AND test I",
                "candidate": "a c",
                "expression": "a & b",
                "result": False,
            },
            {
                "test_name": "AND test II",
                "candidate": "a c",
                "expression": "b & a",
                "result": False,
            },
            {
                "test_name": "AND test III",
                "candidate": "a c",
                "expression": "a & c",
                "result": True,
            },
            {
                "test_name": "AND test IV",
                "candidate": "a c",
                "expression": "c & a",
                "result": True,
            },
            {
                "test_name": "OR test I",
                "candidate": "a c",
                "expression": "a | c",
                "result": True,
            },
            {
                "test_name": "OR test II",
                "candidate": "a c",
                "expression": "c | a",
                "result": True,
            },
            {
                "test_name": "OR test III",
                "candidate": "a c",
                "expression": "a | b",
                "result": True,
            },
            {
                "test_name": "OR test IV",
                "candidate": "a c",
                "expression": "b | a",
                "result": True,
            },
            {
                "test_name": "OR test V",
                "candidate": "a c",
                "expression": "b | d",
                "result": False,
            },
            {
                "test_name": "OR test VI",
                "candidate": "a c",
                "expression": "a | a",
                "result": True,
            },
            {
                "test_name": "Order of operations test 1",
                "candidate": "a c",
                "expression": "¬ a | b",
                "result": False,
            },
            {
                "test_name": "Order of operations test 2",
                "candidate": "a c",
                "expression": "¬a | ¬b",
                "result": True,
            },
            {
                "test_name": "Order of operations test 3",
                "candidate": "a c",
                "expression": "¬(a & b) | c",
                "result": True,
            },
            {
                "test_name": "Order of operations test 4",
                "candidate": "a c",
                "expression": "¬ (a | b) & c",
                "result": False,
            },
            {
                "test_name": "Order of operations test 5",
                "candidate": "a c",
                "expression": "a & ¬ b",
                "result": True,
            },
            {
                "test_name": "Order of operations test 6",
                "candidate": "a c",
                "expression": "a | ¬ b",
                "result": True,
            },
            {
                "test_name": "Order of operations test 7",
                "candidate": "a c",
                "expression": "¬ a & b",
                "result": False,
            },
            {
                "test_name": "Order of operations test 8",
                "candidate": "a c",
                "expression": "¬ (a & ¬ b)",
                "result": False,
            },
            {
                "test_name": "Order of operations test 9",
                "candidate": "a c",
                "expression": "¬ (a | ¬ b)",
                "result": False,
            },
            {
                "test_name": "Order of operations test 10",
                "candidate": "a c",
                "expression": "¬ (¬ a & b)",
                "result": True,
            },
            {
                "test_name": "Order of operations test 11",
                "candidate": "a c",
                "expression": "¬ (¬ a | b)",
                "result": True,
            },
            {
                "test_name": "Order of operations test 12",
                "candidate": "a c",
                "expression": "¬ (a & b) & ¬ (¬ a | b)",
                "result": True,
            },
            {
                "test_name": "Order of operations test 14",
                "candidate": "a c",
                "expression": "¬ (a | b) & ¬ (¬ a & b)",
                "result": False,
            },
            {
                "test_name": "Order of operations test 15",
                "candidate": "a c",
                "expression": "¬ (¬ a & ¬ b) & ¬ (a | b)",
                "result": False,
            },
            {
                "test_name": "Order of operations test 16",
                "candidate": "a c",
                "expression": "¬ (¬ a | ¬ b) & ¬ (a & b)",
                "result": False,
            },
        ]

        self.ls_test_prox_search = [
            {
                "test_name": "Proximity test adjacent I",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick~0brown",
                "result": True,
            },
            {
                "test_name": "Proximity test adjacent II",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick~1brown",
                "result": True,
            },
            {
                "test_name": "Proximity test expression with spaces",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": " quick ~1 brown ",
                "result": True,
            },
            {
                "test_name": "Proximity test wrong order",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "brown ~1 quick",
                "result": False,
            },
            {
                "test_name": "Proximity test non adjacent I",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick ~1 fox",
                "result": True,
            },
            {
                "test_name": "Proximity test non adjacent II",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick ~1 dog",
                "result": False,
            },
            {
                "test_name": "Proximity test non adjacent III",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick ~5 dog",
                "result": False,
            },
            {
                "test_name": "Proximity test non adjacent IV",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick ~6 dog",
                "result": True,
            },
            {
                "test_name": "Proximity test centre search I",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick ~~1 fox",
                "result": True,
            },
            {
                "test_name": "Proximity test centre search II",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "fox  ~~1 quick",
                "result": True,
            },
            {
                "test_name": "Proximity test wildcards I",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "qui* ~5 dog",
                "result": False,
            },
            {
                "test_name": "Proximity test wildcards II",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "qui* ~6 dog",
                "result": True,
            },
            {
                "test_name": "Proximity test wildcards III",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "qui* ~10 ca*",
                "result": False,
            },
            {
                "test_name": "Proximity test wildcards IV",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "qui* ~6 _do?",
                "result": True,
            },
            {
                "test_name": "Proximity test same sentence I",
                "candidate": "the quick brown fox. the dog jumps over the lazy rabbit",
                "expression": "quick ~~3 dog",
                "result": False,
            },
            {
                "test_name": "Proximity test same sentence II",
                "candidate": "the quick brown fox. the dog jumps over the lazy rabbit",
                "expression": "fox ~~3 dog",
                "result": False,
            },
            {
                "test_name": "Proximity test same sentence III",
                "candidate": "the quick brown fox. the dog jumps over the lazy rabbit",
                "expression": "fox ~3 dog",
                "result": False,
            },
            {
                "test_name": "Proximity test NEAR I",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick NEAR1 fox",
                "result": True,
            },
            {
                "test_name": "Proximity test NEAR II",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick NEAR3 dog",
                "result": False,
            },
            {
                "test_name": "Proximity test THEN I",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quick THEN1 fox",
                "result": True,
            },
            {
                "test_name": "Proximity test THEN II",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "fox THEN1 quick",
                "result": False,
            },
        ]

        self.ls_test_boolean_wildcard_proximity_search = [
            {
                "test_name": "Boolean wildcard test 1",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "qui* & laz*",
                "result": True,
            },
            {
                "test_name": "Boolean wildcard test 2",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "d?g | kanga*",
                "result": True,
            },
            {
                "test_name": "Boolean wildcard test 3",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "quic? & _ox",
                "result": False,
            },
            {
                "test_name": "Boolean wildcard test 4",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "beaver | ¬_ox & lazy*",
                "result": True,
            },
            {
                "test_name": "Boolean wildcard test 5",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "_quick_ ~2 fox & lazy* ~1 ??og",
                "result": True,
            },
            {
                "test_name": "Boolean wildcard test 6",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "fox~1 jumps over & dog",
                "result": True,
            },
            {
                "test_name": "Boolean wildcard test 7",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "(lazy*~1dog) & ¬(lazy*~1fox)",
                "result": True,
            },
            {
                "test_name": "Too many brackets",
                "candidate": "the quick brown fox jumps over the lazy dog",
                "expression": "((quick))",
                "result": True,
            },
        ]

    def test_standard_search(self):
        """Simple test searches with no wildcards or logical operators"""
        print("\n")
        for testnumber, test in enumerate(self.ls_test_standard_search):
            candidate = test["candidate"]
            expression = test["expression"]
            expected_result = test["result"]
            actual_result = evaluate_logical_statement(
                candidate, self.expr.parse_string(expression)
            )

            self.assertEqual(
                actual_result,
                expected_result,
                msg=f"\n\nFailed test #{testnumber}\n'{candidate}', \
                                 expression: '{expression}', \
                                     expected: {expected_result}, \
                                         result:{actual_result}",
            )
            print(f'Test {testnumber}: {test["test_name"]} - PASSED')

    def test_wildcard_search(self):
        """Test searches with wildcards"""
        print("\n")
        for testnumber, test in enumerate(self.ls_test_wildcard_search):
            candidate = test["candidate"]
            expression = test["expression"]
            expected_result = test["result"]
            actual_result = evaluate_logical_statement(
                candidate, self.expr.parse_string(expression)
            )

            self.assertEqual(
                actual_result,
                expected_result,
                msg=f"\n\nFailed test #{testnumber}\nCandidate:'{candidate}'\nExpression: '{expression}'\nExpected: {expected_result}\nResult: {actual_result}",
            )
            print(f'Test {testnumber}: {test["test_name"]} - PASSED')

    def test_boolean_search(self):
        """Test searches with boolean operators"""
        print("\n")
        for testnumber, test in enumerate(self.ls_test_bool_search):
            candidate = test["candidate"]
            expression = test["expression"]
            expected_result = test["result"]
            actual_result = evaluate_logical_statement(
                candidate, self.expr.parse_string(expression)
            )

            self.assertEqual(
                actual_result,
                expected_result,
                msg=f"\n\nFailed test #{testnumber}\nCandidate:'{candidate}'\nExpression: '{expression}'\nExpected: {expected_result}\nResult: {actual_result}",
            )
            print(f'Test {testnumber}: {test["test_name"]} - PASSED')

    def test_proximity_search(self):
        """Test searches with proximity operators"""
        print("\n")
        for testnumber, test in enumerate(self.ls_test_prox_search):
            candidate = test["candidate"]
            expression = test["expression"]
            expected_result = test["result"]
            actual_result = evaluate_logical_statement(
                candidate, self.expr.parse_string(expression)
            )

            self.assertEqual(
                actual_result,
                expected_result,
                msg=f"\n\nFailed test #{testnumber}\nCandidate:'{candidate}'\nExpression: '{expression}'\nExpected: {expected_result}\nResult: {actual_result}",
            )
            print(f'Test {testnumber}: {test["test_name"]} - PASSED')

    def test_all(self):
        """Test searches with wildcards, boolean operators and proximity operators"""
        print("\n")
        for testnumber, test in enumerate(
            self.ls_test_boolean_wildcard_proximity_search
        ):
            candidate = test["candidate"]
            expression = test["expression"]
            expected_result = test["result"]
            actual_result = evaluate_logical_statement(
                candidate, self.expr.parse_string(expression)
            )

            self.assertEqual(
                actual_result,
                expected_result,
                msg=f"\n\nFailed test #{testnumber}\nCandidate:'{candidate}'\nExpression: '{expression}'\nExpected: {expected_result}\nResult: {actual_result}",
            )
            print(f'Test {testnumber}: {test["test_name"]} - PASSED')

    # def test_exceptions(self):
    #     """_summary_
    #     """
    #     self.assertRaises(ValueError, evaluate_logical_statement,
    #                       'candidate',
    #                       '((a)')
    # def test_prime_invalid_type(self):
    #     """_summary_
    #     """
    #     self.assertRaises(TypeError, is_prime, 'a')


if __name__ == "__main__":
    unittest.main(verbosity=2)

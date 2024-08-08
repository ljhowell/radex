"""
Define grammar for logical expressions and parse the input string 
into a nested list of logical expressions and operators.
"""

import re

from pyparsing import (
    Word,
    ZeroOrMore,
    alphanums,
    infixNotation,
    oneOf,
    opAssoc,
)


class Expression:
    """
    This class represents the grammer for defining a logical expression
    with a set of boolean operators.

    The grammar represents the allowed operators and their precedence.
    The parseString method of the grammar is used to parse the logical expression
    into a form that can be evaluated.

    e.g. "quick~1dog & brown~1fox | camel* & ¬hippo"
        -> [['quick~1dog ', '&', 'brown~1fox '], '|', ['camel* ', '&', ['¬', 'hippo?']]]
        Here:
        - the expressions are quick~1dog, brown~1fox, camel*, hippo?
        - the operators are &, |, ¬
        - the precedence is ¬ > &, > |, so the expression is evaluated as
                (quick~1dog & brown~1fox) | (camel* & ¬hippo)
    """

    def __init__(self):
        # Define the grammar for logical expressions.
        self.statement = Word("_" + alphanums + "~" + "*" + "?" + " " + "_")
        self.not_ = oneOf("! ¬")
        self.and_ = oneOf("& ^")
        self.or_ = oneOf("| ∨")

        self.grammar = self._get_grammar()

    def _get_grammar(self):
        """
        determine the grammar for logical expressions

        Returns:
            pyparsing.infixNotation: The grammar for logical expressions
        """

        expr = infixNotation(
            self.statement
            | "("
            + ZeroOrMore(self.not_)
            + self.statement
            + ZeroOrMore(self.and_ | self.or_)
            + ")"
            | ZeroOrMore(self.not_) + "(" + self.statement + ")",
            [
                (self.not_, 1, opAssoc.RIGHT),
                (self.and_, 2, opAssoc.LEFT),
                (self.or_, 2, opAssoc.LEFT),
            ],
        )
        return expr

    def parse_string(self, input_str: str, verbose=False) -> list:
        """
        Parse the input string into a nested list of logical expressions and operators

        Args:
            input_str (str): The input string
            verbose (bool, optional): Verbose output. Defaults to False.

        Returns:
            list: The nested list of logical expressions and operators
        """
        # replace words with operators, case sensitive using regex
        input_str = re.sub(r"AND", r"&", input_str)
        input_str = re.sub(r"OR", r"|", input_str)
        input_str = re.sub(r"NOT", r"¬", input_str)

        input_str = re.sub(r"EXCEPT", r"&¬", input_str)

        # replace NEAR and ADJ with ~~
        input_str = re.sub(r"NEAR", r"~~", input_str)
        input_str = re.sub(r"ADJ", r"~~", input_str)

        # repleace THEN and BEFORE with ~
        input_str = re.sub(r"THEN", r"~", input_str)
        input_str = re.sub(r"BEFORE", r"~", input_str)

        if verbose:
            print("Input string: ", input_str)

        parsed_list = self.grammar.parseString(input_str).as_list()

        self.check_input_string(input_str)

        search_terms = set(re.findall(r"\b\w[\w*~?]*\b", input_str))
        parsed_terms = set(re.findall(r"\b\w[\w*~?]*\b", str(parsed_list)))

        if not len(search_terms) == len(parsed_terms):
            raise ValueError(f"Input search string {input_str} is invalid.")

        return parsed_list

    def check_input_string(self, input_str: str) -> bool:
        """
        Check if the input string contains any characters which will not be parsed correctly.

        Args:
            input_str (str): The input string

        Returns:
            bool: True if the input string contains only valid characters and has matching number
                    of opening and closing parentheses, False otherwise.
        """
        valid_chars = set(
            "_"
            + alphanums
            + "~"
            + "*"
            + "?"
            + " "
            + "|"
            + "&"
            + "^"
            + "¬"
            + "!"
            + "("
            + ")"
        )
        num_open_parentheses = input_str.count("(")
        num_close_parentheses = input_str.count(")")

        if not num_open_parentheses == num_close_parentheses:
            raise ValueError(
                f"Input search string has mismatching \
                             number of opening and closing parentheses \n {input_str}"
            )

        for c in input_str:
            if c not in valid_chars:
                raise ValueError(
                    f"Input search string contains \
                                 invalid characters: {c} \n {input_str}"
                )

        return True

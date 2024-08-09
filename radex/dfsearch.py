"""
Search a string or dataframe based on a logical expression.
- Wildcards: * for multiple characters, ? for single character, _ for word boundary
- Proximity: ~X where X is the maximum distance between two words
- Operators: & for AND, | for OR, ¬ for NOT
"""

from typing import List, Optional, Union

import pandas as pd

from radex.radexpressions import string_search

def flatten_list(list_in: list) -> list:
    """
    Recursive function to flatten a list of lists into a single 1D list.

    Args:
        list_in (list): Input list

    Returns:
        list: Flattened list
    """
    result = []
    for elem in list_in:
        if isinstance(elem, list):
            result.extend(flatten_list(elem))  # Recursive call
        else:
            result.append(elem)
    return result


def list_to_string(input_list: Union[list, str]) -> str:
    """
    Recursively converts a nested list into a string.
    Or just return the string if it is not a list.

    Args:
        input_list (list): The list to convert.

    Returns:
        str: The converted string.
    """
    if isinstance(input_list, list):
        return "(" + ", ".join([list_to_string(x) for x in input_list]) + ")"
    else:
        return str(input_list).strip()


def check_all_matches(
    candidate: str,
    expression: list,
) -> dict:
    """
    Return a dictionary of all the statements with matches found
    in a string of statements for debugging purposes.
    N.B can accept a nested list with boolean operators
    such as that returned by the parse_logical_expression function.
    e.g. candidate = "the quick brown fox jumps over the lazy dog",
            expression = ["the", "qui*"]
            => {'the': [('the', 31, 34)], 'qui*': [('quick ', 4, 10)]}


    Args:
        candidate (str): The string to match against
        expression (list): A list of logical expressions to match against

    Returns:
        dict: Dictionary of all the statements with matches found
    """

    # Flatten the expression
    expression = flatten_list(expression)
    expression = [
        i for i in expression if i not in ["&", "|", "¬", "(", ")"]
    ]  # Remove operators

    return {
        part.strip(): string_search(candidate, part.strip())
        for part in expression
    }


def evaluate_sentences(
    candidate: str,
    expression: Union[list, str],
    verbose: Optional[bool] = False,
) -> Union[bool, str]:
    """
    evaluate_sentences is a wrapper for evaluate_logical_statement

    Args:
        candidate (str): The candidate string to match against
        expression (list): The logical expression to evaluate
        verbose (bool, optional): Verbose. Defaults to False.

    Returns:
        bool: The result of the logical expression evaluation
    """
    for sentence in candidate.split("."):
        if verbose:
            print("\nSentence:", sentence)
        if evaluate_logical_statement(sentence, expression, verbose=verbose):
            return True
    return False


def evaluate_logical_statement(
    candidate: str,
    expression: Union[list, str],
    verbose: Optional[bool] = False,
) -> Union[list, str, bool]:
    """
    The main point of input to evaluate a logical statement.


    Args:
        candidate (str): The candidate string to match against
        expression (str): The logical expression to evluate
        verbose (bool, optional): Verbose ouput. Defaults to False.

    Raises:
        ValueError: If the expression is not a valid logical expression

    Returns:
        bool: The result of the logical expression evaluation
    """

    # Recursively evaluate a logical statement
    if isinstance(expression, str):  # symbol or statement to evaluate
        if expression in [
            "&",
            "|",
            "¬",
            "^",
            "v",
            "!",
        ]:  # Replace symbols with python operators
            expression = (
                expression.replace("&", "and")
                .replace("|", "or")
                .replace("¬", "not")
            )
            expression = (
                expression.replace("^", "and")
                .replace("v", "or")
                .replace("!", "not")
            )
            return expression
        else:  # Assume expression is statement to be evaluated
            result = string_search(candidate, expression.strip())
            if verbose:
                print(list_to_string(expression), "=>", result[0], result[1])
            return string_search(
                candidate, expression.strip()
            )[0]

    if isinstance(expression, list):  # Evaluate sub-statements recursively
        expression = [
            i for i in expression if i not in ["(", ")"]
        ]  # Remove excess brackets
        sub_results = [
            evaluate_logical_statement(candidate, sub, verbose=verbose)
            for sub in expression
        ]

        # Evaluate subexpression
        sub_results_str = " ".join(str(elem) for elem in sub_results)
        if verbose:
            print(
                list_to_string(expression)[1:-1],
                "=>",
                sub_results_str,
                "=>",                    
                eval(sub_results_str),
            )
        return eval(sub_results_str) 

    raise ValueError("Invalid logical statement")


def search_dataframe(
    df: pd.DataFrame,
    column: str,
    expression: List,
    new_column_name: Optional[str] = None,
    debug_column: Optional[bool] = False,
    sentencizer: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Search a column of a dataframe based on a logical expression.

    Args:
        df (pd.DataFrame): The dataframe to search
        column (str): The column to search
        expression (str): The logical expression to search for
        new_column_name (str, optional): The new column name to store the results of the search.
                                        Defaults to None.
        debug_column (bool, optional): Return matching strings for regex search to enable debugging.
                                        Defaults to False.
        sentencizer (bool, optional): If True, search each sentence independently.
                                        Defaults to False.

    Returns:
        pd.DataFrame: Results of the search
    """
    if sentencizer:  # Split the column into sentences and search each sentence
        func = evaluate_sentences
    else:  # Search the column as a whole
        func = evaluate_logical_statement

    if new_column_name is None:
        new_column_name = column + "_matches"

    # Filter a column based on a logical expression
    df[new_column_name] = df[column].apply(
        lambda x: func(str(x), expression=expression, verbose=False)
    )

    if debug_column:
        df[new_column_name + "_matches"] = df[column].apply(
            lambda x: check_all_matches(str(x), expression)
        )

    return df

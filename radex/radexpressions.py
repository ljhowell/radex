"""
Wrapper for regular expressions including wildcards and proximity matching.
Evaluate regular expressions.
"""

from math import e
import re


def evaluate_regex(candidate: str, regex: str) -> list:
    """
    Performs a regex search on a candidate string, returning all matches and start/ end indices.

    Args:
        candidate (str): String to match against
        regex (str): Regex pattern to match

    Returns:
        list: A list of tuples. Each tuple contains the matched substring and start/ end indices.
    """
    # Split candidate into sentences which are searched individually
    candidates = [
        sentence for sentence in candidate.split(".") if sentence.strip() != ""
    ]
    result = []
    for c in candidates:
        result += [
            (match.group(), match.start(), match.end())
            for match in re.finditer(regex, c.strip())
        ]

    return result


def get_regex_wildcards(expression: str) -> str:
    """
    Converts a regular expression with wildcards to a regex pattern.
    Allowed wildcards are:
    - '*' for a multiple character wildcard e.g. 'colou*' will match 'colour' and 'colours'
    - '?' for a single/none character wildcard e.g. 'colo?r' will match 'colour' and 'color'

    Args:
        expression (str): The regular expression with wildcards.

    Returns:
        str: The regex pattern
    """
    regex = re.escape(expression.strip())
    regex = regex.replace(
        r"\*", r"\w*"
    )  # replace * with multiple character wildcard
    regex = regex.replace(
        r"\?", r".?"
    )  # replace ? with single character wildcard

    # add word boundary to start and end of regex
    regex = r"\b" + regex + r"\b"
    return regex


def get_regex_proximity(
    word1: str, word2: str, max_distance: int, direction: str = "centre"
) -> str:
    """
    Creates a regex pattern that matches two words within a specified distance of each other.

    Args:
        word1 (str): The first word to match.
        word2 (str): The second word to match.
        max_distance (int): The maximum distance between the two words.
                            e.g. if max_distance=1, words can be separated by a single word.
        direction (str): The direction to match:
                        - 'centre' means word2 can appear before or after word1
                        - 'right' means word2 must appear after word1
                        - 'left' means word2 must appear before word1

    Returns:
        str: The regex pattern
    """
    if direction not in ["centre", "center", "right", "left"]:
        raise ValueError("direction must be 'centre', 'right', or 'left'")
    if not isinstance(max_distance, int):
        raise ValueError("max_distance must be an integer")
    if max_distance < 0:
        raise ValueError("max_distance must be greater than 0")
    if not isinstance(word1, str) or not isinstance(word2, str):
        raise ValueError("word1 and word2 must be strings")

    word1 = re.escape(word1.strip())
    word2 = re.escape(word2.strip())
    max_dist = max_distance

    if direction in ["centre", "center"]:
        regex = rf"\b{word1}\b\W+(?:\w+\W+){{0,{max_dist}}}?\b{word2}\b|\b{word2}\b\W+(?:\w+\W+){{0,{max_dist}}}?\b{word1}\b"
    elif direction == "right":
        regex = rf"\b{word1}\b\W+(?:\w+\W+){{0,{max_dist}}}?\b{word2}\b"
    elif direction == "left":
        regex = rf"\b{word2}\b\W+(?:\w+\W+){{0,{max_dist}}}?\b{word1}\b"
    else:
        raise ValueError("Invalid direction")

    regex = regex.replace(r"\*", r"\w*")  # non greedy matching
    regex = regex.replace(r"\?", r".?")
    regex = regex.replace(r"_", r"\b")  # replace _ with word boundary

    return regex


def string_search(
    candidate: str,
    expression: str,
) -> tuple:
    """
    Evaluates a logical expression containing wildcards */?/_ or proximity matching ~X.
    e.g.
        candidate="The quick brown fox jumps over the lazy dog",
        expression="quick~2fo*"
        => (True, [('quick brown fox ', 4, 20)])

    For the proximity search
        wordA ~2 wordB => wordB must be a maximum of 2 words after wordA
        wordA ~~2 wordB => wordB must be a maximum of 2 words before OR after wordA

    Args:
        candidate (str): String to match against
        expression (str): Logical expression containing wildcards */?/_ or proximity matching ~X.
        return_bool (bool, optional): Return True if >=1 matches are found. Defaults to False.

    Raises:
        ValueError: If the expression is invalid.

    Returns:
        tuple: A tuple containing a boolean indicating if the expression was found in the candidate and a list of matches.
    """

    # Proximity search
    if "~" in expression:
        parts = re.split(
            r"(~{1,2}\d+)", expression
        )  # split on proximity string e.g. '~2' or '~~2'

        if len(parts) == 3:
            word1 = parts[0].strip()
            word2 = parts[2].strip()

            # Get max distance from proximity string e.g. '~2'
            max_distance = int(parts[1].replace("~", ""))

            # Decide whether to do a center search or right search
            if parts[1].count("~") == 2:
                direction = "centre"
            else:
                direction = "right"

            regex = get_regex_proximity(
                word1, word2, max_distance, direction=direction
            )

        else:
            raise ValueError(f"Invalid proximity search: {expression}")

    # Normal wildcard regex
    else:
        regex = get_regex_wildcards(expression)

    result = evaluate_regex(candidate, regex)

    return (True, result) if len(result) > 0 else (False, result)


def wildcard_search(string, pattern):
    """Searches for the specified pattern in the string using Linux-style wildcards.

    Args:
        string (str): The string to search in.
        pattern (str): The wildcard pattern to match.

    Returns:
        list: A list of tuples, where each tuple contains matches and start/ end indices.
    """
    regex = re.escape(pattern)
    regex = regex.replace(
        r"\*", r"\w*"
    )  # replace * with multiple character wildcard
    regex = regex.replace(
        r"\?", r".?"
    )  # replace ? with single character wildcard
    regex = regex.replace(r"_", r"\b")  # replace _ with word boundary

    matches = [
        (match.group(), match.start(), match.end())
        for match in re.finditer(regex, string)
    ]

    return matches

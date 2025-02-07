"""
Preprocessing functions for text data. 
Includes functions to clean text, remove stopwords, and combine columns.
"""

from pickle import STOP
import re
from pathlib import Path
from typing import List, Union

import pandas as pd

from negex.negexPython.negex import negTagger, sortRules

RULES_FILE = Path(__file__).parent.parent / 'data' / 'negex_triggers.txt'
STOPWORDS_FILE = Path(__file__).parent.parent / 'data' / 'stopwords.csv'

# assert RULES_FILE.exists(), f"Negex rules file not found: {RULES_FILE}"
print(RULES_FILE)


def clean_dataframe(
    df_data: pd.DataFrame,
    text_columns: Union[List[str], str],
    **kwargs,
) -> pd.DataFrame:
    """
    Clean dataframe by removing punctuation, new line characters, and trailing whitespace.
    Make all text lowercase.
    Optionally drop duplicates, nulls, and empty rows.

    Args:
        df_data (pd.DataFrame): The dataframe to clean.
        text_columns (Union[List[str], str]): The text columns to clean.
        **kwargs: Additional keyword arguments.
            drop_duplicates (bool, optional): Whether to drop duplicates. Defaults to False.
            drop_nulls (bool, optional): Whether to drop nulls. Defaults to False.
            drop_negatives (list, optional): List of negation rules to remove. Defaults to None.
            drop_stopwords (list, optional): List of stopwords to remove. Defaults to None.

    Returns:
        pd.DataFrame: The cleaned dataframe.
    """
    drop_duplicates = kwargs.get("drop_duplicates", False)
    drop_nulls = kwargs.get("drop_nulls", False)
    drop_negatives = kwargs.get("drop_negatives", None)
    drop_stopwords = kwargs.get("drop_stopwords", None)

    if isinstance(text_columns, str):
        text_columns = [text_columns]

    if not all(isinstance(col, str) for col in text_columns):
        raise ValueError(
            "text_columns must contains the column names as a string or list of strings"
        )

    for col in text_columns:

        if drop_duplicates:
            df_data = df_data.drop_duplicates(subset=[col])  # drop duplicates
        if drop_nulls:
            df_data = df_data.dropna(subset=[col])  # drop nulls

        # remove new line characters
        df_data[col] = df_data[col].str.replace("\n", " ", regex=True)
        # remove forward slash
        df_data[col] = df_data[col].str.replace("/", " ", regex=True)
        # remove dash
        df_data[col] = df_data[col].str.replace("-", " ", regex=True)
        # remove punctuation
        df_data[col] = df_data[col].str.replace(r"[^\w\s.]", "", regex=True)
        # remove extra whitespace
        df_data[col] = df_data[col].str.replace(r"\s+", " ", regex=True)
        # remove trailing period
        df_data[col] = df_data[col].str.replace(r"\.$", "", regex=True)
        # Convert to lowercase
        df_data[col] = df_data[col].str.lower()

        if drop_negatives:
            if drop_negatives == "negex":  # load negex default rules
                rules_file = RULES_FILE
                with open(rules_file, encoding="utf-8") as rfile:
                    drop_negatives = sortRules(rfile.readlines())

            df_data[col] = df_data[col].apply(
                lambda x: remove_negated_phrases(
                    x,
                    rules=drop_negatives,
                )
            )

        if drop_stopwords:
            if drop_stopwords == "nltk":  # load nltk default stopwords
                drop_stopwords = pd.read_csv(STOPWORDS_FILE).T.values[0]

            df_data[col] = df_data[col].apply(
                lambda x: remove_stopwords(
                    x,
                    stopwords=drop_stopwords,
                )
            )

        # Remove extra whitespace
        df_data[col] = df_data[col].str.strip()

    return df_data


def remove_stopwords(
    text: str,
    stopwords: List,
) -> str:
    """
    Remove stopwords from text.

    Args:
        text (str): The input text from which stopwords will be removed.
        stopwords (list[str]): List of stopwords.

    Returns:
        str: The text with stopwords removed.
    """
    # remove punctuation from stopwords
    stopwords = list(re.sub(r"[^\w\s]", "", s) for s in stopwords)

    data = re.sub(r"\b(" + r"|".join(stopwords) + r")\b\s*", "", text)
    return data


def merge_columns(
    df: pd.DataFrame,
    cols: list,
    new_col_name: str = "combined",
    delimiter: str = " ",
) -> pd.DataFrame:
    """
    Combine multiple columns with strings into a single column.

    Args:
        df (pd.DataFrame): The dataframe to combine columns in.
        cols (list): The columns to combine.
        new_col_name (str, optional): The name of the new column. Defaults to 'combined'.
        delimiter (str, optional): The delimiter to use between columns. Defaults to ' '.

    Returns:
        pd.DataFrame: The dataframe with the columns combined.
    """

    df_copy = df.copy()  # make a copy of the dataframe

    df_copy[new_col_name] = df_copy[cols[0]]
    for col in cols[1:]:
        df_copy[new_col_name] += delimiter + df_copy[col]

    return df_copy


def remove_negated_phrases(
    text: str,
    rules: List,
    verbose: bool = False,
) -> str:
    """
    Use negex to remove negated phrases from text.

    Args:
        text (str): The input text from which negated phrases will be removed.
        rules (list): List of negation rules.
        verbose (bool, optional): Whether to print the tagged sentence. Defaults to False.

    Returns:
        str: The text with negated phrases removed.
    """

    # if rules_file is None:
    #     rules_file = r"negex/negexPython/negex_triggers.txt"

    # with open(rules_file, encoding="utf-8") as rfile:
    #     rules = sortRules(rfile.readlines())

    output = ""
    for sentence in text.split("."):
        tagger = negTagger(
            sentence=sentence, phrases=[], rules=rules, negP=False
        )
        negated_phrases = tagger.getScopes()
        tagged_sentence = tagger.getNegTaggedSentence()

        if verbose:
            print("Tagged sentence:", tagged_sentence)
            print("Negated phrases to be removed:", negated_phrases)

        # remove negated phrases
        for phrase in negated_phrases:
            # if verbose:
            #     print(phrase, "[PREN] " + phrase in tagged_sentence)
            # if phrase is before or afte [PREN] or [POST], remove it
            tagged_sentence = tagged_sentence.replace(
                "[PREN] " + phrase, " XXXXX"
            )
            tagged_sentence = tagged_sentence.replace(
                phrase + " [POST]", "XXXXX "
            )

        # Remove all the tags i.e. [PREN], [POST], [CONJ]
        tagged_sentence = re.sub(r"\[.*?\]", "", tagged_sentence)

        if verbose:
            print("Sentence with negated phrases removed:", tagged_sentence)

        output += tagged_sentence + ". "

    # Clean up text
    output = re.sub(r"\s+", " ", output)  # remove extra whitespace
    output = re.sub(r"\s+\.", ".", output)  # remove spaces before full stops
    output = re.sub(r"\.+", ".", output)  # remove extra full stops
    output = output.strip()  # remove trailing whitespace
    output = re.sub(r"\.$", "", output)  # remove trailing full stop

    return output

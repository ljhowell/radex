"""
Preprocessing functions for text data. 
Includes functions to clean text, remove stopwords, and combine columns.
"""

import re  # regex
from typing import List, Optional  # type hinting

import pandas as pd  # pandas for dataframes

from negex.negexPython.negex import negTagger, sortRules


def clean_dataframe(
    df_data: pd.DataFrame,
    text_columns: str,
    drop_duplicates: bool = False,
    drop_nulls: bool = False,
    drop_negatives: bool = False,
    drop_ambiguous: bool = False,
    drop_stopwords: bool = False,
    replace_connectors: bool = False,
) -> pd.DataFrame:
    """
    Clean dataframe by removing punctuation, new line characters, and trailing whitespace.
    Make all text lowercase.
    Optionally drop duplicates, nulls, and empty rows.

    Args:
        df (pd.DataFrame): The dataframe to clean.
        text_columns (str): The column(s) to clean.
        drop_duplicates (bool, optional): Drop duplicate rows. Defaults to True.
        drop_nulls (bool, optional): Drop rows with null values. Defaults to True.
        drop_negatives (bool, optional): Remove negated phrases. Defaults to True.
        drop_ambiguous (bool, optional): Remove ambiguous phrases. Defaults to True.
        drop_stopwords (bool, optional): Remove stopwords. Defaults to True.
        replace_connectors (bool, optional): Replace connectors with full stops. Defaults to True.

    Returns:
        pd.DataFrame: The cleaned dataframe.
    """
    for col in text_columns:

        if drop_duplicates:
            df_data = df_data.drop_duplicates(subset=[col])  # drop duplicates
        if drop_nulls:
            df_data = df_data.dropna(subset=[col])  # drop nulls

        df_data[col] = df_data[col].str.replace("\n", " ", regex=True)  # remove new line characters
        df_data[col] = df_data[col].str.replace("/", " ", regex=True)  # remove forward slash
        df_data[col] = df_data[col].str.replace("-", " ", regex=True)  # remove dash
        df_data[col] = df_data[col].str.replace(r"[^\w\s.]", "", regex=True)  # remove punctuation
        df_data[col] = df_data[col].str.replace(r"\s+", " ", regex=True)  # remove whitespace
        df_data[col] = df_data[col].str.replace(r"\.$", "", regex=True)  # remove trailing period
        df_data[col] = df_data[col].str.lower()  # Convert to lowercase

        if drop_negatives:
            df_data[col] = df_data[col].apply(
                lambda x: remove_negated_phrases(
                    x,
                    rules=None,
                    drop_ambiguous=drop_ambiguous,
                    replace_connectors=replace_connectors,
                )
            )
        if drop_stopwords:
            df_data = remove_stopwords(df_data, text_columns=[col])

        return df_data


def remove_stopwords(
    df: pd.DataFrame,
    text_columns: List[str],
    stop_words: Optional[set[str]] = None,
) -> pd.DataFrame:
    """
    Remove stopwords from text columns.

    Args:
        df (pd.DataFrame): Dataframe to remove stopwords from.
        text_columns (list[str]): The text columns to remove stopwords from.
        stop_words (list[str], optional): List of stopwords. Defaults to None.

    Returns:
        pd.DataFrame: Dataframe with stopwords removed.
    """

    if stop_words is None:  # if no stopwords are provided, use nltk stopwords with some exceptions

        # Load stopwords from csv]
        stop_words = pd.read_csv("data/stopwords.csv").T.values[0]
        exceptions = ["no", "not", "nor", "few", "other"]
        ls_stop_words = [re.sub(r"[^\w\s]", "", s) for s in stop_words]  # remove punctuation
        ls_stop_words = [word for word in stop_words if word not in exceptions]

    stop_words = set(ls_stop_words)

    for col in text_columns:  # Remove stopwords from text in each column using regex
        df[col] = df[col].apply(lambda x: re.sub(r"\b(" + r"|".join(stop_words) + r")\b\s*", "", x))

    return df


def combine_colums(
    df: pd.DataFrame,
    cols: list,
    new_col_name: str = "combined",
    delimiter: str = " ",
    inplace=False,
) -> pd.DataFrame:
    """
    Combine multiple columns with strings into a single column.

    Args:
        df (pd.DataFrame): The dataframe to combine columns in.
        cols (list): The columns to combine.
        new_col_name (str, optional): The name of the new column. Defaults to 'combined'.
        delimiter (str, optional): The delimiter to use between columns. Defaults to ' '.
        inplace (bool, optional): Whether to modify the dataframe inplace. Defaults to False.

    Returns:
        pd.DataFrame: The dataframe with the columns combined.
    """

    df_copy = df.copy()  # make a copy of the dataframe

    df_copy[new_col_name] = df_copy[cols[0]]
    for col in cols[1:]:
        df_copy[new_col_name] += delimiter + df_copy[col]

    if inplace:
        df_copy.drop(columns=cols, inplace=True)

    return df_copy


def remove_negated_phrases(
    text: str,
    rules: Optional[List] = None,
    drop_ambiguous: bool = False,
    replace_connectors: bool = False,
    verbose: bool = False,
):
    """
    Use negex to remove negated phrases from text.

    Args:
        text (str): The input text from which negated phrases will be removed.
        rules (List, optional): A list of negation rules.
        drop_ambiguous (bool, optional): Whether to drop ambiguous phrases. Defaults to False.
        replace_connectors (bool, optional): Replace connectors with a period. Defaults to False.
        verbose (bool, optional): Whether to print the tagged sentence. Defaults to False.

    Returns:
        str: The text with negated phrases removed.
    """

    if rules is None:
        with open(r"nlprules/negex_triggers.txt", encoding="utf-8") as rfile:
            rules = sortRules(rfile.readlines())

    # ls_negations = []
    ls_connectors = []
    for sentence in text.split("."):
        tagger = negTagger(sentence=sentence, phrases=[], rules=rules, negP=drop_ambiguous)
        negated_phrases = tagger.getScopes()
        tagged_sentence = tagger.getNegTaggedSentence()

        if verbose:
            print(tagged_sentence)

        # // Tags are:    [PREN] - Prenegation rule tag
        # //              [POST] - Postnegation rule tag
        # //              [PREP] - Pre possible negation tag
        # //              [POSP] - Post possible negation tag
        # //              [PSEU] - Pseudo negation tag
        # //              [CONJ] - Conjunction tag

        # use regex to get words between the tags
        # ls_negations += re.findall(r'\[PREN\](.*?)\[PREN\]',
        #                     tagged_sentence)
        # ls_negations += re.findall(r'\[POST\](.*?)\[POST\]',
        #                             tagged_sentence)

        # if drop_ambiguous:
        #     ls_negations += re.findall(r'\[PSEU\](.*?)\[PSEU\]',
        #                                tagged_sentence)
        #     ls_negations += re.findall(r'\[PREP\](.*?)\[PREP\]',
        #                                tagged_sentence)
        #     ls_negations += re.findall(r'\[POSP\](.*?)\[POSP\]',
        #                                tagged_sentence)

        if replace_connectors:
            ls_connectors += re.findall(r"\[CONJ\](.*?)\[CONJ\]", tagged_sentence)

        for phrase in negated_phrases:
            # remove negated phrases
            text = text.replace(phrase, "")

    # remove ambiguous phrases
    # sort by length of phrase, so that longer phrases are removed first
    # ls_negations = sorted(ls_negations, key=len, reverse=True)

    # print(ls_negations)
    # # if drop_ambiguous:
    # for phrase in ls_negations:
    #     # sub with regex, using word boundaries
    #     text = re.sub(r'\b' + phrase + r'\b', '', text)

    if replace_connectors:
        for phrase in ls_connectors:
            text = re.sub(r"\b" + phrase + r"\b", ".", text)

    text = re.sub(r"\s+", " ", text)  # remove extra whitespace
    text = re.sub(r"\s+\.", ".", text)  # remove spaces before full stops
    text = re.sub(r"\.+", ".", text)  # remove extra full stops
    text = text.strip()  # remove trailing whitespace
    text = re.sub(r"\.$", "", text)  # remove trailing full stop

    return text

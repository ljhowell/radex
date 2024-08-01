"""This module contains functions for post-processing data.

Functions:
- extract_regex_matches_single_entry(entry): Extract text matches from a single entry.
- extract_regex_matches_all(df, cols): Extract matches from all entries in a column.
- highlight_text(text, matches, colour="#0000FF"): Highlight text based on specified matches.
- highlight_table(df, cmap=None): Apply highlighting to a table based on specified colors.
"""

import re

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import rgb2hex


def extract_regex_matches_single_entry(entry):
    """
    Extract text matches from a single entry

    e.g.
    {
        'normal~2thyroid': (True, [('normal thyroid', 11, 23),
                                    ['normal appearing thyroid', 25, 35]]),
        'no~1evidence': (False, [])
    }
    returns ['normal thyroid', 'normal appearing thyroid']
    """
    out = set()

    flag = 0
    for matches in entry.values():  # each search
        if matches[0] is True:
            flag = 1
            out = [val[0] for val in matches[1]]

    if flag:
        return ", ".join(set(out))

    return ""


def extract_regex_matches_all(df, cols):
    """
    Extract text matches from all entries in a column of a dataframe
    """

    # Get text matches from all cols and combine into a new column
    df_tmp = pd.DataFrame()
    for col in cols:
        df_tmp[col + "_text"] = df[col].apply(extract_regex_matches_single_entry)

    # Combine all text matches into a single column
    df["all_text"] = df_tmp.astype(str).agg(",".join, axis=1)

    # Use regex to remove the extra commas
    df["all_text"] = df["all_text"].str.replace(",+", ", ", regex=True)

    return df


def highlight_text(text, matches, colour="#0000FF"):
    """
    _summary_

    Args:
        text (_type_): _description_
        matches (_type_): _description_
        colour (str, optional): _description_. Defaults to '#0000FF'.

    Returns:
        _type_: _description_
    """

    matches_text = list(
        set([matches[key][1][0][0] for key in matches.keys() if matches[key][0] is True])
    )
    for match in matches_text:
        text = re.sub(
            rf"\b{re.escape(match)}\b",
            f'<b><font color="{colour}">{match}</font></b>',
            text,
        )
    return text


def highlight_table(df, cmap=None):
    """
    Apply highlighting to a table based on specified colors.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the table.
        cmap (dict or list, optional): A dictionary or list of colors to be used for highlighting.
            If None, a default color map will be used. Defaults to None.

    Returns:
        pandas.DataFrame: The DataFrame with the highlighted table.
    """

    df["report_highlighted"] = df["report"]
    cols = []

    for col in df.columns:
        if "matches" in col:
            try:
                df[col] = pd.eval(df[col])
                cols.append(col)
            except pd.errors.ParserError:
                cols.append(col)

    if cmap is None:
        cmap = {col: rgb2hex(color) for col, color in zip(cols, plt.cm.get_cmap("tab20").colors)}
    elif isinstance(cmap, list):
        cmap = {col: rgb2hex(color) for col, color in zip(cols, cmap)}

    for col in cols:
        df["report_highlighted"] = df.apply(
            lambda x, col=col: highlight_text(x["report_highlighted"], x[col], colour=cmap[col]),
            axis=1,
        )

    return df
